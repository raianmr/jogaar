import sqlalchemy as sa
from app.data.base import Base, BaseRead
from pydantic import BaseModel
from sqlalchemy.orm import Session


class FAQ(Base):
    campaign_id = sa.Column(
        sa.Integer, sa.ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False
    )

    question = sa.Column(sa.String, nullable=False)
    answer = sa.Column(sa.String, nullable=False)

    order = sa.Column(sa.Integer, server_default="0", nullable=False)

    __table_args__ = tuple(sa.UniqueConstraint(campaign_id, question))


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


def create(c_id: int | sa.Column, f: FAQCreate, db: Session) -> FAQ:
    new_faq = FAQ(campaign_id=c_id, **f.dict())  # type: ignore
    db.add(new_faq)

    db.commit()
    db.refresh(new_faq)

    return new_faq


def read(id: int | sa.Column, db: Session) -> FAQ | None:
    return db.query(FAQ).filter(FAQ.id == id).first()


def read_all_by_campaign(
    c_id: int | sa.Column, limit: int, offset: int, db: Session
) -> list[FAQ]:
    return (
        db.query(FAQ).filter(FAQ.campaign_id == c_id).limit(limit).offset(offset).all()
    )


def read_all(limit: int, offset: int, db: Session) -> list[FAQ]:
    return db.query(FAQ).limit(limit).offset(offset).all()


def update(id: int | sa.Column, f: FAQUpdate, db: Session) -> None:
    db.query(FAQ).filter(FAQ.id == id).update(f.dict(exclude_unset=True))

    db.commit()


def delete(id: int | sa.Column, db: Session) -> None:
    db.query(FAQ).filter(FAQ.id == id).delete()

    db.commit()
