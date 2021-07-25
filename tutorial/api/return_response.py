# coding=utf-8

from fastapi import APIRouter, status, Response
from fastapi.responses import JSONResponse
from fastapi.params import Body


router = APIRouter()

items = {
    "foo": {"name": "foo"},
}


@router.put(
    "/upsert/{item_id}",
    summary="Additional status code",
    description="It won't be included in the OpenAPI schema and docs.",
)
def upsert(item_id: str, name: str = Body(...)):
    if item_id in items:
        item = items[item_id]
        item["name"] = name
        return item
    else:
        item = {"name": name}
        items[item_id] = item
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=item)


@router.get("/xml", summary="Return xml response")
def get_xml_data():
    data = """<?xml version="1.0"?>
    <shampoo>
    <Header>
        Apply shampoo here.
    </Header>
    <Body>
        You'll have to use soap here.
    </Body>
    </shampoo>
    """
    return Response(content=data, media_type="application/xml")
