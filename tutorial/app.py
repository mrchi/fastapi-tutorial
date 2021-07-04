# coding=utf-8

from fastapi import FastAPI

from tutorial.api import path_params, query_params

app = FastAPI(
    title="FastAPI Tutorial",
    description="A FastAPI application written by following tutorial in FastAPI Documents.",
    openapi_url="/help/v1/openapi.json",
    docs_url="/help/docs",
    redoc_url="/help/redoc",
)

app.include_router(path_params.router, prefix="/pathparams", tags=["Path Params"])
app.include_router(query_params.router, prefix="/queryparams", tags=["Query Params"])


@app.get("/", tags=["Index"], summary="Hello, world!")
async def index():
    return {"hello": "world"}
