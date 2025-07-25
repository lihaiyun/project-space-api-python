# Project Space API - Python

A comprehensive Flask REST API for project management with user authentication, file uploads, and advanced error handling.

## 🚀 Features

### **Authentication & Security**
- User authentication (register, login, logout) with JWT tokens
- HTTP-only cookies for secure token storage
- Environment-aware cookie security settings
- Comprehensive CORS configuration for frontend integration
- Owner-based authorization for project operations

### **Project Management**
- Full CRUD operations for projects
- Advanced search functionality (case-insensitive)
- Sorting by multiple fields (dueDate, createdAt, name, status)
- Pagination support with metadata
- Owner permission controls

### **File Management**
- Cloudinary integration for image uploads
- File size validation and security checks
- Image transformation capabilities
- Organized file storage with folder structure

### **Error Handling & Monitoring**
- Global error handlers for all HTTP status codes
- Detailed console logging with color-coded messages
- Environment-aware error responses (detailed in dev, secure in prod)
- Comprehensive exception handling

### **Developer Experience**
- Input validation with Marshmallow schemas
- Modular code structure with blueprints
- Production-ready Gunicorn configuration
- Environment variable management
- Comprehensive API documentation

## 🛠️ Tech Stack

- **Backend:** Flask 3.0.3, MongoEngine 0.29.1
- **Database:** MongoDB
- **Authentication:** PyJWT 2.8.0 with HTTP-only cookies
- **Validation:** Marshmallow 3.21.1
- **File Storage:** Cloudinary 1.41.0, Pillow 10.4.0
- **CORS:** Flask-CORS 4.0.1
- **Production:** Gunicorn 23.0.0
- **Environment:** Python 3.11+

## 📋 Prerequisites

- Python 3.11 or higher
- MongoDB (running locally or connection string)
- Cloudinary account (for file uploads)

## 🔧 Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd project-space-api-python
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv .venv
   ```

3. **Activate virtual environment:**
   ```bash
   # Windows
   .venv\Scripts\activate
   
   # macOS/Linux
   source .venv/bin/activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Environment Configuration

Create a `.env` file in the root directory:

```env
# Flask Environment
FLASK_ENV=development

# Database
MONGODB_URI=mongodb://localhost:27017/project_space_db

# JWT Configuration
JWT_SECRET_KEY=your-super-secret-jwt-key-change-in-production
JWT_EXPIRATION_DAYS=7

# Frontend URL for CORS
FRONTEND_URL=http://localhost:3000

# Gunicorn Settings (Production)
PORT=5000
WORKERS=2
LOG_LEVEL=info

# Cloudinary Configuration (for file uploads)
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

## 🗄️ Database Setup
JWT_EXPIRATION_DAYS=7
FLASK_ENV=development

### Database Setup

Make sure MongoDB is running locally:
- The database and collections will be created automatically
- Default connection: `mongodb://localhost:27017/project_space_db`

## 🚀 Running the Application

### Development Mode
```bash
python -m src.app
```

### Production Mode
```bash
# Windows
start-production.bat

# Linux/Mac
chmod +x start-production.sh
./start-production.sh

# Manual
gunicorn -c gunicorn.conf.py src.app:app
```

The API will be available at: `http://localhost:5000`

## 📚 API Endpoints

### 🔐 Authentication
- `POST /users/register` - Register new user
- `POST /users/login` - Login user  
- `POST /users/logout` - Logout user
- `GET /users/auth` - Get current user info

### 📁 Projects
- `GET /projects/` - List projects with search, sort, pagination
- `POST /projects/` - Create project (auth required)
- `GET /projects/<id>` - Get specific project
- `PUT /projects/<id>` - Update project (auth required, owner only)
- `DELETE /projects/<id>` - Delete project (auth required, owner only)

#### Project Search & Filtering
```bash
# Search projects
GET /projects/?search=website&limit=10&skip=0

# Sort projects
GET /projects/?sort=dueDate&order=desc

# Combined
GET /projects/?search=api&sort=createdAt&order=asc&limit=5
```

### 📎 File Management
- `POST /files/upload` - Upload image to Cloudinary (auth required)
- `DELETE /files/<public_id>` - Delete image from Cloudinary (auth required)
- `GET /files/<public_id>/info` - Get image information

## 🔧 API Usage Examples

### 👤 Register User
```bash
curl -X POST http://localhost:5000/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "password123"
  }'
```

### 🔑 Login
```bash
curl -X POST http://localhost:5000/users/login \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{
    "email": "john@example.com",
    "password": "password123"
  }'
```

### 📁 Create Project
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

### 📎 Upload File
```bash
curl -X POST http://localhost:5000/files/upload \
  -H "Authorization: Bearer <your-jwt-token>" \
  -F "file=@image.jpg"
```

## 📁 Project Structure

```
src/
├── __init__.py
├── app.py                    # Main Flask application with CORS & error handling
├── config.py                 # Environment configuration
├── models/
│   ├── __init__.py
│   ├── user.py              # User model with MongoEngine
│   └── project.py           # Project model with relationships
├── routes/
│   ├── __init__.py
│   ├── user_routes.py       # Authentication endpoints
│   ├── project_routes.py    # Project CRUD with search/sort
│   └── file_route.py        # Cloudinary file upload endpoints
├── schemas/
│   ├── user_schema.py       # User validation schemas
│   ├── auth_schema.py       # Login/register validation
│   └── project_schema.py    # Project validation schemas
└── utils/
    ├── __init__.py
    ├── auth.py              # JWT token verification decorator
    ├── cookies.py           # Cookie management utilities
    └── error_handlers.py    # Global error handling system
```

## 🔒 Security Features

- **JWT Authentication**: Secure token-based auth with HTTP-only cookies
- **Owner Authorization**: Users can only modify their own projects
- **Input Validation**: Comprehensive validation with Marshmallow
- **CORS Protection**: Configured for specific frontend origins
- **File Upload Security**: Size limits and type validation
- **Environment-aware**: Different security settings for dev/prod

## 🚀 Production Deployment
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
   - Configure Cloudinary for production

3. **Performance:**
   - Set `WORKERS` to 2x CPU cores (recommended)
   - Configure load balancer if needed
   - Monitor memory usage with `max_requests=1000`

4. **Monitoring:**
   - Check logs: Gunicorn logs to stdout/stderr
   - Set `LOG_LEVEL=info` or `warning` for production
   - Monitor error rates and performance

## 🐛 Development & Debugging

### Error Handling
- Comprehensive global error handlers
- Color-coded console logging (🔴 🟡 🟠)
- Stack traces in development mode
- Production-safe error messages

### Testing Error Handlers
```bash
# Test routes (remove in production)
GET /test-error     # Triggers exception handler
GET /test-500       # Triggers division by zero
GET /nonexistent    # Triggers 404 handler
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Related Projects

- **Frontend**: Connect with React, Vue, or Angular
- **Mobile**: Use the API with React Native or Flutter
- **Desktop**: Integrate with Electron or desktop frameworks

---

## 📞 Support

For questions or issues:
1. Check the API documentation above
2. Review error messages in console
3. Check environment variable configuration
4. Verify MongoDB connection

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
