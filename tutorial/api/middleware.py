# coding=utf-8

import time
from fastapi import Request, APIRouter
from fastapi.param_functions import Header

router = APIRouter()


# See app.add_middleware() in tutorial.app
# @app.middleware('http')
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@router.get("/http_middleware/", summary="Custom HTTP middleware example")
def middleware_example():
    return {"msg": "Check X-Process-Time header."}


@router.get(
    "/cors/",
    summary="CORS middleware example",
    description=(
        "See tutorial.app. "
        "request with header is incorrect in swagger UI, "
        "Test with [amis](https://baidu.github.io/amis/zh-CN/components/crud)"
    ),
)
def cors_example(origin: str = Header(...)):
    return {
        "msg": "Check response header access-control-allow-*",
        "origin": origin,
    }
