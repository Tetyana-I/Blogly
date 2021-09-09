from enum import unique
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()
def connect_db(app):
    """ Connect the database to app """
    db.app = app
    db.init_app(app)


"""Models for Blogly."""

class User(db.Model):
    """ User """
    __tablename__ = "users"

    def __repr__(self):
        """ better representation for debugging purposes """
        u = self
        return f"<User id={u.id} first_name={u.first_name} last_name={u.last_name} image_url={u.image_url}>"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False, default="/static/unknown.jpg")
    userposts = db.relationship('Post', cascade="all, delete")
    
class Post(db.Model):
    """ Post """
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"))
    u = db.relationship('User')
    
    tags = db.relationship('Tag', secondary="posttags", backref="posts")


    @property
    def formatted_date(self):
        """Return formatted date"""
        return self.created_at.strftime("%x %X")

class Tag(db.Model):
    """ Tag """
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)

class PostTag(db.Model):
    """ Mapping posts and tags """
    __tablename__ = "posttags"

    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), primary_key=True)


