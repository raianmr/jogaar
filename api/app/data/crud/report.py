from enum import Enum

from app.data.base import Base, BaseRead
from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Session


class ContentType(str, Enum):
    USER = "user"
    CAMPAIGN = "campaign"
    REPLY = "reply"


class Report(Base):
    reporter_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    description = Column(String, nullable=False)

    content_id = Column(Integer, nullable=False)
    content_type = Column(String, server_default=ContentType.CAMPAIGN, nullable=False)

    __table_args__ = tuple(UniqueConstraint(reporter_id, content_type, content_id))


class ReportCreate(BaseModel):
    description: str

    content_id: int
    content_type: ContentType


class ReportRead(BaseRead):
    reporter_id: int

    description: str

    content_id: int
    content_type: ContentType


def create(_reporter_id: int | Column, r: ReportCreate, db: Session) -> Report:
    new_report = Report(reporter_id=_reporter_id, **r.dict())  # type: ignore
    db.add(new_report)

    db.commit()
    db.refresh(new_report)

    return new_report


def read(id: int | Column, db: Session) -> Report | None:
    return db.query(Report).filter(Report.id == id).first()


def read_all(limit: int, offset: int, db: Session) -> list[Report]:
    return db.query(Report).limit(limit).offset(offset).all()
