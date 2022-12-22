from app.core import security
from app.data.crud import misc
from app.data.crud.campaign import Campaign, CampaignRead
from app.data.crud.reply import Reply, ReplyRead
from app.data.crud.update import Update, UpdateRead
from app.data.crud.user import User
from app.data.crud.vote import Vote, VoteRead
from app.data.session import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()

# types of alerts (for now):
# 1. replies to updates authored by user
# 2. votes to the replies authored by user


@router.get("/alerts/replies", response_model=list[ReplyRead])
async def get_reply_alerts(
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db),
    curr_u: User = Depends(security.get_current_valid_user),
) -> list[Reply]:
    return misc.reply_alerts(curr_u.id, limit, offset, db)


@router.get("/alerts/votes", response_model=list[VoteRead])
async def get_vote_alerts(
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db),
    curr_u: User = Depends(security.get_current_valid_user),
) -> list[Vote]:
    return misc.vote_alerts(curr_u.id, limit, offset, db)
