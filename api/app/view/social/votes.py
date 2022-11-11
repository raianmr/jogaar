from app.core.campaigning import get_existing_campaign, get_existing_reply
from app.core.security import NotAllowedErr, get_current_valid_user, has_access_over
from app.data.crud import vote
from app.data.crud.user import User
from app.data.crud.vote import Vote, VoteRead
from app.data.session import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

router = APIRouter()

# TODO embed score in reply fetching


class UserAndReplyConflictErr(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="vote by current user already exists for the reply",
        )


class VoteNotFoundErr(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="bookmark was not found",
        )


def get_existing_vote(u_id: int, r_id: int, db: Session) -> Vote:
    existing_b = vote.read_by_user_and_reply(u_id, r_id, db)
    if not existing_b:
        raise VoteNotFoundErr

    return existing_b


@router.post(
    "/replies/{r_id}/votes",
    status_code=status.HTTP_201_CREATED,
    response_model=VoteRead,
)
async def create_vote(
    r_id: int,
    db: Session = Depends(get_db),
    curr_u: User = Depends(get_current_valid_user),
) -> Vote:
    existing_r = get_existing_reply(r_id, db)

    try:
        new_v = vote.create(curr_u.id, existing_r.id, db)

    except IntegrityError:
        raise UserAndReplyConflictErr

    return new_v


@router.delete(
    "/replies/{r_id}/votes",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_vote(
    r_id: int,
    db: Session = Depends(get_db),
    curr_u: User = Depends(get_current_valid_user),
) -> None:
    existing_v = get_existing_vote(curr_u.id, r_id, db)  # type: ignore
    existing_r = get_existing_reply(existing_v.reply_id, db)  # type: ignore

    vote.delete_by_user_and_reply(curr_u.id, existing_r.id, db)


@router.get("/replies/{r_id}/votes")
async def read_votes_by_reply(
    r_id: int,
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db),
) -> list[Vote]:
    all_v_by_r = vote.read_all_by_reply(r_id, limit, offset, db)

    return all_v_by_r
