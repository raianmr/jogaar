from fastapi import APIRouter

from . import campaigns, faqs, milestones, rewards, tags

router = APIRouter(tags=["Fundraising"])

router.include_router(campaigns.router)
router.include_router(faqs.router)
router.include_router(milestones.router)
router.include_router(rewards.router)
router.include_router(tags.router)
