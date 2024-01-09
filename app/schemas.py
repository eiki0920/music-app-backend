from datetime import datetime

from pydantic import BaseModel

class PostBase(BaseModel):
    music: str
    image: str
    artist: str
    comment: str
    music_id: str
    pass

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    updated_at: datetime
    user_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    created_at: datetime
    is_active: bool
    hashed_password: str
    posts: list[Post] = []

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None