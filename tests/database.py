from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db
from app.schemas import UserResponse
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
import pytest

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
