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
    pass


class UserOut(BaseModel):
    id: int
    email: str
    created_at: datetime

    class Config:
        orm_mode = True


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True


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
