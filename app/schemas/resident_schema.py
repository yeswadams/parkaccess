from marshmallow import fields, validate, validates, ValidationError
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app import db
from app.models.residents import Resident


class ResidentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Resident
        load_instance = True
        sqla_session = db.session

    full_name = fields.String(
        required=True,
        validate=validate.Length(
            min=3,
            max=100,
            error="Full name must be between 3 and 100 characters."
        )
    )

    phone = fields.String(
        required=True,
        validate=validate.Length(
            min=10,
            max=15,
            error="Phone number must be between 10 and 15 digits."
        )
    )

    email = fields.Email(
        required=True,
        error_messages={
            "invalid": "Please enter a valid email address."
        }
    )

    unit_number = fields.String(required=True)

    @validates("phone")
    def validate_phone(self, value, **kwargs):
        if not value.isdigit():
            raise ValidationError("Phone number must contain only digits.")