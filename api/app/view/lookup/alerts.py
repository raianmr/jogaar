from fastapi import APIRouter

router = APIRouter()


@router.get("/alerts")
async def get_alerts(skip: int = 0, limit: int = 100):
    pass
