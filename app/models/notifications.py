from datetime import datetime
from app import db


class Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)

    blocking_incident_id = db.Column(
        db.Integer,
        db.ForeignKey("blocking_incidents.id")
    )

    recipient_resident_id = db.Column(
        db.Integer,
        db.ForeignKey("residents.id"),
        nullable=True
    )

    recipient_visitor_id = db.Column(
        db.Integer,
        db.ForeignKey("visitors.id"),
        nullable=True
    )

    channel = db.Column(db.String(20))
    message = db.Column(db.String(255))
    sent_at = db.Column(db.DateTime, default=datetime)
    status = db.Column(db.String(30))