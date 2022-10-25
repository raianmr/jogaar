from app.core.campaigning import CampaignNotFoundErr
from app.core.security import NotAllowedErr, get_current_user
from app.data.crud import campaign, reward
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


@router.post(
    "/campaigns/{c_id}/rewards",
    status_code=status.HTTP_201_CREATED,
    response_model=RewardRead,
)
async def create_reward(
    c_id: int,
    r: RewardCreate,
    db: Session = Depends(get_db),
    curr_u: User = Depends(get_current_user),
) -> Reward:
    existing_c = campaign.read(c_id, db)

    if not existing_c:
        raise CampaignNotFoundErr

    if existing_c.campaigner_id != curr_u.id:
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
    curr_u: User = Depends(get_current_user),
) -> Reward | None:
    existing_r = reward.read(r_id, db)

    if not existing_r:
        raise RewardNotFoundErr

    existing_c = campaign.read(existing_r.campaign_id, db)  # type: ignore

    if not existing_c:
        raise CampaignNotFoundErr

    if existing_c.campaigner_id != curr_u.id:
        raise NotAllowedErr

    try:
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
    curr_u: User = Depends(get_current_user),
) -> None:
    existing_r = reward.read(r_id, db)

    if not existing_r:
        raise RewardNotFoundErr

    existing_c = campaign.read(existing_r.campaign_id, db)  # type: ignore

    if not existing_c:
        raise CampaignNotFoundErr

    if existing_c.campaigner_id != curr_u.id:
        raise NotAllowedErr

    reward.delete(r_id, db)


@router.get("/rewards/{r_id}", response_model=RewardRead)
async def read_reward(r_id: int, db: Session = Depends(get_db)) -> Reward:
    existing_r = reward.read(r_id, db)

    if not existing_r:
        raise RewardNotFoundErr

    return existing_r


@router.get("/campaigns/{c_id}/rewards", response_model=list[RewardRead])
async def read_rewards_by_campaign(
    c_id: int, limit: int = 100, offset: int = 0, db: Session = Depends(get_db)
) -> list[Reward]:
    all_r_by_c = reward.read_all_by_campaign(c_id, limit, offset, db)

    return all_r_by_c
