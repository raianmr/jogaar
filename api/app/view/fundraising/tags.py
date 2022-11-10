from app.core.campaigning import get_existing_campaign
from app.core.security import NotAllowedErr, get_current_valid_user, has_access_over
from app.data.crud import tag
from app.data.crud.tag import Tag, TagCreate, TagRead, TagUpdate
from app.data.crud.user import User
from app.data.session import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

router = APIRouter()


class NameConflictErr(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="tag with given name already exists for the campaign",
        )


class TagNotFoundErr(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="tag was not found",
        )


def get_existing_tag(tag_id: int, db: Session) -> Tag:
    existing_t = tag.read(tag_id, db)
    if not existing_t:
        raise TagNotFoundErr

    return existing_t


@router.post(
    "/campaigns/{c_id}/tags",
    status_code=status.HTTP_201_CREATED,
    response_model=TagRead,
)
async def create_tag(
    c_id: int,
    t: TagCreate,
    db: Session = Depends(get_db),
    curr_u: User = Depends(get_current_valid_user),
) -> Tag:
    existing_c = get_existing_campaign(c_id, db)

    if not has_access_over(existing_c, curr_u):
        raise NotAllowedErr

    try:
        new_t = tag.create(c_id, t, db)

    except IntegrityError:
        raise NameConflictErr

    return new_t


@router.put("/tags/{t_id}", response_model=TagRead)
async def update_tag(
    t_id: int,
    t: TagUpdate,
    db: Session = Depends(get_db),
    curr_u: User = Depends(get_current_valid_user),
) -> Tag | None:
    existing_t = get_existing_tag(t_id, db)
    existing_c = get_existing_campaign(existing_t.campaign_id, db)

    if not has_access_over(existing_c, curr_u):
        raise NotAllowedErr

    try:
        tag.update(t_id, t, db)
        updated_t = tag.read(t_id, db)

    except IntegrityError:
        raise NameConflictErr

    return updated_t


@router.delete(
    "/tags/{t_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_tag(
    t_id: int,
    db: Session = Depends(get_db),
    curr_u: User = Depends(get_current_valid_user),
) -> None:
    existing_t = get_existing_tag(t_id, db)
    existing_c = get_existing_campaign(existing_t.campaign_id, db)

    if not has_access_over(existing_c, curr_u):
        raise NotAllowedErr

    tag.delete(t_id, db)


@router.get("/tags/{t_id}", response_model=TagRead)
async def read_tag(t_id: int, db: Session = Depends(get_db)) -> Tag:
    existing_t = get_existing_tag(t_id, db)

    return existing_t


@router.get("/campaigns/{c_id}/tags")
async def read_tags_by_campaign(
    c_id: int,
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db),
) -> list[Tag]:
    all_t_by_c = tag.read_all_by_campaign(c_id, limit, offset, db)

    return all_t_by_c
