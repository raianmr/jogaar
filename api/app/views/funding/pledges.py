from app.core import security, utils
from app.data.crud import pledge
from app.data.crud.pledge import Pledge, PledgeCreate, PledgeRead, PledgeUpdate
from app.data.crud.user import User
from app.data.session import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

router = APIRouter()


class PledgerAndCampaignConflictErr(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="pledge by current user already exists for the campaign",
        )


class PledgeNotFoundErr(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="pledge was not found",
        )


def get_existing_pledge(u_id: int, c_id: int, db: Session) -> Pledge:
    existing_p = pledge.read_by_user_and_campaign(u_id, c_id, db)
    if existing_p is None:
        raise PledgeNotFoundErr

    return existing_p


@router.post(
    "/campaigns/{c_id}/pledges",
    status_code=status.HTTP_201_CREATED,
    response_model=PledgeRead,
)
async def create_pledge(
    c_id: int,
    p: PledgeCreate,
    db: Session = Depends(get_db),
    curr_u: User = Depends(security.get_current_valid_user),
) -> Pledge:
    existing_c = utils.get_existing_campaign(c_id, db)

    try:
        new_p = pledge.create(curr_u.id, existing_c.id, p, db)

    except IntegrityError:
        raise PledgerAndCampaignConflictErr

    return new_p


@router.put("/campaigns/{c_id}/pledges", response_model=PledgeRead)
async def update_pledge(
    c_id: int,
    p: PledgeUpdate,
    db: Session = Depends(get_db),
    curr_u: User = Depends(security.get_current_valid_user),
) -> Pledge | None:
    existing_p = get_existing_pledge(curr_u.id, c_id, db)  # type: ignore
    existing_c = utils.get_existing_campaign(existing_p.campaign_id, db)

    try:
        pledge.update(existing_p.id, p, db)
        updated_p = pledge.read(existing_p.id, db)

    except IntegrityError:
        raise PledgerAndCampaignConflictErr

    return updated_p


@router.delete(
    "/campaigns/{c_id}/pledges",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_pledge(
    c_id: int,
    db: Session = Depends(get_db),
    curr_u: User = Depends(security.get_current_valid_user),
) -> None:
    existing_p = get_existing_pledge(curr_u.id, c_id, db)  # type: ignore
    existing_c = utils.get_existing_campaign(existing_p.campaign_id, db)

    pledge.delete_by_user_and_campaign(curr_u.id, existing_c.id, db)


@router.get("/campaigns/{c_id}/pledges")
async def read_pledges_by_campaign(
    c_id: int,
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db),
) -> list[Pledge]:
    all_p_by_c = pledge.read_all_by_campaign(c_id, limit, offset, db)

    return all_p_by_c


@router.get("/users/{u_id}/pledges")
async def read_pledges_by_user(
    u_id: int,
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db),
) -> list[Pledge]:
    all_p_by_u = pledge.read_all_by_user(u_id, limit, offset, db)

    return all_p_by_u
