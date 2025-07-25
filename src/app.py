from flask import Flask, jsonify
from flask_cors import CORS
from mongoengine import connect
from src.routes import user_routes, project_routes, file_route
from src.config import Config

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

# Global Error Handlers
@app.errorhandler(404)
def not_found_error(error):
    """Handle not found errors (404)"""
    return jsonify({
        "error": "Not found",
        "message": "The requested resource was not found."
    }), 404

@app.errorhandler(Exception)
def handle_unexpected_error(error):
    """Handle all unexpected exceptions to prevent app crashes"""
    import traceback
    
    error_msg = f"Unexpected Error: {str(error)}"
    error_type = type(error).__name__
    
    # Print detailed error info to console
    print(f"🔴 EXCEPTION CAUGHT: {error_msg}")
    print(f"📍 Error Type: {error_type}")
    
    if app.debug:
        print("📋 Stack Trace:")
        traceback.print_exc()
    
    # Log the error with full stack trace
    app.logger.error(error_msg, exc_info=True)
    
    # Return appropriate response based on environment
    if app.debug:
        return jsonify({
            "error": "Unexpected error",
            "message": str(error),
            "type": error_type,
            "debug": True
        }), 500
    else:
        return jsonify({
            "error": "Internal server error",
            "message": "An unexpected error occurred. Please try again later."
        }), 500

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
