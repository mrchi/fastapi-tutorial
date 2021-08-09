# coding=utf-8

import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient

from tutorial.app import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
@pytest.mark.asyncio
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def access_token(client):
    resp = client.post(
        "/securityjwt/token",
        data={"username": "johndoe", "password": "secret"},
    )
    # assert resp.status_code == 200
    # assert 'access_token' in resp.json()
    # assert resp.json()['token_type'] == 'bearer'
    return resp.json()["access_token"]
