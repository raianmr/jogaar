from fastapi import APIRouter, status

router = APIRouter()


@router.post(
    "/campaigns/{c_id}/updates/{u_id}/replies/{r_id}/votes",
    status_code=status.HTTP_201_CREATED,
)
async def create_vote(c_id: int, u_id: int, r_id: int):
    pass


@router.delete(
    "/campaigns/{c_id}/updates/{u_id}/replies/{r_id}/votes/{v_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_vote(c_id: int, u_id: int, r_id: int, v_id: int):
    pass


@router.get("/campaigns/{c_id}/updates/{u_id}/replies/{r_id}/votes/{v_id}")
async def read_vote(c_id: int, u_id: int, r_id: int, v_id: int):
    pass


@router.get("/campaigns/{c_id}/updates/{u_id}/replies/{r_id}/votes")
async def read_votes(c_id: int, u_id: int, r_id: int, skip: int = 0, limit: int = 100):
    pass
