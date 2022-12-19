from datetime import datetime, timedelta, timezone

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


def get_existing_campaign(campaign_id: int | Column, db: Session) -> Campaign:
    existing_c = campaign.read(campaign_id, db)
    if existing_c is None:
        raise CampaignNotFoundErr

    return existing_c


def campaign_with_meta(existing_c: Campaign, existing_u: User, db: Session):
    existing_b = bookmark.read_by_user_and_campaign(existing_u.id, existing_c.id, db)

    return {
        **jsonable_encoder(existing_c),
        "bookmarked": bool(existing_b),
    }


class UpdateNotFoundErr(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="update was not found",
        )


def get_existing_update(update_id: int, db: Session) -> Update:
    existing_u = update.read(update_id, db)
    if existing_u is None:
        raise UpdateNotFoundErr

    return existing_u


class ReplyNotFoundErr(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="reply was not found",
        )


def get_existing_reply(update_id: int, db: Session) -> Reply:
    existing_r = reply.read(update_id, db)
    if existing_r is None:
        raise ReplyNotFoundErr

    return existing_r


class ImageNotFoundErr(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="image was not found",
        )


def get_existing_image(img_id: int, db: Session) -> image.Image:
    # TODO find a better way to handle this
    if img_id <= 0:
        raise ImageNotFoundErr

    existing_img = image.read(img_id, db)
    if existing_img is None:
        raise ImageNotFoundErr

    if existing_img.location is None:
        raise ImageNotFoundErr

    return existing_img


class BookmarkNotFoundErr(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="bookmark was not found",
        )


def get_existing_bookmark(u_id: int, c_id: int, db: Session) -> bookmark.Bookmark:
    existing_b = bookmark.read_by_user_and_campaign(u_id, c_id, db)
    if existing_b is None:
        raise BookmarkNotFoundErr

    return existing_b


def has_crossed_deadline(c: Campaign) -> bool:
    return datetime.now(timezone.utc) > c.deadline  # type: ignore
