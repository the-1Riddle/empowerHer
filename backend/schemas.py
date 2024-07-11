#!/usr/bin/python3
"""
pydantic schemes
"""
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    user_name: str
    user_email: EmailStr
    first_name: str
    last_name: str
    phone_number: str
    age: int
    user_image: Optional[str] = None

class UserCreate(UserBase):
    user_password: str

class User(UserBase):
    id: int
    user_email: EmailStr

    class Config:
        orm_mode: True

class PostBase(BaseModel):
    post_title: str
    post_desc: str
    image: Optional[str] = None

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    user_email: EmailStr
    created_at: datetime

    class Config:
        orm_mode: True

class CommentBase(BaseModel):
    comments_data: str

class CommentCreate(CommentBase):
    post_id: int

class Comment(CommentBase):
    id: int
    user_email: EmailStr
    post_id: int
    created_at: datetime

    class Config:
        orm_mode: True

# Adding token-related schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_email: Optional[str] = None

class ResetPassword(BaseModel):
    reset_password_token: str

class PasswordResetRequest(BaseModel):
    email: str

class PasswordReset(BaseModel):
    token: str
    new_password: str

class PasswordUpdate(BaseModel):
    email: str
    old_password: str
    new_password: str


class EmailSchema(BaseModel):
    email: EmailStr
    full_name: str
    subject: str
    phone_number: str
    message: str