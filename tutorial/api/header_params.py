# coding=utf-8

from typing import Optional
from fastapi import APIRouter, Cookie, Header

router = APIRouter()


@router.get(
    "/dangal/",
    summary="Cookie parameter",
    description="Request is incorrect in swagger UI.",
)
def dangal(uid: Optional[str] = Cookie(None)):
    return {"uid": uid}


@router.get(
    "/lifeofpi/",
    summary="Header parameter",
    description="Request is incorrect in swagger UI.",
)
def life_of_pi(
    user_agent: Optional[str] = Header(None),
    strange_header: Optional[str] = Header(None, convert_underscores=False),
    x_token: Optional[list[str]] = Header(None),
):
    return {
        "user_agent": user_agent,
        "strange_header": strange_header,
        "x_token": x_token,
    }
