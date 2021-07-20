# coding=utf-8

from fastapi import APIRouter


router = APIRouter()
sub_router = APIRouter()


@router.get("/", summary="Router example")
def router_index():
    return {"msg": "This is router index."}


@sub_router.get("/", summary="Sub router example")
def sub_router_index():
    return {"msg": "This is sub router index."}
