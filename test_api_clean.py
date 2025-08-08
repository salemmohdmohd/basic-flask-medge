"""
API Testing Script for Flask Social Media CRUD Operations

This script demonstrates how to use the CRUD API endpoints.
You can run this script to test all the API functionality.

Make sure your Flask server is running on http://localhost:5000
"""

import json
import requests

BASE_URL = "http://localhost:5000/api"

def print_response(response, operation):
    """Helper function to print API responses nicely."""
    print(f"\n{'='*50}")
    print(f"{operation}")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except (ValueError, TypeError, json.JSONDecodeError):
        print(f"Response: {response.text}")
    print(f"{'='*50}")

def test_crud_operations():
    """Test all CRUD operations for the social media API."""

    print("Starting CRUD API Tests...")

    # Initialize variables to avoid "possibly-used-before-assignment" warnings
    user1_id = None
    user2_id = None
    post1_id = None
    comment1_id = None

    # ============================================================================
    # USER CRUD TESTS
    # ============================================================================

    print("\nTESTING USER OPERATIONS")

    # 1. Create users
    user1_data = {
        "email": "john.doe@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "password": "securepass123"
    }

    user2_data = {
        "email": "jane.smith@example.com",
        "first_name": "Jane",
        "last_name": "Smith",
        "password": "anotherpass456"
    }

    # Create first user
    response = requests.post(f"{BASE_URL}/users", json=user1_data)
    print_response(response, "CREATE USER 1")
    user1_id = response.json().get('id') if response.status_code == 201 else None

    # Create second user
    response = requests.post(f"{BASE_URL}/users", json=user2_data)
    print_response(response, "CREATE USER 2")
    user2_id = response.json().get('id') if response.status_code == 201 else None

    # 2. Get all users
    response = requests.get(f"{BASE_URL}/users")
    print_response(response, "GET ALL USERS")

    # 3. Get specific user
    if user1_id:
        response = requests.get(f"{BASE_URL}/users/{user1_id}")
        print_response(response, f"GET USER {user1_id}")

    # 4. Update user
    if user1_id:
        update_data = {"first_name": "Johnny", "last_name": "Updated"}
        response = requests.put(f"{BASE_URL}/users/{user1_id}", json=update_data)
        print_response(response, f"UPDATE USER {user1_id}")

    # ============================================================================
    # POST CRUD TESTS
    # ============================================================================

    print("\nTESTING POST OPERATIONS")

    # 1. Create posts
    if user1_id:
        post1_data = {
            "user_id": user1_id,
            "image_url": "https://example.com/sunset.jpg",
            "caption": "Beautiful sunset at the beach!"
        }

        response = requests.post(f"{BASE_URL}/posts", json=post1_data)
        print_response(response, "CREATE POST 1")
        post1_id = response.json().get('id') if response.status_code == 201 else None

    if user2_id:
        post2_data = {
            "user_id": user2_id,
            "image_url": "https://example.com/coffee.jpg",
            "caption": "Morning coffee"
        }

        response = requests.post(f"{BASE_URL}/posts", json=post2_data)
        print_response(response, "CREATE POST 2")

    # 2. Get all posts
    response = requests.get(f"{BASE_URL}/posts")
    print_response(response, "GET ALL POSTS")

    # 3. Update post
    if post1_id:
        update_data = {"caption": "Updated caption: Amazing sunset!"}
        response = requests.put(f"{BASE_URL}/posts/{post1_id}", json=update_data)
        print_response(response, f"UPDATE POST {post1_id}")

    # ============================================================================
    # COMMENT CRUD TESTS
    # ============================================================================

    print("\nTESTING COMMENT OPERATIONS")

    # 1. Create comments
    if post1_id and user2_id:
        comment1_data = {
            "user_id": user2_id,
            "post_id": post1_id,
            "content": "Wow, such a beautiful photo!"
        }

        response = requests.post(f"{BASE_URL}/comments", json=comment1_data)
        print_response(response, "CREATE COMMENT 1")
        comment1_id = response.json().get('id') if response.status_code == 201 else None

    if post1_id and user1_id:
        comment2_data = {
            "user_id": user1_id,
            "post_id": post1_id,
            "content": "Thank you! It was an amazing moment."
        }

        response = requests.post(f"{BASE_URL}/comments", json=comment2_data)
        print_response(response, "CREATE COMMENT 2")

    # 2. Get comments for a post
    if post1_id:
        response = requests.get(f"{BASE_URL}/posts/{post1_id}/comments")
        print_response(response, f"GET COMMENTS FOR POST {post1_id}")

    # 3. Update comment
    if comment1_id:
        update_data = {"content": "Updated: Absolutely stunning!"}
        response = requests.put(f"{BASE_URL}/comments/{comment1_id}", json=update_data)
        print_response(response, f"UPDATE COMMENT {comment1_id}")

    # ============================================================================
    # FOLLOWER CRUD TESTS
    # ============================================================================

    print("\nTESTING FOLLOWER OPERATIONS")

    # 1. Create follow relationship (user1 follows user2)
    if user1_id and user2_id:
        follow_data = {
            "user_from_id": user1_id,
            "user_to_id": user2_id
        }

        response = requests.post(f"{BASE_URL}/followers", json=follow_data)
        print_response(response, f"USER {user1_id} FOLLOWS USER {user2_id}")

    # 2. Get followers
    if user2_id:
        response = requests.get(f"{BASE_URL}/users/{user2_id}/followers")
        print_response(response, f"GET FOLLOWERS OF USER {user2_id}")

    # 3. Get following
    if user1_id:
        response = requests.get(f"{BASE_URL}/users/{user1_id}/following")
        print_response(response, f"GET WHO USER {user1_id} IS FOLLOWING")

    print("\nCRUD Tests Completed!")
    print("\nAPI Documentation:")
    print("- All endpoints support JSON input/output")
    print("- CORS is enabled for frontend integration")
    print("- Error handling with proper HTTP status codes")
    print("- Relationships are properly maintained")

if __name__ == "__main__":
    try:
        test_crud_operations()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the Flask server.")
        print("Make sure the Flask app is running on http://localhost:5000")
        print("Run: pipenv run start")
    except (requests.exceptions.RequestException, ValueError, TypeError) as e:
        print(f"Error: {e}")
