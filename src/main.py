from fastapi import FastAPI
from contextlib import asynccontextmanager
from database.mongodb import mongodb
from database.redis import redis_db
from api import router

import os 
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

@asynccontextmanager
async def lifespan(app: FastAPI):
    await mongodb.initialize_connection()
    await redis_db.initialize_connection()
    yield
    await mongodb.close_connection()
    await redis_db.close_connection()


app = FastAPI(
    title="API Artist",
    description="APIArtist is a no-code platform that enables users to create custom APIs instantly by defining responses and generating endpoints effortlessly.",
    version="0.1.0",
    docs_url="/",
    redoc_url="/docs",

    lifespan=lifespan
)

app.include_router(router)