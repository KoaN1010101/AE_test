from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseSettings, EmailStr

load_dotenv('.env')


class Settings(BaseSettings):
    app_title: str = 'Проектный менеджер'
    database_url: str = 'sqlite+aiosqlite:///./project_manager'
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    class Config:
        env_file = '.env'


settings = Settings()
