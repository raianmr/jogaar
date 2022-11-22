from app.data.base import Base, BaseRead
from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Session


class Reward(Base):
    campaign_id = Column(
        Integer, ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False
    )

    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    picture_id = Column(Integer, ForeignKey("images.id", ondelete="CASCADE"))

    pledge = Column(Integer, nullable=False)

    __table_args__ = tuple(UniqueConstraint(campaign_id, pledge))


class RewardCreate(BaseModel):
    title: str
    description: str
    pledge: int


class RewardRead(BaseRead):
    title: str
    description: str
    picture_id: int | None
    pledge: int


class RewardUpdate(BaseModel):
    title: str | None
    description: str | None
    picture_id: int | None
    pledge: int | None


def create(c_id: int | Column, r: RewardCreate, db: Session) -> Reward:
    new_r = Reward(campaign_id=c_id, **r.dict())  # type: ignore
    db.add(new_r)

    db.commit()
    db.refresh(new_r)

    return new_r


def read(id: int | Column, db: Session) -> Reward | None:
    return db.query(Reward).filter(Reward.id == id).first()


def read_all_by_campaign(
    c_id: int | Column, limit: int, offset: int, db: Session
) -> list[Reward]:
    return (
        db.query(Reward)
        .filter(Reward.campaign_id == c_id)
        .limit(limit)
        .offset(offset)
        .all()
    )


def read_all(limit: int, offset: int, db: Session) -> list[Reward]:
    return db.query(Reward).limit(limit).offset(offset).all()


def update(id: int | Column, r: RewardUpdate, db: Session) -> None:
    db.query(Reward).filter(Reward.id == id).update(r.dict(exclude_unset=True))

    db.commit()


def delete(id: int | Column, db: Session) -> None:
    db.query(Reward).filter(Reward.id == id).delete()

    db.commit()
