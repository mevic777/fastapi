from app import schemas
from .database import client, session
import pytest
from jose import jwt
from app.config import settings


@pytest.fixture
def test_user(client):
    user_data = {
        "email": "example@gmail.com",
        "password": "example123"
    }

    res = client.post('/users', json=user_data)

    assert res.status_code == 201
    print(res.json())

    new_user = res.json()
    new_user['password'] = user_data["password"]

    return new_user


# def test_root(client):
#     res = client.get("/")
#     print(res.json().get('message'))

#     assert res.json().get('message') == "Hello world"


def test_create_user(client):
    res = client.post("/users", json={
        'email': "example@gmail.com",
        "password": "example123"
    })

    new_user = schemas.UserResponse(**res.json())

    # print(res.json())
    # assert res.status_code == 201

    assert new_user.email == 'example@gmail.com'


def test_login_user(client, test_user):
    res = client.post("/login", data={
        "username": test_user['email'],
        "password": test_user['password']
    })

    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token,
                         settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")

    assert id == test_user['id']
    assert login_res.token_type == 'bearer'
    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'example123', 403),
    ('example@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'example123', 403),
    ('example@gmail.com', None, 403)
])
def test_incorrect_login(client, test_user, email, password, status_code):
    res = client.post('/login', data={
        'username': email,
        'password': password
    })

    assert res.status_code == status_code
    # assert res.json().get('detail') == 'Invalid credentials'
