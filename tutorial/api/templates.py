# coding=utf-8

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse

router = APIRouter()
tpls = Jinja2Templates(directory="tutorial/templates")


@router.get("/hello", response_class=HTMLResponse, summary="Render jinja2 templates")
async def hello(request: Request):
    return tpls.TemplateResponse("hello.html", {"request": request, "id": 3})
