from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    is_active = Column(Boolean(), nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    profile_picture = Column(String(250))
    bio = Column(Text)

    posts = relationship("Post", backref="user", lazy=True)
    comments = relationship("Comment", backref="user", lazy=True)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
        }

class Post(db.Model):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    image_url = Column(String(255), nullable=False)
    caption = Column(String(500))
    timestamp = Column(DateTime)

    comments = relationship("Comment", backref="post", lazy=True)

    def serialize(self):
        return {
            "id": self.id,
            "image_url": self.image_url,
            "caption": self.caption,
            "user_id": self.user_id
        }

class Comment(db.Model):
    __tablename__ = "comment"

    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("post.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    text = Column(String(500), nullable=False)
    timestamp = Column(DateTime)

    def serialize(self):
        return {
            "id": self.id,
            "text": self.text,
            "user_id": self.user_id,
            "post_id": self.post_id,
        }

class Follower(db.Model):
    __tablename__ = "follower"

    id = Column(Integer, primary_key=True)
    follower_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    followed_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "follower_id": self.follower_id,
            "followed_id": self.followed_id,
        }
    
class Media(db.Model):
    __tablename__ = "media"

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)
    type = db.Column(db.String(10), nullable=False)  # 'image' or 'video'
    url = db.Column(db.String(255), nullable=False)

    post = db.relationship("Post", backref="media", lazy=True)

    def serialize(self):
        return {
            "id": self.id,
            "type": self.type,
            "url": self.url,
            "post_id": self.post_id
        }