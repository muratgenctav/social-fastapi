from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from pydantic.networks import EmailStr
from enum import IntEnum

from app.models import Post

class UserCreateRqst(BaseModel):
    email: EmailStr
    password: str

class UserCreateResp(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class UserGetResp(UserCreateResp):
    pass

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreateRqst(PostBase):
    pass

class PostCreateResp(PostBase):
    id: int
    created_at: datetime
    owner: UserCreateResp

    class Config:
        orm_mode = True

class PostGetResp(BaseModel):
    Post: PostCreateResp
    votes: int

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str]

class VoteDirEnum(IntEnum):
    unvote = 0
    vote = 1

class VoteRqst(BaseModel):
    post_id: int
    dir: VoteDirEnum