from .base import BaseSchema


class UserSchema(BaseSchema):
    fields = [
        "id",
        "username",
        "email",
        "created_at",
    ]
    datetime_fields = ["created_at"]
