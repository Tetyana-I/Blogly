from unittest import TestCase

from app import app
from models import db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class User_Post_TestCase(TestCase):
    """Tests for views for Users"""

    def setUp(self):
        """Add a sample user"""

        User.query.delete()

        user = User(first_name="Test", last_name="User", image_url="/static/unknown.jpg")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

        Post.query.delete()

        post = Post(title="First Post", content="something very interesting", user_id=self.user_id)
        db.session.add(post)
        db.session.commit()

        self.post_id = post.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_users(self):
        """ test that shows users list page """
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            # we went to the correct page
            self.assertIn('<h3 class="h3">Users:</h3>', html)
            # user list is shown:
            self.assertIn('Test', html)

    def test_redirect(self):
        """ test redirect to the users list page after adding new user """
        with app.test_client() as client: 
            res = client.post('/users/new', data = {"first_name": "Test2", "last_name": "User2", "url": "/static/unknown.jpg"})
            self.assertEqual(res.status_code, 302)        
            self.assertEqual(res.location, 'http://localhost/users')

    def test_add_user(self):
        """ test that a new user was added to the user list"""
        with app.test_client() as client:
            u = {"first_name": "Test3", "last_name": "User3", "url": "/static/unknown.jpg"}
            resp = client.post("/users/new", data=u, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Test3 User3", html)

    def test_post_list(self):
        """ test that user info page contains list of user's posts """
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            # went to the correct page
            self.assertIn('<h3 class="h4">Posts</h3>', html)
            # user list is shown:
            self.assertIn('First Post', html)

    def test_edit_post(self):
        """ test that existing post edited as expected """
        with app.test_client() as client:
            p = {"title": "new title", "content": "new content"}
            resp = client.post(f"/posts/{self.post_id}/edit", data=p, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            # went to the correct page
            self.assertIn('Post Details', html)  
            # page contains correct info: new post title and old content
            self.assertIn('new title', html)   
            self.assertIn('<p>new content</p>', html)   

    def test_delete_post(self):
        """ test post deleting """
        with app.test_client() as client:
            resp = client.post(f'/posts/{self.post_id}/delete', data={"id": self.post_id}, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            # redirect to correct page
            self.assertIn('Posts', html) 
            # test that the post was deleted, post list is empty
            self.assertNotIn('First Post', html)
            self.assertIn('<h6>No posts so far ...</h6>', html)



