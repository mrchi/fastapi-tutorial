# coding=utf-8

from typing import Optional
from fastapi import APIRouter, Query


router = APIRouter()


@router.get("/items/", summary="Query parameter with default value")
def get_items(limit: int = 10, offset: int = 0):
    return {"limit": limit, "offset": offset}


@router.get("/products/", summary="Required and optional query parameter")
def search_products(category: str, keyword: Optional[str] = None):
    return {"category": category, "keyword": keyword}


@router.get(
    "/shawshank/",
    summary="Bool type query parameter",
    description="Try to use yes/no, on/off, 0/1, True/False as value.",
)
def search_shawshank(innocent: bool = False):
    return {"innocent": innocent}


@router.get("/concubines/", summary="Query parameters with additional validation")
def search_concubines(
    hh: Optional[str] = Query(
        None,
        min_length=1,
        max_length=2,
        regex=r"^(0?[1-9]|1[0-2])$",
    ),
    hhmm: str = Query(
        ..., min_length=4, max_length=5, regex=r"^(0?[1-9]|1[0-2]):[0-5][0-9]$"
    ),
):
    return {"hh": hh, "hhmm": hhmm}


@router.get("/titanic/", summary="Query parameter list / multiple value")
def show_titanic(
    actors: Optional[list[str]] = Query(None),
    roles: list[str] = Query(["Jack", "Rose"]),
):
    return {"actors": actors, "roles": roles}


@router.get("/schindler/", summary="Query parameter with metadata")
def get_schindler_list(
    name: Optional[str] = Query(
        None,
        title="name of Jew",
        description="The name of Jew which is choosen by Schindler",
        min_length=3,
    )
):
    return {"name": name}


@router.get("/inception/", summary="Alias query parameter")
def show_inception(
    ring: str = Query("darry ring", alias="wedding-ring"),
):
    return {"ring": ring}


@router.get("/hachi/", summary="Deprecated query parameter")
def get_tale_of_hachi(
    professor: Optional[str] = Query(None, deprecated=True),
):
    return {"professor": professor}
