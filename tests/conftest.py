# coding=utf-8

import pytest
from fastapi.testclient import TestClient

from tutorial.app import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def access_token(client):
    resp = client.post(
        "/securityjwt/token/",
        data={"username": "johndoe", "password": "secret"},
    )
    # assert resp.status_code == 200
    # assert 'access_token' in resp.json()
    # assert resp.json()['token_type'] == 'bearer'
    return resp.json()["access_token"]
