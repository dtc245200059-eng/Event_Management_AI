"""
Venue Model for locations and meeting rooms.
"""
from datetime import datetime
from app.extensions import db

class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    venue_code = db.Column(db.String(30), unique=True, nullable=False, index=True)
    name = db.Column(db.String(200), nullable=False)
    address = db.Column(db.Text, nullable=False)
    capacity = db.Column(db.Integer, nullable=False, default=100)
    room_name = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(20), default='available')  # available, maintenance, occupied
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    schedules = db.relationship('Schedule', backref='venue', lazy='dynamic')

    def __repr__(self):
        return f"<Venue id={self.id} code='{self.venue_code}' name='{self.name}'>"
