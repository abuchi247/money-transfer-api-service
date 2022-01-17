import pytest
from jose import jwt
from app import schemas
from app.config import settings


# @pytest.mark.parametrize("email, password, status_code", [
#     ('hello123@gmail.com', 'password123', 201),
#     ('test@example.com', 'test2', 201),
#     ('email@gmail.com', 'test123', 201)
# ])
# def test_create_user(client, email, password, status_code):
#     res = client.post("/users/", json={"email": email, "password": password})
#     new_user = schemas.ShowUser(**res.json())  # validate response schema
#     print(new_user)
#     assert new_user.email == email
#     assert res.status_code == status_code
#
#
# def test_fail_create_user(client, test_regular_user):
#     user_data = {'email': 'test@regular.com', 'password':'password123'}
#     res = client.post("/users/", json=user_data)
#     assert res.status_code == 400
#
#
# def test_regular_login(client, test_regular_user):
#     data = {
#         "username": test_regular_user['email'],
#         "password": "test"
#     }
#     res = client.post("/login", data=data)
#
#     login_res = schemas.Token(**res.json())
#     # decode token
#     payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
#     #
#     user_id = payload.get("user_id")
#     assert user_id == test_regular_user['id']
#     assert login_res.token_type == 'bearer'
#     assert res.status_code == 200
#
#
# @pytest.mark.parametrize("email, password, status_code", [
#     ('wrongemail@gmail.com', 'password123', 401),
#     ('test@example.com', 'test2', 401),
#     ('wrongemail@gmail.com', 'wrongPassword', 401),
#     (None, 'wrongPassword', 422),
#     ('wrongemail@gmail.com', None, 422),
# ])
# def test_incorrect_login(client, email, password, status_code):
#     res = client.post("/login", data={"username": email, "password": password})
#     assert res.status_code == status_code
#
#
# def test_admin_list_users(authorized_admin_client, test_multiple_users):
#     res = authorized_admin_client.get("/users")
#     assert res.status_code == 200
#
#
# def test_unauthorized_list_users(authorized_regular_client, test_multiple_users):
#     res = authorized_regular_client.get("/users")
#     assert res.status_code == 403
#
#
# def test_admin_get_user(authorized_admin_client, test_multiple_users):
#     user_to_retrieve = test_multiple_users[len(test_multiple_users)-1]
#     res = authorized_admin_client.get(f"/users/{user_to_retrieve.id}")
#     assert res.status_code == 200
#     assert res.json()['id'] == user_to_retrieve.id
#     assert res.json()['email'] == user_to_retrieve.email
#
#
# def test_current_user_own_user(authorized_regular_client):
#     res = authorized_regular_client.get(f"/users/1")
#     assert res.status_code == 200
#     assert res.json()['id'] == 1
#
#
# def test_unauthorized_get_another_user(authorized_regular_client, test_multiple_users):
#     user_to_retrieve = test_multiple_users[len(test_multiple_users)-1]
#     res = authorized_regular_client.get(f"/users/{user_to_retrieve.id}")
#     assert res.status_code == 403
#
#
# def test_admin_get_user_non_exist(authorized_admin_client, test_multiple_users):
#     res = authorized_admin_client.get(f"/users/100000")
#     assert res.status_code == 404
#

def test_admin_update_user(authorized_admin_client, test_multiple_users):
    user_to_retrieve = test_multiple_users[len(test_multiple_users) - 1]
    update_user = {
        "email": "updateduser@example.com"
    }
    res = authorized_admin_client.put(f"/users/{user_to_retrieve.id}", json=update_user)

    assert res.status_code == 200
    assert res.json()['email'] == update_user['email']


def test_regular_update_own_user(authorized_regular_client, test_regular_user):
    update_user = {
        "email": f"updated{test_regular_user['email']}"
    }
    res = authorized_regular_client.put(f"/users/{test_regular_user['id']}", json=update_user)

    assert res.status_code == 200
    assert res.json()['email'] == update_user['email']


def test_unauthorized_update_user(authorized_regular_client, test_multiple_users):
    user_to_retrieve = test_multiple_users[len(test_multiple_users) - 1]
    update_user = {
        "email": "updateduser@example.com"
    }
    res = authorized_regular_client.put(f"/users/{user_to_retrieve.id}", json=update_user)

    assert res.status_code == 403
