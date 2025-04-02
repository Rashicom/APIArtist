from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    """
    Settings configuration
    """

    # mongodb credentials
    MONGODB_URI: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "testdatabase"
    
    # reids credentials
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_MAX_CONNECTIONS: int = 100
    REDIS_PASSWORD: str = "password"

    # google auth credentials
    CLIENT_ID: str = None
    PROJECT_ID: str = None
    CLIENT_SECRET: str = None
    AUTH_REDIRECT_URL: str = None

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings():
    return Settings()