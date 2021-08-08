# coding=utf-8

from fastapi.testclient import TestClient
from tutorial.app import app


def test_startup_event_handler(capsys):
    # Don't use client defined by conftest
    # Because client startup and shutdown is in fixture function
    with TestClient(app) as client:
        client.get("/")
        stdout = capsys.readouterr().out
        assert "App startup and say hello." in stdout
        assert "App startup and say world." in stdout


def test_shutdown_event_handler(capsys):
    # Don't use client defined by conftest
    # Because client startup and shutdown is in fixture function
    with TestClient(app) as client:
        client.get("/")
    stdout = capsys.readouterr().out
    assert "App shutdown." in stdout
