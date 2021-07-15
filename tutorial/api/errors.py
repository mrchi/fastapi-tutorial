# coding=utf-8

from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException, RequestValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


router = APIRouter()


class WestWorldException(Exception):
    def __init__(self, name: str) -> None:
        self.name = name


def westworld_exception_handler(request: Request, exc: WestWorldException):
    return JSONResponse(
        status_code=418,
        content={"message": f"{exc.name} is a Teapot."},
    )


def request_validation_error_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={
            "attention": "This is returned by custom handler in tutorial.api.errors",
            "detail": exc.errors(),
            "body": exc.body,  # only JSON body
        },
    )


def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "confused": exc.detail,
        },
        headers=getattr(exc, "headers", {})
        or {}
        | {
            "X-Info": "This is returned by custom handler in tutorial.api.errors",
        },
    )


@router.get("/teapot/", summary="Raise HTTPException")
def teapot():
    raise HTTPException(
        status_code=status.HTTP_418_IM_A_TEAPOT,
        detail={"msg": "I'am a teapot."},
        headers={"X-Error": "A teapot!"},
    )


@router.get(
    "/deadpoetssociety/",
    summary="Custom exception handler",
    description="Error handler function is defined in `tutorial.app`.",
)
def dead_poets_society(name: str):
    raise WestWorldException(name)


@router.get(
    "/fightclub/",
    summary="Override request validation error by fastapi.exceptions.RequestValidationError",
    description="Visit [this link](/errors/fightclub/?name=abc) to test.",
)
def fight_club(name: int = "abc"):
    return {"name": name}


@router.get(
    "/thematrix/",
    summary="Override http exception by starlette.exceptions.HTTPException",
)
def the_matrix():
    raise HTTPException(
        status_code=status.HTTP_418_IM_A_TEAPOT,
        detail={"msg": "I'm a teapot."},
        headers={"X-Flag": "Set by API handler"},
    )


@router.get(
    "/greenbook/",
    summary="Re-use FastAPI's exception handlers",
    description="Not a example API, but just show the handlers' path in response.",
)
def green_book():
    return {
        "http_exception": "fastapi.exception_handlers.http_exception_handler(request, exc)",
        "request_validation_error": "fastapi.exception_handlers.request_validation_exception_handler(request, exc)",
    }
