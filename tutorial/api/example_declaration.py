# coding=utf-8

from typing import Optional

from fastapi import APIRouter, Body
from pydantic import BaseModel, Field, HttpUrl

router = APIRouter()


class User(BaseModel):
    name: str
    desc: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "name": "ZhangSan",
                "desc": "Leading role in videoes of Luoxiang.",
            }
        }


class Item(BaseModel):
    name: str = Field(..., example="saying")
    desc: Optional[str] = Field(
        None, example="All work, no play, makes a jack dull boy."
    )


class Image(BaseModel):
    name: str
    url: Optional[HttpUrl] = None


@router.post("/coco", summary="Declare request example in Field and Model")
def coco(user: User, item: Item):
    return {"user": user, "item": item}


@router.post("/lifetimes", summary="Declare request example in Body")
def lifetimes(
    image: Image = Body(
        ...,
        example={"name": "Mona Lisa", "url": "https://en.wikipedia.org/wiki/Mona_Lisa"},
    )
):
    return {"image": image}


@router.post(
    "/lordofring",
    summary="Declare multiple examples",
    description=(
        "examples is **NOT** working.\n\n"
        "See: [Declare Request Example Data \- FastAPI]"
        "(https://fastapi.tiangolo.com/tutorial/schema-extra-example/#technical-details)"
    ),
)
def lord_of_ring(
    image: Image = Body(
        ...,
        examples={
            "Leonardo da Vinci": {
                "name": "Mona Lisa",
                "url": "https://en.wikipedia.org/wiki/Mona_Lisa",
            },
            "Van Gogh": {
                "name": "Sunflowers",
                "url": "https://en.wikipedia.org/wiki/Sunflowers_(Van_Gogh_series)",
            },
        },
    )
):
    return {"image": image}
