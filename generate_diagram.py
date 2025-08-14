from eralchemy2 import render_er

from app import db
from models import Comment, Follower, Post, User

if __name__ == "__main__":
    # Use the SQLAlchemy metadata, not the database file
    render_er(db.Model.metadata, "diagram.png")
    print("diagram.png generated!")
