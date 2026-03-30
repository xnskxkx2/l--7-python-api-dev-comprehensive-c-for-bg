import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app import schemas
from app.config import settings
from app.database import Base, get_db
from app.main import app

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:12345@172.26.112.1:5432/fastapi_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)

def test_root(client):
    res = client.get("/")
    print(res.json())
    assert res.json() == {"message": "It's a bad day today"}
    assert res.status_code == 200


def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "test_user123_1@gmail.com", "password": "12345"}
    )

    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "test_user123_1@gmail.com"
    assert res.status_code == 201


def test_get_user(client):
    # create user first
    res = client.post(
        "/users/",
        json={"email": "test_user123_1@gmail.com", "password": "12345"},
    )

    user = res.json()

    # then fetch the user
    res = client.get(f"/users/{user['id']}")

    assert res.status_code == 200
    assert res.json()["id"] == user["id"]
