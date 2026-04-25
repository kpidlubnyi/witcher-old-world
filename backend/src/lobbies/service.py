import uuid
import time
import json
import redis.asyncio as redis
from fastapi import HTTPException

from .schemas import CreateLobby, Lobby, LobbyResponse
from ..auth.models import User


def get_user_active_lobby_key(user_id: int) -> str:
    return f'user_active_lobby:{user_id}'

def get_lobby_data_key(lobby_id: str) -> str:
    return f'lobby:data:{lobby_id}'

def get_lobby_players_key(lobby_id: str) -> str:
    return f'lobby:players:{lobby_id}'


async def user_has_active_lobby(user: User, r: redis.Redis) -> bool:
    key = get_user_active_lobby_key(user.id)
    return await r.exists(key)


async def get_raw_lobby(lobby_id: str, r: redis.Redis):
    key = get_lobby_data_key(lobby_id)
    return await r.get(key)
    
    
def create_lobby_model(data: CreateLobby, user: User):
    return Lobby(
        id=str(uuid.uuid4()),
        host_id=user.id,
        host_name=user.name,
        name=data.name,
        max_players=data.max_players,
        created_at=int(time.time())
    )


async def create_lobby(lobby: Lobby, r: redis.Redis, user: User):
    lobby_id = lobby.id
    lobby_json = lobby.model_dump_json()
    lobby_user_key = get_user_active_lobby_key(user.id) 
    lobby_data_key = get_lobby_data_key(lobby_id)
    lobby_players_key = get_lobby_players_key(lobby_id)
    
    async with r.pipeline(transaction=True) as pipe:
        pipe.set(lobby_data_key, lobby_json, ex=3600)
        pipe.zadd("lobbies:open", {lobby_id: lobby.created_at})
        pipe.set(lobby_user_key, lobby_id, ex=3600)
        pipe.sadd(lobby_players_key, user.id)
        pipe.expire(lobby_players_key, 3600)
        
        await pipe.execute()    
        

async def join_lobby(user_id: int, lobby: Lobby, r: redis.Redis):
    lobby_players_key = get_lobby_players_key(lobby.id)
    user_lobby_key = get_user_active_lobby_key(user_id)
    
    async with r.pipeline(transaction=True) as pipe:
        await pipe.watch(lobby_players_key)
    
        current_count = await r.scard(lobby_players_key)
        if current_count >= lobby.max_players:
            await pipe.unwatch()
            raise HTTPException(status_code=400, detail="Lobby is full!")

        pipe.multi()
        pipe.sadd(lobby_players_key, user_id)
        pipe.set(user_lobby_key, lobby.id, ex=3600) 
    
        await pipe.execute()
    

async def leave_lobby(user_id: int, lobby_id: str, r: redis.Redis):
    players_key = get_lobby_players_key(lobby_id)
    user_key = get_user_active_lobby_key(user_id)
    data_key = get_lobby_data_key(lobby_id)
    
    async with r.pipeline(transaction=True) as pipe:
        pipe.srem(players_key, user_id)
        pipe.delete(user_key)
        await pipe.execute()
    
    remaining_players = await r.scard(players_key)
    
    if remaining_players == 0:
        async with r.pipeline(transaction=True) as pipe:
            pipe.delete(data_key)
            pipe.delete(players_key)
            pipe.zrem("lobbies:open", lobby_id)
            await pipe.execute()

            
async def get_lobbies(r: redis.Redis):
    lobby_ids = await r.zrange("lobbies:open", 0, -1)
    if not lobby_ids:
        return []
    
    data_keys = [get_lobby_data_key(l_id) for l_id in lobby_ids]
    
    async with r.pipeline() as pipe:
        for key in data_keys:
            pipe.get(key)
        for l_id in lobby_ids:
            pipe.scard(get_lobby_players_key(l_id))
        
        results = await pipe.execute()

    mid = len(results) // 2
    raw_lobbies = results[:mid]
    player_counts = results[mid:]

    active_lobbies = []
    for raw, count in zip(raw_lobbies, player_counts):
        if raw:
            data = json.loads(raw)
            data["current_players"] = count
            active_lobbies.append(LobbyResponse(**data))
            
    return active_lobbies