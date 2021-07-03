# coding=utf-8

from fastapi import FastAPI

from tutorial.api import path_params

app = FastAPI(
    title="FastAPI Tutorial",
    description="A FastAPI application written by following tutorial in FastAPI Documents.",
    openapi_url="/help/v1/openapi.json",
    docs_url="/help/docs",
    redoc_url="/help/redoc",
)

app.include_router(path_params.router, prefix="/pathparams", tags=["Path Params"])


@app.get("/", tags=["Index"])
async def index():
    "Hello, world!"
    return {"hello": "world"}
