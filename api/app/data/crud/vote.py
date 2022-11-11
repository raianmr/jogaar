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


class VoteRead(BaseRead):
    user_id: int
    reply_id: int


def create(u_id: int | Column, r_id: int | Column, db: Session) -> Vote:
    new_v = Vote(user_id=u_id, reply_id=r_id)  # type: ignore
    db.add(new_v)

    db.commit()
    db.refresh(new_v)

    return new_v


def read(id: int | Column, db: Session) -> Vote | None:
    return db.query(Vote).filter(Vote.id == id).first()


def read_by_user_and_reply(
    u_id: int | Column, r_id: int | Column, db: Session
) -> Vote | None:
    return db.query(Vote).filter(Vote.user_id == u_id, Vote.reply_id == r_id).first()


def read_all_by_reply(
    r_id: int | Column, limit: int, offset: int, db: Session
) -> list[Vote]:
    return (
        db.query(Vote).filter(Vote.reply_id == r_id).limit(limit).offset(offset).all()
    )


def read_score_for_reply(r_id: int | Column, db: Session) -> int:
    return db.query(Vote).filter(Vote.reply_id == r_id).count()


def read_all(limit: int, offset: int, db: Session) -> list[Vote]:
    return db.query(Vote).limit(limit).offset(offset).all()


def delete(id: int | Column, db: Session) -> None:
    db.query(Vote).filter(Vote.id == id).delete()

    db.commit()


def delete_by_user_and_reply(
    u_id: int | Column, r_id: int | Column, db: Session
) -> None:
    db.query(Vote).filter(Vote.user_id == u_id, Vote.reply_id == r_id).delete()

    db.commit()
