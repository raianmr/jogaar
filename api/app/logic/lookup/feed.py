from fastapi import APIRouter

router = APIRouter()


@router.get("/feed")
async def get_feed():
    pass
