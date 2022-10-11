from datetime import datetime

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

from app.data.base import Base, BaseRead


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
