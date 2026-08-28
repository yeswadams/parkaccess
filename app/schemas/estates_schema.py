from marshmallow import fields, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app import db
from app.models.estates import Estate


class EstateSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Estate
        load_instance = True
        sqla_session = db.session

    name = fields.String(
        required=True,
        validate=validate.Length(
            min=3,
            max=100
        )
    )

    address = fields.String(required=True)