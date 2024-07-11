#!/usr/bin/python3
"""
the models
"""
from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, func
from sqlalchemy.orm import relationship

Base = __import__("database").Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, index=True)
    user_email = Column(String, unique=True, index=True)
    user_password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    phone_number = Column(String)
    age = Column(Integer)
    user_image = Column(String, nullable=True)

    posts = relationship("Post", back_populates="owner", cascade="all, delete")
    comments = relationship(
            "Comment",
            back_populates="owner",
            cascade="all, delete"
            )


class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String, ForeignKey("users.user_email"))
    image = Column(String, nullable=True)
    post_desc = Column(Text)
    post_title = Column(String)
    created_at = Column(DateTime(timezone=True), default=func.now())

    owner = relationship("User", back_populates="posts")
    comments = relationship(
        "Comment", back_populates="post", cascade="all, delete-orphan"
    )


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String, ForeignKey("users.user_email"))
    post_id = Column(Integer, ForeignKey("post.id"))
    comments_data = Column(Text)
    created_at = Column(DateTime(timezone=True), default=func.now())

    owner = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")
