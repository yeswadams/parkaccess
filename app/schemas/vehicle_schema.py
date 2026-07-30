from .base import BaseSchema


class VehicleSchema(BaseSchema):
    fields = [
        "id",
        "plate_number",
        "make",
        "model",
        "color",
        "vehicle_category",
        "owner_resident_id",
        "owner_visitor_id",
        "registered_at_checkpoint_id",
        "registered_by_user_id",
        "created_at",
    ]
    datetime_fields = ["created_at"]
