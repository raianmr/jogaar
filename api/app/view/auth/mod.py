from app.core.security import (
    AuthenticatingErr,
    BannedUserErr,
    Token,
    create_access_token,
    verify_password,
)
from app.data.crud import user
from app.data.session import get_db
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

router = APIRouter()
