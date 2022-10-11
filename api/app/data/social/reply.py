from pydantic import BaseModel
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, text
from sqlalchemy.orm import Session

from app.data.base import Base, BaseRead


class Reply(Base):
    __tablename__ = "replies"  # type: ignore

    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    update_id = Column(
        Integer, ForeignKey("updates.id", ondelete="CASCADE"), nullable=False
    )

    content = Column(String, nullable=False)
    edited = Column(Boolean, server_default=text("False"), nullable=False)


class ReplyCreate(BaseModel):
    update_id: int

    content: str


class ReplyRead(BaseRead):
    user_id: int
    update_id: int
    campaign_id: int

    content: str
    edited: bool


class ReplyUpdate(BaseModel):
    content: str
