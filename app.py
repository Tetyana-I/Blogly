"""Blogly application."""

from flask import Flask, render_template, request,  redirect
#flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from blogly import input_validation, check_if_updated

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "very-very-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
# Commented here because we have this line in seed.py
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
    """ Process the add form, adding a new user and going back to /users """
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    url = request.form["url"]
    if input_validation(first_name, last_name, url):
        if check_if_updated(url):
            new_user = User(first_name=first_name, last_name=last_name, image_url=url)
        else:
            new_user = User(first_name=first_name, last_name=last_name)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/users')
    else:
        return render_template('/add_user.html')


@app.route('/users/<int:user_id>')
def user_info(user_id):
    """ Shows information about the given user,
        has a button to get to their edit page, and to delete the user """
    user = User.query.get_or_404(user_id)
    return render_template("user_info.html", user=user)


@app.route('/users/<int:user_id>/edit')
def show_edit_user_form(user_id):
    """ Shows the edit page for a user,
    has a cancel button that returns to the detail page for a user, 
    and a save button that updates the user. """
    user = User.query.get_or_404(user_id)
    return render_template("/edit_user.html", user=user)

@app.route('/users/<int:user_id>/edit', methods = ["POST"])
def save_user_changes(user_id):
    """ Process the edit form, returning the user to the /users page """
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    url = request.form["url"]
    updated = False
    updated_user = User.query.get_or_404(user_id)
    if check_if_updated(first_name):
        updated_user.first_name = first_name
        updated = True
    if check_if_updated(last_name):
        updated_user.last_name = last_name
        updated = True
    if check_if_updated(url):
        updated_user.image_url = url
        updated = True
    if updated and input_validation(updated_user.first_name, updated_user.last_name, updated_user.image_url):
            db.session.add(updated_user)
            db.session.commit()
            return redirect('/users')
    else:
        return redirect(f'/users/{user_id}/edit')


@app.route('/users/<int:user_id>/delete', methods = ["POST"])
def delete_user(user_id):
    """ Delete the user """
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    return redirect('/users')

