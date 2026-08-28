from marshmallow import fields, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app import db
from app.models.visitor import Visitor


class VisitorSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Visitor
        load_instance = True
        sqla_session = db.session

    full_name = fields.String(
        required=True,
        validate=validate.Length(min=3, max=100)
    )

    phone = fields.String(required=True)

    id_number = fields.String(required=True)

    host_resident_id = fields.Integer(required=True)