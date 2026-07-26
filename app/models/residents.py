from datetime import datetime
from app import db


class Resident(db.Model):
    __tablename__ = "residents"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(120))
    unit_number = db.Column(db.String(20))

    court_id = db.Column(db.Integer, db.ForeignKey("courts.id"))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    visitors = db.relationship("Visitor", backref="host_resident", lazy=True)
    notifications = db.relationship("Notification", backref="resident", lazy=True)