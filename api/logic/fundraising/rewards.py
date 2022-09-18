from fastapi import APIRouter, status

router = APIRouter()


@router.post(
    "/campaigns/{c_id}/rewards",
    status_code=status.HTTP_201_CREATED,
)
async def create_reward(c_id: int):
    pass


@router.put("/campaigns/{c_id}/rewards/{r_id}")
async def update_reward(c_id: int, r_id: int):
    pass


@router.delete(
    "/campaigns/{c_id}/rewards/{r_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_reward(c_id: int, r_id: int):
    pass


@router.get("/campaigns/{c_id}/rewards/{r_id}")
async def read_reward(c_id: int, r_id: int):
    pass


@router.get("/campaigns/{c_id}/rewards")
async def read_rewards(c_id: int, skip: int = 0, limit: int = 100):
    pass
