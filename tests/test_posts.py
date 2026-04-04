from typing import List

import pytest

from app import schemas


def test_get_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")

    def validate(post):
        return schemas.PostOut(**post)

    posts_map = map(validate, res.json())
    posts_list = list(posts_map)

    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200


def test_unauthorized_user_get_posts(client, test_posts):
    res = client.get("/posts/")

    assert res.status_code == 200


def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")

    assert res.status_code == 200


def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get("/posts/88888")

    assert res.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())

    assert res.status_code == 200
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert post.Post.title == test_posts[0].title


@pytest.mark.parametrize("title, content, published", [
    ("awesome new title", "awesome new content", True),
])
def test_create_post(authorized_client, test_user, title, content, published):
    # Если в схеме PostCreate есть category_id, добавь его сюда
    payload = {"title": title, "content": content, "published": published}
    
    res = authorized_client.post("/posts/", json=payload)

    # Если тут упадет — в консоли будет написано, какой статус пришел (скорее всего 422)
    assert res.status_code == 201 
    
    # Если твой API возвращает сложную структуру (с votes), используй PostOut
    # Если чистый пост — используй свою модель для вывода (например PostResponse)
    created_post = schemas.PostResponse(**res.json()) 

    assert created_post.title == title
    assert created_post.owner_id == test_user['id']