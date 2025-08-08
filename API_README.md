# Flask Social Media CRUD API

A comprehensive RESTful API built with Flask for managing social media data including users, posts, comments, and follower relationships.

## 🚀 Features

- **Complete CRUD Operations** for all entities
- **RESTful API Design** with proper HTTP methods
- **CORS Support** for frontend integration
- **Modern SQLAlchemy 2.x** with typed relationships
- **JSON Input/Output** with proper error handling
- **Relationship Management** between entities
- **Database Auto-Creation** on startup

## 📋 Prerequisites

- Python 3.8+
- pipenv

## 🛠️ Installation

1. **Clone and navigate to the project:**

   ```bash
   cd /path/to/newprojectflask
   ```

2. **Install dependencies:**

   ```bash
   pipenv install
   ```

3. **Start the API server:**

   ```bash
   pipenv run start
   ```

4. **The API will be available at:**
   - Local: `http://127.0.0.1:5000`
   - Network: `http://[your-local-ip]:5000` (displayed in terminal when starting)

## 📚 API Documentation

### Base URL

```
http://localhost:5000/api
```

### 👤 User Operations

#### Create User

```bash
POST /api/users
Content-Type: application/json

{
    "email": "john.doe@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "password": "securepassword"
}
```

#### Get All Users

```bash
GET /api/users
```

#### Get User by ID

```bash
GET /api/users/1
```

#### Update User

```bash
PUT /api/users/1
Content-Type: application/json

{
    "first_name": "Updated Name",
    "email": "newemail@example.com"
}
```

#### Delete User

```bash
DELETE /api/users/1
```

### 📸 Post Operations

#### Create Post

```bash
POST /api/posts
Content-Type: application/json

{
    "user_id": 1,
    "image_url": "https://example.com/image.jpg",
    "caption": "Beautiful sunset! 🌅"
}
```

#### Get All Posts

```bash
GET /api/posts
```

#### Get Post by ID

```bash
GET /api/posts/1
```

#### Update Post

```bash
PUT /api/posts/1
Content-Type: application/json

{
    "caption": "Updated caption text"
}
```

#### Delete Post

```bash
DELETE /api/posts/1
```

### 💬 Comment Operations

#### Create Comment

```bash
POST /api/comments
Content-Type: application/json

{
    "user_id": 1,
    "post_id": 1,
    "content": "Great photo!"
}
```

#### Get All Comments

```bash
GET /api/comments
```

#### Get Comments for a Post

```bash
GET /api/posts/1/comments
```

#### Update Comment

```bash
PUT /api/comments/1
Content-Type: application/json

{
    "content": "Updated comment text"
}
```

#### Delete Comment

```bash
DELETE /api/comments/1
```

### 👥 Follower Operations

#### Follow a User

```bash
POST /api/followers
Content-Type: application/json

{
    "user_from_id": 1,  // follower
    "user_to_id": 2     // being followed
}
```

#### Get User's Followers

```bash
GET /api/users/1/followers
```

#### Get Who User is Following

```bash
GET /api/users/1/following
```

#### Unfollow

```bash
DELETE /api/followers/1
```

## 🧪 Testing the API

### Using cURL

1. **Test the home endpoint:**

   ```bash
   curl http://localhost:5000/
   ```

2. **Create a user:**

   ```bash
   curl -X POST http://localhost:5000/api/users \
     -H "Content-Type: application/json" \
     -d '{
       "email": "test@example.com",
       "first_name": "Test",
       "last_name": "User",
       "password": "test123"
     }'
   ```

3. **Get all users:**
   ```bash
   curl http://localhost:5000/api/users
   ```

### Using the Test Script

Run the comprehensive test script:

```bash
pipenv run python test_api.py
```

This will test all CRUD operations for all entities.

## 📊 Database Schema

### Users Table

- `id` (Primary Key)
- `email` (Unique)
- `first_name`
- `last_name`
- `password`
- `is_active`

### Posts Table

- `id` (Primary Key)
- `user_id` (Foreign Key → users.id)
- `image_url`
- `caption`

### Comments Table

- `id` (Primary Key)
- `user_id` (Foreign Key → users.id)
- `post_id` (Foreign Key → posts.id)
- `content`

### Followers Table

- `id` (Primary Key)
- `user_from_id` (Foreign Key → users.id)
- `user_to_id` (Foreign Key → users.id)

## 🔧 Available Scripts

```bash
# Start the API server
pipenv run start

# Initialize database only
pipenv run init-db

# Generate database diagram
pipenv run diagram

# Run in development mode
pipenv run dev
```

## 🛡️ Error Handling

The API returns proper HTTP status codes:

- `200` - Success
- `201` - Created
- `400` - Bad Request (missing fields)
- `404` - Not Found
- `409` - Conflict (duplicate email, etc.)
- `500` - Internal Server Error

Example error response:

```json
{
  "error": "Missing required field: email"
}
```

## 🌐 CORS Support

CORS is enabled for all origins, making it easy to integrate with frontend applications running on different ports.

## 📝 Example Frontend Integration

```javascript
// Example: Create a user from JavaScript
fetch("http://localhost:5000/api/users", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    email: "user@example.com",
    first_name: "John",
    last_name: "Doe",
    password: "secure123",
  }),
})
  .then((response) => response.json())
  .then((data) => console.log("User created:", data));
```

## 🔐 Security Notes

- **Password Storage**: Currently stores plain text passwords. In production, implement proper password hashing (bcrypt, Argon2, etc.)
- **Authentication**: No authentication implemented. Add JWT or session-based auth for production
- **Input Validation**: Basic validation implemented. Consider more robust validation
- **Rate Limiting**: Not implemented. Add rate limiting for production APIs

## 🚧 Development

### Project Structure

```
src/
├── main.py          # Main API application with all routes
├── app.py           # Database initialization script
├── models.py        # SQLAlchemy models
└── extensions.py    # Flask extensions
test_api.py          # API testing script
```

### Adding New Endpoints

1. Add route to `src/main.py`
2. Follow existing patterns for error handling
3. Update this documentation
4. Add tests to `test_api.py`

## 📄 License

This project is for educational purposes.
