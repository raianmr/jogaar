from datetime import datetime

import sqlalchemy as sa
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import orm

# TODO enforce char limit
# TODO explore sqlalchemy relationships


@orm.as_declarative()
class Base:
    @orm.declared_attr
    def __tablename__(cls) -> str:  # sourcery skip: instance-method-first-arg-name
        return f"{cls.__name__.lower()}s"  # type: ignore

    def __repr__(self) -> str:
        return str(jsonable_encoder(self))

    id = sa.Column(sa.Integer, primary_key=True)
    created_at = sa.Column(
        sa.TIMESTAMP(timezone=True), server_default=sa.func.now(), nullable=False
    )


class BaseRead(BaseModel):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
        use_enum_values = True
