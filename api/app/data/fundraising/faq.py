from datetime import datetime

from pydantic import BaseModel, EmailStr
from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Session

from app.data.base import Base, BaseRead


class FAQ(Base):
    campaign_id = Column(
        Integer, ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False
    )

    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)

    order = Column(Integer, server_default="0", nullable=False)

    __table_args__ = tuple(UniqueConstraint(campaign_id, question))


class FAQCreate(BaseModel):
    question: str
    answer: str
    order: int


class FAQRead(BaseRead):
    question: str
    answer: str
    order: int


class FAQUpdate(BaseModel):
    question: str | None
    answer: str | None
    order: int | None


def create(c_id: int, faq: FAQCreate, db: Session) -> FAQ:
    new_faq = FAQ(campaign_id=c_id, **faq.dict())  # type: ignore
    db.add(new_faq)

    db.commit()
    db.refresh(new_faq)

    return new_faq


def read(id: int, db: Session) -> FAQ | None:
    return db.query(FAQ).filter(FAQ.id == id).first()


def read_all_by_campaign(c_id: int, limit: int, offset: int, db: Session) -> list[FAQ]:
    return (
        db.query(FAQ).filter(FAQ.campaign_id == c_id).limit(limit).offset(offset).all()
    )


def read_all(limit: int, offset: int, db: Session) -> list[FAQ]:
    return db.query(FAQ).limit(limit).offset(offset).all()


def update(id: int, u: FAQUpdate, db: Session) -> None:
    db.query(FAQ).filter(FAQ.id == id).update(u.dict(exclude_unset=True))

    db.commit()


def delete(id: int, db: Session) -> None:
    db.query(FAQ).filter(FAQ.id == id).delete()

    db.commit()
