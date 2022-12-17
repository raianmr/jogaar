from app.core.security import NotAllowedErr, get_current_valid_user, has_access_over
from app.core.utils import get_existing_campaign, get_existing_image
from app.data.crud import reward
from app.data.crud.reward import Reward, RewardCreate, RewardRead, RewardUpdate
from app.data.crud.user import User
from app.data.session import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

router = APIRouter()


class PledgeConflictErr(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="reward with given pledge already exists for the campaign",
        )


class RewardNotFoundErr(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="reward was not found",
        )


def get_existing_reward(reward_id: int, db: Session) -> Reward:
    existing_r = reward.read(reward_id, db)
    if existing_r is None:
        raise RewardNotFoundErr

    return existing_r


@router.post(
    "/campaigns/{c_id}/rewards",
    status_code=status.HTTP_201_CREATED,
    response_model=RewardRead,
)
async def create_reward(
    c_id: int,
    r: RewardCreate,
    db: Session = Depends(get_db),
    curr_u: User = Depends(get_current_valid_user),
) -> Reward:
    existing_c = get_existing_campaign(c_id, db)

    if not has_access_over(existing_c, curr_u):
        raise NotAllowedErr

    try:
        new_r = reward.create(c_id, r, db)

    except IntegrityError:
        raise PledgeConflictErr

    return new_r


@router.put("/rewards/{r_id}", response_model=RewardRead)
async def update_reward(
    r_id: int,
    r: RewardUpdate,
    db: Session = Depends(get_db),
    curr_u: User = Depends(get_current_valid_user),
) -> Reward | None:
    existing_r = get_existing_reward(r_id, db)
    existing_c = get_existing_campaign(existing_r.campaign_id, db)

    if not has_access_over(existing_c, curr_u):
        raise NotAllowedErr

    try:
        if r.picture_id is not None:
            _ = get_existing_image(r.picture_id, db)

        reward.update(r_id, r, db)
        updated_r = reward.read(r_id, db)

    except IntegrityError:
        raise PledgeConflictErr

    return updated_r


@router.delete(
    "/rewards/{r_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_reward(
    r_id: int,
    db: Session = Depends(get_db),
    curr_u: User = Depends(get_current_valid_user),
) -> None:
    existing_r = get_existing_reward(r_id, db)
    existing_c = get_existing_campaign(existing_r.campaign_id, db)

    if not has_access_over(existing_c, curr_u):
        raise NotAllowedErr

    reward.delete(r_id, db)


@router.get("/rewards/{r_id}", response_model=RewardRead)
async def read_reward(r_id: int, db: Session = Depends(get_db)) -> Reward:
    existing_r = get_existing_reward(r_id, db)

    return existing_r


@router.get("/campaigns/{c_id}/rewards", response_model=list[RewardRead])
async def read_rewards_by_campaign(
    c_id: int, limit: int = 100, offset: int = 0, db: Session = Depends(get_db)
) -> list[Reward]:
    all_r_by_c = reward.read_all_by_campaign(c_id, limit, offset, db)

    return all_r_by_c
