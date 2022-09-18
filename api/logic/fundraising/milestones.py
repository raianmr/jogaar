from fastapi import APIRouter, status

router = APIRouter()


@router.post(
    "/campaigns/{c_id}/milestones",
    status_code=status.HTTP_201_CREATED,
)
async def create_milestone(c_id: int):
    pass


@router.put("/campaigns/{c_id}/milestones/{m_id}")
async def update_milestone(c_id: int, m_id: int):
    pass


@router.delete(
    "/campaigns/{c_id}/milestones/{m_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_milestone(c_id: int, m_id: int):
    pass


@router.get("/campaigns/{c_id}/milestones/{m_id}")
async def read_milestone(c_id: int, m_id: int):
    pass


@router.get("/campaigns/{c_id}/milestones")
async def read_milestones(c_id: int, skip: int = 0, limit: int = 100):
    pass
