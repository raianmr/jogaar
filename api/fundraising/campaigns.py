from fastapi import APIRouter, status

router = APIRouter()


@router.post("/campaigns", status_code=status.HTTP_201_CREATED)
async def create_campaign():
    pass


@router.put("/campaigns/{c_id}")
async def update_campaign(c_id: int):
    pass


@router.delete("/campaigns/{c_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_campaign(c_id: int):
    pass


@router.get("/campaigns/{c_id}")
async def read_campaign(c_id: int):
    pass


@router.get("/campaigns")
async def read_campaigns(skip: int = 0, limit: int = 100):
    pass
