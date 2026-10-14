"""
Application Factory for Flask Event Management System.
"""
import os
from flask import Flask, render_template
from app.config import config_by_name
from app.extensions import db, login_manager

def create_app(config_name='default'):
    app = Flask(__name__)
    
    # Load configuration
    app_config = config_by_name.get(config_name, config_by_name['default'])
    app.config.from_object(app_config)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Setup User Loader for Flask-Login
    from app.models.user import User
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join(app.static_folder, 'qr_codes'), exist_ok=True)

    # Register Blueprints
    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.events import events_bp
    from app.routes.tickets import tickets_bp
    from app.routes.checkin import checkin_bp
    from app.routes.admin import admin_bp
    from app.routes.ai import ai_bp
    from app.routes.notifications import notifications_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(events_bp, url_prefix='/events')
    app.register_blueprint(tickets_bp, url_prefix='/tickets')
    app.register_blueprint(checkin_bp, url_prefix='/checkin')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(ai_bp, url_prefix='/ai')
    app.register_blueprint(ai_bp, url_prefix='/api/ai', name_prefix='api_')
    app.register_blueprint(notifications_bp)

    # Register Error Handlers
    register_error_handlers(app)

    # Context processors (e.g. current year, app title, user notifications)
    @app.context_processor
    def inject_globals():
        user_notifications = []
        unread_notif_count = 0
        from flask_login import current_user
        if current_user.is_authenticated:
            try:
                from app.models.notification import Notification
                from app.models.event import Registration
                if current_user.attendee_profile:
                    regs = current_user.attendee_profile.registrations.filter(Registration.registration_status != 'cancelled').all()
                    event_ids = [r.event_id for r in regs]
                    if event_ids:
                        user_notifications = Notification.query.filter(
                            Notification.event_id.in_(event_ids),
                            Notification.status == 'sent'
                        ).order_by(Notification.sent_at.desc()).limit(5).all()
                        unread_notif_count = len(user_notifications)
                elif current_user.is_admin or current_user.is_organizer:
                    user_notifications = Notification.query.filter_by(status='sent').order_by(Notification.sent_at.desc()).limit(5).all()
                    unread_notif_count = len(user_notifications)
            except Exception:
                user_notifications = []
                unread_notif_count = 0

        return {
            'app_title': 'EventAI Pro - Quản Lý Sự Kiện Tích Hợp AI',
            'current_year': 2026,
            'recent_notifications': user_notifications,
            'unread_notif_count': unread_notif_count
        }

    # Security & Permission Headers
    @app.after_request
    def set_permissions_policy(response):
        response.headers['Permissions-Policy'] = 'camera=*, microphone=*'
        return response

    return app

def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(error):
        return render_template('errors/400.html', error=error), 400

    @app.errorhandler(403)
    def forbidden(error):
        return render_template('errors/403.html', error=error), 403

    @app.errorhandler(404)
    def not_found(error):
        return render_template('errors/404.html', error=error), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        db.session.rollback()
        return render_template('errors/500.html', error=error), 500
