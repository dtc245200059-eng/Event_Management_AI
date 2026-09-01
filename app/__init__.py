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
        return User.query.get(int(user_id))

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

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(events_bp, url_prefix='/events')
    app.register_blueprint(tickets_bp, url_prefix='/tickets')
    app.register_blueprint(checkin_bp, url_prefix='/checkin')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(ai_bp, url_prefix='/ai')
    app.register_blueprint(ai_bp, url_prefix='/api/ai', name_prefix='api_')

    # Register Error Handlers
    register_error_handlers(app)

    # Context processors (e.g. current year, app title)
    @app.context_processor
    def inject_globals():
        return {
            'app_title': 'EventAI Pro - Quản Lý Sự Kiện Tích Hợp AI',
            'current_year': 2026
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
