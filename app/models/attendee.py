"""
Attendee Model.
"""
from datetime import datetime
from app.extensions import db, utc_now

class Attendee(db.Model):
    __tablename__ = 'attendees'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    attendee_code = db.Column(db.String(40), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True, unique=True)
    full_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(20), nullable=True)
    organization = db.Column(db.String(200), nullable=True)
    job_title = db.Column(db.String(100), nullable=True)
    interests = db.Column(db.Text, nullable=True)  # e.g., "AI, Machine Learning, Data Science, Cloud Computing"
    created_at = db.Column(db.DateTime, default=utc_now)

    # Relationships
    registrations = db.relationship('Registration', backref='attendee', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Attendee id={self.id} code='{self.attendee_code}' name='{self.full_name}'>"
