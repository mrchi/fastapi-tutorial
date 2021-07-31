# coding=utf-8

from dataclasses import field
from typing import Optional

from fastapi import APIRouter
from pydantic.dataclasses import dataclass

router = APIRouter()


@dataclass
class Item:
    name: str
    price: float
    desc: Optional[str] = None
    tax: Optional[float] = None


@dataclass
class Author:
    name: str
    items: list[Item] = field(default_factory=list)


@router.post(
    "/items/",
    response_model=Item,
    summary="dataclasses in request body and response model",
    description="There's a bug or feature when using dataclasses from Python standard library."
    "See [issue-3636](https://github.com/tiangolo/fastapi/issues/3636)",
)
async def create_item(item: Item):
    return item


@router.post(
    "/authors/{author_id}/items/",
    response_model=Author,
    summary="dataclasses in nested data structures",
)
def create_author_item(author_id: str, items: list[Item]):
    return {"name": author_id, "items": items}
