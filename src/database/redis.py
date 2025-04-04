import redis.asyncio as redis
from config import get_settings
from fastapi import Depends
from typing import Annotated

settings = get_settings()


class RedisConnection:
    def __init__(self):
        self.connection_pool = None
        self.cache = None
    
    async def initialize_connection(self):
        # Initialize Redis connection
        self.connection_pool = redis.ConnectionPool(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            max_connections=settings.REDIS_MAX_CONNECTIONS,
            password=settings.REDIS_PASSWORD,
            decode_responses=True,
        )
        self.cache = redis.Redis(connection_pool=self.connection_pool)

        # Test connection
        try:
            await self.cache.ping()
        except Exception as e:
            raise Exception("Redis initialization Failed")
        else:
            print("Redis initialized successfully")
    
    async def close_connection(self):
        if self.cache:
            await self.cache.aclose()
            print("Redis connection closed")

redis_db = RedisConnection()

async def get_cache():
    return redis_db.cache

redis_cache = Annotated[redis.Redis, Depends(get_cache)]