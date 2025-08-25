from app import schemas
from .database import client, session


def test_root(client):
    res = client.get("/")
    print(res.json().get('message'))

    assert res.json().get('message') == "Hello world"


def test_create_user(client):
    res = client.post("/users", json={
        'email': "example@gmail.com",
        "password": "example123"
    })

    new_user = schemas.UserResponse(**res.json())

    # print(res.json())
    # assert res.status_code == 201

    assert new_user.email == 'example@gmail.com'


def test_login_user(client):
    res = client.post("/login", data={
        "username": "example@gmail.com",
        "password": "example123"
    })

    assert res.status_code == 200
