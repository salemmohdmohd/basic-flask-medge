"""
Main Flask application with CRUD API routes.

This module provides RESTful API endpoints for:
- User management (CRUD operations)
- Post management (CRUD operations)
- Comment management (CRUD operations)
- Follower relationships (CRUD operations)

All endpoints return JSON responses and include proper error handling.
Uses Flask-CORS for cross-origin requests from frontend applications.
Uses modern SQLAlchemy 2.x syntax with db.session.execute() and select().
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from extensions import db
from models import User, Post, Comment, Follower


def create_app():
    """
    Application factory pattern for creating Flask app instance.

    Returns:
        Flask: Configured Flask application
    """
    flask_app = Flask(__name__)

    # Database configuration
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database.db'
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Enable CORS for all domains on all routes
    CORS(flask_app)

    # Initialize extensions
    db.init_app(flask_app)

    return flask_app


app = create_app()


# ============================================================================
# USER CRUD OPERATIONS
# ============================================================================

@app.route('/api/users', methods=['GET'])
def get_all_users():
    """
    Get all users from the database using modern SQLAlchemy 2.x syntax.

    Returns:
        JSON: List of all users (excluding passwords)
    """
    try:
        # Modern SQLAlchemy 2.x: Use db.session.execute() with select()
        users = db.session.execute(select(User)).scalars().all()
        return jsonify([user.to_json() for user in users]), 200
    except (AttributeError, TypeError) as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """
    Get a specific user by ID using modern SQLAlchemy 2.x syntax.

    Args:
        user_id (int): User ID to retrieve

    Returns:
        JSON: User data or error message
    """
    try:
        # Modern SQLAlchemy 2.x: Use db.session.get() for primary key lookup
        user = db.session.get(User, user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        return jsonify(user.to_json()), 200
    except (SQLAlchemyError, ValueError) as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/users', methods=['POST'])
def create_user():
    """
    Create a new user.

    Expected JSON:
        {
            "email": "user@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "password": "securepassword"
        }

    Returns:
        JSON: Created user data or error message
    """
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ['email', 'first_name', 'last_name', 'password']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        # Check if email already exists using modern syntax
        existing_user = db.session.execute(
            select(User).where(User.email == data['email'])
        ).scalar_one_or_none()
        if existing_user:
            return jsonify({"error": "Email already exists"}), 409

        # Create new user
        new_user = User(
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            password=data['password'],  # In production, hash this password!
            is_active=data.get('is_active', True)
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify(new_user.to_json()), 201

    except (SQLAlchemyError, ValueError) as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Update an existing user.

    Args:
        user_id (int): User ID to update

    Expected JSON:
        {
            "email": "newemail@example.com",
            "first_name": "Jane",
            "last_name": "Smith",
            "is_active": true
        }

    Returns:
        JSON: Updated user data or error message
    """
    try:
        # Modern SQLAlchemy 2.x: Use db.session.get() for primary key lookup
        user = db.session.get(User, user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        data = request.get_json()

        # Update fields if provided
        if 'email' in data:
            # Check if new email already exists (exclude current user) using modern syntax
            existing_user = db.session.execute(
                select(User).where(
                    (User.email == data['email']) & (User.id != user_id)
                )
            ).scalar_one_or_none()
            if existing_user:
                return jsonify({"error": "Email already exists"}), 409
            user.email = data['email']

        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'is_active' in data:
            user.is_active = data['is_active']
        if 'password' in data:
            user.password = data['password']  # In production, hash this!

        db.session.commit()
        return jsonify(user.to_json()), 200

    except (SQLAlchemyError, ValueError) as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Delete a user using modern SQLAlchemy 2.x syntax.

    Args:
        user_id (int): User ID to delete

    Returns:
        JSON: Success message or error
    """
    try:
        # Modern SQLAlchemy 2.x: Use db.session.get() for primary key lookup
        user = db.session.get(User, user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        db.session.delete(user)
        db.session.commit()

        return jsonify({"message": "User deleted successfully"}), 200

    except (SQLAlchemyError, ValueError) as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# ============================================================================
# POST CRUD OPERATIONS
# ============================================================================

@app.route('/api/posts', methods=['GET'])
def get_all_posts():
    """Get all posts with author information using modern SQLAlchemy 2.x syntax."""
    try:
        # Modern SQLAlchemy 2.x: Use db.session.execute() with select()
        posts = db.session.execute(select(Post)).scalars().all()
        posts_data = []
        for post in posts:
            post_data = post.serialize()
            # Add author information
            post_data['author'] = post.author.to_json() if post.author else None
            posts_data.append(post_data)
        return jsonify(posts_data), 200
    except (SQLAlchemyError, ValueError) as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    """Get a specific post by ID using modern SQLAlchemy 2.x syntax."""
    try:
        # Modern SQLAlchemy 2.x: Use db.session.get() for primary key lookup
        post = db.session.get(Post, post_id)
        if not post:
            return jsonify({"error": "Post not found"}), 404

        post_data = post.serialize()
        post_data['author'] = post.author.to_json() if post.author else None
        return jsonify(post_data), 200
    except (SQLAlchemyError, ValueError) as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/posts', methods=['POST'])
def create_post():
    """
    Create a new post.

    Expected JSON:
        {
            "user_id": 1,
            "image_url": "https://example.com/image.jpg",
            "caption": "Beautiful sunset!"
        }
    """
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ['user_id', 'image_url']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        # Verify user exists using modern syntax
        user = db.session.get(User, data['user_id'])
        if not user:
            return jsonify({"error": "User not found"}), 404

        new_post = Post(
            user_id=data['user_id'],
            image_url=data['image_url'],
            caption=data.get('caption')
        )

        db.session.add(new_post)
        db.session.commit()

        return jsonify(new_post.serialize()), 201

    except (SQLAlchemyError, ValueError) as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """Update an existing post using modern SQLAlchemy 2.x syntax."""
    try:
        # Modern SQLAlchemy 2.x: Use db.session.get() for primary key lookup
        post = db.session.get(Post, post_id)
        if not post:
            return jsonify({"error": "Post not found"}), 404

        data = request.get_json()

        if 'image_url' in data:
            post.image_url = data['image_url']
        if 'caption' in data:
            post.caption = data['caption']

        db.session.commit()
        return jsonify(post.serialize()), 200

    except (SQLAlchemyError, ValueError) as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """Delete a post using modern SQLAlchemy 2.x syntax."""
    try:
        # Modern SQLAlchemy 2.x: Use db.session.get() for primary key lookup
        post = db.session.get(Post, post_id)
        if not post:
            return jsonify({"error": "Post not found"}), 404

        db.session.delete(post)
        db.session.commit()

        return jsonify({"message": "Post deleted successfully"}), 200

    except (SQLAlchemyError, ValueError) as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# ============================================================================
# COMMENT CRUD OPERATIONS
# ============================================================================

@app.route('/api/comments', methods=['GET'])
def get_all_comments():
    """Get all comments using modern SQLAlchemy 2.x syntax."""
    try:
        # Modern SQLAlchemy 2.x: Use db.session.execute() with select()
        comments = db.session.execute(select(Comment)).scalars().all()
        comments_data = []
        for comment in comments:
            comment_data = comment.serialize()
            comment_data['author'] = comment.author.to_json() if comment.author else None
            comments_data.append(comment_data)
        return jsonify(comments_data), 200
    except (SQLAlchemyError, ValueError) as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/posts/<int:post_id>/comments', methods=['GET'])
def get_post_comments(post_id):
    """Get all comments for a specific post using modern SQLAlchemy 2.x syntax."""
    try:
        # Modern SQLAlchemy 2.x: Use db.session.get() for primary key lookup
        post = db.session.get(Post, post_id)
        if not post:
            return jsonify({"error": "Post not found"}), 404

        # Modern SQLAlchemy 2.x: Use db.session.execute() with select() and where()
        comments = db.session.execute(
            select(Comment).where(Comment.post_id == post_id)
        ).scalars().all()
        comments_data = []
        for comment in comments:
            comment_data = comment.serialize()
            comment_data['author'] = comment.author.to_json() if comment.author else None
            comments_data.append(comment_data)
        return jsonify(comments_data), 200
    except (SQLAlchemyError, ValueError) as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/comments', methods=['POST'])
def create_comment():
    """
    Create a new comment.

    Expected JSON:
        {
            "user_id": 1,
            "post_id": 1,
            "content": "Great photo!"
        }
    """
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ['user_id', 'post_id', 'content']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        # Verify user and post exist using modern syntax
        user = db.session.get(User, data['user_id'])
        if not user:
            return jsonify({"error": "User not found"}), 404

        post = db.session.get(Post, data['post_id'])
        if not post:
            return jsonify({"error": "Post not found"}), 404

        new_comment = Comment(
            user_id=data['user_id'],
            post_id=data['post_id'],
            content=data['content']
        )

        db.session.add(new_comment)
        db.session.commit()

        return jsonify(new_comment.serialize()), 201

    except (SQLAlchemyError, ValueError) as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@app.route('/api/comments/<int:comment_id>', methods=['PUT'])
def update_comment(comment_id):
    """Update a comment using modern SQLAlchemy 2.x syntax."""
    try:
        # Modern SQLAlchemy 2.x: Use db.session.get() for primary key lookup
        comment = db.session.get(Comment, comment_id)
        if not comment:
            return jsonify({"error": "Comment not found"}), 404

        data = request.get_json()

        if 'content' in data:
            comment.content = data['content']

        db.session.commit()
        return jsonify(comment.serialize()), 200

    except (SQLAlchemyError, ValueError) as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@app.route('/api/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    """Delete a comment using modern SQLAlchemy 2.x syntax."""
    try:
        # Modern SQLAlchemy 2.x: Use db.session.get() for primary key lookup
        comment = db.session.get(Comment, comment_id)
        if not comment:
            return jsonify({"error": "Comment not found"}), 404

        db.session.delete(comment)
        db.session.commit()

        return jsonify({"message": "Comment deleted successfully"}), 200

    except (SQLAlchemyError, ValueError) as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# ============================================================================
# FOLLOWER CRUD OPERATIONS
# ============================================================================

@app.route('/api/followers', methods=['POST'])
def create_follow_relationship():
    """
    Create a follow relationship.

    Expected JSON:
        {
            "user_from_id": 1,  // follower
            "user_to_id": 2     // being followed
        }
    """
    try:
        data = request.get_json()

        required_fields = ['user_from_id', 'user_to_id']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        # Prevent self-following
        if data['user_from_id'] == data['user_to_id']:
            return jsonify({"error": "Users cannot follow themselves"}), 400

        # Verify both users exist using modern syntax
        follower = db.session.get(User, data['user_from_id'])
        followee = db.session.get(User, data['user_to_id'])

        if not follower:
            return jsonify({"error": "Follower user not found"}), 404
        if not followee:
            return jsonify({"error": "User to follow not found"}), 404

        # Check if relationship already exists using modern syntax
        existing = db.session.execute(
            select(Follower).where(
                (Follower.user_from_id == data['user_from_id']) &
                (Follower.user_to_id == data['user_to_id'])
            )
        ).scalar_one_or_none()

        if existing:
            return jsonify({"error": "Follow relationship already exists"}), 409

        new_follow = Follower(
            user_from_id=data['user_from_id'],
            user_to_id=data['user_to_id']
        )

        db.session.add(new_follow)
        db.session.commit()

        return jsonify(new_follow.serialize()), 201

    except (SQLAlchemyError, ValueError) as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@app.route('/api/users/<int:user_id>/followers', methods=['GET'])
def get_user_followers(user_id):
    """Get all followers of a user using modern SQLAlchemy 2.x syntax."""
    try:
        # Modern SQLAlchemy 2.x: Use db.session.get() for primary key lookup
        user = db.session.get(User, user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Modern SQLAlchemy 2.x: Use db.session.execute() with select() and where()
        followers = db.session.execute(
            select(Follower).where(Follower.user_to_id == user_id)
        ).scalars().all()
        followers_data = []
        for follow in followers:
            follow_data = follow.serialize()
            follow_data['follower_info'] = follow.follower_user.to_json()
            followers_data.append(follow_data)

        return jsonify(followers_data), 200
    except (SQLAlchemyError, ValueError) as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/users/<int:user_id>/following', methods=['GET'])
def get_user_following(user_id):
    """Get all users that a user is following using modern SQLAlchemy 2.x syntax."""
    try:
        # Modern SQLAlchemy 2.x: Use db.session.get() for primary key lookup
        user = db.session.get(User, user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Modern SQLAlchemy 2.x: Use db.session.execute() with select() and where()
        following = db.session.execute(
            select(Follower).where(Follower.user_from_id == user_id)
        ).scalars().all()
        following_data = []
        for follow in following:
            follow_data = follow.serialize()
            follow_data['following_info'] = follow.followed_user.to_json()
            following_data.append(follow_data)

        return jsonify(following_data), 200
    except (SQLAlchemyError, ValueError) as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/followers/<int:follow_id>', methods=['DELETE'])
def unfollow(follow_id):
    """Delete a follow relationship (unfollow) using modern SQLAlchemy 2.x syntax."""
    try:
        # Modern SQLAlchemy 2.x: Use db.session.get() for primary key lookup
        follow = db.session.get(Follower, follow_id)
        if not follow:
            return jsonify({"error": "Follow relationship not found"}), 404

        db.session.delete(follow)
        db.session.commit()

        return jsonify({"message": "Unfollowed successfully"}), 200

    except (SQLAlchemyError, ValueError) as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# ============================================================================
# DATABASE INITIALIZATION AND SERVER STARTUP
# ============================================================================

@app.route('/', methods=['GET'])
def home():
    """Home endpoint with API documentation."""
    return jsonify({
        "message": "Flask Social Media API",
        "version": "1.0",
        "endpoints": {
            "users": "/api/users",
            "posts": "/api/posts",
            "comments": "/api/comments",
            "followers": "/api/followers"
        },
        "documentation": "Visit /api/users, /api/posts, /api/comments for CRUD operations"
    })


if __name__ == '__main__':
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database tables created successfully!")
        print("API endpoints available:")
        print("- GET/POST /api/users")
        print("- GET/PUT/DELETE /api/users/<id>")
        print("- GET/POST /api/posts")
        print("- GET/PUT/DELETE /api/posts/<id>")
        print("- GET/POST /api/comments")
        print("- GET/PUT/DELETE /api/comments/<id>")
        print("- POST /api/followers")
        print("- GET /api/users/<id>/followers")
        print("- GET /api/users/<id>/following")

    # Run the Flask development server
    app.run(debug=True, host='0.0.0.0', port=5000)
