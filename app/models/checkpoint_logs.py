from datetime import datetime
from . import db

class CheckpointLog(db.Model):
    __tablename__ = "checkpoint_logs"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey("vehicles.id"), nullable=False)
    checkpoint_id = db.Column(db.Integer, db.ForeignKey("checkpoints.id"), nullable=False)
    verified_by_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    action = db.Column(db.String(80), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    notes = db.Column(db.String(500), nullable=True)

    vehicle = db.relationship("Vehicle", backref="checkpoint_logs")
    checkpoint = db.relationship("Checkpoint", backref="checkpoint_logs")
    verified_by_user = db.relationship("User", backref="checkpoint_logs")

    def __repr__(self):
        return f"<CheckpointLog vehicle={self.vehicle_id} action={self.action}>"
