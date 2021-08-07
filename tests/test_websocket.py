# coding=utf-8

import pytest
from fastapi import WebSocketDisconnect
from fastapi.testclient import TestClient


def test_websocket(client: TestClient):
    with pytest.raises(WebSocketDisconnect):
        with client.websocket_connect("/websockets/foo/ws") as ws:
            ws.send_text("hello")

    token = "alpha"
    with client.websocket_connect(f"/websockets/foo/ws?token={token}") as ws:
        ws.send_text("hello")
        assert ws.receive_text() == f"Session cookie or query token value is: {token}"
        assert ws.receive_text() == "Message text was: hello, for item ID: foo"
