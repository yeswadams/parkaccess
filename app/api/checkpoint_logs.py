from flask import Blueprint, jsonify, request

from app.models import CheckpointLog, db
from app.schemas import CheckpointLogSchema

bp = Blueprint("checkpoint_logs", __name__, url_prefix="/checkpoint-logs")


@bp.route("", methods=["GET"])
def list_checkpoint_logs():
    logs = CheckpointLog.query.all()
    return jsonify([CheckpointLogSchema.dump(log) for log in logs])


@bp.route("/<int:log_id>", methods=["GET"])
def get_checkpoint_log(log_id):
    log = CheckpointLog.query.get_or_404(log_id)
    return jsonify(CheckpointLogSchema.dump(log))


@bp.route("", methods=["POST"])
def create_checkpoint_log():
    payload = request.get_json(silent=True) or {}
    if not payload.get("vehicle_id") or not payload.get("checkpoint_id"):
        return jsonify({"error": "vehicle_id and checkpoint_id are required"}), 400

    log = CheckpointLog(
        vehicle_id=payload.get("vehicle_id"),
        checkpoint_id=payload.get("checkpoint_id"),
        verified_by_user_id=payload.get("verified_by_user_id"),
        action=payload.get("action", "entry"),
        notes=payload.get("notes"),
    )

    db.session.add(log)
    db.session.commit()
    return jsonify(CheckpointLogSchema.dump(log)), 201


@bp.route("/<int:log_id>", methods=["PUT", "PATCH"])
def update_checkpoint_log(log_id):
    log = CheckpointLog.query.get_or_404(log_id)
    payload = request.get_json(silent=True) or {}

    for field in ["vehicle_id", "checkpoint_id", "verified_by_user_id", "action", "notes"]:
        if field in payload:
            setattr(log, field, payload[field])

    db.session.commit()
    return jsonify(CheckpointLogSchema.dump(log))


@bp.route("/<int:log_id>", methods=["DELETE"])
def delete_checkpoint_log(log_id):
    log = CheckpointLog.query.get_or_404(log_id)
    db.session.delete(log)
    db.session.commit()
    return jsonify({"message": "Checkpoint log deleted"})
