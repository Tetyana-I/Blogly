""" Seed file to make sample data to pets db """

from models import User, Post, db 
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If query isn't empty, empty it
User.query.delete()
Post.query.delete()

# Add users
cooper = User(first_name="Michael", last_name="Cooper", image_url="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=634&q=80")
racoon = User(first_name="Rocket", last_name="Racoon")
stark = User(first_name="Tina", last_name="Stark", image_url="https://images.unsplash.com/photo-1534528741775-53994a69daeb?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=700&q=80")
jackson = User(first_name="Monica", last_name="Jackson", image_url="https://images.unsplash.com/photo-1488426862026-3ee34a7d66df?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=634&q=80")

# Add new objects to session, so they'll persist

db.session.add_all([cooper, racoon, stark, jackson])
# db.session.add(racoon)
# db.session.add(stark)
# db.session.add(jackson)

# Commit addings
db.session.commit()

# Add posts for users
p1_1 = Post(title="First Post", content="Hello there!", user_id=1)
p2_1 = Post(title="First Post", content="Hi everybody!", user_id=2)
p3_1 = Post(title="First Post", content="Hi!", user_id=3)
p1_2 = Post(title="Second Post", content="Hello again!", user_id=1)
p2_2 = Post(title="My Next Post", content="Hmm, I don't know that to say...", user_id=2)

db.session.add_all([p1_1, p2_1, p3_1, p1_2, p2_2])
# db.session.add(p2_1)
# db.session.add(p3_1)
# db.session.add(p1_2)
# db.session.add(p2_2)


# Commit addings
db.session.commit()
