from app.data.auth import user
from app.data.auth.user import User, UserLogin
from app.data.session import get_db
from app.config import env

from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from datetime import datetime, timedelta

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int | None = None


class InvalidCredsErr(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="given credentials are invalid",
        )


class UnauthorizedErr(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def hash(password: str) -> str:
    return pwd_context.hash(password)


def verify(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=env.EXPIRE_DELTA)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, env.SECRET_KEY, algorithm=env.ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str):

    try:
        payload = jwt.decode(token, env.SECRET_KEY, algorithms=[env.ALGORITHM])
        id = payload.get("user_id")

        if id is None:
            raise UnauthorizedErr

        token_data = TokenData(id=id)

    except JWTError:
        raise UnauthorizedErr

    return token_data


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):

    token_data = verify_access_token(token)

    existing_u = user.read(token_data.id, db)  # type: ignore

    return existing_u


@router.post("/login")
async def login(creds: UserLogin, db: Session = Depends(get_db)) -> dict:
    existing_u = user.read_by_email(creds.email, db)

    if not existing_u:
        raise InvalidCredsErr

    if not verify(creds.password, existing_u.password):
        raise InvalidCredsErr

    access_token = create_access_token(data={"user_id": existing_u.id})

    return {"access_token": access_token, "token_type": "bearer"}
