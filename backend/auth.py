#!/usr/bin/python3
"""
user aunthetication
"""
from passlib.context import CryptContext
from typing import Optional
from datetime import datetime, timedelta
import jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Constants for JWT token configuration
SECRET_KEY = "empowerher_token"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class Hash:
    """
    Verify if the hashed password is equal to the provided plain password.
    Generate a password hash.
    """
    @staticmethod
    def verify_pwd(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def hash_pwd(password):
        return pwd_context.hash(password)

# Function to create JWT access token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
