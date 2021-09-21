"""Blogly application."""

from flask import Flask, render_template, request,  redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "very-very-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
# Commented here because we have this command in seed.py:
# db.create_all()

@app.route('/')    
def home_page():
    """Shows 5 recent posts """
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template("/home_page.html", posts=posts)

@app.route('/users')
def show_users():
    """ Shows list of all users in db,
    has links to view the detail page for each user,
    has a link here to the add-user form. """
    users = User.query.order_by(User.last_name, User.first_name).all()
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
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')

###################################################
# post routes
###################################################

@app.route('/users/<int:user_id>/posts/new')
def show_post_form(user_id):
    """ Show form to add a post for that user """
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template("/add_post.html", user=user, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_new_post(user_id):
    """ Processes add-post form, adding a new post to the given user and going back to user info """
    title = request.form["title"]
    content = request.form["content"]
    tags_list = [name for name in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.name.in_(tags_list)).all() 
    new_post = Post(title=title, content=content, user_id=user_id, tags=tags)
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
    tags = Tag.query.all()
    return render_template("/edit_post.html", post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def handle_post_changes(post_id):
    """ Handle editing of a post. Redirect back to the post view. """
    title = request.form["title"]
    content = request.form["content"]
    tags_list = [name for name in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.name.in_(tags_list)).all()
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
    
    updated_post.tags = tags
    db.session.add(updated_post)
    db.session.commit()
  
    return redirect(f"/posts/{post_id}")

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """ Delete the post """
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(f'/users/{post.user_id}')

##################################################################
#  tags routes
##################################################################

@app.route('/tags')  
def show_tags():
    """ Lists all tags, with links to the tag detail page """
    tags = Tag.query.order_by(Tag.name).all()
    return render_template('/tags_list.html', tags=tags)
 
@app.route('/tags/<int:tag_id>')
def tag_info(tag_id):
    """ Shows detail about a tag. Have links to edit form and to delete """
    tag = Tag.query.get_or_404(tag_id)
    return render_template("/show_tag.html", tag=tag)

@app.route('/tags/new')
def show_tag_form():
    """ Shows a form to add a new tag """
    return render_template('/create_tag.html')

@app.route('/tags/new', methods=["POST"])
def add_new_tag():
    """ Process add form, adds tag, and redirect to tag list """
    name = request.form["name"]
    new_tag = Tag(name=name)
    db.session.add(new_tag)
    db.session.commit()
    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit')
def show_edit_tag_form(tag_id):
    """ Shows edit form for a tag """
    tag = Tag.query.get_or_404(tag_id)
    return render_template("/edit_tag.html", tag=tag)
    
@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def handle_edit_tag(tag_id):
    """ Processes edit form, edit tag, and redirects to the tags list. """
    name = request.form["name"]
    updated_tag = Tag.query.get_or_404(tag_id)
    updated = False
    if name:
        updated_tag.name = name
        updated = True
    if updated:
        db.session.add(updated_tag)
        db.session.commit()
    return redirect("/tags")
    
@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def handle_delete_tag(tag_id):
    """ Deletes a tag """
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect('/tags')