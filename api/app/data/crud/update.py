import sqlalchemy as sa
from app.data.base import Base, BaseRead
from pydantic import BaseModel
from sqlalchemy.orm import Session


class Update(Base):
    user_id = sa.Column(
        sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    campaign_id = sa.Column(
        sa.Integer, sa.ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False
    )

    title = sa.Column(sa.String, nullable=False)
    content = sa.Column(sa.String, nullable=False)
    picture_id = sa.Column(sa.Integer, sa.ForeignKey("images.id", ondelete="CASCADE"))

    edited = sa.Column(sa.Boolean, server_default=sa.text("False"), nullable=False)


class UpdateCreate(BaseModel):
    title: str
    content: str


class UpdateRead(BaseRead):
    user_id: int
    campaign_id: int

    title: str
    content: str
    picture_id: int | None

    edited: bool


class UpdateUpdate(BaseModel):
    title: str | None
    content: str | None
    picture_id: int | None


def create(c_id: int | sa.Column, up: UpdateCreate, db: Session) -> Update:
    new_up = Update(campaign_id=c_id, **up.dict())  # type: ignore
    db.add(new_up)

    db.commit()
    db.refresh(new_up)

    return new_up


def read(id: int | sa.Column, db: Session) -> Update | None:
    return db.query(Update).filter(Update.id == id).first()


def read_all_by_campaign(
    c_id: int | sa.Column, limit: int, offset: int, db: Session
) -> list[Update]:
    return (
        db.query(Update)
        .filter(Update.campaign_id == c_id)
        .limit(limit)
        .offset(offset)
        .all()
    )


def read_all(limit: int, offset: int, db: Session) -> list[Update]:
    return db.query(Update).limit(limit).offset(offset).all()


def update(id: int | sa.Column, up: UpdateUpdate, db: Session) -> None:
    db.query(Update).filter(Update.id == id).update(
        {Update.edited: True, **up.dict(exclude_unset=True)}
    )

    db.commit()


def delete(id: int | sa.Column, db: Session) -> None:
    db.query(Update).filter(Update.id == id).delete()

    db.commit()
