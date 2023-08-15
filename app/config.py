import os
import pytz
from pydantic import BaseSettings
from passlib.context import CryptContext


class Settings(BaseSettings):
    # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    TELEGRAM_BOT_TOKEN: str = '6026174140:AAFK-yv9KjrazxhjK-SD1WN4IAk5TJfF3Qw'

    SERVICE_NAME: str = 'fab'
    SERVICE_HOST: str = '0.0.0.0'
    SERVICE_PORT: int = 8000

    JWT_ALGORITHM: str = 'HS256'
    JWT_SECRET_KEY: str = 'secret'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 24*60

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG: bool = False
    SHOW_DOCS: bool = True

    TIMEZONE = pytz.timezone('Asia/Almaty')
    PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

    class Config:
        case_sensitive = True
        env_file = 'env/app'


settings = Settings()
