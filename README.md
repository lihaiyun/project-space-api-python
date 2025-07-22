# Project Space API - Python

A Flask REST API for project management with user authentication using JWT tokens and MongoDB.

## Features

- User authentication (register, login, logout)
- JWT token-based authentication with HTTP-only cookies
- Project CRUD operations
- User and project relationship management
- MongoDB with MongoEngine ODM
- Input validation with Marshmallow schemas
- Environment-aware cookie security settings

## Tech Stack

- **Backend:** Flask, MongoEngine
- **Database:** MongoDB
- **Authentication:** JWT with HTTP-only cookies
- **Validation:** Marshmallow
- **Environment:** Python 3.x

## Setup

### Prerequisites
- Python 3.x
- MongoDB (running locally or connection string)

### Installation

1. **Create virtual environment:**
   
   This creates a `.venv` folder in your project directory.
   ```bash
   python -m venv .venv
   ```

2. **Activate virtual environment:**
   ```bash
   # Windows
   .venv\Scripts\activate
   
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **VS Code Setup (optional):**
   
   VS Code will usually detect `.venv` automatically. If not:
   - Press `Ctrl+Shift+P` → `Python: Select Interpreter` → select `.venv`

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Verify installation:**
   
   Check that Flask is installed:
   ```bash
   pip list
   ```

### Environment Configuration

Create a `.env` file in the root directory:

```env
MONGODB_URI=mongodb://localhost:27017/mydb
JWT_SECRET_KEY=your-super-secret-jwt-key
JWT_EXPIRATION_DAYS=7
FLASK_ENV=development
```

### Database Setup

Make sure MongoDB is running locally:
- The database and collections will be created automatically
- Default connection: `mongodb://localhost:27017/mydb`

## Running the Application

```bash
python -m src.app
```

The API will be available at: `http://localhost:5000`

## API Endpoints

### Authentication
- `POST /users/register` - Register new user
- `POST /users/login` - Login user
- `POST /users/logout` - Logout user
- `GET /users/auth` - Get current user info


### Projects
- `GET /projects/` - List all projects
- `POST /projects/` - Create project (auth required)
- `GET /projects/<id>` - Get specific project
- `PUT /projects/<id>` - Update project (auth required)
- `DELETE /projects/<id>` - Delete project (auth required)

## API Usage Examples

### Register User
```bash
curl -X POST http://localhost:5000/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "password123"
  }'
```

### Login
```bash
curl -X POST http://localhost:5000/users/login \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{
    "email": "john@example.com",
    "password": "password123"
  }'
```

### Create Project
```bash
curl -X POST http://localhost:5000/projects/ \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "name": "My Project",
    "description": "Project description",
    "dueDate": "2025-12-31",
    "status": "not-started"
  }'
```

## Project Structure

```
src/
├── __init__.py
├── app.py              # Main Flask application
├── config.py           # Configuration settings
├── models/             # Database models
│   ├── user.py
│   └── project.py
├── routes/             # API routes
│   ├── user_routes.py
│   └── project_routes.py
├── schemas/            # Validation schemas
│   ├── user_schema.py
│   ├── auth_schema.py
│   └── project_schema.py
└── utils/              # Utility functions
    ├── auth.py         # Authentication decorators
    └── cookies.py      # Cookie utilities
```

## Security Features

- Password hashing with Werkzeug
- JWT tokens stored in HTTP-only cookies
- Environment-aware cookie security settings
- Input validation and sanitization
- CORS support for frontend integration

## Production Deployment

### Quick Start
```bash
# Windows
start-production.bat

# Linux/Mac
chmod +x start-production.sh
./start-production.sh

# Manual
gunicorn -c gunicorn.conf.py src.app:app
```

### Production Checklist

Before deploying to production:

1. **Environment Variables:**
   ```bash
   FLASK_ENV=production
   JWT_SECRET_KEY=your-strong-secret-key-here
   MONGODB_URI=your-production-mongodb-connection
   FRONTEND_URL=https://your-frontend-domain.com
   WORKERS=2  # Adjust based on CPU cores
   ```

2. **Security:**
   - Use strong, unique JWT secret key
   - Configure HTTPS (update `FRONTEND_URL` to https)
   - Set proper CORS origins
   - Use environment-specific MongoDB credentials

3. **Performance:**
   - Set `WORKERS` to 2x CPU cores (recommended)
   - Configure load balancer if needed
   - Monitor memory usage with `max_requests=1000`

4. **Monitoring:**
   - Check logs: Gunicorn logs to stdout/stderr
   - Set `LOG_LEVEL=info` or `warning` for production

## Development

The application runs in debug mode by default when using `python -m src.app`.

For production deployment, make sure to:
- Set `FLASK_ENV=production`
- Use strong secret keys
- Configure proper CORS settings
- Use HTTPS for secure cookies
