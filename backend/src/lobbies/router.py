import redis.asyncio as redis
from redis.exceptions import WatchError
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
    current_user: CurrentUserDependency,
    r: RedisDependency,
):
    if await user_has_active_lobby(current_user, r):
        raise HTTPException(status_code=409, detail="User already has active lobby!")
    
    try:
        lobby = create_lobby_model(lobby_form, current_user)
        await create_lobby(lobby, r, current_user)
        
        return Response(
            status_code=status.HTTP_201_CREATED,
            content=LobbyResponse(**lobby.model_dump(), current_players=1).model_dump_json(),
            media_type="application/json"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@lobbies_router.post("/{lobby_id}/join")
async def join_lobby_endpoint(
    lobby_id: str,
    user: CurrentUserDependency,
    r: RedisDependency
):
    if await user_has_active_lobby(user, r):
        raise HTTPException(status_code=400, detail="You are already in lobby!")

    raw_lobby = await get_raw_lobby(lobby_id, r)
    if not raw_lobby:
        raise HTTPException(status_code=404, detail="Lobby not found")
    
    lobby = Lobby.model_validate_json(raw_lobby)
    
    try:
        await join_lobby(user.id, lobby, r)
        
        current_players = await r.scard(get_lobby_players_key(lobby_id))
        
        return Response(
            status_code=status.HTTP_200_OK,
            content=LobbyResponse(**lobby.model_dump(), current_players=current_players).model_dump_json(),
            media_type="application/json"
        )
    except WatchError:
        raise HTTPException(status_code=409, detail="Error occurred, try again!")


@lobbies_router.post("/{lobby_id}/leave")
async def leave_lobby_endpoint(
    lobby_id: str,
    user: CurrentUserDependency,
    r: RedisDependency
):
    user_lobby = await r.get(get_user_active_lobby_key(user.id))

    if not user_lobby or user_lobby != lobby_id:
        raise HTTPException(status_code=400, detail="User is not in this lobby!")

    await leave_lobby(user.id, lobby_id, r)
    
    response_content = {
        "status": "success",
        "message": "You have left the lobby",
        "data": {
            "user_id": user.id,
            "lobby_id": lobby_id
        }
    }
    
    return Response(
        status_code=status.HTTP_200_OK,
        content=json.dumps(response_content),
        media_type="application/json"
    )
    
    
@lobbies_router.get("/my-status")
async def get_my_status(
    user: CurrentUserDependency,
    r: RedisDependency
):
    lobby_id = await r.get(get_user_active_lobby_key(user.id))
    
    status_data = {
        "is_in_lobby": lobby_id is not None,
        "lobby_id": lobby_id
    }
    
    return Response(
        status_code=status.HTTP_200_OK,
        content=json.dumps(status_data),
        media_type="application/json"
    )