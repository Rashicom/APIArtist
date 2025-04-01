from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Settings configuration
    """
    
    
    model_config = SettingsConfigDict(env_file=".env")