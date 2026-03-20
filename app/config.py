from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # Эти поля остаются для локальной разработки
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    # Новое поле для Heroku (Optional, так как локально его может не быть)
    database_url: Optional[str] = None 
    
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()