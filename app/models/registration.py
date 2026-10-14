"""
Registration Model for attendee bookings, payment transactions, check-in, and feedback.
"""
from datetime import datetime
from app.extensions import db, utc_now

class Registration(db.Model):
    __tablename__ = 'registrations'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    registration_code = db.Column(db.String(50), unique=True, nullable=False, index=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id', ondelete='CASCADE'), nullable=False, index=True)
    attendee_id = db.Column(db.Integer, db.ForeignKey('attendees.id', ondelete='CASCADE'), nullable=False, index=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id', ondelete='RESTRICT'), nullable=False, index=True)
    
    # Registration Lifecycle
    registration_status = db.Column(db.String(20), default='confirmed', index=True)  # pending, confirmed, cancelled
    
    # Payment Tracking
    payment_status = db.Column(db.String(20), default='free', index=True)  # free, unpaid, paid, failed, refunded
    payment_ref = db.Column(db.String(100), nullable=True)  # Transaction ID / Gate Ref
    payment_amount = db.Column(db.Float, default=0.0)
    paid_at = db.Column(db.DateTime, nullable=True)
    refund_status = db.Column(db.String(20), default='none')  # none, requested, approved, refunded, rejected
    
    # Ticket & QR Check-in
    ticket_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    qr_code_path = db.Column(db.String(255), nullable=True)  # static relative path to QR image or base64
    checked_in = db.Column(db.Boolean, default=False, index=True)
    checked_in_at = db.Column(db.DateTime, nullable=True)
    checked_in_by = db.Column(db.String(100), nullable=True)  # Staff name or device ID
    
    # Feedback & Sentiment
    feedback_rating = db.Column(db.Integer, nullable=True)  # 1 to 5 stars
    feedback_text = db.Column(db.Text, nullable=True)
    sentiment = db.Column(db.String(20), nullable=True)  # positive, neutral, negative
    sentiment_score = db.Column(db.Float, nullable=True)  # Polarity score (-1.0 to 1.0)
    feedback_submitted_at = db.Column(db.DateTime, nullable=True)

    created_at = db.Column(db.DateTime, default=utc_now)
    updated_at = db.Column(db.DateTime, default=utc_now, onupdate=utc_now)

    # Unique constraint: One attendee per event per ticket
    __table_args__ = (
        db.UniqueConstraint('event_id', 'attendee_id', name='uq_event_attendee'),
    )

    def __repr__(self):
        return f"<Registration id={self.id} code='{self.registration_code}' status='{self.registration_status}' checked_in={self.checked_in}>"
