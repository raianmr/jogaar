from fastapi import APIRouter

from . import bookmarks, pledges

router = APIRouter(tags=["Funding [WIP]"])

router.include_router(bookmarks.router)
router.include_router(pledges.router)
