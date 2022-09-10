from fastapi import FastAPI
from pydantic import BaseModel

api = FastAPI()


class User(BaseModel):
    id: int
    email: str
    password: str


Users: list[User] = [
    User(id=1, email="mamod@jogaar.com", password="shouldBeHashed"),
    User(id=2, email="fatin@jogaar.com", password="shouldBeHashed"),
    User(id=3, email="jayed@jogaar.com", password="shouldBeHashed"),
]


@api.get("/")
async def root():
    return {"message": "it works!"}


@api.get("/users")
async def get_users():
    return Users
