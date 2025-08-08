from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import List
from flask_migrate import Migrate


db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(16), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(20), nullable=False)
    lastname: Mapped[str] = mapped_column(String(20), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    posts: Mapped[List["Post"]] = relationship("Post", back_populates="author")
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="user")
    followers: Mapped[List["Follower"]] = relationship("Follower", foreign_keys="Follower.following_id", back_populates="following_user")
    following: Mapped[List["Follower"]] = relationship("Follower", foreign_keys="Follower.follower_id", back_populates="follower_user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname
        }


class Post(db.Model):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    image_url: Mapped[str] = mapped_column(String(255), nullable=False)
    caption: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    author: Mapped["User"] = relationship("User", back_populates="posts")
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="post")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "image_url": self.image_url,
            "caption": self.caption
        }


class Comment(db.Model):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship("User", back_populates="comments")
    post: Mapped["Post"] = relationship("Post", back_populates="comments")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "post_id": self.post_id,
            "content": self.content
        }


class Follower(db.Model):
    __tablename__ = "follower"

    id: Mapped[int] = mapped_column(primary_key=True)
    follower_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    following_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    follower_user: Mapped["User"] = relationship("User", foreign_keys=[follower_id], back_populates="following")
    following_user: Mapped["User"] = relationship("User", foreign_keys=[following_id], back_populates="followers")

    def serialize(self):
        return {
            "id": self.id,
            "follower_id": self.follower_id,
            "following_id": self.following_id
        }
    