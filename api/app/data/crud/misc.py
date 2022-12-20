from typing import Final

import sqlalchemy as sa
from app.data.base import Base, BaseRead
from app.data.crud.bookmark import Bookmark
from app.data.crud.campaign import Campaign, State
from app.data.crud.pledge import Pledge
from app.data.crud.tag import Tag
from app.data.crud.update import Update
from pydantic import BaseModel
from sqlalchemy.orm import Session


def greenlit_count(db: Session) -> int:
    return db.query(Campaign).filter(Campaign.current_state == State.GREENLIT).count()


def successful_campaigner_count(db: Session):
    return (
        db.query(Campaign)
        .filter(Campaign.current_state == State.GREENLIT)
        .distinct(Campaign.campaigner_id)
        .count()
    )


def successful_pledger_count(db: Session) -> int:
    return (
        db.query(Campaign)
        .join(Pledge, Pledge.campaign_id == Campaign.id)
        .filter(Campaign.current_state == State.GREENLIT)
        .distinct(Pledge.pledger_id)
        .count()
    )


def successfully_raised(db: Session) -> int:
    return (
        db.query(Campaign)
        .filter(Campaign.current_state == State.GREENLIT)
        .with_entities(sa.func.sum(Campaign.pledged))
        .scalar()
    )


featured_query: Final = (
    sa.select(Campaign)
    .join(Pledge, Pledge.campaign_id == Campaign.id, isouter=True)
    .where(Campaign.current_state == State.STARTED)
    .group_by(Campaign.id)
    .order_by(sa.desc(sa.func.count(sa.distinct(Pledge.pledger_id))))
)


def featured_campaigns(limit: int, offset: int, db: Session) -> list[Campaign]:
    return db.execute(featured_query.limit(limit).offset(offset)).scalars().all()


def bookmarked_campaigns(
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


def pledged_campaigns(
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


# def updates_for_bookmarked(
#     u_id: int | sa.Column, limit: int, offset: int, db: Session
# ) -> list[Update]:
#     return (
#         db.query(Update)
#         .filter(Update.campaign_id == u_id)
#         .limit(limit)
#         .offset(offset)
#         .all()
#     )


def searched_campaigns(
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
