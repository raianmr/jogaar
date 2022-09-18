from fastapi import APIRouter, status

router = APIRouter()


@router.post(
    "/campaigns/{c_id}/faqs",
    status_code=status.HTTP_201_CREATED,
)
async def create_faq(c_id: int):
    pass


@router.put("/campaigns/{c_id}/faqs/{f_id}")
async def update_faq(c_id: int, f_id: int):
    pass


@router.delete(
    "/campaigns/{c_id}/faqs/{f_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_faq(c_id: int, f_id: int):
    pass


@router.get("/campaigns/{c_id}/faqs/{f_id}")
async def read_faq(c_id: int, f_id: int):
    pass


@router.get("/campaigns/{c_id}/faqs")
async def read_faqs(c_id: int, skip: int = 0, limit: int = 100):
    pass
