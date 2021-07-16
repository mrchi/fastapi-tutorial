# coding=utf-8

from fastapi import FastAPI, Depends
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from tutorial.api import (
    dependencies,
    errors,
    path_params,
    query_params,
    request_body,
    example_declaration,
    security,
    status_code,
    validation,
    header_params,
    response_model,
    extra_models,
    form_and_files,
    path_configuration_operation,
    body_updates,
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
