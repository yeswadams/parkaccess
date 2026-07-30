from marshmallow import fields, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app import db
from app.models.notifications import Notification


class NotificationSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Notification
        load_instance = True
        sqla_session = db.session

    channel = fields.String(
        required=True,
        validate=validate.OneOf(
            ["sms", "call", "in_app"],
            error="Channel must be sms, call or in_app."
        )
    )

    status = fields.String(
        required=True,
        validate=validate.OneOf(
            ["sent", "delivered", "failed", "acknowledged"]
        )
    )

    message = fields.String(required=True)