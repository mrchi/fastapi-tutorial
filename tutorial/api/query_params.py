# coding=utf-8

from typing import Optional
from fastapi import APIRouter


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
