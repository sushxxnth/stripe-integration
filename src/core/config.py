from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_PASSWORD: str
    model_config = SettingsConfigDict(env_file=".env")
