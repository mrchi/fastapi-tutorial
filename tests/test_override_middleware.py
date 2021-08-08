# coding=utf-8

from typing import Optional
from tutorial.app import app
from tutorial.api.dependencies import common_parameters, CommonParams


def fake_common_parameters(q: Optional[str] = None):
    return {"q": q, "limit": 22, "offset": 33}


def test_override_function_middleware(client):
    app.dependency_overrides[common_parameters] = fake_common_parameters

    resp = client.get("/dependencies/loveletter")
    assert resp.json() == {"q": None, "limit": 22, "offset": 33}

    resp = client.get("/dependencies/loveletter", params={"q": "foo", "limit": 11})
    assert resp.json() == {"q": "foo", "limit": 22, "offset": 33}

    app.dependency_overrides = {}
    resp = client.get("/dependencies/loveletter")
    assert resp.json() == {"q": None, "limit": 10, "offset": 10}


def test_override_class_middleware(client):
    app.dependency_overrides[CommonParams] = fake_common_parameters

    resp = client.get("/dependencies/contratiempo")
    assert resp.json() == {"q": None, "limit": 22, "offset": 33}
