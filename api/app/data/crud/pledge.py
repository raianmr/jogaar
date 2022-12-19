import sqlalchemy as sa
from app.data.base import Base, BaseRead
from pydantic import BaseModel
from sqlalchemy.orm import Session


class Pledge(Base):
    pledger_id = sa.Column(
        sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    campaign_id = sa.Column(
        sa.Integer, sa.ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False
    )
    amount = sa.Column(sa.Integer, nullable=False)

    __table_args__ = tuple(sa.UniqueConstraint(campaign_id, pledger_id))


class PledgeCreate(BaseModel):
    amount: int


class PledgeRead(BaseRead):
    pledger_id: int
    campaign_id: int
    amount: int


class PledgeUpdate(BaseModel):
    amount: int | None


def create(
    u_id: int | sa.Column,
    c_id: int | sa.Column,
    p: PledgeCreate,
    db: Session,
) -> Pledge:
    new_p = Pledge(pledger_id=u_id, campaign_id=c_id, **p.dict())  # type: ignore
    db.add(new_p)

    db.commit()
    db.refresh(new_p)

    return new_p


def read(id: int | sa.Column, db: Session) -> Pledge | None:
    return db.query(Pledge).filter(Pledge.id == id).first()


def read_by_user_and_campaign(
    u_id: int | sa.Column, c_id: int | sa.Column, db: Session
) -> Pledge | None:
    return (
        db.query(Pledge)
        .filter(Pledge.pledger_id == u_id, Pledge.campaign_id == c_id)
        .first()
    )


def read_all_by_user(
    u_id: int | sa.Column, limit: int, offset: int, db: Session
) -> list[Pledge]:
    return (
        db.query(Pledge)
        .filter(Pledge.pledger_id == u_id)
        .limit(limit)
        .offset(offset)
        .all()
    )


def read_all_by_campaign(
    c_id: int | sa.Column, limit: int, offset: int, db: Session
) -> list[Pledge]:
    return (
        db.query(Pledge)
        .filter(Pledge.campaign_id == c_id)
        .limit(limit)
        .offset(offset)
        .all()
    )


def read_all(limit: int, offset: int, db: Session) -> list[Pledge]:
    return db.query(Pledge).limit(limit).offset(offset).all()


def update(id: int | sa.Column, p: PledgeUpdate, db: Session) -> None:
    db.query(Pledge).filter(Pledge.id == id).update(p.dict(exclude_unset=True))

    db.commit()


def delete(id: int | sa.Column, db: Session) -> None:
    db.query(Pledge).filter(Pledge.id == id).delete()

    db.commit()


def delete_by_user_and_campaign(
    u_id: int | sa.Column, c_id: int | sa.Column, db: Session
) -> None:
    db.query(Pledge).filter(
        Pledge.pledger_id == u_id, Pledge.campaign_id == c_id
    ).delete()

    db.commit()
