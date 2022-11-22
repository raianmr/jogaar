from datetime import datetime, timedelta, timezone

from app.core.security import NotAllowedErr, get_current_valid_user, is_super
from app.data.crud import bookmark, campaign, image, reply, update
from app.data.crud.campaign import Campaign
from app.data.crud.reply import Reply
from app.data.crud.update import Update
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
            detail="entity already exists",
        )


class CampaignNotFoundErr(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="campaign was not found",
        )


class UpdateNotFoundErr(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="update was not found",
        )


class ReplyNotFoundErr(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="reply was not found",
        )


class ImageNotFoundErr(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="image was not found",
        )


def get_existing_campaign(campaign_id: int | Column, db: Session) -> Campaign:
    existing_c = campaign.read(campaign_id, db)
    if not existing_c:
        raise CampaignNotFoundErr

    return existing_c


def campaign_with_meta(existing_c: Campaign, existing_u: User, db: Session):
    existing_b = bookmark.read_by_user_and_campaign(existing_u.id, existing_c.id, db)

    return {
        **jsonable_encoder(existing_c),
        "bookmarked": bool(existing_b),
    }


def get_existing_update(update_id: int, db: Session) -> Update:
    existing_u = update.read(update_id, db)
    if not existing_u:
        raise UpdateNotFoundErr

    return existing_u


def get_existing_reply(update_id: int, db: Session) -> Reply:
    existing_r = reply.read(update_id, db)
    if not existing_r:
        raise ReplyNotFoundErr

    return existing_r


def get_existing_image(image_id: int, db: Session) -> image.Image:
    existing_img = image.read(image_id, db)
    if not existing_img:
        raise ImageNotFoundErr

    if not existing_img.location:
        raise ImageNotFoundErr

    return existing_img


def has_crossed_deadline(c: Campaign) -> bool:
    return datetime.now(timezone.utc) > c.deadline  # type: ignore
