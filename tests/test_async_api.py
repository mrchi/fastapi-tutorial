# coding=utf-8

import pytest


@pytest.mark.asyncio
async def test_orjson_response(async_client):
    resp = await async_client.get('/customresp/orjson')
    assert resp.status_code == 200
    assert resp.json() == [{"item_id": "Foo"}]
