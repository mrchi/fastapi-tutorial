# coding=utf-8

from typing import Optional
from fastapi import APIRouter, Depends, Cookie, Header, HTTPException

router = APIRouter()
global_dependency_router = APIRouter()


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


def verify_key(x_key: str = Header(...)):
    if x_key != "fake_x_key":
        raise HTTPException(status_code=400, detail="X-Key header is invalid")


def verify_token(x_token: str = Header(...)):
    if x_token != "fake_x_token":
        raise HTTPException(status_code=400, detail="X-Token header is invalid")


def get_db():
    print("get_db.start")
    db = "DBConn"
    print("get_db.yield")
    yield db
    print("get_db.end")


def get_db_with_try():
    print("get_db_with_try.start")
    db = "DBConn"
    # Don't write except block, so Exception could be raised.
    try:
        raise ValueError("get_db_with_try.ValueError before try")
        print("get_db_with_try.yield")
        yield db
    finally:
        print("get_db_with_try.finally")


def get_db_with_http_exception():
    print("get_db_with_try.start")
    db = "DBConn"
    try:
        print("get_db_with_try.yield")
        yield db
    finally:
        # raise HTTPException in finally is useless, because response already returned.
        print("get_db_with_try.finally")
        raise HTTPException(404)


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


@router.get(
    "/thesoundofmusic/",
    dependencies=[Depends(verify_key), Depends(verify_token)],
    summary="Dependencies in path operation decorators",
)
def the_sound_of_music():
    return {"foo": "bar"}


@global_dependency_router.get(
    "/avatar/",
    summary="Global Dependencies",
    description="See `app.include_router(dependencies=[...])` in `tutorial.app`, or you can use `FastApi(dependencies=[...])`",
)
def avatar():
    return {"foo": "bar"}


@router.get("/thecove/", summary="Dependencies with yield")
def the_cove(db: str = Depends(get_db)):
    print("the_cove.start")
    print(f"the_cove.db: {db}")
    print("the_cove.end")
    return {"db": db}


@router.get("/theprestige/", summary="Dependencies with yield and try")
def the_prestige(db: str = Depends(get_db_with_try)):
    print("the_prestige.start")
    print(f"the_prestige.db: {db}")
    print("the_prestige.end")
    return {"db": db}


@router.get("/lambs", summary="Sub dependencies with yield and HTTPException")
def lambs(db: str = Depends(get_db_with_http_exception)):
    print("lambs.start")
    print(f"lambs.db: {db}")
    print("lambs.end")
    return {
        "db": db,
        "msg": "It's useless to raise HTTPException after yield in dependencies.",
    }
