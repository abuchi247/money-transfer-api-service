import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.session import get_db, Base
from app.db import models
from app.config import settings
from app.core.oauth2 import create_access_token
from app.db.repository.users import create_new_user, list_users
from app import schemas

# SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def session():
    print("my session fixture ran")
    Base.metadata.drop_all(bind=engine)  # drop all tables
    Base.metadata.create_all(bind=engine)  # create my tables
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def test_regular_user(session):
    user_data = {
        "email": "test@regular.com",
        "password": "test"
    }

    new_user = create_new_user(user=schemas.UserCreate(**user_data), db=session)
    return new_user.to_json()


@pytest.fixture
def test_admin_user(session):
    user_data = {
        "email": "test@admin.com",
        "password": "admin"
    }
    new_user = create_new_user(user=schemas.UserCreate(**user_data), db=session, is_superuser=True)
    return new_user.to_json()


@pytest.fixture
def test_multiple_users(session):
    users_data = [
        {
            "email": "user1@example.com",
            "password": "user1"
        },
        {
            "email": "user2@example.com",
            "password": "user2"
        },
        {
            "email": "user3@example.com",
            "password": "user3"
        },
        {
            "email": "user4@example.com",
            "password": "user4"
        }
    ]

    for user in users_data:
        # create a new user to the user
        create_new_user(user=schemas.UserCreate(**user),db=session)

    return list_users(db=session)


@pytest.fixture
def token_regular_user(test_regular_user):
    return create_access_token({"user_id": test_regular_user['id']})


@pytest.fixture
def token_admin_user(test_admin_user):
    return create_access_token({"user_id": test_admin_user['id']})


@pytest.fixture(scope="function")
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def authorized_regular_client(client, token_regular_user):
    # adding token to the client headers
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token_regular_user}"
    }
    return client


@pytest.fixture
def authorized_admin_client(client, token_admin_user):
    # adding token to the client headers
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token_admin_user}"
    }
    return client