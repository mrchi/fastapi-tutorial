# coding=utf-8

import pathlib

from typing import Optional
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette.responses import FileResponse

router = APIRouter(
    responses={
        418: {"description": "I'm a teapot."},
    }
)
image_path = pathlib.Path(__file__).parents[1] / "static" / "atom.png"


class Item(BaseModel):
    id: str
    value: str


class Message(BaseModel):
    message: str


@router.get(
    "/item",
    response_model=Item,
    responses={404: {"model": Message}},
    summary="Additional Response with model",
)
def get_item(item_id: str = "foo"):
    if item_id == "foo":
        return {"id": "foo", "value": "Dolores"}
    else:
        return JSONResponse(content={"message": "Item not found"}, status_code=404)


@router.get(
    "/media",
    response_model=Item,
    responses={
        200: {
            "content": {"image/png": {}},
            "description": "Return the JSON item or an image.",
        }
    },
    summary="Additional media type for main reponse",
)
def return_item_or_image(item_id: str = "foo", img: Optional[bool] = True):
    if img:
        return FileResponse(image_path, media_type="image/png")
    else:
        return {"id": "foo", "value": "Dolores"}


@router.get(
    "/combine",
    response_model=Item,
    responses={
        404: {"model": Message, "description": "The item was not found."},
        200: {
            "description": "Item requested by ID.",
            "content": {
                "application/json": {
                    "example": {"id": "bar", "value": "the bar tenders"}
                }
            },
        },
    },
    summary="Combining information from response_model, status_code, responses",
)
def combine(item_id: str = "foo"):
    if item_id == "foo":
        return {"id": "foo", "value": "Dolores"}
    else:
        return JSONResponse(content={"message": "Item not found"}, status_code=404)


@router.get(
    "/default", response_model=Item, summary="Additional responses set by APIRouter."
)
def default():
    return {"id": "foo", "value": "Dolores"}
