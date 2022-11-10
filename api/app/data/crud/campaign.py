from datetime import datetime
from enum import Enum

from app.data.base import Base, BaseRead
from app.data.crud.bookmark import Bookmark
from app.data.crud.pledge import Pledge
from pydantic import BaseModel
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, text
from sqlalchemy.orm import Session


class State(str, Enum):
    DRAFT = "draft"
    STARTED = "started"
    ENDED = "ended"
    LOCKED = "locked"
    GREENLIT = "greenlit"


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

    current_state = Column(String, server_default=State.DRAFT, nullable=False)


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

    current_state: State


class CampaignReadMeta(CampaignRead):
    bookmarked: bool


class CampaignUpdate(BaseModel):
    title: str | None
    description: str | None
    challenges: str | None


def create(u_id: int | Column, c: CampaignCreate, db: Session) -> Campaign:
    new_c = Campaign(campaigner_id=u_id, **c.dict())  # type: ignore
    db.add(new_c)

    db.commit()
    db.refresh(new_c)

    return new_c


def read(id: int | Column, db: Session) -> Campaign | None:
    return db.query(Campaign).filter(Campaign.id == id).first()


def read_all_by_campaigner(
    u_id: int | Column, limit: int, offset: int, db: Session
) -> list[Campaign]:
    return (
        db.query(Campaign)
        .filter(Campaign.campaigner_id == u_id)
        .limit(limit)
        .offset(offset)
        .all()
    )


def read_all_bookmarked(
    u_id: int | Column, limit: int, offset: int, db: Session
) -> list[Campaign]:
    return (
        db.query(Campaign)
        .join(Bookmark, Bookmark.campaign_id == Campaign.id)
        .filter(Bookmark.user_id == u_id)
        .limit(limit)
        .offset(offset)
        .all()
    )


def read_all_pledged(
    u_id: int | Column, limit: int, offset: int, db: Session
) -> list[Campaign]:
    return (
        db.query(Campaign)
        .join(Pledge, Pledge.campaign_id == Campaign.id)
        .filter(Pledge.pledger_id == u_id)
        .limit(limit)
        .offset(offset)
        .all()
    )


def read_all(limit: int, offset: int, db: Session) -> list[Campaign]:
    return db.query(Campaign).limit(limit).offset(offset).all()


def update(id: int | Column, c: CampaignUpdate, db: Session) -> None:
    db.query(Campaign).filter(Campaign.id == id).update(c.dict(exclude_unset=True))

    db.commit()


def update_state(id: int | Column, s: State, db: Session):
    db.query(Campaign).filter(Campaign.id == id).update({Campaign.current_state: s})

    db.commit()


def delete(id: int | Column, db: Session) -> None:
    db.query(Campaign).filter(Campaign.id == id).delete()

    db.commit()
