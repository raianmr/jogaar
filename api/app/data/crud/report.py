from enum import Enum

import sqlalchemy as sa
from app.data.base import Base, BaseRead
from pydantic import BaseModel
from sqlalchemy.orm import Session


class Reportable(str, Enum):
    USER = "user"
    CAMPAIGN = "campaign"
    REPLY = "reply"


class Report(Base):
    reporter_id = sa.Column(
        sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    description = sa.Column(sa.String, nullable=False)

    content_id = sa.Column(sa.Integer, nullable=False)
    content_type = sa.Column(
        sa.String, server_default=Reportable.CAMPAIGN, nullable=False
    )

    __table_args__ = tuple(sa.UniqueConstraint(reporter_id, content_type, content_id))


class ReportCreate(BaseModel):
    description: str

    content_id: int
    content_type: Reportable


class ReportRead(BaseRead):
    reporter_id: int

    description: str

    content_id: int
    content_type: Reportable


def create(_reporter_id: int | sa.Column, r: ReportCreate, db: Session) -> Report:
    new_report = Report(reporter_id=_reporter_id, **r.dict())  # type: ignore
    db.add(new_report)

    db.commit()
    db.refresh(new_report)

    return new_report


def read(id: int | sa.Column, db: Session) -> Report | None:
    return db.query(Report).filter(Report.id == id).first()


def read_all(limit: int, offset: int, db: Session) -> list[Report]:
    return db.query(Report).limit(limit).offset(offset).all()
