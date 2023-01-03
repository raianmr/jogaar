from fastapi import APIRouter

from . import alerts, feed, images, search, stats

router = APIRouter(tags=["Lookup [Done]"])

router.include_router(alerts.router)
router.include_router(feed.router)
router.include_router(images.router)
router.include_router(search.router)
router.include_router(stats.router)
