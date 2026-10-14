"""
Schedule Model for agenda and session timelines.
"""
from datetime import datetime
from app.extensions import db, utc_now

class Schedule(db.Model):
    __tablename__ = 'schedules'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id', ondelete='CASCADE'), nullable=False, index=True)
    speaker_id = db.Column(db.Integer, db.ForeignKey('speakers.id', ondelete='SET NULL'), nullable=True, index=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id', ondelete='SET NULL'), nullable=True, index=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_at = db.Column(db.DateTime, nullable=False)
    end_at = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=utc_now)

    def __repr__(self):
        return f"<Schedule id={self.id} event_id={self.event_id} title='{self.title}'>"
