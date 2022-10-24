from app.data.base import Base, BaseRead
from pydantic import BaseModel
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, text
from sqlalchemy.orm import Session


class Reply(Base):
    __tablename__ = "replies"  # type: ignore

    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    update_id = Column(
        Integer, ForeignKey("updates.id", ondelete="CASCADE"), nullable=False
    )

    content = Column(String, nullable=False)
    edited = Column(Boolean, server_default=text("False"), nullable=False)


class ReplyCreate(BaseModel):
    content: str


class ReplyRead(BaseRead):
    user_id: int
    update_id: int

    content: str
    edited: bool


class ReplyUpdate(BaseModel):
    content: str


def create(_user_id: int, _update_id: int, r: ReplyCreate, db: Session) -> Reply:
    new_r = Reply(user_id=_user_id, update_id=_update_id, **r.dict())  # type: ignore
    db.add(new_r)

    db.commit()
    db.refresh(new_r)

    return new_r


def read(id: int, db: Session) -> Reply | None:
    return db.query(Reply).filter(Reply.id == id).first()


def read_all_by_update(u_id: int, limit: int, offset: int, db: Session) -> list[Reply]:
    return (
        db.query(Reply)
        .filter(Reply.update_id == u_id)
        .limit(limit)
        .offset(offset)
        .all()
    )


def read_all(limit: int, offset: int, db: Session) -> list[Reply]:
    return db.query(Reply).limit(limit).offset(offset).all()


def update(id: int, u: ReplyUpdate, db: Session) -> None:
    db.query(Reply).filter(Reply.id == id).update(u.dict(exclude_unset=True))

    db.commit()


def delete(id: int, db: Session) -> None:
    db.query(Reply).filter(Reply.id == id).delete()

    db.commit()
