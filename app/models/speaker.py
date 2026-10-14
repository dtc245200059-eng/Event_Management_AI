"""
Speaker Model.
"""
from datetime import datetime
from app.extensions import db, utc_now

class Speaker(db.Model):
    __tablename__ = 'speakers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), nullable=False, index=True)
    title = db.Column(db.String(150), nullable=True)  # e.g., Senior AI Architect, CTO
    bio = db.Column(db.Text, nullable=True)
    avatar_url = db.Column(db.String(255), nullable=True)
    organization = db.Column(db.String(200), nullable=True)
    email = db.Column(db.String(150), nullable=True)
    phone = db.Column(db.String(30), nullable=True)
    linkedin_url = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=utc_now)

    # Relationships
    schedules = db.relationship('Schedule', backref='speaker', lazy='dynamic')

    def __repr__(self):
        return f"<Speaker id={self.id} name='{self.name}'>"
