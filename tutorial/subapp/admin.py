# coding=utf-8

from fastapi import FastAPI

admin_app = FastAPI(
    title="Admin subapp",
    description="APIs in subapp won't occured in docs of top-level application.",
    docs_url="/",
)


@admin_app.get("/wow", summary="Amazing sub-application")
def foo():
    return {"msg": "This is an API defined by admin subapp."}
