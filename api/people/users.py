from fastapi import APIRouter, status

router = APIRouter()


@router.post("/users", status_code=status.HTTP_201_CREATED)
async def create_user():
    pass


@router.put("/users/{id}")
async def update_user(id: int):
    pass


@router.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: int):
    pass


@router.get("/users/{id}")
async def read_user(id: int):
    pass


@router.get("/users")
async def read_users(skip: int = 0, limit: int = 100):
    pass
