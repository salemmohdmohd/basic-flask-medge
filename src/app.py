from flask import Flask
from extensions import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

if __name__ == '__main__':
    # Import models after app context is created
    from models import User, Post, Comment, Follower
    
    with app.app_context():
        db.create_all()
        print("Database created successfully!")
        print(f"Tables created: {db.metadata.tables.keys()}")
    print("Run 'pipenv run diagram' to generate the database diagram")
