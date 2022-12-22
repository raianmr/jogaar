import logging

from pydantic import BaseSettings, EmailStr, ValidationError


class Settings(BaseSettings):
    DB_TYPE: str
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str

    WEB_PORT: str
    API_PORT: str

    ALGORITHM: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    ADMIN_NAME: str
    ADMIN_MAIL: EmailStr
    ADMIN_PASS: str

    class Config:
        case_sensitive = False


try:
    env = Settings()  # type: ignore
except ValidationError as err:
    print("env variables unset, set those and restart: \n", err)
    exit()
