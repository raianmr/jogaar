from datetime import datetime
from enum import Enum

import sqlalchemy as sa
from app.data.base import Base, BaseRead
from app.data.crud.bookmark import Bookmark
from app.data.crud.pledge import Pledge
from app.data.crud.tag import Tag
from pydantic import BaseModel
from sqlalchemy.orm import Session


class State(str, Enum):
    DRAFT = "draft"
    STARTED = "started"
    ENDED = "ended"
    LOCKED = "locked"
    GREENLIT = "greenlit"


class Campaign(Base):
    campaigner_id = sa.Column(
        sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    title = sa.Column(sa.String, nullable=False)
    description = sa.Column(sa.String, nullable=False)
    challenges = sa.Column(sa.String, nullable=False)
    cover_id = sa.Column(sa.Integer, sa.ForeignKey("images.id", ondelete="CASCADE"))

    goal = sa.Column(sa.Integer, nullable=False)
    pledged = sa.Column(sa.Integer, server_default="0", nullable=False)

    deadline = sa.Column(
        sa.TIMESTAMP(timezone=True),
        server_default=sa.text("NOW() + INTERVAL '1 month'"),
        nullable=False,
    )

    current_state = sa.Column(sa.String, server_default=State.DRAFT, nullable=False)


class CampaignCreate(BaseModel):
    title: str
    description: str
    challenges: str

    goal: int
    deadline: datetime


class CampaignRead(BaseRead):
    campaigner_id: int

    title: str
    description: str
    challenges: str
    cover_id: int | None

    goal: int
    pledged: int
    deadline: datetime

    current_state: State


class CampaignReadMeta(CampaignRead):
    bookmarked: bool


class CampaignUpdate(BaseModel):
    title: str | None
    description: str | None
    challenges: str | None
    cover_id: int | None


def create(u_id: int | sa.Column, c: CampaignCreate, db: Session) -> Campaign:
    new_c = Campaign(campaigner_id=u_id, **c.dict())  # type: ignore
    db.add(new_c)

    db.commit()
    db.refresh(new_c)

    return new_c


def read(id: int | sa.Column, db: Session) -> Campaign | None:
    return db.query(Campaign).filter(Campaign.id == id).first()


def read_all_by_campaigner(
    u_id: int | sa.Column, limit: int, offset: int, db: Session
) -> list[Campaign]:
    return (
        db.query(Campaign)
        .filter(Campaign.campaigner_id == u_id)
        .limit(limit)
        .offset(offset)
        .all()
    )


def read_all_bookmarked(
    u_id: int | sa.Column, limit: int, offset: int, db: Session
) -> list[Campaign]:
    return (
        db.query(Campaign)
        .join(Bookmark, Bookmark.campaign_id == Campaign.id)
        .filter(Bookmark.user_id == u_id)
        .limit(limit)
        .offset(offset)
        .all()
    )


def read_all_pledged(
    u_id: int | sa.Column, limit: int, offset: int, db: Session
) -> list[Campaign]:
    return (
        db.query(Campaign)
        .join(Pledge, Pledge.campaign_id == Campaign.id)
        .filter(Pledge.pledger_id == u_id)
        .limit(limit)
        .offset(offset)
        .all()
    )


def read_all_by_query(
    title: str, tags: list[str], limit: int, offset: int, db: Session
) -> list[Campaign]:
    # select campaigns.* from campaigns inner join tags
    # ON tags.campaign_id = campaigns.id where tags.name
    # in (_, _) group by campaigns.id having count(campaigns.id) = 2;
    # http://web.archive.org/web/20150813211028/http://tagging.pui.ch/post/37027745720/tags-database-schemas

    q = db.query(Campaign)

    if len(tags) != 0:
        q = (
            q.join(Tag, Tag.campaign_id == Campaign.id)
            .filter(Tag.name.in_(tags))
            .group_by(Campaign.id)
            .having(sa.func.count(Campaign.id) == len(tags))
        )

    # https://web.archive.org/web/20170609041347/http://chairnerd.seatgeek.com/fuzzywuzzy-fuzzy-string-matching-in-python/
    if title != "":
        # TODO try elastic search next time
        q = q.order_by(sa.desc(sa.func.word_similarity(Campaign.title, title)))

    all_c = q.limit(limit).offset(offset).all()

    return all_c


def read_all(limit: int, offset: int, db: Session) -> list[Campaign]:
    return db.query(Campaign).limit(limit).offset(offset).all()


def update(id: int | sa.Column, c: CampaignUpdate, db: Session) -> None:
    db.query(Campaign).filter(Campaign.id == id).update(c.dict(exclude_unset=True))

    db.commit()


def update_state(id: int | sa.Column, s: State, db: Session):
    db.query(Campaign).filter(Campaign.id == id).update({Campaign.current_state: s})

    db.commit()


def delete(id: int | sa.Column, db: Session) -> None:
    db.query(Campaign).filter(Campaign.id == id).delete()

    db.commit()
