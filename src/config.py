import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/mydb")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-secret-key")
    JWT_EXPIRATION_DAYS = int(os.getenv("JWT_EXPIRATION_DAYS", "7"))
    
    # Environment-aware cookie settings
    IS_PRODUCTION = os.getenv("FLASK_ENV", "development") == "production"
    COOKIE_SECURE = IS_PRODUCTION
    COOKIE_SAMESITE = "None" if IS_PRODUCTION else "Lax"
    
    # CORS settings
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
    CORS_ORIGINS = [FRONTEND_URL]
    CORS_SUPPORTS_CREDENTIALS = True
    
    # Cloudinary settings
    CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
    CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")
    
    # File upload settings
    MAX_CONTENT_IN_MB = 10  # 10MB max file size
    MAX_CONTENT_LENGTH = MAX_CONTENT_IN_MB * 1024 * 1024  # Convert to bytes for Flask
    UPLOAD_FOLDER = 'projects'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
