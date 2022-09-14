from fastapi import APIRouter

from . import users

router = APIRouter(tags=["People"])

router.include_router(users.router)
