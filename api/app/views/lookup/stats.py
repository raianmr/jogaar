from fastapi import APIRouter

router = APIRouter()


@router.get("/stats")
async def get_stats():
    pass
