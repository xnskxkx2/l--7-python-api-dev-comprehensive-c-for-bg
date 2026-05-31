import pytest
from jose import jwt

from app import schemas
from app.config import settings

# def test_root(client):
#     res = client.get("/")
#     print(res.json())
#     assert res.json() == {"message": "It's a bad day today"}
#     assert res.status_code == 200


def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "test_user123_1@gmail.com", "password": "12345"}
    )

    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "test_user123_1@gmail.com"
    assert res.status_code == 201


def test_login_user(client, test_user):
    res = client.post(
        "/login",
        data={"username": test_user["email"], "password": test_user["password"]},
    )

    login_res = schemas.Token(**res.json())
    payload = jwt.decode(
        login_res.access_token, settings.secret_key, algorithms=[settings.algorithm]
    )
    user_id = payload.get("user_id")

    assert user_id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("wrongemail@gmail.com", "password123", 401),
        ("sanjeev@gmail.com", "wrongpassword", 401),
        ("wrongemail@gmail.com", "wrongpassword", 401),
        (None, "password123", 422),
        ("sanjeev@gmail.com", None, 422),
    ],
)
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})

    assert res.status_code == status_code
    # assert res.json().get("detail") == "Incorrect email or password"


def test_get_user(client, test_user):  # Добавили фикстуру test_user
    # Теперь юзер УЖЕ создан фикстурой. Просто запрашиваем его.
    res = client.get(f"/users/{test_user['id']}")

    assert res.status_code == 200
    assert res.json()["id"] == test_user["id"]
    assert res.json()["email"] == test_user["email"]
