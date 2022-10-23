from app.data.auth.user import User
from app.data.fundraising import campaign, milestone
from app.data.fundraising.milestone import (
    Milestone,
    MilestoneCreate,
    MilestoneRead,
    MilestoneUpdate,
)
from app.data.session import get_db
from app.logic.auth.login import NotAllowedErr, get_current_user
from app.logic.fundraising.campaigns import CampaignNotFoundErr
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


@router.post(
    "/campaigns/{c_id}/milestones",
    status_code=status.HTTP_201_CREATED,
    response_model=MilestoneRead,
)
async def create_milestone(
    c_id: int,
    m: MilestoneCreate,
    db: Session = Depends(get_db),
    curr_u: User = Depends(get_current_user),
) -> Milestone:
    existing_c = campaign.read(c_id, db)

    if not existing_c:
        raise CampaignNotFoundErr

    if existing_c.campaigner_id != curr_u.id:
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
    curr_u: User = Depends(get_current_user),
) -> Milestone | None:
    existing_m = milestone.read(m_id, db)

    if not existing_m:
        raise MilestoneNotFoundErr

    existing_c = campaign.read(existing_m.campaign_id, db)  # type: ignore

    if not existing_c:
        raise CampaignNotFoundErr

    if existing_c.campaigner_id != curr_u.id:
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
    curr_u: User = Depends(get_current_user),
) -> None:
    existing_m = milestone.read(m_id, db)

    if not existing_m:
        raise MilestoneNotFoundErr

    existing_c = campaign.read(existing_m.campaign_id, db)  # type: ignore

    if not existing_c:
        raise CampaignNotFoundErr

    if existing_c.campaigner_id != curr_u.id:
        raise NotAllowedErr

    milestone.delete(m_id, db)


@router.get("/milestones/{m_id}", response_model=MilestoneRead)
async def read_milestone(
    m_id: int, db: Session = Depends(get_db)
) -> Milestone:
    existing_m = milestone.read(m_id, db)

    if not existing_m:
        raise MilestoneNotFoundErr

    return existing_m


@router.get("/campaigns/{c_id}/milestones", response_model=list[MilestoneRead])
async def read_milestones_by_campaign(
    c_id: int, limit: int = 100, offset: int = 0, db: Session = Depends(get_db)
) -> list[Milestone]:
    all_m_by_c = milestone.read_all_by_campaign(c_id, limit, offset, db)

    return all_m_by_c
