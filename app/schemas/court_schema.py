from marshmallow import fields, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app import db
from app.models.court import Court


class CourtSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Court
        load_instance = True
        sqla_session = db.session

    name = fields.String(
        required=True,
        validate=validate.Length(
            min=2,
            max=100,
            error="Court name must be between 2 and 100 characters."
        )
    )

    estate_id = fields.Integer(required=True)