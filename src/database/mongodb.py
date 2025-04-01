from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase


MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "mydatabase"

class MongoDBConnection:
    def __init__(self):
        self.client = None
        self.db = None
    
    async def initialize_connection(self):
        self.client = AsyncIOMotorClient(MONGO_URI)
        self.db = self.client[DB_NAME]

        # Test connection
        respose = await self.db.command("ping")
        if int(respose["ok"]) != 1:
            raise Exception("MongoDB initialization Failed")
        else:
            print("MongoDB initialized successfully")

    async def close_connection(self):
        if self.client:
            await self.client.close()
            print("MongoDB connection closed")


mongodb = MongoDBConnection()


async def get_database() -> AsyncIOMotorDatabase:
    return mongodb.db