from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, text
from sqlalchemy.orm import Session

from app.data.base import Base, BaseRead


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
