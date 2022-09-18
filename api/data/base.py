from sqlalchemy import Column, Integer, TIMESTAMP, func
from sqlalchemy.orm import as_declarative, declared_attr
from fastapi.encoders import jsonable_encoder

# TODO payment related info, enforce char limit


@as_declarative()
class Base:
    @declared_attr
    def __tablename__(cls) -> str:  # sourcery skip: instance-method-first-arg-name
        return cls.__name__.lower()  # type: ignore # TODO plural table names

    def __repr__(self):
        return str(jsonable_encoder(self))

    id = Column(Integer, primary_key=True)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )


