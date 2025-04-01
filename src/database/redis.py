import redis.asyncio as redis


class RedisConnection:
    def __init__(self):
        self.connection_pool = None
        self.cache = None
    
    async def initialize_connection(self):
        # Initialize Redis connection
        self.connection_pool = redis.ConnectionPool(
            host='localhost',
            port=6379,
            db=0,
            max_connections=100,
            password="123",
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
            self.cache.aclose()
            print("Redis connection closed")

redis_db = RedisConnection()

async def get_cache():
    return redis_db.cache