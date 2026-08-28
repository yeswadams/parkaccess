from flask import Blueprint, jsonify, request

from app.models import Checkpoint, db
from app.schemas import CheckpointSchema

bp = Blueprint("checkpoints", __name__, url_prefix="/checkpoints")


@bp.route("", methods=["GET"])
def list_checkpoints():
    checkpoints = Checkpoint.query.all()
    return jsonify([CheckpointSchema.dump(checkpoint) for checkpoint in checkpoints])


@bp.route("/<int:checkpoint_id>", methods=["GET"])
def get_checkpoint(checkpoint_id):
    checkpoint = Checkpoint.query.get_or_404(checkpoint_id)
    return jsonify(CheckpointSchema.dump(checkpoint))


@bp.route("", methods=["POST"])
def create_checkpoint():
    payload = request.get_json(silent=True) or {}
    if not payload.get("name"):
        return jsonify({"error": "name is required"}), 400

    checkpoint = Checkpoint(
        estate_id=payload.get("estate_id"),
        court_id=payload.get("court_id"),
        name=payload.get("name"),
        type=payload.get("type"),
    )

    db.session.add(checkpoint)
    db.session.commit()
    return jsonify(CheckpointSchema.dump(checkpoint)), 201


@bp.route("/<int:checkpoint_id>", methods=["PUT", "PATCH"])
def update_checkpoint(checkpoint_id):
    checkpoint = Checkpoint.query.get_or_404(checkpoint_id)
    payload = request.get_json(silent=True) or {}

    for field in ["estate_id", "court_id", "name", "type"]:
        if field in payload:
            setattr(checkpoint, field, payload[field])

    db.session.commit()
    return jsonify(CheckpointSchema.dump(checkpoint))


@bp.route("/<int:checkpoint_id>", methods=["DELETE"])
def delete_checkpoint(checkpoint_id):
    checkpoint = Checkpoint.query.get_or_404(checkpoint_id)
    db.session.delete(checkpoint)
    db.session.commit()
    return jsonify({"message": "Checkpoint deleted"})
