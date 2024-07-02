#!/usr/bin/env python3
"""
main app:
    where all parts created would be implemented
"""
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
SessionLocal = __import__("database").SessionLocal
engine = __import__("database").engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


"""
    more would be implemented here,
    this commect should be deleted when implementation is being done.
    
    More info:
        tutorial link if stuck is:
        `https://fastapi.tiangolo.com/tutorial/sql-databases/`
"""
