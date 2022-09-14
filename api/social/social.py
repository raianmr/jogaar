from fastapi import APIRouter

from . import replies, updates, votes

router = APIRouter(tags=["Social"])

router.include_router(replies.router)
router.include_router(updates.router)
router.include_router(votes.router)
