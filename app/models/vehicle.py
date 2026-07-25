from . import db

class Vehicle(db.Model):
    __tablename__ = "Vehicle"

    VehicleID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    RegistrationNumber = db.Column(db.String(120), unique=True, nullable=False)
    Make = db.Column(db.String(120), nullable=True)
    Model = db.Column(db.String(120), nullable=True)
    Color = db.Column(db.String(80), nullable=True)
    OwnerType = db.Column(db.String(80), nullable=True)
    ResidentID = db.Column(db.Integer, db.ForeignKey("Resident.ResidentID"), nullable=True)
    VisitorID = db.Column(db.Integer, db.ForeignKey("Visitor.VisitorID"), nullable=True)

    resident = db.relationship("Resident", backref="vehicles", foreign_keys=[ResidentID])
    visitor = db.relationship("Visitor", backref="vehicles", foreign_keys=[VisitorID])

    def __repr__(self):
        return f"<Vehicle {self.RegistrationNumber}>"
