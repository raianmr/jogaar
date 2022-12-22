from contextlib import contextmanager
from typing import Final, Generator

from app.core.config import env
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

DB_URL = f"{env.DB_TYPE}://{env.DB_USER}:{env.DB_PASS}@{env.DB_HOST}:{env.DB_PORT}/{env.DB_NAME}"

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)  # type: ignore


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


get_db_ctx: Final = contextmanager(get_db)
