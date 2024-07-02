python3
"""
main app:
    where all parts created would be implemented
"""
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from typing import List

import crud
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/users/{user_id}')
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.get('/users')
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.post('/users', response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@app.get('/posts/{post_id}')
def get_post(post_id: int, db: Session = Depends(get_db)):
    db_post = crud.get_post(db, post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post

@app.get('/posts')
def get_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts = crud.get_posts(db, skip=skip, limit=limit)
    return posts

@app.post('/create_post', response_model=schemas.Post)
def create_post(post: schemas.PostCreate, user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    created_post = crud.create_post(db, post, db_user)
    return {'created_post': created_post, 'User_id': user_id}

@app.delete('/delete_post/{post_id}', response_model= schemas.Post)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    return crud.delete_post(db, post_id)

@app.get('/comment/{comment_id}')
def get_comment(comment_id: int, db: Session = Depends(get_db)):
    db_comment = crud.get_comment(db, comment_id)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return db_comment

@app.get("/posts/{post_id}/comments/", response_model=List[schemas.Comment])
def read_comments(post_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    comments = crud.get_comments_by_post(db, post_id, skip=skip, limit=limit)
    return comments

@app.post("/posts/{post_id}/comments", response_model = schemas.Comment)
def create_comment(post_id: int, comment: schemas.CommentCreate, db: Session = Depends(get_db)):
    return crud.create_comment(db, post_id, comment)

@app.delete("/comment_delete/{comment_id}", response_model=schemas.Comment)
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    db_comment = crud.delete_comment(db, comment_id)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return db_comment

@app.post("/login", response_model=schemas.Token)
def login(user_email: str, password: str, db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, user_email, password)
    if user is None:
        raise HTTPException(status_code=404, detail="Wrong email or Password")
    access_token = create_access_token({"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
