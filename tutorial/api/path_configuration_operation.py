# coding=utf-8

from fastapi import APIRouter

router = APIRouter()


@router.get(
    "/eatdrinkmenwomen/",
    summary="Path Operation Configuration",
    tags=["Path Operation Configuration"],
    response_description="This is a response descrition.",
    deprecated=True,
)
def eat_drink_men_women(name: str = "abc"):
    """This is a description from docstring, and it supports **markdown**."""
    return {"name": name}
