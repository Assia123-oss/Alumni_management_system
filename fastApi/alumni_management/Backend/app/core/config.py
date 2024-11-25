from pydantic import ConfigDict
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Alumni Management System"
    DATABASE_URL:str = "postgresql://postgres:tetaassia1@localhost:5432/alumni_management"
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=True
    )
    

settings = Settings()