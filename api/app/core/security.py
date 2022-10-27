from datetime import datetime, timedelta, timezone
from functools import singledispatch
from typing import Callable

from app.core.config import env
from app.data.crud import user
from app.data.crud.campaign import Campaign, State
from app.data.crud.user import Access, User
from app.data.session import get_db
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy import Column
from sqlalchemy.orm import Session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int


class AuthenticatingErr(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="given credentials are invalid",
            headers={"WWW-Authenticate": "Bearer"},
        )


class NotAllowedErr(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"not allowed to do that",
        )


class BannedUserErr(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"banned by a moderator",
        )


class UserNotFoundErr(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user was not found",
        )


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str | Column) -> bool:
    return pwd_context.verify(plain_password, hashed_password)  # type: ignore


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=env.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode["exp"] = expire

    encoded_jwt = jwt.encode(to_encode, env.SECRET_KEY, algorithm=env.ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, env.SECRET_KEY, algorithms=[env.ALGORITHM])
        user_id = payload.get("user_id")

        if not user_id:
            raise AuthenticatingErr

        token_data = TokenData(id=user_id)

    except JWTError:
        raise AuthenticatingErr

    return token_data


def is_valid(u: User) -> bool:
    return Access.BANNED != u.access_level


def is_super(u: User) -> bool:
    return u.access_level in [Access.MOD, Access.ADMIN]


def is_admin(u: User) -> bool:
    return Access.ADMIN == u.access_level


# for securing resources


@singledispatch
def has_access_over(r, curr_u: User) -> bool:
    if is_super(curr_u):
        return True

    try:
        return r.user_id == curr_u.id
    except AttributeError:
        return False


@has_access_over.register
def _(u: User, curr_u: User) -> bool:
    if is_super(curr_u):
        return True

    if u.id == curr_u.id:
        return True

    return False


@has_access_over.register
def _(c: Campaign, curr_u: User) -> bool:
    if is_super(curr_u):
        return True

    if c.campaigner_id == curr_u.id and c.current_state != State.LOCKED:
        return True

    return False


# for securing endpoints


def get_existing_user(user_id: int, db: Session) -> User:
    existing_u = user.read(user_id, db)
    if not existing_u:
        raise UserNotFoundErr

    return existing_u


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:

    token_data = verify_access_token(token)

    existing_u = get_existing_user(token_data.id, db)

    return existing_u


class AuthorizedUser:
    def __init__(self, criterion: Callable[[User], bool]) -> None:
        self.authorized = criterion

    def __call__(self, curr_u: User = Depends(get_current_user)) -> User:
        if not self.authorized(curr_u):
            raise NotAllowedErr

        return curr_u


get_current_valid_user = AuthorizedUser(criterion=is_valid)
get_current_super_user = AuthorizedUser(criterion=is_super)
get_current_admin_user = AuthorizedUser(criterion=is_admin)
