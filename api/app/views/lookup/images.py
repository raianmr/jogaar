from app.core import security, utils
from app.data.crud import image
from app.data.crud.image import Image, ImageRead
from app.data.crud.user import User
from app.data.session import get_db
from fastapi import APIRouter, Depends, File, UploadFile, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

router = APIRouter()


@router.post(
    "/images",
    status_code=status.HTTP_201_CREATED,
)
async def upload_image(
    file: UploadFile = File(),
    db: Session = Depends(get_db),
    curr_u: User = Depends(security.get_current_valid_user),
) -> Image:
    try:
        new_img = image.create(
            u_id=curr_u.id,
            name=file.filename,
            type=file.content_type,
            contents=await file.read(),
            db=db,
        )

    except IntegrityError:
        raise utils.MiscConflictErr

    return new_img


@router.delete("/images/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_image(
    id: int,
    db: Session = Depends(get_db),
    curr_u: User = Depends(security.get_current_valid_user),
) -> None:
    existing_img = utils.get_existing_image(id, db)

    if not security.has_access_over(existing_img, curr_u):
        raise security.NotAllowedErr

    image.delete(id, db)


@router.get("/images/{id}", response_model=ImageRead)
async def download_image(id: int, db: Session = Depends(get_db)) -> Image:
    existing_img = utils.get_existing_image(id, db)

    return existing_img
