from . import db

class Checkpoint(db.Model):
    __tablename__ = "Checkpoint"

    CheckpointID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CheckpointName = db.Column(db.String(120), nullable=False)
    Location = db.Column(db.String(200), nullable=True)
    CourtID = db.Column(db.Integer, db.ForeignKey("Court.CourtID"), nullable=False)

    court = db.relationship("Court", backref="checkpoints")

    def __repr__(self):
        return f"<Checkpoint {self.CheckpointName}>"
