from datetime import datetime, timedelta, timezone

from app.core.security import Access, NotAllowedErr, get_current_valid_user, is_super
from app.data.crud import bookmark, campaign
from app.data.crud.campaign import Campaign
from app.data.crud.user import User
from app.data.session import get_db
from fastapi import Depends, HTTPException, Path, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy import Column
from sqlalchemy.orm import Session


class MiscConflictErr(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="campaign already exists",
        )


class CampaignNotFoundErr(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="campaign was not found",
        )


def get_existing_campaign(campaign_id: int | Column, db: Session) -> Campaign:
    existing_c = campaign.read(campaign_id, db)
    if not existing_c:
        raise CampaignNotFoundErr

    return existing_c


def campaign_with_meta(existing_c: Campaign, existing_u: User, db: Session):
    existing_b = bookmark.real_by_user_and_campaign(existing_u.id, existing_c.id, db)

    return {
        **jsonable_encoder(existing_c),
        "bookmarked": bool(existing_b),
    }


def has_crossed_deadline(c: Campaign) -> bool:
    return datetime.now(timezone.utc) > c.deadline  # type: ignore
