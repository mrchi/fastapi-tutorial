# coding=utf-8

from typing import Optional
from fastapi import APIRouter
from pydantic import HttpUrl


router = APIRouter()
callback_router = APIRouter()


@callback_router.post(
    "{$callback_url}/invoices/{$request.body.id}",
    summary="Callback APIRouter",
    description="CAN NOT be run in docs.",
)
def callback_func():
    pass


@router.get(
    "/dosomething",
    callbacks=callback_router.routes,
    summary="Just do sth and trigger callback",
)
def do_some_thing(callback_url: Optional[HttpUrl] = None):
    return {"hello": "world"}
