# coding=utf-8

import time
from fastapi import Request, APIRouter

router = APIRouter()


# See app.add_middleware() in tutorial.app
# @app.middleware('http')
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@router.get("/", summary="Middleware example")
def middleware_example():
    return {"msg": "Check X-Process-Time header."}
