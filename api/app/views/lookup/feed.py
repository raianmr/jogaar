from fastapi import APIRouter

router = APIRouter()

# feed should contain:
# + news feed
#   - updates from bookmarked campaigns
# + featured campaigns
#   - sort by number of distinct pledgers
#   - only show ongoing campaigns
# + based on your interests
#   - sort featured campaigns by user's most bookmarked tags
# + recently viewed
#   - based on GET on /campaigns endpoints
#   - custom lru cache or redis?


@router.get("/feed")
async def get_feed():
    pass
