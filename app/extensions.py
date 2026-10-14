"""
Flask extensions initialization.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from datetime import datetime, timezone

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Vui lòng đăng nhập để truy cập trang này.'
login_manager.login_message_category = 'warning'

def utc_now():
    """Returns current UTC datetime without tzinfo for consistent multi-database compatibility."""
    return datetime.now(timezone.utc).replace(tzinfo=None)

