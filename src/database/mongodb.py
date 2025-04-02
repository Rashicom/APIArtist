from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from config import get_settings
from beanie import init_beanie

settings = get_settings()

class MongoDBConnection:
    def __init__(self):
        self.client = None
        self.db = None
    
    async def initialize_connection(self):
        self.client = AsyncIOMotorClient(settings.MONGODB_URI)
        self.db = self.client[settings.MONGODB_DB_NAME]

        # Test connection
        respose = await self.db.command("ping")
        if int(respose["ok"]) != 1:
            raise Exception("MongoDB initialization Failed")
        
        print("MongoDB initialized successfully")
        await init_beanie(database=self.db, document_models=[])
        print("Beanie initialized successfully")

    async def close_connection(self):
        if self.client:
            await self.client.close()
            print("MongoDB connection closed")


mongodb = MongoDBConnection()


async def get_database() -> AsyncIOMotorDatabase:
    return mongodb.db