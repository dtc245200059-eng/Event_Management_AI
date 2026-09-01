"""
AI Chat History Model for logging user interactions and audits.
"""
from datetime import datetime
from app.extensions import db

class AIChatHistory(db.Model):
    __tablename__ = 'ai_chat_history'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True, index=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id', ondelete='SET NULL'), nullable=True, index=True)
    chat_type = db.Column(db.String(30), nullable=False, default='rag_chat')  # rag_chat, recommendation, generator, predictive, sentiment
    user_message = db.Column(db.Text, nullable=False)
    ai_response = db.Column(db.Text, nullable=False)
    model_name = db.Column(db.String(80), default='gemini-2.0-flash')
    response_mode = db.Column(db.String(20), default='live')  # live, mock, cached
    latency_ms = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    event = db.relationship('Event', backref='chat_logs')

    def __repr__(self):
        return f"<AIChatHistory id={self.id} type='{self.chat_type}' mode='{self.response_mode}'>"
