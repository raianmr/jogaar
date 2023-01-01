from app.core import security, utils
from app.data.crud import campaign, misc, report, user
from app.data.crud.campaign import Campaign, CampaignRead, State
from app.data.crud.report import Report, Reportable, ReportCreate, ReportRead
from app.data.crud.user import Access, User, UserRead
from app.data.session import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

router = APIRouter()


class ReportNotFoundErr(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="report was not found",
        )


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
    elif utils.has_crossed_deadline(c):
        campaign.update_state(c.id, State.ENDED, db)
    else:
        campaign.update_state(c.id, State.STARTED, db)


@router.post("/users/{id}/ban", response_model=UserRead)
async def ban_user(
    id: int,
    status: bool,
    db: Session = Depends(get_db),
    curr_u: User = Depends(security.get_current_super_user),
) -> User | None:
    existing_u = security.get_existing_user(id, db)

    change_user_access(status, existing_u, Access.BANNED, db)

    updated_u = user.read(id, db)

    return updated_u


@router.post("/users/{id}/mod", response_model=UserRead)
async def create_moderator(
    id: int,
    status: bool,
    db: Session = Depends(get_db),
    curr_u: User = Depends(security.get_current_admin_user),
) -> User | None:
    existing_u = security.get_existing_user(id, db)

    change_user_access(status, existing_u, Access.MOD, db)

    updated_u = user.read(id, db)

    return updated_u


@router.get("/super", response_model=list[UserRead])
async def read_super_users(
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db),
    curr_u: User = Depends(security.get_current_super_user),
) -> list[User]:
    return misc.read_all_super(limit, offset, db)


@router.post("/campaigns/{id}/greenlight", response_model=CampaignRead)
async def greenlight_campaign(
    id: int,
    status: bool,
    db: Session = Depends(get_db),
    curr_u: User = Depends(security.get_current_super_user),
) -> Campaign | None:
    existing_c = utils.get_existing_campaign(id, db)

    change_campaign_state(status, existing_c, State.GREENLIT, db)

    # TODO trigger other services

    updated_c = campaign.read(id, db)

    return updated_c


@router.post("/campaigns/{id}/lock", response_model=CampaignRead)
async def lock_campaign(
    id: int,
    status: bool,
    db: Session = Depends(get_db),
    curr_u: User = Depends(security.get_current_super_user),
) -> Campaign | None:
    existing_c = utils.get_existing_campaign(id, db)

    change_campaign_state(status, existing_c, State.LOCKED, db)

    # TODO trigger other services

    updated_c = campaign.read(id, db)

    return updated_c


@router.post("/reports", status_code=status.HTTP_201_CREATED, response_model=ReportRead)
async def create_report(
    r: ReportCreate,
    db: Session = Depends(get_db),
    curr_u: User = Depends(security.get_current_valid_user),
) -> Report:
    try:
        new_report = report.create(curr_u.id, r, db)

    except IntegrityError:
        raise utils.MiscConflictErr

    return new_report


@router.delete("/reports/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_report(
    id: int,
    db: Session = Depends(get_db),
    curr_u: User = Depends(security.get_current_super_user),
) -> None:
    existing_report = utils.get_existing_report(id, db)

    report.delete(existing_report.id, db)


@router.get("/reports/{id}", response_model=ReportRead)
async def read_report(
    id: int,
    db: Session = Depends(get_db),
    curr_u: User = Depends(security.get_current_super_user),
) -> Report:
    existing_report = report.read(id, db)
    if existing_report is None:
        raise ReportNotFoundErr

    return existing_report


@router.get("/reports", response_model=list[ReportRead])
async def read_reports(
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db),
    curr_u: User = Depends(security.get_current_super_user),
) -> list[Report]:
    all_reports = report.read_all(limit, offset, db)

    return all_reports
