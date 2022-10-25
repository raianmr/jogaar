from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_TYPE: str = ""
    DB_USER: str = ""
    DB_PASS: str = ""
    DB_HOST: str = ""
    DB_PORT: str = ""
    DB_NAME: str = ""

    WEB_PORT: str = ""
    API_PORT: str = ""

    ALGORITHM: str = ""
    SECRET_KEY: str = ""
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 0

    class Config:
        case_sensitive = False


env = Settings()
