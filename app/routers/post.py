from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from .. import models, oauth2, schemas
from ..database import get_db

router = APIRouter(prefix="/posts", tags=["Posts"])


# --- СОЗДАНИЕ ПОСТА ---
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # cursor.execute(
    #     """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    #     (post.title, post.content, post.published),
    # )
    # new_post = cursor.fetchone()
    # conn.commit()
    print(current_user.email)
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


# --- ПОЛУЧЕНИЕ ВСЕХ ПОСТОВ ---
# @router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.PostOut])
async def get_posts(
    db: Session = Depends(get_db),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()

    # posts = (
    #     db.query(models.Post)
    #     .filter(models.Post.title.contains(search)).offset(skip).limit(limit).all()
    # )

    # В твоем запросе в post.py
    posts = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes")) # Поменяй post_votes на votes
        .join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.title.contains(search)).offset(skip).limit(limit).all()
    )

    return posts


# --- ПОЛУЧЕНИЕ ОДНОГО ПОСТА ---
# @router.get("/{post_id}", response_model=schemas.Post)
@router.get("/{post_id}", response_model=schemas.PostOut)
async def get_post(
    post_id: int, db: Session = Depends(get_db)
):  # FastAPI сам сконвертирует post_id в int
    # Используем кортеж (post_id,) — запятая обязательна для одного элемента!
    
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (post_id,))
    # post = cursor.fetchone()
    # post = db.query(models.Post).filter(models.Post.id == post_id).first()

    post = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True)
        .filter(models.Post.id == post_id)  # <--- ВОТ ЭТОТ ФИКС
        .group_by(models.Post.id)
        .first()
    )
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {post_id} was not found",
        )

    return post


# --- УДАЛЕНИЕ ПОСТА ---
@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # Пытаемся удалить и вернуть удаленную запись, чтобы проверить, была ли она
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (post_id,))
    # deleted_post = cursor.fetchone()
    post_query = db.query(models.Post).filter(models.Post.id == post_id)

    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {post_id} doesn't exist",
        )
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    post_query.delete(synchronize_session=False)
    db.commit()
    # conn.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# --- ОБНОВЛЕНИЕ ПОСТА ---
@router.put("/{post_id}", response_model=schemas.Post)
async def update_post(
    post_id: int,
    updated_post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # cursor.execute(
    #     """UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #     (post.title, post.content, post.published, post_id),
    # )
    # updated_post = cursor.fetchone()
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {post_id} doesn't exist",
        )
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    # conn.commit()

    return post_query.first()
