# coding=utf-8

from fastapi import FastAPI, Depends
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.gzip import GZipMiddleware

# from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware

from tutorial.api import (
    additional_response,
    apirouter_sub_include,
    background_task,
    custom_response,
    dependencies,
    errors,
    middleware,
    path_operation_advanced_configuration,
    path_params,
    query_params,
    request_body,
    example_declaration,
    request_object,
    response_parameter,
    return_response,
    security,
    security_jwt,
    status_code,
    use_dataclasses,
    validation,
    header_params,
    response_model,
    extra_models,
    form_and_files,
    path_configuration_operation,
    body_updates,
)

# The order of each tag metadata dictionary also defines the order shown in the docs UI.
tags_metadata = [
    {
        "name": "Index",
        "description": "Index page description, defined by `FastAPI.openapi_tags`.",
        "externalDocs": {
            "description": "External FastAPI Docment",
            "url": "https://fastapi.tiangolo.com",
        },
    }
]

app = FastAPI(
    title="FastAPI Tutorial",
    description="A FastAPI application written by following tutorial in FastAPI Documents.",
    version="0.1.0",
    openapi_url="/help/v1/openapi.json",
    docs_url="/",
    redoc_url=None,  # disabled
    openapi_tags=tags_metadata,
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
app.include_router(header_params.router, prefix="/header", tags=["Header Params"])
app.include_router(
    response_model.router, prefix="/responsemodel", tags=["Response Model"]
)
app.include_router(extra_models.router, prefix="/extramodels", tags=["Extra Models"])
app.include_router(status_code.router, prefix="/statuscode", tags=["Status Code"])
app.include_router(
    form_and_files.router, prefix="/formandfiles", tags=["Form and Files"]
)
app.include_router(errors.router, prefix="/errors", tags=["Handle Errors"])
app.include_router(path_configuration_operation.router, prefix="/pathconfigops")
app.include_router(
    body_updates.router, prefix="/updatebody", tags=["Jsonable encoder and update body"]
)
app.include_router(dependencies.router, prefix="/dependencies", tags=["Dependencies"])
app.include_router(
    dependencies.global_dependency_router,
    prefix="/globaldependencies",
    dependencies=[Depends(dependencies.verify_token)],
    tags=["Dependencies"],
)
app.include_router(security.router, prefix="/security", tags=["Security"])
app.include_router(
    security_jwt.router, prefix="/securityjwt", tags=["JWT Security Example"]
)
app.include_router(middleware.router, prefix="/middleware", tags=["Middleware"])

# Make sure you do it before including router in the FastAPI app
# so that the path operations from other_router are also included
# https://fastapi.tiangolo.com/tutorial/bigger-applications/
apirouter_sub_include.router.include_router(
    apirouter_sub_include.sub_router, prefix="/subrouter"
)
app.include_router(
    apirouter_sub_include.router, prefix="/router", tags=["APIRouter sub include"]
)

app.include_router(
    background_task.router, prefix="/backgroundtask", tags=["Background Task"]
)
app.include_router(
    path_operation_advanced_configuration.router,
    prefix="/pathoperationadvancedconf",
    tags=["Path operation advanced configuration"],
)
app.include_router(
    return_response.router, prefix="/returnresp", tags=["Return Responses Directly"]
)
app.include_router(
    custom_response.router, prefix="/customresp", tags=["Custom Responses"]
)
app.include_router(
    additional_response.router, prefix="/additionalresp", tags=["Additional Response"]
)
app.include_router(
    response_parameter.router, prefix="/responseparam", tags=["Response parameter"]
)
app.include_router(request_object.router, prefix="/request", tags=["Request object"])
app.include_router(
    use_dataclasses.router, prefix="/dataclasses", tags=["Use dataclasses"]
)

app.add_exception_handler(errors.WestWorldException, errors.westworld_exception_handler)

# Override the default error handlers
# Override the default request validation handler, use fastapi.exceptions.RequestValidationError
# https://fastapi.tiangolo.com/tutorial/handling-errors/#requestvalidationerror-vs-validationerror
app.add_exception_handler(
    RequestValidationError, errors.request_validation_error_handler
)

# Override the default http exception handler, use starlette.exceptions.HTTPException
# https://fastapi.tiangolo.com/tutorial/handling-errors/#fastapis-httpexception-vs-starlettes-httpexception
app.add_exception_handler(StarletteHTTPException, errors.http_exception_handler)

app.add_middleware(BaseHTTPMiddleware, dispatch=middleware.add_process_time_header)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://baidu1234.github.io"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["localhost"])
app.add_middleware(GZipMiddleware, minimum_size=10)
# app.add_middleware(HTTPSRedirectMiddleware)

app.mount("/static", StaticFiles(directory="tutorial/static"), name="static")
