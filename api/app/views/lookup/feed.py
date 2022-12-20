from app.data.crud import misc
from app.data.crud.campaign import Campaign, CampaignRead
from app.data.crud.update import Update, UpdateRead
from app.data.session import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()

# feed should contain:
# + featured campaigns DONE
#   - sort by number of distinct pledgers
#   - only show ongoing campaigns
# + news feed
#   - updates from bookmarked campaigns
#   - sort by creation time
# + based on your interests
#   - sort featured campaigns by user's most bookmarked tags
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


# @router.get("/news", response_model=list[UpdateRead])
# async def get_news(
#     limit: int = 100,
#     offset: int = 0,
#     db: Session = Depends(get_db),
# ) -> list[Campaign]:
#     featured = misc.featured_campaigns(limit, offset, db)

#     return featured


# @router.get("/search/campaigns", response_model=list[CampaignRead])
# async def search_campaigns(
#     title: str = "",
#     tags: list[str] = Query(default=[]),
#     limit: int = 100,
#     offset: int = 0,
#     db: Session = Depends(get_db),
# ) -> list[Campaign]:
#     all_c = campaign.read_all_by_query(title, tags, limit, offset, db)

#     return all_c
