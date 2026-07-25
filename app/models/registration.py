from datetime import datetime
from . import db

class Registration(db.Model):
    __tablename__ = "Registration"

    RegistrationID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    VehicleID = db.Column(db.Integer, db.ForeignKey("Vehicle.VehicleID"), nullable=False)
    CheckpointID = db.Column(db.Integer, db.ForeignKey("Checkpoint.CheckpointID"), nullable=False)
    EntryTime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    ExitTime = db.Column(db.DateTime, nullable=True)
    RegisteredBy = db.Column(db.Integer, db.ForeignKey("SecurityOfficer.OfficerID"), nullable=False)

    vehicle = db.relationship("Vehicle", backref="registrations")
    checkpoint = db.relationship("Checkpoint", backref="registrations")
    security_officer = db.relationship("SecurityOfficer", backref="registrations")

    def __repr__(self):
        return f"<Registration vehicle={self.VehicleID} checkpoint={self.CheckpointID}>"
