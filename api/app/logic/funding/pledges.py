from fastapi import APIRouter, status

router = APIRouter()


@router.post("/campaigns/{c_id}/pledges", status_code=status.HTTP_201_CREATED)
async def create_pledge(c_id: int):
    pass


@router.put("/campaigns/{c_id}/pledges/{p_id}")
async def update_pledge(c_id: int, p_id: int):
    pass


@router.delete(
    "/campaigns/{c_id}/pledges/{p_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_pledge(c_id: int, p_id: int):
    pass


@router.get("/campaigns/{c_id}/pledges/{p_id}")
async def read_pledge(c_id: int, p_id: int):
    pass


@router.get("/campaigns/{c_id}/pledges")
async def read_pledges(c_id: int, skip: int = 0, limit: int = 100):
    pass
