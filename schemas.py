# schemas.py
from pydantic import BaseModel
from datetime import datetime

# User
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    role: str

    class Config:
        orm_mode = True

# Token
class Token(BaseModel):
    access_token: str
    token_type: str

# Post
class PostCreate(BaseModel):
    title: str
    content: str

class PostOut(BaseModel):
    id: int
    title: str
    content: str
    owner_id: int
    created: datetime

    class Config:
        orm_mode = True
