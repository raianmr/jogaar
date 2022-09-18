from data import user
from data.session import get_db
from data.user import User, UserCreate, UserRead
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .security import hash_password

router = APIRouter()


@router.post("/users", status_code=status.HTTP_201_CREATED)
async def create_user(u: UserCreate, db: Session = Depends(get_db)):
    existing_u: User | None = user.read_by_email(u.email, db)

    if existing_u:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"user with email {u.email} already exists",
        )

    u.password = hash_password(u.password)
    new_u = user.create(u, db)

    return new_u


@router.put("/users/{id}")
async def update_user(id: int):
    pass


@router.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: int):
    pass


@router.get("/users/{id}", response_model=UserRead)
async def read_user(id: int):
    pass


@router.get("/users", response_model=list[UserRead])
async def read_users(limit: int = 100, offset: int = 0, db: Session = Depends(get_db)):
    all_u = user.read_all(limit, offset, db)

    return all_u
