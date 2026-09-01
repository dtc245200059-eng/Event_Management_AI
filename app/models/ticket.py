"""
Ticket Model for ticket tiers, prices and quotas.
"""
from datetime import datetime
from app.extensions import db

class Ticket(db.Model):
    __tablename__ = 'tickets'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id', ondelete='CASCADE'), nullable=False, index=True)
    ticket_code = db.Column(db.String(40), unique=True, nullable=False, index=True)
    ticket_type = db.Column(db.String(30), nullable=False)  # free, standard, vip
    name = db.Column(db.String(100), nullable=False)  # e.g., "Vé Tiêu Chuẩn", "Vé VIP Hàng Đầu"
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, default=0.0, nullable=False)
    quota = db.Column(db.Integer, nullable=False, default=100)  # Maximum available tickets
    sold_count = db.Column(db.Integer, nullable=False, default=0)
    status = db.Column(db.String(20), default='active')  # active, closed, sold_out
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    registrations = db.relationship('Registration', backref='ticket', lazy='dynamic')

    @property
    def remaining_quota(self):
        return max(0, self.quota - self.sold_count)

    @property
    def is_available(self):
        return self.status == 'active' and self.remaining_quota > 0

    def __repr__(self):
        return f"<Ticket id={self.id} code='{self.ticket_code}' type='{self.ticket_type}' price={self.price}>"
