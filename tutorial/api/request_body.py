# coding=utf-8

from typing import Optional
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class Item(BaseModel):
    name: str
    desciption: Optional[str] = None
    price: float
    tax: Optional[float] = None


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
