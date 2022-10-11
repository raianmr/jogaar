from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Session

from app.data.base import Base, BaseRead


class Bookmark(Base):
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    campaign_id = Column(
        Integer, ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False
    )

    __table_args__ = tuple(UniqueConstraint(campaign_id, user_id))


class BookmarkCreate(BaseModel):
    campaign_id: int


class BookmarkRead(BaseRead):
    user_id: int
    campaign_id: int
