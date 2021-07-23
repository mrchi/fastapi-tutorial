# coding=utf-8


def test_index(client):
    """test index page."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
