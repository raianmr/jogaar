from datetime import datetime

from pydantic import BaseModel, EmailStr
from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Session

from app.data.base import Base, BaseRead


class FAQ(Base):
    campaign_id = Column(
        Integer, ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False
    )

    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)

    order = Column(Integer, server_default="0", nullable=False)

    __table_args__ = tuple(UniqueConstraint(campaign_id, question))


class FAQCreate(BaseModel):
    question: str
    answer: str
    order: int


class FAQRead(BaseRead):
    question: str
    answer: str
    order: int


class FAQUpdate(BaseModel):
    question: str | None
    answer: str | None
    order: int | None
