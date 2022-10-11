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

    class Config:
        case_sensitive = False


env = Settings()
