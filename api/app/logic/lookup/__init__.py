from fastapi import APIRouter

from . import alerts, feed, search

router = APIRouter(tags=["Lookup"])

router.include_router(alerts.router)
router.include_router(feed.router)
router.include_router(search.router)
