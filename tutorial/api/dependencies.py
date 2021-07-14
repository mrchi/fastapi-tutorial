# coding=utf-8

from typing import Optional
from fastapi import APIRouter, Depends, Cookie

router = APIRouter()


async def common_parameters(q: Optional[str] = None, limit: int = 10, offset: int = 10):
    return {"q": q, "limit": limit, "offset": offset}


async def more_common_parameters(
    commons: dict = Depends(common_parameters), last_query: Optional[str] = Cookie(None)
):
    return {"commons": commons, "last_query": last_query}


def fresh_common_parameters(
    commons: dict = Depends(common_parameters, use_cache=False)
):
    return commons


class CommonParams:
    def __init__(self, q: Optional[str] = None, limit: int = 10, offset: int = 10):
        self.q = q
        self.limit = limit
        self.offset = offset


@router.get("/loveletter/", summary="Functions as dependencies")
def love_letter(commons: dict = Depends(common_parameters)):
    return commons


@router.get("/contratiempo/", summary="Classes as dependencies")
def contratiempo(commons: CommonParams = Depends(CommonParams)):
    return commons


@router.get("/stripedpajamas/", summary="Shortcuts of classes as dependencies")
def striped_pajamas(commons: CommonParams = Depends()):
    return commons


@router.get("/malena/", summary="Sub dependencies")
def malena(more_commons: dict = Depends(more_common_parameters)):
    return more_commons


@router.get(
    "/savingprivateryan/",
    summary="Disable cache when using the same dependency multiple times",
)
def save_private_ryan(commons: dict = Depends(fresh_common_parameters)):
    return commons
