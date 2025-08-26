from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db
from app.schemas import UserResponse
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
import pytest
from app.oauth2 import create_access_token
from app import models

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}-test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
testing_session_local = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

# Base.metadata.create_all(bind=engine)


# def override_get_db():
#     db = testing_session_local()

#     try:
#         yield db
#     finally:
#         db.close()


# client = TestClient(app)

# with the session fixture we have access to our database object so we could manipulate with database data
@pytest.fixture()
def session():
    print("my session fixture ran")

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = testing_session_local()

    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    # return TestClient(app)
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    # yield is actually ~ to return but the code will run further with no breaking the function
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


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


@pytest.fixture
def test_user1(client):
    user_data = {
        "email": "example1@gmail.com",
        "password": "example1123"
    }

    res = client.post('/users', json=user_data)

    assert res.status_code == 201
    print(res.json())

    new_user = res.json()
    new_user['password'] = user_data["password"]

    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token(data={'user_id': test_user['id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        'Authorization': f"Bearer {token}"
    }

    return client


@pytest.fixture
def test_posts(test_user, session, test_user1):
    posts_data = [
        {
            "title": "title1",
            "content": "content1",
            "user_id": test_user["id"]
        },
        {
            "title": "title2",
            "content": "content2",
            "user_id": test_user["id"]
        },
        {
            "title": "title2",
            "content": "content2",
            "user_id": test_user["id"]
        },
        {
            "title": "title4",
            "content": "content4",
            "user_id": test_user1["id"]
        }
    ]

    # THIS IS THE HARDCODED WAY
    # session.add_all(
    #     [models.Post(title="title1", content="content2", owner_id=test_user["id"]),
    #      models.Post(title="title2", content="content3",
    #                  owner_id=test_user["id"]),
    #      models.Post(title="title3", content="content3", owner_id=test_user["id"])])

    def create_post_model(post):
        return models.Post(**post)

    # BUT WE COULD DO LIKE THIS USING MAP
    post_map = map(create_post_model, posts_data)
    posts = list(post_map)

    session.add_all(posts)

    session.commit()
    posts = session.query(models.Post).all()

    return posts
