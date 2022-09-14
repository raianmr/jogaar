from fastapi import APIRouter

from . import login

router = APIRouter(tags=["Authentication"])

router.include_router(login.router)
