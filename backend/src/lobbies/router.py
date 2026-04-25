import redis.asyncio as redis
import asyncio
from fastapi import APIRouter, Depends, Form, HTTPException, Response, status, WebSocket, Path
from typing import Annotated

from src.database import get_redis
from src.auth.dependencies import get_current_user
from src.auth.models import User

from .schemas import CreateLobby
from .service import create_lobby_model, add_lobby, get_lobbies, user_has_active_lobby


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
        await asyncio.sleep(5)


@lobbies_router.post("/create")
async def create_lobby(
    lobby_form: Annotated[CreateLobby, Form], 
    r: RedisDependency,
    current_user: CurrentUserDependency
):
    if await user_has_active_lobby(current_user, r):
        raise HTTPException(status_code=409, detail="User already has active lobby!")
    
    try:
        lobby = create_lobby_model(lobby_form, current_user)
        await add_lobby(lobby, r, current_user)
        
        return Response(
            status_code=status.HTTP_201_CREATED,
            content=lobby.model_dump_json(),
            media_type="application/json"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
#@lobbies_router.post("/{lobby_id}/join")
#async def join_to_lobby(lobby_id: Annotated[str, Path], r: RedisDependency, user=Depends(get_user)):
#    try:
#        await r.sadd(
#            f"lobby:{lobby_id}:players",
#            user
#        )
    


@lobbies_router.get("/test")
async def test(r: redis.Redis = Depends(get_redis)):
    await r.set("key", "value", ex=60)
    return {"value": await r.get("key")}