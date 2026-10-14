"""
Event FAQ Model for event guidelines, policies, and RAG Chatbot Knowledge Grounding.
"""
from datetime import datetime
from app.extensions import db, utc_now

class EventFAQ(db.Model):
    __tablename__ = 'event_faqs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False, index=True)
    question = db.Column(db.String(255), nullable=False)
    answer = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), default='general')  # checkin, ticketing, venue, logistics, general
    created_at = db.Column(db.DateTime, default=utc_now)

    # Relationships
    event = db.relationship('Event', backref=db.backref('faqs', lazy='dynamic', cascade='all, delete-orphan'))

    def __repr__(self):
        return f"<EventFAQ id={self.id} event_id={self.event_id} question='{self.question[:30]}...'>"
