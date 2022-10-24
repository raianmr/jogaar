from app.data.base import Base, BaseRead
from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.orm import Session


class Vote(Base):
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    reply_id = Column(
        Integer, ForeignKey("replies.id", ondelete="CASCADE"), nullable=False
    )
    __table_args__ = tuple(UniqueConstraint(reply_id, user_id))


class VoteCreate(BaseModel):
    reply_id: int


class VoteRead(BaseRead):
    user_id: int
    reply_id: int


def create(_user_id: int, _reply_id: int, v: VoteCreate, db: Session) -> Vote:
    new_v = Vote(user_id=_user_id, reply_id=_reply_id, **v.dict())  # type: ignore
    db.add(new_v)

    db.commit()
    db.refresh(new_v)

    return new_v


def read(id: int, db: Session) -> Vote | None:
    return db.query(Vote).filter(Vote.id == id).first()


def read_all_by_reply(r_id: int, limit: int, offset: int, db: Session) -> list[Vote]:
    return (
        db.query(Vote).filter(Vote.reply_id == r_id).limit(limit).offset(offset).all()
    )


def read_score_for_reply(r_id: int, db: Session) -> int:
    return db.query(Vote).filter(Vote.reply_id == r_id).count()


def read_all(limit: int, offset: int, db: Session) -> list[Vote]:
    return db.query(Vote).limit(limit).offset(offset).all()


def delete(id: int, db: Session) -> None:
    db.query(Vote).filter(Vote.id == id).delete()

    db.commit()
