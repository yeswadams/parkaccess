from flask import Blueprint, jsonify, request

from app.models import Vehicle, db
from app.schemas import VehicleSchema

bp = Blueprint("vehicles", __name__, url_prefix="/vehicles")


@bp.route("", methods=["GET"])
def list_vehicles():
    vehicles = Vehicle.query.all()
    return jsonify([VehicleSchema.dump(vehicle) for vehicle in vehicles])


@bp.route("/<int:vehicle_id>", methods=["GET"])
def get_vehicle(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    return jsonify(VehicleSchema.dump(vehicle))


@bp.route("", methods=["POST"])
def create_vehicle():
    payload = request.get_json(silent=True) or {}
    if not payload.get("plate_number"):
        return jsonify({"error": "plate_number is required"}), 400

    vehicle = Vehicle(
        plate_number=payload.get("plate_number"),
        make=payload.get("make"),
        model=payload.get("model"),
        color=payload.get("color"),
        vehicle_category=payload.get("vehicle_category"),
        owner_resident_id=payload.get("owner_resident_id"),
        owner_visitor_id=payload.get("owner_visitor_id"),
        registered_at_checkpoint_id=payload.get("registered_at_checkpoint_id"),
        registered_by_user_id=payload.get("registered_by_user_id"),
    )

    db.session.add(vehicle)
    db.session.commit()
    return jsonify(VehicleSchema.dump(vehicle)), 201


@bp.route("/<int:vehicle_id>", methods=["PUT", "PATCH"])
def update_vehicle(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    payload = request.get_json(silent=True) or {}

    for field in [
        "plate_number",
        "make",
        "model",
        "color",
        "vehicle_category",
        "owner_resident_id",
        "owner_visitor_id",
        "registered_at_checkpoint_id",
        "registered_by_user_id",
    ]:
        if field in payload:
            setattr(vehicle, field, payload[field])

    db.session.commit()
    return jsonify(VehicleSchema.dump(vehicle))


@bp.route("/<int:vehicle_id>", methods=["DELETE"])
def delete_vehicle(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    db.session.delete(vehicle)
    db.session.commit()
    return jsonify({"message": "Vehicle deleted"})
