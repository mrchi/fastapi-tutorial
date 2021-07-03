# coding=utf-8

from enum import Enum

from fastapi import APIRouter

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


@router.get("/users/{user_id}", summary="Path parameter with types")
def read_user(user_id: int):
    return {"user_id": user_id}


@router.get("/webframeworks/{framework}", summary="Path parameter with Enum class type")
def get_webframework(framework: WebFramework):
    return {
        "framework": framework,
        "type": str(type(framework)),
        "value": framework.value,
    }


@router.get("/files/{file_path:path}", summary="Path parameter containing a path")
def read_file(file_path: str):
    return {"file_path": file_path}
