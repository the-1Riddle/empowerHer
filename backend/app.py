#!/usr/bin/env python3
"""
main app:
    where all parts created would be implemented
"""
from fastapi import Depends, FastAPI, HTTPException, status, File, Form, UploadFile, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import logging
from sqlalchemy.orm import Session
from typing import List
from fastapi.responses import JSONResponse
from pydantic.networks import EmailStr

import crud
import models
import schemas
Hash = __import__("auth").Hash
create_access_token = __import__("auth").create_access_token
get_current_user = __import__("auth").get_current_user
SessionLocal = __import__("database").SessionLocal
engine = __import__("database").engine
get_db = __import__("database").get_db
contact = __import__("send_mail").contact
EmailSchema = __import__("schemas").EmailSchema
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


"""
    added CORS Middleware
    more info:
        `https://fastapi.tiangolo.com/tutorial/cors/`
        `https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS`
"""
origins = [
    "http://localhost:3000",
    "http://empowerher.net"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # allow all origins, this works well with the frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PICTURES_DIR = os.path.join(BASE_DIR, 'static/Pictures')
os.makedirs(PICTURES_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")


"""
    more would be implemented here,
    this comment should be deleted when implementation is being done.

    More info:
        tutorial link if stuck is:
        `https://fastapi.tiangolo.com/tutorial/sql-databases/`
        `https://fastapi.tiangolo.com/tutorial/response-model/`
"""


# User Routes
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user.user_email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    hashed_password = Hash.hash_pwd(user.user_password)
    user.user_password = hashed_password
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
                )
    return db_user


@app.get("/users/email/{user_email}", response_model=schemas.User)
def read_user_by_email(user_email: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user_email=user_email)
    if db_user is None:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
                )
    return db_user


# Post Routes

@app.post("/posts/", response_model=schemas.Post)
def create_post(
    post_title: str = Form(...),
    post_desc: str = Form(...),
    user_email: str = Form(...),
    image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    logging.info(f"Received post_title: {post_title}")
    logging.info(f"Received post_desc: {post_desc}")
    logging.info(f"Received user_email: {user_email}")
    logging.info(f"Received image: {image.filename if image else 'No image uploaded'}")

    image_name = None
    if image:
        image_name = image.filename
        image_path = os.path.join(PICTURES_DIR, image_name)
        with open(image_path, "wb") as f:
            f.write(image.file.read())

    post_data = schemas.PostCreate(
        post_title=post_title,
        post_desc=post_desc,
        image=image_name
    )

    new_post = crud.create_post(db=db, post=post_data, user_email=user_email)
    return new_post


@app.get("/posts/", response_model=List[schemas.Post])
def read_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    posts = crud.get_posts(db, skip=skip, limit=limit)
    return posts


@app.get("/posts/{post_id}", response_model=schemas.Post)
def read_post(post_id: int, db: Session = Depends(get_db)):
    db_post = crud.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found"
                )
    return db_post


@app.delete("/posts/{post_id}", response_model=schemas.Post)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    db_post = crud.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found"
                )
    return crud.delete_post(db=db, post_id=post_id)


# Comment Routes
@app.post("/comments/", response_model=schemas.Comment)
def create_comment(
    comment: schemas.CommentCreate,
    user_email: str,
    db: Session = Depends(get_db)
):
    print(f"Received request to create comment: {comment} by user {user_email}")
    new_comment = crud.create_comment(db=db, comment=comment, user_email=user_email)
    print(f"Comment created successfully: {new_comment}")
    return new_comment


@app.get("/comments/", response_model=List[schemas.Comment])
def read_comments(
        post_id: int,
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db)
        ):
    comments = crud.get_comments_by_post(
            db,
            post_id=post_id,
            skip=skip,
            limit=limit
            )
    return comments


@app.get("/comments/{comment_id}", response_model=schemas.Comment)
def read_comment(comment_id: int, db: Session = Depends(get_db)):
    db_comment = crud.get_comment(db, comment_id=comment_id)
    if db_comment is None:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comment not found"
                )
    return db_comment


@app.delete("/comments/{comment_id}", response_model=schemas.Comment)
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    db_comment = crud.get_comment(db, comment_id=comment_id)
    if db_comment is None:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comment not found"
                )
    return crud.delete_comment(db=db, comment_id=comment_id)


@app.post("/token", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.user_email})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(get_current_user)):
    return current_user


@app.post("/password-reset-request")
def password_reset_request(request: schemas.PasswordResetRequest, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, request.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    reset_token = crud.create_password_reset_token(user.user_email)
    # In a real application, you would send the reset token via email here
    return {"reset_token": reset_token}


@app.post("/password-update")
def password_reset(password_update: schemas.PasswordUpdate, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, password_update.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not Hash.verify_pwd(password_update.old_password, user.user_password):
        raise HTTPException(status_code=401, detail="Old password is incorrect")
        
    hashed_password = Hash.hash_pwd(password_update.new_password)
    user.user_password = hashed_password
    db.commit()
    db.refresh(user)
    return {"message": "Password reset successful"}


@app.post("/contact-mail/")
async def send_contact_email(
    background_tasks: BackgroundTasks,
    email: EmailStr = Form(...),
    full_name: str = Form(...),
    subject: str = Form(...),
    phone_number: str = Form(...),
    message: str = Form(...)
):
    email_data = EmailSchema(
        email=email,
        full_name=full_name,
        subject=subject,
        phone_number=phone_number,
        message=message
    )
    background_tasks.add_task(contact, email_data)
    return JSONResponse(
        status_code=200,
        content={"message": "Email has been sent"}
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
