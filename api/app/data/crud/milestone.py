from datetime import datetime

from app.data.base import Base, BaseRead
from pydantic import BaseModel
from sqlalchemy import (
    TIMESTAMP,
    Column,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    text,
)
from sqlalchemy.orm import Session


class Milestone(Base):
    campaign_id = Column(
        Integer, ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False
    )

    title = Column(String, nullable=False)
    description = Column(String, nullable=False)

    deadline = Column(
        TIMESTAMP(timezone=True),
        server_default=text("NOW() + INTERVAL '1 week'"),
        nullable=False,
    )

    __table_args__ = tuple(UniqueConstraint(campaign_id, deadline))


class MilestoneCreate(BaseModel):
    title: str
    description: str
    deadline: datetime


class MilestoneRead(BaseRead):
    title: str
    description: str
    deadline: datetime


class MilestoneUpdate(BaseModel):
    title: str | None
    description: str | None
    deadline: datetime | None


def create(c_id: int | Column, m: MilestoneCreate, db: Session) -> Milestone:
    new_m = Milestone(campaign_id=c_id, **m.dict())  # type: ignore
    db.add(new_m)

    db.commit()
    db.refresh(new_m)

    return new_m


def read(id: int | Column, db: Session) -> Milestone | None:
    return db.query(Milestone).filter(Milestone.id == id).first()


def read_all_by_campaign(
    c_id: int | Column, limit: int, offset: int, db: Session
) -> list[Milestone]:
    return (
        db.query(Milestone)
        .filter(Milestone.campaign_id == c_id)
        .limit(limit)
        .offset(offset)
        .all()
    )


def read_all(limit: int, offset: int, db: Session) -> list[Milestone]:
    return db.query(Milestone).limit(limit).offset(offset).all()


def update(id: int | Column, m: MilestoneUpdate, db: Session) -> None:
    db.query(Milestone).filter(Milestone.id == id).update(m.dict(exclude_unset=True))

    db.commit()


def delete(id: int | Column, db: Session) -> None:
    db.query(Milestone).filter(Milestone.id == id).delete()

    db.commit()
