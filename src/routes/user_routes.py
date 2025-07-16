from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from src.models.user import User
from src.schemas.user_schema import UserSchema

bp = Blueprint("users", __name__, url_prefix="/users")
user_schema = UserSchema()
users_schema = UserSchema(many=True)

@bp.route("/", methods=["GET"])
def list_users():
    users = User.objects()
    return jsonify(users_schema.dump(users))

@bp.route("/", methods=["POST"])
def create_user():
    try:
        # Validate input data using schema
        data = user_schema.load(request.get_json())
        user = User(**data).save()
        return jsonify(user_schema.dump(user)), 201
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    except Exception as err:
        return jsonify({"error": str(err)}), 500
