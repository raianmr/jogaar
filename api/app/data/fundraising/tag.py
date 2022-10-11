from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Session

from app.data.base import Base, BaseRead


class Tag(Base):
    campaign_id = Column(
        Integer, ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False
    )

    name = Column(String, nullable=False)

    __table_args__ = tuple(UniqueConstraint(campaign_id, name))


class TagCreate(BaseModel):
    name: str


class TagRead(BaseRead):
    name: str


class TagUpdate(BaseModel):
    name: str
