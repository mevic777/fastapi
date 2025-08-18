from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from typing import Optional
from datetime import datetime

'''
    class Post(BaseModel):
        This is for our request -> pydantic module, but for our database CHECK models.py 
        title: str
        content: str
        published: bool = True


    class CreatePost(BaseModel):
        title: str
        content: str
        published: bool


    class UpdatePost(BaseModel):
        title: str
        content: str
        published: bool

        

    This is one use case that we could use, but repeat a lot of code
    Instead we could do the next
'''

'''
    JWT TOKEN:
        1. Header -> algorithm + type of token
        2. Payload / data -> some data that we get from the request
        3. Verify signature -> a special / secret password that devs know

    This make our API extremely secure

    CLIENT -> REQUEST (LOGIN, PASSWORD) -> API 
    CLIENT <- JWT TOKEN <- API
    CLIENT -> POST / JWT TOKEN -> API VERIFY JWT TOKEN
    CLIENT <- DATA <- API
'''


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    id: Optional[int] = None


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class Post(PostBase):  # here because we inherit the PostBase, we don't need to specify the other fields for our response class
    id: int
    created_at: datetime
    user_id: int
    owner: UserResponse  # -> returning a pydantic model to our user

    # This is for SQLALCHEMY to tell our pydantic module that this is a dictionary or a pydantic model
    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: Post
    votes: int = 0

    class Config:
        orm_mode = True


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
