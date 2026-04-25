import redis.asyncio as redis
import asyncio
from fastapi import APIRouter, Depends, Form, HTTPException, Response, status, WebSocket
from typing import Annotated

from src.database import get_redis
from src.auth.dependencies import get_current_user
from src.auth.models import User

from .schemas import *
from .service import *


type RedisDependency = Annotated[redis.Redis, Depends(get_redis)]
type CurrentUserDependency = Annotated[User, Depends(get_current_user)]


lobbies_router = APIRouter(
    prefix='/lobbies',
    tags=['lobbies']
)


@lobbies_router.websocket("/")
async def lobbies_root(websocket: WebSocket, r: RedisDependency):
    await websocket.accept()

    while True:
        data = await get_lobbies(r)
        await websocket.send_json([lobby.model_dump() for lobby in data])
        await asyncio.sleep(2)


@lobbies_router.post("/create")
async def create_lobby_endpoint(
    lobby_form: Annotated[CreateLobby, Form], 
    r: RedisDependency,
    current_user: CurrentUserDependency
):
    if await user_has_active_lobby(current_user, r):
        raise HTTPException(status_code=409, detail="User already has active lobby!")
    
    try:
        lobby = create_lobby_model(lobby_form, current_user)
        await create_lobby(lobby, r, current_user)
        
        return Response(
            status_code=status.HTTP_201_CREATED,
            content=lobby.model_dump_json(),
            media_type="application/json"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
from redis.exceptions import WatchError

@lobbies_router.post("/{lobby_id}/join")
async def join_lobby_endpoint(
    lobby_id: str,
    user: User = Depends(get_current_user),
    r: redis.Redis = Depends(get_redis)
):
    if await user_has_active_lobby(user, r):
        raise HTTPException(status_code=400, detail="You are already in lobby!")

    if not (raw_lobby :=  await get_raw_lobby(lobby_id, r)):
        raise HTTPException(status_code=404, detail="Lobby not found")
    
    lobby = Lobby.model_validate_json(raw_lobby)
    
    try:
        await join_lobby(user, lobby, r)
    except WatchError:
        raise HTTPException(
            status_code=409, 
            detail="Error occured, try again!"
        )

    return LobbyResponse(**lobby.model_dump())


@lobbies_router.get("/test")
async def test(r: redis.Redis = Depends(get_redis)):
    await r.set("key", "value", ex=60)
    return {"value": await r.get("key")}