from app.data.base import Base, BaseRead
from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Session


class Bookmark(Base):
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    campaign_id = Column(
        Integer, ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False
    )

    __table_args__ = tuple(UniqueConstraint(campaign_id, user_id))


class BookmarkRead(BaseRead):
    user_id: int
    campaign_id: int


def create(u_id: int | Column, c_id: int | Column, db: Session) -> Bookmark:
    new_b = Bookmark(user_id=u_id, campaign_id=c_id)  # type: ignore
    db.add(new_b)

    db.commit()
    db.refresh(new_b)

    return new_b


def read(id: int | Column, db: Session) -> Bookmark | None:
    return db.query(Bookmark).filter(Bookmark.id == id).first()


def read_by_user_and_campaign(
    u_id: int | Column, c_id: int | Column, db: Session
) -> Bookmark | None:
    return (
        db.query(Bookmark)
        .filter(Bookmark.user_id == u_id, Bookmark.campaign_id == c_id)
        .first()
    )


def read_all_by_user(
    u_id: int | Column, limit: int, offset: int, db: Session
) -> list[Bookmark]:
    return (
        db.query(Bookmark)
        .filter(Bookmark.user_id == u_id)
        .limit(limit)
        .offset(offset)
        .all()
    )


def read_all_by_campaign(
    c_id: int | Column, limit: int, offset: int, db: Session
) -> list[Bookmark]:
    return (
        db.query(Bookmark)
        .filter(Bookmark.campaign_id == c_id)
        .limit(limit)
        .offset(offset)
        .all()
    )


def read_all(limit: int, offset: int, db: Session) -> list[Bookmark]:
    return db.query(Bookmark).limit(limit).offset(offset).all()


def delete(id: int | Column, db: Session) -> None:
    db.query(Bookmark).filter(Bookmark.id == id).delete()

    db.commit()


def delete_by_user_and_campaign(
    u_id: int | Column, c_id: int | Column, db: Session
) -> None:
    db.query(Bookmark).filter(
        Bookmark.user_id == u_id, Bookmark.campaign_id == c_id
    ).delete()

    db.commit()
