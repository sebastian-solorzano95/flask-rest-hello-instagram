from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(
        String(16), unique=True, nullable=False)
    firsname: Mapped[str] = mapped_column(
        String(20), unique=False, nullable=False)
    lastname: Mapped[str] = mapped_column(
        String(20), unique=False, nullable=False)
    post: Mapped["Post"] = db.relationship(back_populates="User")
    following: Mapped[int] = db.relationship(back_populates="following")
    follower: Mapped[int] = db.relationship(back_populates="follower")

    # password: Mapped[str] = mapped_column(nullable=False)#
    # is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)#

    class Post(db.Model):
        id: Mapped[int] = mapped_column(primary_key=True)
        user_id: Mapped[int] = mapped_column(db.ForeignKey("user.id"))
        author: Mapped["User"] = db.relationship(back_populates="post")

        class Follower(db.Model):
            id: Mapped[int] = mapped_column(primary_key=True)

            following_id: Mapped[int] = mapped_column(db.ForeignKey("user.id"))
            following: Mapped[int] = db.relationship(
                back_populates="following")

            follower_id: Mapped[int] = mapped_column(db.ForeignKey("user.id"))
            follower: Mapped[int] = db.relationship(back_populates="follower")

            class Comment(db.Model):

                id: Mapped[int] = mapped_column(primary_key=True)
                user_id: Mapped[int] = mapped_column(
                    db.ForeignKey("user.id"), nullable=False)
                post_id: Mapped[int] = mapped_column(
                    db.ForeignKey("post.id"), nullable=False)
                content: Mapped[str] = mapped_column(nullable=False)

    author: Mapped["User"] = db.relationship("User", back_populates="comments")
    post: Mapped["Post"] = db.relationship("Post", back_populates="comments")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
