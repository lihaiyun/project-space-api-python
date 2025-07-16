import jwt
from functools import wraps
from flask import request, jsonify
from src.config import Config

def token_required(f):
    """
    Decorator to protect routes that require authentication.
    Usage: @token_required above your route function
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Check for token in cookies
        if 'accessToken' in request.cookies:
            token = request.cookies.get('accessToken')
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            # Decode the token
            payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
            
            # Get the user from database
            current_user = payload
            if not current_user:
                return jsonify({'error': 'User not found'}), 401
                
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token is invalid'}), 401
        except Exception as e:
            return jsonify({'error': 'Token verification failed'}), 401
        
        # Pass the current user to the route
        return f(current_user, *args, **kwargs)
    
    return decorated
