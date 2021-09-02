from unittest import TestCase

from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserTestCase(TestCase):
    """Tests for views for Users"""

    def setUp(self):
        """Add a sample user"""

        User.query.delete()

        user = User(first_name="Test", last_name="User", image_url="/static/unknown.jpg")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            # we went to the correct page
            self.assertIn('<h3 class="h3">Users:</h3>', html)
            # user list is shown:
            self.assertIn('Test', html)

    def test_redirect(self):
        """ test redirect to the users list page after input validation"""
        with app.test_client() as client: 
            res = client.post('/users/new', data = {"first_name": "Test2", "last_name": "User2", "url": "/static/unknown.jpg"})
            self.assertEqual(res.status_code, 302)        
            self.assertEqual(res.location, 'http://localhost/users')

    def test_add_user(self):
        with app.test_client() as client:
            u = {"first_name": "Test3", "last_name": "User3", "url": "/static/unknown.jpg"}
            resp = client.post("/users/new", data=u, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Test3 User3", html)

