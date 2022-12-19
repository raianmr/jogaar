from pathlib import Path

import sqlalchemy as sa
from app.data.base import Base, BaseRead
from sqlalchemy.orm import Session


class Image(Base):
    uploader_id = sa.Column(
        sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    filename = sa.Column(sa.String, nullable=False)
    filetype = sa.Column(sa.String, nullable=False)
    location = sa.Column(sa.String)


class ImageRead(BaseRead):
    uploader_id: int

    filename: str
    filetype: str
    location: str


def store(img: Image, contents: bytes) -> str:
    parentdir = Path(f"static/images/{img.uploader_id}")
    parentdir.mkdir(parents=True, exist_ok=True)

    location = parentdir / Path(f"{img.id}-{img.filename}")
    location.touch()
    location.write_bytes(contents)

    return location.as_posix()


def create(
    u_id: int | sa.Column,
    name: str,
    type: str,
    contents: bytes,
    db: Session,
) -> Image:
    # TODO do all these in one db transaction

    new_image = Image(
        uploader_id=u_id,
        filename=name,
        filetype=type,
    )  # type: ignore
    db.add(new_image)
    db.commit()
    db.refresh(new_image)

    location = store(new_image, contents)
    (
        db.query(Image)
        .filter(Image.id == new_image.id)
        .update({Image.location: location})
    )
    db.commit()
    db.refresh(new_image)

    return new_image


def read(id: int | sa.Column, db: Session) -> Image | None:
    return db.query(Image).filter(Image.id == id).first()


def read_all(limit: int, offset: int, db: Session) -> list[Image]:
    return db.query(Image).limit(limit).offset(offset).all()


def read_all_by_user(
    u_id: int | sa.Column, limit: int, offset: int, db: Session
) -> list[Image]:
    return (
        db.query(Image)
        .filter(Image.uploader_id == u_id)
        .limit(limit)
        .offset(offset)
        .all()
    )


def delete(id: int | sa.Column, db: Session) -> None:
    db.query(Image).filter(Image.id == id).delete()

    db.commit()
