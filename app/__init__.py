"""
Application Factory for Flask Event Management System.
"""
import os
from flask import Flask, render_template, request, abort, jsonify
from app.config import config_by_name
from app.extensions import db, login_manager, csrf

def create_app(config_name='default'):
    app = Flask(__name__)
    
    # Load configuration
    app_config = config_by_name.get(config_name, config_by_name['default'])
    app.config.from_object(app_config)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

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

    # Register SEO Filters & Helpers
    from app.seo_helpers import (
        clean_meta_description,
        build_canonical_url,
        format_og_image,
        build_event_schema,
        build_breadcrumb_schema,
        DEFAULT_META_DESCRIPTION
    )
    app.jinja_env.filters['clean_meta_desc'] = clean_meta_description

    # Context processors (e.g. current year, app title, user notifications, SEO helpers)
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
            'unread_notif_count': unread_notif_count,
            'default_meta_desc': DEFAULT_META_DESCRIPTION,
            'canonical_url': build_canonical_url,
            'clean_meta_description': clean_meta_description,
            'format_og_image': format_og_image,
            'default_og_image': lambda: format_og_image(None),
            'get_event_schema': build_event_schema,
            'get_breadcrumb_schema': build_breadcrumb_schema,
        }

    # Access Control for Sensitive Static QR Codes
    @app.before_request
    def protect_sensitive_static_assets():
        path = request.path
        if path.startswith('/static/qr_codes/'):
            filename = os.path.basename(path)
            from flask_login import current_user
            if not current_user.is_authenticated:
                abort(403)

            # Staff and Admin have role-based authorization for check-in and oversight
            if current_user.is_staff or current_user.is_admin:
                return None

            from app.models.registration import Registration
            
            # Case 1: Ticket QR (e.g., TCK-001-0001-86CB98.svg)
            if filename.startswith('TCK-') and filename.endswith('.svg'):
                ticket_number = filename[:-4]
                reg = Registration.query.filter_by(ticket_number=ticket_number).first()
                if reg:
                    if current_user.attendee_profile and reg.attendee_id == current_user.attendee_profile.id:
                        return None
                    else:
                        abort(403)  # Cross-user unauthorized access attempt
                else:
                    abort(404)

            # Case 2: Dynamic Payment QR (e.g., pay_REG-202610-12345678.svg)
            elif filename.startswith('pay_') and filename.endswith('.svg'):
                reg_code = filename[4:-4]
                reg = Registration.query.filter_by(registration_code=reg_code).first()
                if reg:
                    if current_user.attendee_profile and reg.attendee_id == current_user.attendee_profile.id:
                        return None
                    else:
                        abort(403)
                else:
                    abort(404)

            else:
                abort(404)

    # Security & Permission Headers
    @app.after_request
    def set_security_headers(response):
        response.headers['Permissions-Policy'] = 'camera=*, microphone=*'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        if request.path.startswith('/static/qr_codes/'):
            response.headers['X-Robots-Tag'] = 'noindex, nofollow, noarchive'
            response.headers['Cache-Control'] = 'private, no-cache, no-store, must-revalidate'
        elif response.mimetype == 'text/html':
            # Protect session-bound CSRF tokens from intermediate/shared CDN cache leakage
            existing_vary = response.headers.get('Vary', '')
            if 'Cookie' not in existing_vary:
                response.headers['Vary'] = f"{existing_vary}, Cookie".strip(', ')
            # All HTML pages render base.html containing a session-bound CSRF token in <meta name="csrf-token">
            # Both authenticated and anonymous HTML must NEVER be stored in shared proxy/CDN caches
            response.headers['Cache-Control'] = 'private, no-cache, no-store, must-revalidate'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
        return response

    return app

def register_error_handlers(app):
    from flask_wtf.csrf import CSRFError

    @app.errorhandler(CSRFError)
    def handle_csrf_error(error):
        if request.is_json or request.path.startswith('/api/') or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'success': False,
                'error': 'CSRF token missing or invalid. Please refresh the page and try again.',
                'code': 'CSRF_VALIDATION_FAILED'
            }), 400
        return render_template(
            'errors/400.html',
            error=error,
            reason='Phiên làm việc hoặc mã xác thực bảo mật (CSRF Token) không hợp lệ hoặc đã hết hạn. Vui lòng tải lại trang và thử lại.'
        ), 400

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
