"""
SQLAlchemy database models for an Instagram-like social media application.

"""

from typing import List

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import db

from eralchemy2 import render_er



class User(db.Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(100), nullable=False)
    lastname: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)

    posts: Mapped[List["Post"]] = relationship(
        "Post", back_populates="author", cascade="all, delete-orphan"
    )
    comments: Mapped[List["Comment"]] = relationship(
        "Comment", back_populates="author", cascade="all, delete-orphan"
    )
    followers: Mapped[List["Follower"]] = relationship(
        foreign_keys="Follower.user_to_id",
        back_populates="followed_user",
        cascade="all, delete-orphan"
    )
    following: Mapped[List["Follower"]] = relationship(
        foreign_keys="Follower.user_from_id",
        back_populates="follower_user",
        cascade="all, delete-orphan"
    )


class Post(db.Model):
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)

    author: Mapped["User"] = relationship("User", back_populates="posts")
    media: Mapped[List["Media"]] = relationship(
        "Media", back_populates="post", cascade="all, delete-orphan"
    )
    comments: Mapped[List["Comment"]] = relationship(
        "Comment", back_populates="post", cascade="all, delete-orphan"
    )


class Media(db.Model):
    __tablename__ = 'media'

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String(255), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey('posts.id'), nullable=False)

    post: Mapped["Post"] = relationship("Post", back_populates="media")


class Comment(db.Model):
    __tablename__ = 'comments'

    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(300), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey('posts.id'), nullable=False)

    author: Mapped["User"] = relationship("User", back_populates="comments")
    post: Mapped["Post"] = relationship("Post", back_populates="comments")


class Follower(db.Model):
    __tablename__ = 'followers'

    user_from_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
    user_to_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)

    follower_user: Mapped["User"] = relationship(
        foreign_keys=[user_from_id], back_populates="following"
    )
    followed_user: Mapped["User"] = relationship(
        foreign_keys=[user_to_id], back_populates="followers"
    )
