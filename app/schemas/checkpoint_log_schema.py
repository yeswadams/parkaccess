from .base import BaseSchema


class CheckpointLogSchema(BaseSchema):
    fields = [
        "id",
        "vehicle_id",
        "checkpoint_id",
        "verified_by_user_id",
        "action",
        "timestamp",
        "notes",
    ]
    datetime_fields = ["timestamp"]
