from app.data.crud import campaign
from app.data.crud.campaign import Campaign, CampaignRead
from app.data.session import get_db
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/search/campaigns", response_model=list[CampaignRead])
async def search_campaigns(
    title: str = "",
    tags: list[str] = Query(default=[]),
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db),
) -> list[Campaign]:
    all_c = campaign.read_all_by_query(title, tags, limit, offset, db)

    return all_c
