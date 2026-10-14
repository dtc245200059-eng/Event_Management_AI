"""
AI Chat History Model for logging user interactions and audits.
"""
from datetime import datetime
from app.extensions import db, utc_now

class AIChatHistory(db.Model):
    __tablename__ = 'ai_chat_history'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True, index=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id', ondelete='SET NULL'), nullable=True, index=True)
    chat_type = db.Column(db.String(30), nullable=False, default='rag_chat')  # rag_chat, recommendation, generator, predictive, sentiment
    user_message = db.Column(db.Text, nullable=False)
    ai_response = db.Column(db.Text, nullable=False)
    model_name = db.Column(db.String(80), default='gemini-3.1-flash-lite')
    response_mode = db.Column(db.String(20), default='live')  # live, mock, cached
    latency_ms = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=utc_now)

    # Relationships
    event = db.relationship('Event', backref='chat_logs')

    def __init__(
        self,
        user_id=None,
        event_id=None,
        chat_type='rag_chat',
        user_message='',
        ai_response='',
        model_name='gemini-3.1-flash-lite',
        response_mode='live',
        latency_ms=None,
        created_at=None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.user_id = user_id
        self.event_id = event_id
        self.chat_type = chat_type
        self.user_message = user_message
        self.ai_response = ai_response
        self.model_name = model_name
        self.response_mode = response_mode
        self.latency_ms = latency_ms
        if created_at is not None:
            self.created_at = created_at

    def __repr__(self):
        return f"<AIChatHistory id={self.id} type='{self.chat_type}' mode='{self.response_mode}'>"
