"""
Flask application factory and database initialization.

This module creates the Flask application instance, configures the database,
and initializes all SQLAlchemy models. It follows Flask best practices by
using the app factory pattern with extensions.
"""

from flask import Flask
from extensions import db
# Uncomment the next line when you're ready to add API endpoints
# from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Uncomment the next line when you're ready to add API endpoints
# CORS(app)  # This enables CORS for all domains on all routes

db.init_app(app)

if __name__ == '__main__':
    # Import models after app context is created
    # These imports are used by SQLAlchemy to create tables
    # pylint: disable=unused-import,import-outside-toplevel
    from models import User, Post, Comment, Follower

    with app.app_context():
        db.create_all()
        print("Database created successfully!")
        print(f"Tables created: {db.metadata.tables.keys()}")
    print("Run 'pipenv run diagram' to generate the database diagram")
