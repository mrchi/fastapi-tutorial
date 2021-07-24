# coding=utf-8

from fastapi import APIRouter, status


router = APIRouter()


@router.get(
    "/themonkeyking",
    status_code=status.HTTP_418_IM_A_TEAPOT,
    summary="Custom status code",
)
def the_monkey_king():
    return {"foo": "bar"}
