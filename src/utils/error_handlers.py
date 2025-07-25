from flask import jsonify, request
import traceback

def register_error_handlers(app):
    """Register all error handlers with the Flask app"""
    
    @app.errorhandler(400)
    def bad_request_error(error):
        """Handle bad request errors (400)"""
        print(f"🟠 400 Bad Request: {str(error)}")
        return jsonify({
            "error": "Bad request",
            "message": "The request was invalid or malformed."
        }), 400

    @app.errorhandler(401)
    def unauthorized_error(error):
        """Handle unauthorized errors (401)"""
        print(f"🟠 401 Unauthorized: {str(error)}")
        return jsonify({
            "error": "Unauthorized",
            "message": "Authentication required or invalid credentials."
        }), 401

    @app.errorhandler(403)
    def forbidden_error(error):
        """Handle forbidden errors (403)"""
        print(f"🟠 403 Forbidden: {str(error)}")
        return jsonify({
            "error": "Forbidden",
            "message": "You don't have permission to access this resource."
        }), 403

    @app.errorhandler(404)
    def not_found_error(error):
        """Handle not found errors (404)"""
        print(f"🟡 404 Not Found: {request.url}")
        return jsonify({
            "error": "Not found",
            "message": "The requested resource was not found."
        }), 404

    @app.errorhandler(408)
    def request_timeout_error(error):
        """Handle request timeout errors (408)"""
        print(f"🟠 408 Request Timeout: {str(error)}")
        return jsonify({
            "error": "Request timeout",
            "message": "The request took too long to process. Please try again."
        }), 408

    @app.errorhandler(413)
    def request_entity_too_large(error):
        """Handle file too large errors (413)"""
        from src.config import Config
        max_size_mb = Config.MAX_CONTENT_IN_MB
        print(f"🟠 413 File Too Large: Request exceeded {max_size_mb}MB limit")
        return jsonify({
            "error": "File too large",
            "message": f"File size exceeds the maximum allowed limit of {max_size_mb}MB."
        }), 413

    @app.errorhandler(422)
    def unprocessable_entity(error):
        """Handle validation errors (422)"""
        print(f"🟠 422 Unprocessable Entity: {str(error)}")
        return jsonify({
            "error": "Validation error",
            "message": "The request was well-formed but contains semantic errors."
        }), 422

    @app.errorhandler(429)
    def too_many_requests(error):
        """Handle rate limiting errors (429)"""
        print(f"🟠 429 Too Many Requests: {str(error)}")
        return jsonify({
            "error": "Too many requests",
            "message": "Rate limit exceeded. Please try again later."
        }), 429

    @app.errorhandler(500)
    def internal_server_error(error):
        """Handle internal server errors (500)"""
        error_msg = f"500 Internal Server Error: {str(error)}"
        
        # Print to console with request details
        print(f"🔴 {error_msg}")
        print(f"🔍 Request URL: {request.url}")
        print(f"🔍 Request Method: {request.method}")
        
        # Log to Flask logger
        app.logger.error(error_msg, exc_info=True)
        
        return jsonify({
            "error": "Internal server error",
            "message": "Something went wrong on our end. Please try again later."
        }), 500

    @app.errorhandler(503)
    def service_unavailable_error(error):
        """Handle service unavailable errors (503)"""
        print(f"🔴 503 Service Unavailable: {str(error)}")
        return jsonify({
            "error": "Service unavailable",
            "message": "The service is temporarily unavailable. Please try again later."
        }), 503

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        """Handle all unexpected exceptions to prevent app crashes"""
        error_msg = f"Unexpected Error: {str(error)}"
        error_type = type(error).__name__
        
        # Print detailed error info to console
        print(f"🔴 EXCEPTION CAUGHT: {error_msg}")
        print(f"📍 Error Type: {error_type}")
        print(f"🔍 Request URL: {request.url}")
        print(f"🔍 Request Method: {request.method}")
        
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
                "url": request.url,
                "method": request.method,
                "debug": True
            }), 500
        else:
            return jsonify({
                "error": "Internal server error",
                "message": "An unexpected error occurred. Please try again later."
            }), 500

    @app.errorhandler(ConnectionError)
    def handle_connection_error(error):
        """Handle database/connection errors"""
        error_msg = f"Connection Error: {str(error)}"
        print(f"🔴 DATABASE CONNECTION ERROR: {error_msg}")
        
        app.logger.error(error_msg, exc_info=True)
        
        return jsonify({
            "error": "Service unavailable",
            "message": "Unable to connect to the database. Please try again later."
        }), 503

    @app.errorhandler(TimeoutError)
    def handle_timeout_error(error):
        """Handle timeout errors"""
        error_msg = f"Timeout Error: {str(error)}"
        print(f"🔴 TIMEOUT ERROR: {error_msg}")
        
        app.logger.error(error_msg, exc_info=True)
        
        return jsonify({
            "error": "Request timeout",
            "message": "The request took too long to process. Please try again."
        }), 408

    # Log successful registration
    print("✅ Error handlers registered successfully!")
    print("📋 Registered handlers: 400, 401, 403, 404, 408, 413, 422, 429, 500, 503")
    print("🔧 Exception handlers: Exception, ConnectionError, TimeoutError")
    print("🛡️ App crash protection: ENABLED")
