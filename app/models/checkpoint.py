from datetime import datetime
from . import db

class Checkpoint(db.Model):
    __tablename__ = "checkpoints"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    estate_id = db.Column(db.Integer, db.ForeignKey("estates.id"), nullable=False)
    court_id = db.Column(db.Integer, db.ForeignKey("courts.id"), nullable=True)
    name = db.Column(db.String(120), nullable=False)
    type = db.Column(db.String(80), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<Checkpoint {self.name}>"
