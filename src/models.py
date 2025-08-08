"""
SQLAlchemy database models for a social media application.

This module defines the database schema using SQLAlchemy ORM with support for:
- User management and authentication
- Posts with images and captions
- Comments on posts
- Social following/follower relationships

All models include proper relationships, foreign keys, and serialization methods.
Uses modern SQLAlchemy 2.x syntax with Mapped types and relationship() function.
"""

from typing import List
from sqlalchemy import ForeignKey, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from extensions import db


class User(db.Model):
    """
    User model for authentication and profile management.

    This model represents users in the social media platform.
    Each user can create posts, comment on posts, and follow other users.
    Uses modern SQLAlchemy 2.x syntax with explicit typing.
    """

    # Explicitly define table name (good practice for clarity)
    __tablename__ = 'users'

    # Primary key - unique identifier for each user
    id: Mapped[int] = mapped_column(primary_key=True)

    # Email field - must be unique across all users and cannot be null
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)

    # Password hash - stores encrypted password (never store plain text!)
    password: Mapped[str] = mapped_column(String(128), nullable=False)

    # Account status - allows deactivating users without deleting data
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=True)

    # One user can have many posts (one-to-many relationship)
    posts: Mapped[List["Post"]] = relationship(
        back_populates="author", cascade="all, delete-orphan"
    )

    # One user can have many comments (one-to-many relationship)
    comments: Mapped[List["Comment"]] = relationship(
        back_populates="author", cascade="all, delete-orphan"
    )

    # Users who follow this user (followers)
    # Using foreign_keys to specify which FK to use for this relationship
    followers: Mapped[List["Follower"]] = relationship(
        foreign_keys="Follower.user_to_id",
        back_populates="followed_user",
        cascade="all, delete-orphan"
    )

    # Users this user is following
    following: Mapped[List["Follower"]] = relationship(
        foreign_keys="Follower.user_from_id",
        back_populates="follower_user",
        cascade="all, delete-orphan"
    )

    def serialize(self):
        """
        Serialize user data to dictionary format for JSON responses.

        Returns:
            dict: User data excluding sensitive information (password)
        """
        return {
            "id": self.id,
            "email": self.email,
            # SECURITY NOTE: Never serialize the password field!
            # Password hashes should never be exposed in API responses
        }


class Post(db.Model):
    """
    Post model for user-generated content.

    This model represents posts/photos shared by users on the platform.
    Each post belongs to one user and can have multiple comments.
    Uses modern SQLAlchemy 2.x syntax with explicit typing.
    """

    # Explicit table name
    __tablename__ = 'posts'

    # Primary key - unique identifier for each post
    id: Mapped[int] = mapped_column(primary_key=True)

    # Foreign key - links this post to its author (User)
    # Using modern ForeignKey import instead of db.ForeignKey
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)

    # URL to the uploaded image/photo
    # Limited to 255 characters (typical URL length limit)
    image_url: Mapped[str] = mapped_column(String(255), nullable=False)

    # Optional caption/description for the post
    # Can be null (users might post images without captions)
    caption: Mapped[str] = mapped_column(String(500), nullable=True)

    # MODERN RELATIONSHIPS - Using relationship() with back_populates
    # Many-to-one relationship with User (author)
    author: Mapped["User"] = relationship(back_populates="posts")

    # One post can have many comments (one-to-many relationship)
    comments: Mapped[List["Comment"]] = relationship(
        back_populates="post", cascade="all, delete-orphan"
    )

    def serialize(self):
        """
        Serialize post data to dictionary format for JSON responses.

        Returns:
            dict: Post data including all public fields
        """
        return {
            "id": self.id,
            "user_id": self.user_id,  # Author's user ID
            "image_url": self.image_url,  # Link to the image
            "caption": self.caption  # Post description (may be null)
        }


class Comment(db.Model):
    """
    Comment model for post interactions.

    This model represents comments made by users on posts.
    Each comment belongs to one user and one post (many-to-one relationships).
    Uses modern SQLAlchemy 2.x syntax with explicit typing.
    """

    # Explicit table name
    __tablename__ = 'comments'

    # Primary key - unique identifier for each comment
    id: Mapped[int] = mapped_column(primary_key=True)

    # Foreign key - links comment to the user who wrote it
    # Using modern ForeignKey import
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)

    # Foreign key - links comment to the post it belongs to
    # Using modern ForeignKey import
    post_id: Mapped[int] = mapped_column(ForeignKey('posts.id'), nullable=False)

    # The actual comment text
    # Limited to 300 characters (reasonable limit for comments)
    content: Mapped[str] = mapped_column(String(300), nullable=False)

    # MODERN RELATIONSHIPS - Using relationship() with back_populates
    # Many-to-one relationship with User (author)
    author: Mapped["User"] = relationship(back_populates="comments")

    # Many-to-one relationship with Post
    post: Mapped["Post"] = relationship(back_populates="comments")

    def serialize(self):
        """
        Serialize comment data to dictionary format for JSON responses.

        Returns:
            dict: Comment data including all fields
        """
        return {
            "id": self.id,
            "user_id": self.user_id,  # Who wrote the comment
            "post_id": self.post_id,  # Which post this comment is on
            "content": self.content   # The comment text
        }


class Follower(db.Model):
    """
    Follower model for social relationships.

    This model represents the following/follower relationships between users.
    It's a many-to-many relationship implemented with a junction table.
    Uses modern SQLAlchemy 2.x syntax with explicit typing.

    Example: If User A follows User B:
    - user_from_id = A's ID (the follower)
    - user_to_id = B's ID (the one being followed)
    """

    # Explicit table name
    __tablename__ = 'followers'

    # Primary key - unique identifier for each follow relationship
    id: Mapped[int] = mapped_column(primary_key=True)

    # Foreign key - the user who is following (the follower)
    # Using modern ForeignKey import
    user_from_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)

    # Foreign key - the user being followed (the followee)
    # Using modern ForeignKey import
    user_to_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)

    # MODERN RELATIONSHIPS - Using relationship() with back_populates
    # Many-to-one relationship with User (follower)
    follower_user: Mapped["User"] = relationship(
        foreign_keys=[user_from_id], back_populates="following"
    )

    # Many-to-one relationship with User (followed)
    followed_user: Mapped["User"] = relationship(
        foreign_keys=[user_to_id], back_populates="followers"
    )

    def serialize(self):
        """
        Serialize follower relationship to dictionary format for JSON responses.

        Returns:
            dict: Follower relationship data
        """
        return {
            "id": self.id,
            "user_from_id": self.user_from_id,  # Who is following
            "user_to_id": self.user_to_id       # Who is being followed
        }

# DATABASE RELATIONSHIP SUMMARY (Modern SQLAlchemy 2.x Style):
#
# Users ←→ Posts: One-to-Many (One user can have many posts)
#   - User.posts: Mapped[List["Post"]] = relationship(back_populates="author")
#   - Post.author: Mapped["User"] = relationship(back_populates="posts")
#
# Users ←→ Comments: One-to-Many (One user can write many comments)
#   - User.comments: Mapped[List["Comment"]] = relationship(back_populates="author")
#   - Comment.author: Mapped["User"] = relationship(back_populates="comments")
#
# Posts ←→ Comments: One-to-Many (One post can have many comments)
#   - Post.comments: Mapped[List["Comment"]] = relationship(back_populates="post")
#   - Comment.post: Mapped["Post"] = relationship(back_populates="comments")
#
# Users ←→ Followers: Many-to-Many via junction table (Users can follow each other)
#   - User.followers: Mapped[List["Follower"]] = relationship(foreign_keys="Follower.user_to_id")
#   - User.following: Mapped[List["Follower"]] = relationship(foreign_keys="Follower.user_from_id")
#   - Follower.follower_user: Mapped["User"] = relationship(foreign_keys=[user_from_id])
#   - Follower.followed_user: Mapped["User"] = relationship(foreign_keys=[user_to_id])
#
# Key Modern SQLAlchemy 2.x Features Used:
# ✅ Mapped[T] type annotations for all fields and relationships
# ✅ relationship() function instead of db.relationship()
# ✅ back_populates instead of backref for bidirectional relationships
# ✅ Direct ForeignKey import instead of db.ForeignKey
# ✅ List typing for one-to-many relationships
# ✅ Explicit foreign_keys specification for complex relationships
