# coding=utf-8

import pathlib

from fastapi import APIRouter
from fastapi.responses import (
    ORJSONResponse,
    HTMLResponse,
    PlainTextResponse,
    UJSONResponse,
    RedirectResponse,
    StreamingResponse,
    FileResponse,
)

router = APIRouter(default_response_class=PlainTextResponse)
html_string = """\
<html>
    <head>
    </head>
    <body>
        <h1>Hello World</h1>
    </body>
</html>
"""
binary_file_path = pathlib.Path(__file__).parents[1] / "static" / "atom.png"


@router.get("/orjson", response_class=ORJSONResponse, summary="Custom ORJSONResponse")
async def orjson_response():
    return [{"item_id": "Foo"}]


@router.get("/html", response_class=HTMLResponse, summary="Custom HTMLResponse")
async def html_response():
    return html_string


@router.get(
    "/plaintext", response_class=PlainTextResponse, summary="Custom PlainTextResponse"
)
async def plaintext_response():
    return "Hello, world!"


@router.get("/ujson", response_class=UJSONResponse, summary="Custom UJSONResponse")
async def ujson_response():
    return [{"item_id": "Foo"}]


@router.post(
    "/redirect",
    response_class=RedirectResponse,
    summary="Custom RedirectResponse(default: 307)",
    description="307, keep request http method.",
)
def redirect():
    return "https://httpbin.org/anything"


@router.post(
    "/redirect302",
    response_class=RedirectResponse,
    status_code=302,
    summary="Custom RedirectResponse(302)",
    description="302, change request http method to get.",
)
def redirect302():
    return "https://httpbin.org/anything"


@router.get(
    "/stream", response_class=StreamingResponse, summary="Custom StreamingResponse"
)
def stream_response():
    def fake_stream_data():
        with open(binary_file_path, "rb") as f:
            yield from f

    return StreamingResponse(fake_stream_data())


@router.get("/file", response_class=FileResponse, summary="Custom FileResponse")
def file_response():
    return binary_file_path


@router.get(
    "/default", summary="Default Response class", description="See router defination"
)
def default_response_class():
    return "Hello, world!"
