from fastapi import APIRouter
from passlib.context import CryptContext

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str) -> str:
    return pwd_context.hash(password)


def verify(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


@router.post("/login")
async def login():
    pass
