from pydantic import BaseModel
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, text
from sqlalchemy.orm import Session

from app.data.base import Base, BaseRead


class Update(Base):
    campaign_id = Column(
        Integer, ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False
    )

    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    edited = Column(Boolean, server_default=text("False"), nullable=False)


class UpdateCreate(BaseModel):
    campaign_id: int

    title: str
    content: str


class UpdateRead(BaseRead):
    campaign_id: int

    title: str
    content: str
    edited: bool


class UpdateUpdate(BaseModel):
    title: str | None
    content: str | None
