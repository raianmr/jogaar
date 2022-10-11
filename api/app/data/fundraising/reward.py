from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Session

from app.data.base import Base, BaseRead


class Reward(Base):
    campaign_id = Column(
        Integer, ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False
    )

    title = Column(String, nullable=False)
    description = Column(String, nullable=False)

    pledge = Column(Integer, nullable=False)

    __table_args__ = tuple(UniqueConstraint(campaign_id, pledge))


class RewardCreate(BaseModel):
    title: str
    description: str
    pledge: int


class RewardRead(BaseRead):
    title: str
    description: str
    pledge: int


class RewardUpdate(BaseModel):
    title: str | None
    description: str | None
    pledge: int | None
