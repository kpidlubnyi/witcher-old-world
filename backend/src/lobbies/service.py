import uuid
import time
import json
import redis.asyncio as redis

from .schemas import CreateLobby, Lobby, LobbyResponse
from ..auth.models import User


def get_user_active_lobby_key(user_id: int) -> str:
    return f'user_active_lobby:{user_id}'

def get_lobby_data_key(lobby_id: str) -> str:
    return f'lobby:data:{lobby_id}'


async def user_has_active_lobby(user: User, r: redis.Redis) -> bool:
    key = get_user_active_lobby_key(user.id)
    return await r.exists(key)


def create_lobby_model(data: CreateLobby, user: User):
    return Lobby(
        id=str(uuid.uuid4()),
        host_id=user.id,
        host_name=user.name,
        name=data.name,
        max_players=data.max_players,
        created_at=int(time.time())
    )


async def add_lobby(lobby: Lobby, r: redis.Redis, user: User):
    lobby_id = lobby.id
    lobby_json = lobby.model_dump_json()
    user_key = get_user_active_lobby_key(user.id) 
    lobby_data_key = get_lobby_data_key(lobby_id)
    
    async with r.pipeline(transaction=True) as pipe:
        pipe.set(user_key, lobby_id, ex=3600)
        pipe.set(lobby_data_key, lobby_json, ex=3600)
        pipe.zadd("lobbies:open", {lobby_id: lobby.created_at})
        
        await pipe.execute()    
    
    
async def get_lobbies(r:redis.Redis):
    lobby_ids = await r.zrange("lobbies:open", 0, -1)
    
    if not lobby_ids:
        return []
    
    keys = [get_lobby_data_key(l_id) for l_id in lobby_ids]
    lobbies_raw = await r.mget(keys)
    active_lobbies = [LobbyResponse(**json.loads(l)) for l in lobbies_raw if l is not None]    
    return active_lobbies