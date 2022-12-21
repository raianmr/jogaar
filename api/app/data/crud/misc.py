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


# - take the tags the user is interested in based on their bookmarked campaigns
# - sort campaigns by number of distinct tags that match this criteria
#   [this is preferable to just sorting based on user's commonly bookmarked
#   tags because that might result in a lack of diversity in the campaigns
#   recommended -- which should be its own opt-in feature imo. but for now,
#   catalogue/searching should do just fine to tackle such use cases]

# select campaigns.*
# from campaigns left join tags
# on tags.campaign_id = campaigns.id
# group by campaigns.id
# order by count(
#   tags.name in (
#     select tags.name
#     from tags join bookmarks
#     on bookmarks.campaign_id = tags.campaign_id
#     where bookmarks.user_id = _
#     group by tags.name
#   )
# ) desc;
def recommended_campaigns(
    u_id: int | sa.Column, limit: int, offset: int, db: Session
) -> list[Campaign]:
    fav_tags_query = (
        sa.select(Tag.name)
        .join(Bookmark, Tag.campaign_id == Bookmark.campaign_id)
        .where(Bookmark.user_id == u_id)
        .group_by(Tag.name)
    )

    # TODO exclude campaigns that are pledged to by the user
    # select campaigns.*
    # from campaigns left join pledges
    # on pledges.campaign_id = campaigns.id
    # ...

    recommended_query = (
        sa.select(Campaign)
        .join(Tag, Tag.campaign_id == Campaign.id, isouter=True)
        .where(Campaign.current_state == State.STARTED, Campaign.campaigner_id != u_id)
        .group_by(Campaign.id)
        .order_by(sa.desc(sa.func.count(Tag.name.in_(fav_tags_query))))
    )

    return db.execute(recommended_query.limit(limit).offset(offset)).scalars().all()


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


def updates_for_bookmarked(
    u_id: int | sa.Column, limit: int, offset: int, db: Session
) -> list[Update]:
    s = (
        sa.select(Update)
        .join(Bookmark, Update.campaign_id == Bookmark.campaign_id)
        .where(Bookmark.user_id == u_id)
        .order_by(sa.desc(Update.created_at))
        .limit(limit)
        .offset(offset)
    )

    return db.execute(s).scalars().all()


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
