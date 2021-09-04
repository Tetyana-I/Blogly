from flask_sqlalchemy import SQLAlchemy

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
    image_url = db.Column(db.Text, nullable=True, default="/static/unknown.jpg")
    userposts = db.relationship('Post', cascade="all, delete")
    
class Post(db.Model):
    """ Post """
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"))
    u = db.relationship('User')
    
