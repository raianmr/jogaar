from fastapi import APIRouter, status

router = APIRouter()


@router.post(
    "/campaigns/{c_id}/updates/{u_id}/replies",
    status_code=status.HTTP_201_CREATED,
)
async def create_reply(c_id: int, u_id: int):
    pass


@router.put("/campaigns/{c_id}/updates/{u_id}/replies/{r_id}")
async def update_reply(c_id: int, u_id: int, r_id: int):
    pass


@router.delete(
    "/campaigns/{c_id}/updates/{u_id}/replies/{r_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_reply(c_id: int, u_id: int, r_id: int):
    pass


@router.get("/campaigns/{c_id}/updates/{u_id}/replies/{r_id}")
async def read_reply(c_id: int, u_id: int, r_id: int):
    pass


@router.get("/campaigns/{c_id}/updates/{u_id}/replies")
async def read_replies(c_id: int, u_id: int, skip: int = 0, limit: int = 100):
    pass
