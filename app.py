"""Blogly application."""

from flask import Flask,render_template, request,  redirect
#flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True


app.config['SECRET_KEY'] = "very-very-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
# Don't forget to delete
# db.create_all()

@app.route('/')    
def home_page():
    """ Redirect to list of users """
    return redirect("/users")


@app.route('/users')
def show_users():
    """ Shows list of all users in db,
    has links to view the detail page for each user,
    has a link here to the add-user form. """
    users = User.query.all()
    return render_template('/users_list.html', users=users)

@app.route('/users/new')
def show_user_form():
    """ Show a form to add a new user """
    return render_template("/add_user.html")

@app.route('/users/new', methods=['POST'])
def add_new_user():
    """ Process the add-user form, adding a new user and going back to /users """
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    url = request.form["url"]
    if url:
        new_user = User(first_name=first_name, last_name=last_name, image_url=url)
    else:
        new_user = User(first_name=first_name, last_name=last_name)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/users')
    
@app.route('/users/<int:user_id>')
def user_info(user_id):
    """ Shows information about the given user,
        has a button to get to their edit page, and to delete the user """
    user = User.query.get_or_404(user_id)
    return render_template("/user_info.html", user=user)


@app.route('/users/<int:user_id>/edit')
def show_edit_user_form(user_id):
    """ Shows the edit page for a user,
    has a cancel button that returns to the detail page for a user, 
    and a save button that updates the user. """
    user = User.query.get_or_404(user_id)
    return render_template("/edit_user.html", user=user)

@app.route('/users/<int:user_id>/edit', methods = ["POST"])
def handle_user_changes(user_id):
    """ Process the edit form, returning the user to the /users page """
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    url = request.form["url"]
    updated = False
    updated_user = User.query.get_or_404(user_id)
    if first_name:
        updated_user.first_name = first_name
        updated = True
    if last_name:
        updated_user.last_name = last_name
        updated = True
    if url:
        updated_user.image_url = url
        updated = True
    if updated:
        db.session.add(updated_user)
        db.session.commit()
    return redirect(f'/users/{user_id}') 

@app.route('/users/<int:user_id>/delete', methods = ["POST"])
def delete_user(user_id):
    """ Delete the user """
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>/posts/new')
def show_post_form(user_id):
    """ Show form to add a post for that user """
    user = User.query.get_or_404(user_id)
    return render_template("/add_post.html", user=user)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_new_post(user_id):
    """ Processes add-post form, adding a new post to the given user and going back to user info """
    title = request.form["title"]
    content = request.form["content"]
    new_post = Post(title=title, content=content, user_id=user_id)
    db.session.add(new_post)
    db.session.commit()
    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Show a post. Shows buttons to edit and delete the post """
    post = Post.query.get_or_404(post_id)
    return render_template("/post_details.html", post=post)

@app.route('/posts/<int:post_id>/edit')
def show_edit_post_form(post_id):
    """ Shows form to edit a post, and to cancel (back to user page). """
    post = Post.query.get_or_404(post_id)
    return render_template("/edit_post.html", post=post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def handle_post_changes(post_id):
    """ Handle editing of a post. Redirect back to the post view. """
    title = request.form["title"]
    content = request.form["content"]
    updated_post = Post.query.get_or_404(post_id)
    updated = False
    if title:
        updated_post.title = title
        updated = True
    if content:
        updated_post.content = content
        updated = True
    if updated:
        db.session.add(updated_post)
        db.session.commit()
    return redirect(f"/posts/{post_id}")

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """ Delete the post """
    post = Post.query.get_or_404(post_id)
    Post.query.filter_by(id=post_id).delete()
    db.session.commit()
    return redirect(f'/users/{post.user_id}')

   
 