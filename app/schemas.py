from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field
from pydantic.types import conint


class PostBase(BaseModel):
    title: str
    content: Optional[str] = None
    published: bool = True


class PostCreate(PostBase):
    owner_id: int
    category_id: int
    pass


class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    pass

class CategoryOut(BaseModel):
    id: int
    name: str
    created_at: datetime

    class Config:
        from_attributes = True # Для Pydantic v2 (или orm_mode = True для v1)

class UserOut(BaseModel):
    id: int
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    category: CategoryOut

    class Config:
        from_attributes = True

# Правильный вариант
class PostOut(BaseModel):
    Post: Post  # Это вложенная схема со всеми полями поста
    votes: int  # Это наше число голосов

    class Config:
        from_attributes = True # Для Pydantic v2 (или orm_mode = True для v1)


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(max_length=10)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
