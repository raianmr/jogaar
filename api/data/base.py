from datetime import datetime

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import TIMESTAMP, Column, Integer, func
from sqlalchemy.orm import as_declarative, declared_attr

# TODO enforce char limit
# TODO explore sqlalchemy relationships
# TODO get dataclasses to work with sqlalchemy models


@as_declarative()
class Base:
    @declared_attr
    def __tablename__(cls) -> str:  # sourcery skip: instance-method-first-arg-name
        return f"{cls.__name__.lower()}s"  # type: ignore

    def __repr__(self) -> str:
        return str(jsonable_encoder(self))

    id = Column(Integer, primary_key=True)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )


class BaseRead(BaseModel):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
