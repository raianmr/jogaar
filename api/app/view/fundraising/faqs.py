from app.core.campaigning import CampaignNotFoundErr, MiscConflictErr
from app.core.security import NotAllowedErr, get_current_valid_user
from app.data.crud import campaign, faq
from app.data.crud.faq import FAQ, FAQCreate, FAQRead, FAQUpdate
from app.data.crud.user import User
from app.data.session import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

router = APIRouter()


class QuestionConflictErr(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="FAQ with given question already exists for the campaign",
        )


class FAQNotFoundErr(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="FAQ was not found",
        )


@router.post(
    "/campaigns/{c_id}/faqs",
    status_code=status.HTTP_201_CREATED,
    response_model=FAQRead,
)
async def create_faq(
    c_id: int,
    f: FAQCreate,
    db: Session = Depends(get_db),
    curr_u: User = Depends(get_current_valid_user),
) -> FAQ:
    existing_c = campaign.read(c_id, db)

    if not existing_c:
        raise CampaignNotFoundErr

    if existing_c.campaigner_id != curr_u.id:
        raise NotAllowedErr

    try:
        new_f = faq.create(c_id, f, db)

    except IntegrityError:
        raise QuestionConflictErr

    return new_f


@router.put("/faqs/{f_id}", response_model=FAQRead)
async def update_faq(
    f_id: int,
    f: FAQUpdate,
    db: Session = Depends(get_db),
    curr_u: User = Depends(get_current_valid_user),
) -> FAQ | None:
    existing_f = faq.read(f_id, db)

    if not existing_f:
        raise FAQNotFoundErr

    existing_c = campaign.read(existing_f.campaign_id, db)  # type: ignore

    if not existing_c:
        raise CampaignNotFoundErr

    if existing_c.campaigner_id != curr_u.id:
        raise NotAllowedErr

    try:
        faq.update(f_id, f, db)
        updated_f = faq.read(f_id, db)

    except IntegrityError:
        raise QuestionConflictErr

    return updated_f


@router.delete(
    "/faqs/{f_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_faq(
    f_id: int,
    db: Session = Depends(get_db),
    curr_u: User = Depends(get_current_valid_user),
):
    existing_f = faq.read(f_id, db)

    if not existing_f:
        raise FAQNotFoundErr

    existing_c = campaign.read(existing_f.campaign_id, db)  # type: ignore

    if not existing_c:
        raise CampaignNotFoundErr

    if existing_c.campaigner_id != curr_u.id:
        raise NotAllowedErr

    faq.delete(f_id, db)


@router.get("/faqs/{f_id}", response_model=FAQRead)
async def read_faq(f_id: int, db: Session = Depends(get_db)) -> FAQ:
    existing_f = faq.read(f_id, db)

    if not existing_f:
        raise FAQNotFoundErr

    return existing_f


@router.get("/campaigns/{c_id}/faqs", response_model=list[FAQRead])
async def read_faqs_by_campaign(
    c_id: int, limit: int = 100, offset: int = 0, db: Session = Depends(get_db)
) -> list[FAQ]:
    all_f_by_c = faq.read_all_by_campaign(c_id, limit, offset, db)

    return all_f_by_c
