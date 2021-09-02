""" Seed file to make sample data to pets db """

from models import User, db 
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If query isn't empty, empty it
User.query.delete()

# Add users
cooper = User(first_name="Michael", last_name="Cooper", image_url="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=634&q=80")
racoon = User(first_name="Rocket", last_name="Racoon")
stark = User(first_name="Tina", last_name="Stark", image_url="https://images.unsplash.com/photo-1534528741775-53994a69daeb?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=700&q=80")
jackson = User(first_name="Monica", last_name="Jackson", image_url="https://images.unsplash.com/photo-1488426862026-3ee34a7d66df?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=634&q=80")


# Add new objects to session, so they'll persist

db.session.add(cooper)
db.session.add(racoon)
db.session.add(stark)
db.session.add(jackson)


# Commit addings
db.session.commit()