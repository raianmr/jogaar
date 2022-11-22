from app.data.base import Base, BaseRead
from pydantic import BaseModel
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, text
from sqlalchemy.orm import Session


class Update(Base):
    campaign_id = Column(
        Integer, ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False
    )

    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    picture_id = Column(Integer, ForeignKey("images.id", ondelete="CASCADE"))

    edited = Column(Boolean, server_default=text("False"), nullable=False)


class UpdateCreate(BaseModel):
    title: str
    content: str


class UpdateRead(BaseRead):
    campaign_id: int

    title: str
    content: str
    picture_id: int | None

    edited: bool


class UpdateUpdate(BaseModel):
    title: str | None
    content: str | None
    picture_id: int | None


def create(c_id: int | Column, up: UpdateCreate, db: Session) -> Update:
    new_up = Update(campaign_id=c_id, **up.dict())  # type: ignore
    db.add(new_up)

    db.commit()
    db.refresh(new_up)

    return new_up


def read(id: int | Column, db: Session) -> Update | None:
    return db.query(Update).filter(Update.id == id).first()


def read_all_by_campaign(
    c_id: int | Column, limit: int, offset: int, db: Session
) -> list[Update]:
    return (
        db.query(Update)
        .filter(Update.campaign_id == c_id)
        .limit(limit)
        .offset(offset)
        .all()
    )


def read_all(limit: int, offset: int, db: Session) -> list[Update]:
    return db.query(Update).limit(limit).offset(offset).all()


def update(id: int | Column, up: UpdateUpdate, db: Session) -> None:
    db.query(Update).filter(Update.id == id).update(
        {Update.edited: True, **up.dict(exclude_unset=True)}
    )

    db.commit()


def delete(id: int | Column, db: Session) -> None:
    db.query(Update).filter(Update.id == id).delete()

    db.commit()
