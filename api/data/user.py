from datetime import datetime
from .base import Base
from pydantic import BaseModel, EmailStr
from sqlalchemy import Column, String
from sqlalchemy.orm import Session


class User(Base):  # type: ignore
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    about = Column(String)
    contact = Column(String)
    address = Column(String)


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserRead(BaseModel):
    id: int
    email: EmailStr

    name: str
    about: str | None
    contact: str | None
    address: str | None

    created_at: datetime

    class Config:
        orm_mode = True


def read_by_email(email: str, db: Session):
    return db.query(User).filter(User.email == email).first()

def read_all(limit: int, offset: int, db: Session):
    return db.query(User).limit(limit).offset(offset).all()

def create(u: UserCreate, db: Session):
    new_u = User(**u.dict())
    db.add(new_u)
    db.commit()
    db.refresh(new_u)
    return new_u
