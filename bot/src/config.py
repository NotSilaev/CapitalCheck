from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Telegram Bot
    telegram_bot_token: str

    # Database
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str

    # Cache
    cache_host: str
    cache_port: int
    cache_db: int
    cache_max_connections: int

    class Config:
        env_file = Path(__file__).parent / '.env'


settings = Settings()
