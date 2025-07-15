from flask import Blueprint, request, jsonify
from src.models.user import User

bp = Blueprint("users", __name__, url_prefix="/users")

@bp.route("/", methods=["GET"])
def list_users():
    users = User.objects()
    return jsonify([u.to_json() for u in users])

@bp.route("/", methods=["POST"])
def create_user():
    data = request.get_json()
    user = User(**data).save()
    return jsonify(user.to_json()), 201
