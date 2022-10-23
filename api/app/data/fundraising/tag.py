from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Session

from app.data.base import Base, BaseRead


class Tag(Base):
    campaign_id = Column(
        Integer, ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False
    )

    name = Column(String, nullable=False)

    __table_args__ = tuple(UniqueConstraint(campaign_id, name))


class TagCreate(BaseModel):
    name: str


class TagRead(BaseRead):
    name: str


class TagUpdate(BaseModel):
    name: str


def create(c_id: int, t: TagCreate, db: Session) -> Tag:
    new_t = Tag(campaign_id=c_id, **t.dict())  # type: ignore
    db.add(new_t)

    db.commit()
    db.refresh(new_t)

    return new_t


def read(id: int, db: Session) -> Tag | None:
    return db.query(Tag).filter(Tag.id == id).first()


def read_all_by_campaign(
    c_id: int, limit: int, offset: int, db: Session
) -> list[Tag]:
    return (
        db.query(Tag)
        .filter(Tag.campaign_id == c_id)
        .limit(limit)
        .offset(offset)
        .all()
    )


def read_all(limit: int, offset: int, db: Session) -> list[Tag]:
    return db.query(Tag).limit(limit).offset(offset).all()


def update(id: int, u: TagUpdate, db: Session) -> None:
    db.query(Tag).filter(Tag.id == id).update(u.dict(exclude_unset=True))

    db.commit()


def delete(id: int, db: Session) -> None:
    db.query(Tag).filter(Tag.id == id).delete()

    db.commit()
