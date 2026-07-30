from .base import BaseSchema


class CheckpointSchema(BaseSchema):
    fields = [
        "id",
        "estate_id",
        "court_id",
        "name",
        "type",
        "created_at",
    ]
    datetime_fields = ["created_at"]
