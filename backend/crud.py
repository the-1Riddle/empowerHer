#!/usr/bin/python3
"""
crud functions that would interact with the db
"""
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import models
import schemas
import jwt
from datetime import datetime,timedelta

# Password context for hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

"""
User CRUD Operations
"""

# gets user by id
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

# gets user by email
def get_user_by_email(db: Session, user_email: str):
    return (
        db.query(models.User)
        .filter(models.User.user_email == user_email)
        .first()
    )

# gets all users but using pagination
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

# creates a new user
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        user_name=user.user_name,
        user_email=user.user_email,
        user_password=user.user_password,
        first_name=user.first_name,
        last_name=user.last_name,
        phone_number=user.phone_number,
        age=user.age,
        user_image=user.user_image,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Verify password
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# Authenticate user
def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.user_password):
        return False
    return user

"""
Post CRUD Operations
"""

# gets a post by id
def get_post(db: Session, post_id: int):
    return db.query(models.Post).filter(models.Post.id == post_id).first()

# gets all posts but using pagination
def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Post).offset(skip).limit(limit).all()

# creates a new post
def create_post(db: Session, post: schemas.PostCreate, user_email: str):
    db_post = models.Post(
        post_title=post.post_title,
        post_desc=post.post_desc,
        image=post.image,
        user_email=user_email
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

# deletes a post by id
def delete_post(db: Session, post_id: int):
    db_post = get_post(db, post_id)
    if db_post:
        db.delete(db_post)
        db.commit()
    return db_post

"""
Comment CRUD Operations
"""

# gets a comment by id
def get_comment(db: Session, comment_id: int):
    return (
        db.query(models.Comment)
        .filter(models.Comment.id == comment_id)
        .first()
    )

# gets comments from a post but using pagination
def get_comments_by_post(
    db: Session, post_id: int, skip: int = 0, limit: int = 100
):
    return (
        db.query(models.Comment)
        .filter(models.Comment.post_id == post_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

# creates a new comment
def create_comment(db: Session, comment: schemas.CommentCreate, user_email: str):
    db_comment = models.Comment(**comment.dict(), user_email=user_email)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

# deletes a comment by id
def delete_comment(db: Session, comment_id: int):
    db_comment = get_comment(db, comment_id)
    if db_comment:
        db.delete(db_comment)
        db.commit()
    return db_comment


def create_password_reset_token(email: str):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": email, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password_reset_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload["sub"]

        if not email:
            raise jwt.PyJWTError
        return email
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    
def rest_password(db: Session, email: str, new_password: str):
    user = get_user_by_email(db, email)
    if user:
        hashed_password = pwd_context.hash(new_password)
        user.user_password = hashed_password
        db.commit()
        db.refresh(user)
        return user
    else:
        return None