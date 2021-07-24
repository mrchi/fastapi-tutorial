# coding=utf-8

from fastapi import APIRouter

router = APIRouter()


@router.get("/operationid", operation_id="ohhhhhh", summary="Custom operation id")
def operation_id():
    return {"msg": "What is the use of operation id?"}


@router.get("/operationid2", summary="Use path operation function name as operation id")
def operation_id2():
    return {"msg": "You can see the route.operation_id is route.name if you debug."}


def use_path_operation_function_name_as_operation_id(router: APIRouter):
    for route in router.routes:
        if not route.operation_id:
            route.operation_id = route.name


# This function runs after path operation functions definition.
use_path_operation_function_name_as_operation_id(router)


@router.get("/exclude", include_in_schema=False, summary="Exclude route in OpenAPI")
def exclude():
    return {"msg": "This API will not shown in OpenAPI and docs."}


@router.get("/docstring", summary="Advanced description in docstring")
def docstring():
    """
    This part will shown up in docs.
    \f
    This part won't shown up in docs.
    """
    return {"msg": "Check the docstring of path operation function."}
