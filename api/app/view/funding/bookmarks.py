from fastapi import APIRouter, status

router = APIRouter()


@router.post("/campaigns/{c_id}/bookmarks", status_code=status.HTTP_201_CREATED)
async def create_bookmark(c_id: int):
    pass


@router.delete(
    "/campaigns/{c_id}/bookmarks/{b_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_bookmark(c_id: int, b_id: int):
    pass


@router.get("/campaigns/{c_id}/bookmarks/{b_id}")
async def read_bookmark(c_id: int, b_id: int):
    pass


@router.get("/campaigns/{c_id}/bookmarks")
async def read_bookmarks(c_id: int, skip: int = 0, limit: int = 100):
    pass
