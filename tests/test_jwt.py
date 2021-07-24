# coding=utf-8


def test_login_protection(client, access_token):
    resp = client.get(
        "/securityjwt/users/me",
        data={"username": "johndoe", "password": "secret"},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert resp.status_code == 200
    assert resp.json() == {
        "username": "johndoe",
        "email": "johndoe@example.com",
        "fullname": "John Doe",
        "disabled": False,
    }
