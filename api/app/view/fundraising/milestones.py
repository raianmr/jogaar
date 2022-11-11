from app.core.campaigning import get_existing_campaign
from app.core.security import NotAllowedErr, get_current_valid_user, has_access_over
from app.data.crud import milestone
from app.data.crud.milestone import (
    Milestone,
    MilestoneCreate,
    MilestoneRead,
    MilestoneUpdate,
)
from app.data.crud.user import User
from app.data.session import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

router = APIRouter()


class DeadlineConflictErr(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="milestone with given deadline already exists for the campaign",
        )


class MilestoneNotFoundErr(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="milestone was not found",
        )


def get_existing_milestone(milestone_id: int, db: Session) -> Milestone:
    existing_m = milestone.read(milestone_id, db)
    if not existing_m:
        raise MilestoneNotFoundErr

    return existing_m


@router.post(
    "/campaigns/{c_id}/milestones",
    status_code=status.HTTP_201_CREATED,
    response_model=MilestoneRead,
)
async def create_milestone(
    c_id: int,
    m: MilestoneCreate,
    db: Session = Depends(get_db),
    curr_u: User = Depends(get_current_valid_user),
) -> Milestone:
    existing_c = get_existing_campaign(c_id, db)

    if not has_access_over(existing_c, curr_u):
        raise NotAllowedErr

    try:
        new_m = milestone.create(c_id, m, db)

    except IntegrityError:
        raise DeadlineConflictErr

    return new_m


@router.put("/milestones/{m_id}", response_model=MilestoneRead)
async def update_milestone(
    m_id: int,
    m: MilestoneUpdate,
    db: Session = Depends(get_db),
    curr_u: User = Depends(get_current_valid_user),
) -> Milestone | None:
    existing_m = get_existing_milestone(m_id, db)
    existing_c = get_existing_campaign(existing_m.campaign_id, db)

    if not has_access_over(existing_c, curr_u):
        raise NotAllowedErr

    try:
        milestone.update(m_id, m, db)
        updated_m = milestone.read(m_id, db)

    except IntegrityError:
        raise DeadlineConflictErr

    return updated_m


@router.delete(
    "/milestones/{m_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_milestone(
    m_id: int,
    db: Session = Depends(get_db),
    curr_u: User = Depends(get_current_valid_user),
) -> None:
    existing_m = get_existing_milestone(m_id, db)
    existing_c = get_existing_campaign(existing_m.campaign_id, db)

    if not has_access_over(existing_c, curr_u):
        raise NotAllowedErr

    milestone.delete(m_id, db)


@router.get("/milestones/{m_id}", response_model=MilestoneRead)
async def read_milestone(m_id: int, db: Session = Depends(get_db)) -> Milestone:
    existing_m = get_existing_milestone(m_id, db)

    return existing_m


@router.get("/campaigns/{c_id}/milestones", response_model=list[MilestoneRead])
async def read_milestones_by_campaign(
    c_id: int,
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db),
) -> list[Milestone]:
    all_m_by_c = milestone.read_all_by_campaign(c_id, limit, offset, db)

    return all_m_by_c
