import pytest
from jose import jwt
from app import schemas
from app.config import settings


def test_create_user(client):
    res = client.post("/users/", json={"email": "hello123@gmail.com", "password": "testing"})
    new_user = schemas.UserOut(**res.json())  # validate response schema
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201