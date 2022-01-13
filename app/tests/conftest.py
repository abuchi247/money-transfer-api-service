import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.session import get_db, Base
from app.db import models
from app.config import settings
from app.core.oauth2 import create_access_token

# SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# # create all the tables needed
# Base.metadata.create_all(bind=engine)


# Dependency
# def override_get_db():
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# app.dependency_overrides[get_db] = override_get_db


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


# @pytest.fixture
# def client(session):
#     # run our code before we run our test
#     Base.metadata.drop_all(bind=engine)  # drop all tables
#     Base.metadata.create_all(bind=engine)  # create my tables
#     # command.downgrade("base") # using alembic
#     # command.upgrade("head")
#     yield TestClient(app)
#     # run our code after our test finishes
#     # Base.metadata.drop_all(bind=engine)  # drop all tables


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
def test_regular_user(client, session):
    user_data = {
        "email": "test@regular.com",
        "password": "test"
    }

    new_user = models.User(**user_data)

    # create a new user in the database
    session.add(new_user)

    # commit user to db
    session.commit()

    return session.query(models.User).all()


@pytest.fixture
def test_admin_user(client, session):
    user_data = {
        "email": "test@admin.com",
        "password": "test",
        "role": "admin"
    }
    new_user = models.User(**user_data)

    # create a new user in the database
    session.add(new_user)

    # commit user to db
    session.commit()

    return session.query(models.User).all()


@pytest.fixture
def token_regular(test_regular_user):
    return create_access_token({"user_id": test_regular_user['id']})


@pytest.fixture
def token_admin(test_admin_user):
    return create_access_token({"user_id": test_admin_user['id']})


@pytest.fixture
def authorized_client(client, token):
    # adding token to the client headers
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client
