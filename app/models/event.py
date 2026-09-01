"""
Event Model.
"""
from datetime import datetime
from app.extensions import db

class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_code = db.Column(db.String(40), unique=True, nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(100), nullable=False, default='Technology', index=True)  # AI, Cloud, Business, Workshop, etc.
    banner_url = db.Column(db.String(255), nullable=True)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    location_type = db.Column(db.String(20), default='offline')  # offline, online, hybrid
    location_address = db.Column(db.String(255), nullable=True)
    online_meeting_url = db.Column(db.String(255), nullable=True)
    max_attendees = db.Column(db.Integer, default=500)
    status = db.Column(db.String(20), default='published', index=True)  # draft, published, ongoing, completed, cancelled
    tags = db.Column(db.String(255), nullable=True)  # comma separated e.g. "AI, Machine Learning, Python"
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    schedules = db.relationship('Schedule', backref='event', lazy='dynamic', cascade='all, delete-orphan')
    tickets = db.relationship('Ticket', backref='event', lazy='dynamic', cascade='all, delete-orphan')
    registrations = db.relationship('Registration', backref='event', lazy='dynamic', cascade='all, delete-orphan')

    @property
    def total_registered(self):
        return self.registrations.filter_by(registration_status='confirmed').count()

    @property
    def total_checked_in(self):
        return self.registrations.filter_by(checked_in=True).count()

    def __repr__(self):
        return f"<Event id={self.id} code='{self.event_code}' title='{self.title}'>"
