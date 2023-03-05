from typing import Optional
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime

# Dtabase schema velidating from pydentic model (pydentic model)
# class Post(BaseModel):
    # title : str
    # content : str
    # published : bool = True  #defalut true
    # rating : Optional[int] = None

# { define what should request should lokk like
class PostBase(BaseModel):
    title : str
    content : str
    published : bool = True

class PostCreate(PostBase):
    pass
# }

class UserCreate(BaseModel):
    email : EmailStr
    password : str

class UserOut(BaseModel):
    id : int
    email : EmailStr
    created_at : datetime
    class Config:
        orm_mode = True

class Post(PostBase):
    id : int
    created_at : datetime
    owner_id : int
    owner: UserOut
    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email : EmailStr
    password : str

class Token(BaseModel):
    access_token : str
    token_type: str

class TokenData(BaseModel):
    id : Optional[str]


# You can use below class for specific perpose 
# for example in UpdatePosts you can only specify 
# content fild so that user can only change content fild 
# and not able to change other then it.

# class CreatePosts(BaseModel):
#     title : str
#     content : str
#     published : bool = True

# class UpdatePosts(BaseModel):
#     title : str
#     content : str
#     published : bool 

class Vote(BaseModel):
    post_id : int
    dir : conint(le=1)