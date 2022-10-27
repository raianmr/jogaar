from app.core.campaigning import (
    MiscConflictErr,
    get_existing_campaign,
    has_crossed_deadline,
)
from app.core.security import (
    NotAllowedErr,
    get_current_admin_user,
    get_current_super_user,
    get_existing_user,
    has_access_over,
    hash_password,
)
from app.data.crud import campaign, user
from app.data.crud.campaign import (
    Campaign,
    CampaignCreate,
    CampaignRead,
    CampaignUpdate,
    State,
)
from app.data.crud.user import Access, User, UserCreate, UserRead, UserUpdate
from app.data.session import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

router = APIRouter()


def change_user_access(status: bool, u: User, target: Access, db: Session) -> None:
    if status:
        user.update_access(u.id, target, db)
    else:
        user.update_access(u.id, Access.NORMAL, db)


def change_campaign_state(
    status: bool, c: Campaign, target: State, db: Session
) -> None:
    if status:
        campaign.update_state(c.id, target, db)
    elif has_crossed_deadline(c):
        campaign.update_state(c.id, State.ENDED, db)
    else:
        campaign.update_state(c.id, State.STARTED, db)


@router.post("/users/{id}/ban", response_model=UserRead)
async def ban_user(
    id: int,
    status: bool,
    db: Session = Depends(get_db),
    curr_u: User = Depends(get_current_super_user),
) -> User | None:
    existing_u = get_existing_user(id, db)

    change_user_access(status, existing_u, Access.BANNED, db)

    updated_u = user.read(id, db)

    return updated_u


@router.post("/users/{id}/mod", response_model=UserRead)
async def create_moderator(
    id: int,
    status: bool,
    db: Session = Depends(get_db),
    curr_u: User = Depends(get_current_admin_user),
) -> User | None:
    existing_u = get_existing_user(id, db)

    change_user_access(status, existing_u, Access.MOD, db)

    updated_u = user.read(id, db)

    return updated_u


@router.post("/campaigns/{id}/greenlight", response_model=CampaignRead)
async def greenlight_campaign(
    id: int,
    status: bool,
    db: Session = Depends(get_db),
    curr_u: User = Depends(get_current_super_user),
) -> Campaign | None:
    existing_c = get_existing_campaign(id, db)

    change_campaign_state(status, existing_c, State.GREENLIT, db)

    # TODO trigger other services

    updated_c = campaign.read(id, db)

    return updated_c


@router.post("/campaigns/{id}/lock", response_model=CampaignRead)
async def lock_campaign(
    id: int,
    status: bool,
    db: Session = Depends(get_db),
    curr_u: User = Depends(get_current_super_user),
) -> Campaign | None:
    existing_c = get_existing_campaign(id, db)

    change_campaign_state(status, existing_c, State.LOCKED, db)

    # TODO trigger other services

    updated_c = campaign.read(id, db)

    return updated_c
