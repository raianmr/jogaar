import sqlalchemy as sa
from app.data.base import Base, BaseRead
from pydantic import BaseModel
from sqlalchemy.orm import Session


class Reply(Base):
    __tablename__ = "replies"  # type: ignore

    user_id = sa.Column(
        sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    update_id = sa.Column(
        sa.Integer, sa.ForeignKey("updates.id", ondelete="CASCADE"), nullable=False
    )

    content = sa.Column(sa.String, nullable=False)
    edited = sa.Column(sa.Boolean, server_default=sa.text("False"), nullable=False)


class ReplyCreate(BaseModel):
    content: str


class ReplyRead(BaseRead):
    user_id: int
    update_id: int

    content: str
    edited: bool


class ReplyUpdate(BaseModel):
    content: str


def create(
    u_id: int | sa.Column, up_id: int | sa.Column, r: ReplyCreate, db: Session
) -> Reply:
    new_r = Reply(user_id=u_id, update_id=up_id, **r.dict())  # type: ignore
    db.add(new_r)

    db.commit()
    db.refresh(new_r)

    return new_r


def read(id: int | sa.Column, db: Session) -> Reply | None:
    return db.query(Reply).filter(Reply.id == id).first()


def read_all_by_update(
    up_id: int | sa.Column, limit: int, offset: int, db: Session
) -> list[Reply]:
    return (
        db.query(Reply)
        .filter(Reply.update_id == up_id)
        .limit(limit)
        .offset(offset)
        .all()
    )


def read_all(limit: int, offset: int, db: Session) -> list[Reply]:
    return db.query(Reply).limit(limit).offset(offset).all()


def update(id: int | sa.Column, r: ReplyUpdate, db: Session) -> None:
    db.query(Reply).filter(Reply.id == id).update(
        {Reply.edited: True, **r.dict(exclude_unset=True)}
    )

    db.commit()


def delete(id: int | sa.Column, db: Session) -> None:
    db.query(Reply).filter(Reply.id == id).delete()

    db.commit()
