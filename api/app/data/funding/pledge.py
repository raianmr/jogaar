from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Session

from app.data.base import Base, BaseRead


class Pledge(Base):
    pledger_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    campaign_id = Column(
        Integer, ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False
    )
    amount = Column(Integer, nullable=False)

    __table_args__ = tuple(UniqueConstraint(campaign_id, pledger_id))


class PledgeCreate(BaseModel):
    campaign_id: int
    amount: int


class PledgeRead(BaseRead):
    pledger_id: int
    campaign_id: int
    amount: int


class PledgeUpdate(BaseModel):
    amount: int | None

