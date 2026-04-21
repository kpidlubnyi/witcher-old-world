import uuid
import time
import json
import redis.asyncio as redis

from .schemas import CreateLobby, Lobby


def create_lobby_model(data: CreateLobby):
    return Lobby(
        id=str(uuid.uuid4()),
        host_id='123',
        name=data.name,
        max_players=data.max_players,
        created_at=int(time.time())
    )


async def add_lobby(lobby:Lobby, r:redis.Redis):
    dumped_lobby = lobby.model_dump_json()
    
    return await r.zadd(
        "lobbies:open",
        {dumped_lobby: lobby.created_at}
    )
    
    
async def get_lobbies(r:redis.Redis):
    lobbies_from_redis =  await r.zrange("lobbies:open", 0, -1)
    lobbies = [json.loads(lb) for lb in lobbies_from_redis] 
    
    return lobbies
    