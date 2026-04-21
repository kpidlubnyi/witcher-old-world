from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
import redis.asyncio as redis
from typing import AsyncGenerator

class RedisClient:
    def __init__(self):
        self.client: redis.Redis | None = None

    async def connect(self):
        self.client = redis.from_url(
            "redis://localhost:6379/0",
            encoding="utf-8",
            decode_responses=True
        )

    async def disconnect(self):
        if self.client:
            await self.client.close()


class PostgresClient:
    def __init__(self):
        self.engine = None
        self.session_factory = None

    async def connect(self):
        self.engine = create_async_engine(
            "postgresql+asyncpg://user:password@localhost:5432/dbname",
            echo=False
        )
        self.session_factory = async_sessionmaker(
            self.engine,
            expire_on_commit=False
        )

    async def disconnect(self):
        if self.engine:
            await self.engine.dispose()


pg_manager = PostgresClient()
redis_manager = RedisClient()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with pg_manager.session_factory() as session:
        yield session
        

async def get_redis() -> AsyncGenerator[redis.Redis, None]:
    yield redis_manager.client
    