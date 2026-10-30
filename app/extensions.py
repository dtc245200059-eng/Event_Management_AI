"""
Flask extensions initialization.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from datetime import datetime, timezone

from typing import Any

from flask_sqlalchemy.model import Model

class BaseModel(Model):
    """Base declarative model providing __init__(**kwargs) for static type checkers."""
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

class _SQLAlchemy(SQLAlchemy):
    Model: type[BaseModel]

db = _SQLAlchemy(model_class=BaseModel)
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Vui lòng đăng nhập để truy cập trang này.'
login_manager.login_message_category = 'warning'
csrf = CSRFProtect()

def utc_now():
    """Returns current UTC datetime without tzinfo for consistent multi-database compatibility."""
    return datetime.now(timezone.utc).replace(tzinfo=None)

