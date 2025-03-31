from fastapi import FastAPI

app = FastAPI(
    title="API Artist",
    description="APIArtist is a no-code platform that enables users to create custom APIs instantly by defining responses and generating endpoints effortlessly.",
    version="0.1.0",
    docs_url="/",
    redoc_url="/docs"
)