from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, text
from sqlalchemy.orm import Session

from app.data.base import Base, BaseRead

# from app.data.auth import User


class Campaign(Base):
    campaigner_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    challenges = Column(String, nullable=False)

    goal = Column(Integer, nullable=False)
    pledged = Column(Integer, server_default="0", nullable=False)

    deadline = Column(
        TIMESTAMP(timezone=True),
        server_default=text("NOW() + INTERVAL '1 month'"),
        nullable=False,
    )


class CampaignCreate(BaseModel):
    title: str
    description: str
    challenges: str

    goal: int
    deadline: datetime


class CampaignRead(BaseRead):
    campaigner_id: int

    title: str
    description: str
    challenges: str

    goal: int
    pledged: int
    deadline: datetime


class CampaignUpdate(BaseModel):
    title: str | None
    description: str | None
    challenges: str | None


def create(u_id: int, c: CampaignCreate, db: Session) -> Campaign:
    new_c = Campaign(campaigner_id=u_id, **c.dict())  # type: ignore
    db.add(new_c)

    db.commit()
    db.refresh(new_c)

    return new_c


def read(id: int, db: Session) -> Campaign | None:
    return db.query(Campaign).filter(Campaign.id == id).first()


def read_all_by_user(u_id: int, limit: int, offset: int, db: Session) -> list[Campaign]:
    return (
        db.query(Campaign)
        .filter(Campaign.campaigner_id == u_id)
        .limit(limit)
        .offset(offset)
        .all()
    )


def read_all(limit: int, offset: int, db: Session) -> list[Campaign]:
    return db.query(Campaign).limit(limit).offset(offset).all()


def update(id: int, u: CampaignUpdate, db: Session) -> None:
    db.query(Campaign).filter(Campaign.id == id).update(u.dict(exclude_unset=True))

    db.commit()


def delete(id: int, db: Session) -> None:
    db.query(Campaign).filter(Campaign.id == id).delete()

    db.commit()
