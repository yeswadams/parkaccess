from datetime import datetime
from app import db


class Visitor(db.Model):
    __tablename__ = "visitors"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    id_number = db.Column(db.String(50))

    host_resident_id = db.Column(
        db.Integer,
        db.ForeignKey("residents.id")
    )

    created_at = db.Column(db.DateTime, default=datetime)

    notifications = db.relationship("Notification", backref="visitor", lazy=True)