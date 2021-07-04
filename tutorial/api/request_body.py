# coding=utf-8

from typing import Optional
from fastapi import APIRouter, Body
from pydantic import BaseModel, Field, HttpUrl, RedisDsn

router = APIRouter()


class User(BaseModel):
    username: str
    fullname: Optional[str] = None


class Item(BaseModel):
    name: str
    desciption: Optional[str] = None
    price: float
    tax: Optional[float] = None


class Robot(BaseModel):
    name: str
    description: Optional[str] = Field(
        None,
        max_length=100,
        title="Robot description",
        description="The description for robot on earth.",
    )
    battery: float = Field(
        100,
        ge=0,
        le=100,
        title="Robot battery percent",
        description="WALL.E needs to charge every day.",
    )


class Image(BaseModel):
    name: str
    url: str


class Animal(BaseModel):
    name: str
    tags: set[str] = set()
    image: Optional[Image] = None


class Connection(BaseModel):
    name: str
    url: HttpUrl


class ImageGallery(BaseModel):
    name: str
    images: Optional[list[Image]] = None


class MultiImageGallery(BaseModel):
    name: str
    galleries: Optional[list[ImageGallery]] = None


@router.post("/items/", summary="JSON body parameter")
def create_item(item: Item):
    resp = item.dict()
    if item.tax is not None:
        resp["price_with_tax"] = item.price + item.tax
    return resp


@router.put(
    "/items/{item_id}",
    summary="Request body + path parameter + query parameter",
    description=(
        "- If the parameter is also declared in the **path**, it will be used as a **path parameter**.\n"
        "- If the parameter is of a **singular type** (like int, float, str, bool, etc) it will be interpreted as a **query parameter**.\n"
        "- If the parameter is declared to be of the type of a **Pydantic model**, it will be interpreted as a **request body**.\n"
    ),
)
def update_item(item_id: int, item: Item, confirm: bool = True):
    return {
        "item_id": item_id,
        "item": item,
        "confirm": confirm,
    }


@router.post("/item_with_owner/", summary="Multiple body parameters")
def create_item_with_owner(item: Item, owner: User):
    return {"item": item, "owner": owner}


@router.post("/1900/", summary="Singular values in body parameter")
def pinao_genius(item: Optional[Item] = None, importance: str = Body(...)):
    return {"item": item, "importance": importance}


@router.post("/3idiots/", summary="Embed a single body parameter")
def aamir_khan(item: Item = Body(..., embed=True)):
    return {"item": item}


@router.post("/walle/", summary="Model field with extra information")
def build_walle(robot: Robot):
    return {"robot": robot}


@router.post("/zootopia/", summary="Nested models")
def arrest_animal(animal: Animal):
    return {"animal": animal}


@router.post(
    "/connection/", summary="Special types and validation", tags=["Validation"]
)
def create_new_connection(
    conn: Connection,
    redis: RedisDsn = Body(...),
):
    return {"conn": conn, "redis": redis}


@router.post("/darknight/", summary="Deeply nested models")
def dark_knight(gallery: MultiImageGallery):
    return {"gallery": gallery}


@router.post("/images/", summary="Bodies of pure lists")
def create_images(images: list[Image]):
    return {"images": images}


@router.post("/emperors/", summary="Bodies of arbitrary dicts")
def arbirary_dicts(emperors: dict[int, str]):
    return {"emperors": emperors}
