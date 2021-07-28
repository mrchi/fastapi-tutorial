# coding=utf-8

from fastapi import APIRouter, Response

router = APIRouter()


@router.get("/cookie", summary="Use a Response parameter to set cookie")
def response_param_to_set_cookie(resp: Response):
    resp.set_cookie("fakesession", "fake-cookie-session-value")
    return {"message": "we have cookies"}


@router.get("/header", summary="Use a Response parameter to set header")
def response_param_to_set_header(resp: Response):
    resp.headers["x-cat"] = "captain"
    return {"message": "we have headers"}


@router.get("/statuscode", summary="Use a Response parameter to set status code")
def response_param_to_set_status_code(resp: Response):
    resp.status_code = 418
    return {"message": "I'm a teapot"}
