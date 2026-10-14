"""
Notification Model for event communications and broadcast announcements.
Supports AI-generated email/notification drafts (invitations, reminders, thank-you notes).
"""
from datetime import datetime
from app.extensions import db, utc_now

class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False)
    notification_type = db.Column(db.String(30), nullable=False, default='reminder')  # invitation, reminder, thank_you, update
    target_audience = db.Column(db.String(50), nullable=False, default='all_registered')  # all_registered, checked_in, not_checked_in, vip
    content = db.Column(db.Text, nullable=False)
    recipient_count = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default='sent')  # draft, sent
    sent_at = db.Column(db.DateTime, default=utc_now)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=utc_now)

    # Relationships
    event = db.relationship('Event', backref=db.backref('notifications', lazy='dynamic', cascade='all, delete-orphan'))
    sender = db.relationship('User', backref=db.backref('sent_notifications', lazy='dynamic'))

    def __repr__(self):
        return f"<Notification id={self.id} event_id={self.event_id} type='{self.notification_type}' title='{self.title}'>"
