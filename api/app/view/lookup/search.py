from app.core.security import NotAllowedErr, get_current_valid_user, has_access_over
from app.core.utils import MiscConflictErr, get_existing_campaign, get_existing_image
from app.data.crud import bookmark, campaign
from app.data.crud.campaign import (
    Campaign,
    CampaignCreate,
    CampaignRead,
    CampaignUpdate,
    State,
)
from app.data.crud.tag import Tag, TagCreate, TagRead, TagUpdate
from app.data.crud.user import User
from app.data.session import get_db
from fastapi import APIRouter, Body, Depends, Query, status
from rapidfuzz import fuzz
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/search/campaigns", response_model=list[CampaignRead])
async def search_campaigns(
    limit: int = 100,
    offset: int = 0,
    title: str = "",
    tags: list[str] = Query(default=[]),
    db: Session = Depends(get_db),
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
            .having(func.count(Campaign.id) == len(tags))
        )

    all_c = q.limit(limit).offset(offset).all()

    # https://web.archive.org/web/20170609041347/http://chairnerd.seatgeek.com/fuzzywuzzy-fuzzy-string-matching-in-python/
    if title != "":
        all_c = sorted(
            all_c, key=lambda c: fuzz.partial_ratio(c.title, title), reverse=True
        )

    return all_c
