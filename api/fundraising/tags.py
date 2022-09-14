from fastapi import APIRouter, status

router = APIRouter()


@router.post(
    "/campaigns/{c_id}/tags",
    status_code=status.HTTP_201_CREATED,
)
async def create_tag(c_id: int):
    pass


@router.put("/campaigns/{c_id}/tags/{t_id}")
async def update_tag(c_id: int, t_id: int):
    pass


@router.delete(
    "/campaigns/{c_id}/tags/{t_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_tag(c_id: int, t_id: int):
    pass


@router.get("/campaigns/{c_id}/tags/{t_id}")
async def read_tag(c_id: int, t_id: int):
    pass


@router.get("/campaigns/{c_id}/tags")
async def read_tags(c_id: int, skip: int = 0, limit: int = 100):
    pass
