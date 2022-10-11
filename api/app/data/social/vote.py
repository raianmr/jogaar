from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Session

from app.data.base import Base, BaseRead


class Vote(Base):
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    reply_id = Column(
        Integer, ForeignKey("replies.id", ondelete="CASCADE"), nullable=False
    )
    __table_args__ = tuple(UniqueConstraint(reply_id, user_id))


class VoteCreate(BaseModel):
    reply_id: int


class VoteRead(BaseRead):
    user_id: int
    reply_id: int
    update_id: int
    campaign_id: int
