from datetime import datetime
from enum import Enum

import sqlalchemy as sa
from app.data.base import Base, BaseRead
from pydantic import BaseModel
from sqlalchemy.orm import Session


class State(str, Enum):
    DRAFT = "draft"
    STARTED = "started"
    ENDED = "ended"
    LOCKED = "locked"
    GREENLIT = "greenlit"


class Campaign(Base):
    campaigner_id = sa.Column(
        sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    title = sa.Column(sa.String, nullable=False)
    description = sa.Column(sa.String, nullable=False)
    challenges = sa.Column(sa.String, nullable=False)
    cover_id = sa.Column(sa.Integer, sa.ForeignKey("images.id", ondelete="CASCADE"))

    goal = sa.Column(sa.Integer, nullable=False)
    pledged = sa.Column(sa.Integer, server_default="0", nullable=False)

    deadline = sa.Column(
        sa.TIMESTAMP(timezone=True),
        server_default=sa.text("NOW() + INTERVAL '1 month'"),
        nullable=False,
    )

    current_state = sa.Column(sa.String, server_default=State.DRAFT, nullable=False)


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
    cover_id: int | None

    goal: int
    pledged: int
    deadline: datetime

    current_state: State


class CampaignReadMeta(CampaignRead):
    bookmarked: bool


class CampaignUpdate(BaseModel):
    title: str | None
    description: str | None
    challenges: str | None
    cover_id: int | None


def create(u_id: int | sa.Column, c: CampaignCreate, db: Session) -> Campaign:
    new_c = Campaign(campaigner_id=u_id, **c.dict())  # type: ignore
    db.add(new_c)

    db.commit()
    db.refresh(new_c)

    return new_c


def read(id: int | sa.Column, db: Session) -> Campaign | None:
    return db.query(Campaign).filter(Campaign.id == id).first()


def read_all_by_campaigner(
    u_id: int | sa.Column, limit: int, offset: int, db: Session
) -> list[Campaign]:
    return (
        db.query(Campaign)
        .filter(Campaign.campaigner_id == u_id)
        .limit(limit)
        .offset(offset)
        .all()
    )


def read_all_by_state(s: State, limit: int, offset: int, db: Session) -> list[Campaign]:
    return (
        db.query(Campaign)
        .filter(Campaign.current_state == s)
        .limit(limit)
        .offset(offset)
        .all()
    )


def read_all(limit: int, offset: int, db: Session) -> list[Campaign]:
    return db.query(Campaign).limit(limit).offset(offset).all()


def update(id: int | sa.Column, c: CampaignUpdate, db: Session) -> None:
    db.query(Campaign).filter(Campaign.id == id).update(c.dict(exclude_unset=True))

    db.commit()


def update_pledged(c_id: int | sa.Column, amount: int | sa.Column, db: Session):
    db.query(Campaign).filter(Campaign.id == c_id).update({Campaign.pledged: amount})

    db.commit()


def update_state(id: int | sa.Column, s: State, db: Session):
    db.query(Campaign).filter(Campaign.id == id).update({Campaign.current_state: s})

    db.commit()


def delete(id: int | sa.Column, db: Session) -> None:
    db.query(Campaign).filter(Campaign.id == id).delete()

    db.commit()
