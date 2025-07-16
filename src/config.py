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
