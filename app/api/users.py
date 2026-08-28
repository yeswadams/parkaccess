from flask import Blueprint, jsonify, request

from app.models import User, db
from app.schemas import UserSchema

bp = Blueprint("users", __name__, url_prefix="/users")


@bp.route("", methods=["GET"])
def list_users():
    users = User.query.all()
    return jsonify([UserSchema.dump(user) for user in users])


@bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(UserSchema.dump(user))


@bp.route("", methods=["POST"])
def create_user():
    payload = request.get_json(silent=True) or {}
    if not payload.get("username") or not payload.get("email"):
        return jsonify({"error": "username and email are required"}), 400

    user = User(username=payload.get("username"), email=payload.get("email"))

    db.session.add(user)
    db.session.commit()
    return jsonify(UserSchema.dump(user)), 201


@bp.route("/<int:user_id>", methods=["PUT", "PATCH"])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    payload = request.get_json(silent=True) or {}

    for field in ["username", "email"]:
        if field in payload:
            setattr(user, field, payload[field])

    db.session.commit()
    return jsonify(UserSchema.dump(user))


@bp.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"})
