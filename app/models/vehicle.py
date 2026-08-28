from datetime import datetime
from . import db

class Vehicle(db.Model):
    __tablename__ = "vehicles"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    plate_number = db.Column(db.String(120), unique=True, nullable=False)
    make = db.Column(db.String(120), nullable=True)
    model = db.Column(db.String(120), nullable=True)
    color = db.Column(db.String(80), nullable=True)
    vehicle_category = db.Column(db.String(80), nullable=True)
    owner_resident_id = db.Column(db.Integer, db.ForeignKey("residents.id"), nullable=True)
    owner_visitor_id = db.Column(db.Integer, db.ForeignKey("visitors.id"), nullable=True)
    registered_at_checkpoint_id = db.Column(db.Integer, db.ForeignKey("checkpoints.id"), nullable=True)
    registered_by_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    registered_at_checkpoint = db.relationship("Checkpoint", backref="vehicles", foreign_keys=[registered_at_checkpoint_id])
    registered_by_user = db.relationship("User", backref="vehicles", foreign_keys=[registered_by_user_id])

    def __repr__(self):
        return f"<Vehicle {self.plate_number}>"
