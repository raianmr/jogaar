from fastapi import APIRouter

from . import login, users

router = APIRouter(tags=["Authentication [WIP]"])

router.include_router(login.router)
router.include_router(users.router)
