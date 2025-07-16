from flask import Blueprint, request, jsonify, make_response
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta, timezone
from src.models.user import User
from src.schemas.user_schema import UserSchema
from src.schemas.auth_schema import UserRegisterSchema, UserLoginSchema
from src.config import Config
from src.utils.cookies import set_auth_cookie, clear_auth_cookie

bp = Blueprint("users", __name__, url_prefix="/users")
user_schema = UserSchema()
users_schema = UserSchema(many=True)
register_schema = UserRegisterSchema()
login_schema = UserLoginSchema()

@bp.route("/", methods=["GET"])
def list_users():
    users = User.objects()
    return jsonify(users_schema.dump(users))

@bp.route("/", methods=["POST"])
def register_user():
    try:
        # Use UserRegisterSchema for validation
        user_data = register_schema.load(request.get_json())
        
        # Check if email already exists
        existing_user = User.objects(email=user_data['email']).first()
        if existing_user:
            return jsonify({"errors": {"email": ["Email already exists"]}}), 400
        
        # Hash the password before saving
        user_data['password'] = generate_password_hash(user_data['password'])
        
        # Create new user with validated data
        new_user = User(**user_data)
        new_user.save()
        
        # Return user data without password using UserSchema
        return jsonify(user_schema.dump(new_user)), 201
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    except Exception as err:
        return jsonify({"error": str(err)}), 500

@bp.route("/login", methods=["POST"])
def login_user():
    try:
        # Use UserLoginSchema for validation
        login_data = login_schema.load(request.get_json())
        
        # Find user by email
        user = User.objects(email=login_data['email']).first()
        
        # Check if user exists and password is correct
        if user and check_password_hash(user.password, login_data['password']):
            # Generate JWT token
            payload = {
                'user_id': str(user.id),
                'email': user.email,
                'exp': datetime.now(timezone.utc) + timedelta(days=Config.JWT_EXPIRATION_DAYS),
                'iat': datetime.now(timezone.utc)
            }
            
            token = jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm='HS256')
            
            # Create response with user data
            response_data = {
                "message": "Login successful",
                "user": user_schema.dump(user)
            }
            
            response = make_response(jsonify(response_data), 200)
            
            # Set authentication cookie with environment-aware options
            set_auth_cookie(response, token)
            
            return response
        else:
            return jsonify({"errors": {"credentials": ["Invalid email or password"]}}), 401
            
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    except Exception as err:
        return jsonify({"error": str(err)}), 500

@bp.route("/logout", methods=["POST"])
def logout_user():
    response = make_response(jsonify({"message": "Logout successful"}), 200)

    # Clear authentication cookie with consistent options
    clear_auth_cookie(response)
    
    return response
