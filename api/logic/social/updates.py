from fastapi import APIRouter, status

router = APIRouter()


@router.post(
    "/campaigns/{c_id}/updates",
    status_code=status.HTTP_201_CREATED,
)
async def create_update(c_id: int):
    pass


@router.put("/campaigns/{c_id}/updates/{u_id}")
async def update_update(c_id: int, u_id: int):  # lmao
    pass


@router.delete(
    "/campaigns/{c_id}/updates/{u_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_update(c_id: int, u_id: int):
    pass


@router.get("/campaigns/{c_id}/updates/{u_id}")
async def read_update(c_id: int, u_id: int):
    pass


@router.get("/campaigns/{c_id}/updates")
async def read_updates(c_id: int, skip: int = 0, limit: int = 100):
    pass
