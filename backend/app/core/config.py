import os
from functools import lru_cache
from typing import List

from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseSettings


class Settings(BaseSettings):
    # Logging
    LOG_LEVEL: str = "INFO"

    # FastAPI
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALGORITHM: str = "HS256"
    DB_URL : str = "mysql+pymysql://dennis:foobar@mysql/innvesthotels"

@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
