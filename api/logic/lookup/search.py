from fastapi import APIRouter

router = APIRouter()


@router.get("/search")
async def search(skip: int = 0, limit: int = 100, search: str = ""):
    pass
