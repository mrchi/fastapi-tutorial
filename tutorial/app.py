# coding=utf-8

from fastapi import FastAPI

from tutorial.api import (
    path_params,
    query_params,
    request_body,
    example_declaration,
    validation,
)

app = FastAPI(
    title="FastAPI Tutorial",
    description="A FastAPI application written by following tutorial in FastAPI Documents.",
    openapi_url="/help/v1/openapi.json",
    docs_url="/help/docs",
    redoc_url="/help/redoc",
)


@app.get("/", tags=["Index"], summary="Hello, world!")
async def index():
    return {"hello": "world"}


app.include_router(path_params.router, prefix="/pathparams", tags=["Path Params"])
app.include_router(query_params.router, prefix="/queryparams", tags=["Query Params"])
app.include_router(request_body.router, prefix="/requestbody", tags=["Request Body"])
app.include_router(
    example_declaration.router,
    prefix="/example",
    tags=["Example Declaration"],
)
app.include_router(validation.router, prefix="/validation", tags=["Validation"])
