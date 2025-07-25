from flask import Flask
from flask_cors import CORS
from mongoengine import connect
from src.routes import user_routes, project_routes, file_route
from src.config import Config
from src.utils.error_handlers import register_error_handlers

app = Flask(__name__)
app.config.from_object(Config)

# Set max content length for file uploads
app.config['MAX_CONTENT_LENGTH'] = Config.MAX_CONTENT_LENGTH

# Configure CORS with specific origins and credentials support
CORS(app, 
     origins=Config.CORS_ORIGINS,
     supports_credentials=Config.CORS_SUPPORTS_CREDENTIALS,
     methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS', 'HEAD'],
     expose_headers=['Set-Cookie', 'Content-Type', 'Authorization'])

# Disable strict slashes to prevent redirects
app.url_map.strict_slashes = False

connect(host=app.config["MONGODB_URI"])

# Register comprehensive error handlers from utils
register_error_handlers(app)

@app.route('/')
def hello():
    return {"message": "Hello! Welcome to the Project Space API"}

# Test routes for exception handling - REMOVE IN PRODUCTION
@app.route('/test-exception')
def test_exception():
    """Test route to trigger general exception"""
    raise Exception("This is a test exception to verify error handlers!")

app.register_blueprint(user_routes.bp)
app.register_blueprint(project_routes.bp)
app.register_blueprint(file_route.bp)

if __name__ == "__main__":
    # This is only for development - use Gunicorn for production
    print("Running in development mode...")
    print("For production, use: gunicorn -c gunicorn.conf.py src.app:app")
    app.run(debug=True, port=5000)
