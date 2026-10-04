from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):  
    hf_token: str
    ollama_base_url: str
    ollama_api_key: str = ""

    model_config = SettingsConfigDict(env_file=".env")

@lru_cache
def get_settings():
    return Settings()

settings = get_settings()