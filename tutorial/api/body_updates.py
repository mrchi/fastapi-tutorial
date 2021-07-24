# coding=utf-8

from typing import Optional
from datetime import datetime

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.params import Body, Path
from pydantic import BaseModel

router = APIRouter()


class Item(BaseModel):
    title: str
    timestamp: datetime
    description: Optional[str] = None
    price: float = 10.5


items = {
    "foo": {"title": "Foo", "timestamp": datetime(2019, 1, 1), "price": 99},
    "bar": {
        "title": "Bar",
        "timestamp": datetime(2020, 1, 1),
        "description": "This is Bar.",
        "price": 100,
    },
    "baz": {"title": "Bar", "timestamp": datetime(2020, 1, 1)},
}


@router.post("/heidi", summary="jsonable_encoder")
def heidi(item: Item):
    return {"item": jsonable_encoder(item)}


@router.put(
    "/abeautifulmind/{item_id}",
    summary="Replacing updates with PUT",
    description="The input model would take default value if the attribute is not included.",
)
def a_beautiful_mind(
    item_id: str = Path(..., example="foo"),
    item: Item = Body(..., example={"title": "Foo1", "timestamp": datetime.now()}),
):
    return jsonable_encoder(item)


@router.patch(
    "/benjamin/{item_id}",
    summary="Partial updates with PATCH, by model.dict(exclude_unset=True)",
)
def benjamin_button(
    item_id: str = Path(..., example="foo"),
    item: Item = Body(..., example={"title": "Foo1", "timestamp": datetime.now()}),
):
    return item.dict(exclude_unset=True)


@router.patch(
    "/twosmokingbarrels/{item_id}",
    summary="Partial updates with PATCH, by model.copy(update=updated_data)",
)
def two_smoking_barrels(
    item_id: str = Path(..., example="foo"),
    item: Item = Body(..., example={"title": "Foo1", "timestamp": datetime.now()}),
):
    updated_data = item.dict(exclude_unset=True)
    item = Item(**items[item_id])
    return item.copy(update=updated_data)
