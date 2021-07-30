# coding=utf-8

from fastapi import APIRouter
from fastapi.requests import Request

router = APIRouter()


@router.get("/req", summary="Use Request object directly")
def req(req: Request):
    return {"client_host": req.client.host}
