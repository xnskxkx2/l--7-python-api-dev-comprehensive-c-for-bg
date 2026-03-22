from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from .. import models, oauth2, schemas
from ..database import get_db

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.CategoryOut
)
async def create_category(
    category: schemas.CategoryCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    new_category = models.Category(**category.model_dump())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category

# Получение всех категорий
@router.get("/", response_model=List[schemas.CategoryOut])
async def get_categories(
    db: Session = Depends(get_db),
):

    categories = (
        db.query(models.Category)
        .all()
    )

    return categories

# Получение всех постов категории
@router.get("/{category_id}/posts", response_model=List[schemas.Post])
async def get_category_posts(category_id: int, db: Session = Depends(get_db)):
    posts = db.query(models.Post).filter(models.Post.category_id == category_id).all()

    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id: {category_id} was not found",
        )

    return posts