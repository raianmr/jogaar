from app.data.auth import user
from app.data.auth.user import User, UserLogin
from app.data.session import get_db
from app.config import env

from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
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


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=env.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, env.SECRET_KEY, algorithm=env.ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, env.SECRET_KEY, algorithms=[env.ALGORITHM])
        id = payload.get("user_id")

        if not id:
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


@router.post("/login", response_model=Token)
async def login_user(
    creds: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
) -> dict:
    existing_u = user.read_by_email(creds.username, db)

    if not existing_u:
        raise InvalidCredsErr

    if not verify_password(creds.password, existing_u.password):
        raise InvalidCredsErr

    access_token = create_access_token(data={"user_id": existing_u.id})

    return {"access_token": access_token, "token_type": "bearer"}
