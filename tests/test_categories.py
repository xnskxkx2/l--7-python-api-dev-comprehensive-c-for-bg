import pytest

from app import models

def test_create_category(authorized_client):
    res = authorized_client.post(
        "/categories/", json={"name": "Test Category"}
    )
    assert res.status_code == 201
    assert res.json()["name"] == "Test Category"