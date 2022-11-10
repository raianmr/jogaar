from app.core.campaigning import get_existing_campaign
from app.core.security import NotAllowedErr, get_current_valid_user, has_access_over
from app.data.crud import bookmark
from app.data.crud.bookmark import Bookmark, BookmarkRead
from app.data.crud.user import User
from app.data.session import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

router = APIRouter()

# TODO embed bookmark status in campaign fetching


class UserAndCampaignConflictErr(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="bookmark by current user already exists for the campaign",
        )


class BookmarkNotFoundErr(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="bookmark was not found",
        )


def get_existing_bookmark(u_id: int, c_id: int, db: Session) -> Bookmark:
    existing_b = bookmark.read_by_user_and_campaign(u_id, c_id, db)
    if not existing_b:
        raise BookmarkNotFoundErr

    return existing_b


@router.post(
    "/campaigns/{c_id}/bookmarks",
    status_code=status.HTTP_201_CREATED,
    response_model=BookmarkRead,
)
async def create_bookmark(
    c_id: int,
    db: Session = Depends(get_db),
    curr_u: User = Depends(get_current_valid_user),
) -> Bookmark:
    existing_c = get_existing_campaign(c_id, db)

    try:
        new_b = bookmark.create(curr_u.id, existing_c.id, db)

    except IntegrityError:
        raise UserAndCampaignConflictErr

    return new_b


@router.delete(
    "/campaigns/{c_id}/bookmarks",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_bookmark(
    c_id: int,
    db: Session = Depends(get_db),
    curr_u: User = Depends(get_current_valid_user),
) -> None:
    existing_b = get_existing_bookmark(curr_u.id, c_id, db)  # type: ignore
    existing_c = get_existing_campaign(existing_b.campaign_id, db)

    bookmark.delete_by_user_and_campaign(curr_u.id, existing_c.id, db)


@router.get("/campaigns/{c_id}/bookmarks")
async def read_bookmarks_by_campaign(
    c_id: int,
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db),
) -> list[Bookmark]:
    all_b_by_c = bookmark.read_all_by_campaign(c_id, limit, offset, db)

    return all_b_by_c


@router.get("/users/{u_id}/bookmarks")
async def read_bookmarks_by_user(
    u_id: int,
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db),
) -> list[Bookmark]:
    all_b_by_u = bookmark.read_all_by_user(u_id, limit, offset, db)

    return all_b_by_u
