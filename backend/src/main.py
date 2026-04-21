from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .lobbies.router import lobbies_router
from .auth.router import auth_router
from .database import redis_manager, pg_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await pg_manager.connect()
    await redis_manager.connect()

    yield

    await pg_manager.disconnect()
    await redis_manager.disconnect()


app = FastAPI(lifespan=lifespan)
app.include_router(lobbies_router)
app.include_router(auth_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)