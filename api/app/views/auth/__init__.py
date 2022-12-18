from fastapi import APIRouter

from . import login, super, users

router = APIRouter(tags=["Auth [Done]"])

router.include_router(login.router)
router.include_router(super.router)
router.include_router(users.router)
