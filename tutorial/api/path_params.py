# coding=utf-8

import time
from enum import Enum

from fastapi import APIRouter, Path
from fastapi.param_functions import Query

router = APIRouter()


class WebFramework(str, Enum):
    flask = "Flask"
    django = "Django"
    tornado = "Tornado"
    twisted = "Twisted"


@router.get(
    "/users/0",
    summary="Specific path",
    description="Make sure that the path for /users/0 is declared before the one for /users/{user_id}.",
)
def read_user_zero():
    return {"user_id": "Zero, the BOSS."}


@router.get("/users/{user_id}", summary="Path parameter with type hint")
def read_user(user_id: int):
    return {"user_id": user_id}


@router.get("/webframeworks/{framework}", summary="Path parameter of Enum class type")
def get_webframework(framework: WebFramework):
    return {
        "framework": framework,
        "type": str(type(framework)),
        "value": framework.value,
    }


@router.get("/files/{file_path:path}", summary="Path parameter containing a path")
def read_file(file_path: str):
    return {"file_path": file_path}


@router.get("/users/{user_id}/items/{item_id}", summary="Multiple path parameters")
def get_user_items(user_id: int, item_id: int):
    return {"user_id": user_id, "item_id": item_id}


@router.get("/items/{item_id}", summary="Path parameter with metadata")
def get_item_detail(
    item_id: int = Path(..., title="Item ID", description="Item ID of the item to get")
):
    return {"item_id": item_id}


@router.get(
    "/interstellar/{ts_int}/{ts_float}",
    summary="Path parameters with additional validation",
    tags=["Validation"],
)
def get_interstellar_timestamp(
    ts_int: int = Path(..., ge=0, le=1625385023),
    ts_float: float = Path(..., gt=100, lt=200),
):
    return {"ts_int": ts_int, "ts_float": ts_float}
