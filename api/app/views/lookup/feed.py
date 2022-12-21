from app.core import security
from app.data.crud import misc
from app.data.crud.campaign import Campaign, CampaignRead
from app.data.crud.update import Update, UpdateRead
from app.data.crud.user import User
from app.data.session import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()

# feed should contain:
# + featured campaigns DONE
#   - sort by number of distinct pledgers
#   - only show ongoing campaigns
# + news feed DONE
#   - updates from bookmarked campaigns
#   - sort by creation time
# + recommended campaigns
#   - sort featured campaigns by user's most bookmarked tags
#   - exclude already bookmarked (and pledged in turn)
# + recently viewed
#   - based on GET on /campaigns endpoints
#   - custom lru cache or redis?


@router.get("/featured", response_model=list[CampaignRead])
async def get_featured(
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db),
) -> list[Campaign]:
    featured = misc.featured_campaigns(limit, offset, db)

    return featured


@router.get("/recommended", response_model=list[CampaignRead])
# @router.get("/recommended")
async def get_recommended(
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db),
    curr_u: User = Depends(security.get_current_valid_user),
) -> list[Campaign]:
    recommended = misc.recommended_campaigns(curr_u.id, limit, offset, db)

    return recommended


@router.get("/news", response_model=list[UpdateRead])
async def get_news(
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db),
    curr_u: User = Depends(security.get_current_valid_user),
) -> list[Update]:
    news = misc.updates_for_bookmarked(curr_u.id, limit, offset, db)

    return news
