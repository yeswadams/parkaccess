from datetime import datetime
from app import db




class Estate(db.Model):
    __tablename__ = "estates"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    courts = db.relationship("Court", backref="estate", lazy=True)