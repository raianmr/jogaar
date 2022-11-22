from fastapi import APIRouter

from . import alerts, feed, images, search

router = APIRouter(tags=["Lookup [To do]"])

router.include_router(alerts.router)
router.include_router(feed.router)
router.include_router(images.router)
router.include_router(search.router)
