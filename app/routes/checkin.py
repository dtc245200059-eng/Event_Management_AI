"""
Check-in Blueprint (Camera QR scanning, attendee roster, manual code verification, anti-duplicate checks).
"""
import re
import json
from datetime import datetime
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for, abort
from flask_login import login_required, current_user
from app.extensions import db, utc_now
from app.models import Registration, Event

checkin_bp = Blueprint('checkin', __name__)

def staff_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not (current_user.is_checkin_staff or current_user.is_organizer):
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@checkin_bp.route('/')
@login_required
@staff_required
def index():
    events = Event.query.order_by(Event.start_date.desc()).all()
    recent_checkins = Registration.query.filter_by(checked_in=True).order_by(Registration.checked_in_at.desc()).limit(15).all()
    
    # Calculate global check-in metrics
    total_regs = Registration.query.filter(Registration.registration_status != 'cancelled').count()
    total_checked = Registration.query.filter_by(checked_in=True).count()
    overall_rate = round((total_checked / total_regs * 100), 1) if total_regs > 0 else 0.0

    return render_template(
        'checkin/index.html',
        events=events,
        recent_checkins=recent_checkins,
        total_regs=total_regs,
        total_checked=total_checked,
        overall_rate=overall_rate
    )

def extract_ticket_code(raw_input):
    """Bóc tách mã vé linh hoạt từ raw code, URL hoặc JSON payload."""
    if not raw_input:
        return ""
    text = str(raw_input).strip()
    
    # Case 1: JSON payload (e.g. {"ticket_number": "TCK-..."} or {"registration_code": "REG-..."})
    if text.startswith('{') and text.endswith('}'):
        try:
            parsed = json.loads(text)
            if 'ticket_number' in parsed:
                return str(parsed['ticket_number']).strip().upper()
            if 'registration_code' in parsed:
                return str(parsed['registration_code']).strip().upper()
        except Exception:
            pass

    # Case 2: Contains TCK standard pattern (e.g. TCK-001-0001-15C02F or TCK-NUM-...)
    tck_match = re.search(r'(TCK-[A-Za-z0-9\-_]+)', text, re.IGNORECASE)
    if tck_match:
        return tck_match.group(1).upper()

    # Case 3: Contains REG standard pattern (e.g. REG-001-...)
    reg_match = re.search(r'(REG-[A-Za-z0-9\-_]+)', text, re.IGNORECASE)
    if reg_match:
        return reg_match.group(1).upper()

    return text.upper()

@checkin_bp.route('/verify-api', methods=['POST'])
@login_required
@staff_required
def verify_api():
    """API endpoint for validating QR Code scanned via Browser Camera, image file or barcode gun."""
    data = request.get_json() or {}
    raw_input = data.get('ticket_number', '')
    event_id = data.get('event_id')
    ticket_number = extract_ticket_code(raw_input)

    if not ticket_number:
        return jsonify({
            'success': False,
            'message': 'Mã vé hoặc mã đăng ký không được để trống.'
        }), 400

    # Support lookup via either ticket_number or registration_code
    query = Registration.query.filter(
        (Registration.ticket_number == ticket_number) | 
        (Registration.registration_code == ticket_number)
    )
    if event_id:
        query = query.filter_by(event_id=event_id)
    
    registration = query.first()

    if not registration:
        return jsonify({
            'success': False,
            'status': 'invalid',
            'message': f'❌ MÃ VÉ HOẶC MÃ ĐĂNG KÝ "{ticket_number}" KHÔNG HỢP LỆ HOẶC KHÔNG TỒN TẠI TRONG HỆ THỐNG.'
        }), 404

    # Check if ticket was cancelled
    if registration.registration_status == 'cancelled':
        return jsonify({
            'success': False,
            'status': 'cancelled',
            'message': '⛔ CẢNH BÁO: VÉ NÀY ĐÃ BỊ HỦY BỞI NGƯỜI DÙNG! Không thể thực hiện check-in.',
            'attendee_name': registration.attendee.full_name,
            'ticket_type': registration.ticket.name
        }), 400

    # Check payment status
    if registration.payment_status not in ('free', 'paid'):
        return jsonify({
            'success': False,
            'status': 'unpaid',
            'message': f'⚠️ VÉ CHƯA THANH TOÁN (Trạng thái: {registration.payment_status}). Vui lòng hoàn tất thanh toán trước khi check-in.',
            'attendee_name': registration.attendee.full_name,
            'ticket_type': registration.ticket.name
        }), 400

    # Check if already checked in (Anti-duplicate check)
    if registration.checked_in:
        time_str = registration.checked_in_at.strftime('%H:%M:%S ngày %d/%m/%Y') if registration.checked_in_at else 'trước đó'
        return jsonify({
            'success': False,
            'status': 'duplicate',
            'message': f'⛔ CẢNH BÁO: VÉ NÀY ĐÃ ĐƯỢC CHECK-IN LÚC {time_str} bởi {registration.checked_in_by or "hệ thống"}.',
            'attendee_name': registration.attendee.full_name,
            'ticket_type': registration.ticket.name,
            'checked_in_at': time_str
        }), 409

    # Perform Atomic Check-in on shared storage to prevent race conditions
    now_time = utc_now()
    rows_updated = Registration.query.filter(
        Registration.id == registration.id,
        Registration.checked_in == False
    ).update({
        'checked_in': True,
        'checked_in_at': now_time,
        'checked_in_by': current_user.username
    })
    db.session.commit()

    if rows_updated == 0:
        return jsonify({
            'success': False,
            'status': 'duplicate',
            'message': '⛔ CẢNH BÁO: VÉ NÀY VỪA ĐƯỢC CHECK-IN ĐỒNG THỜI BỞI THIẾT BỊ KHÁC.',
            'attendee_name': registration.attendee.full_name,
            'ticket_type': registration.ticket.name
        }), 409

    return jsonify({
        'success': True,
        'status': 'valid',
        'message': f'✅ CHECK-IN THÀNH CÔNG CHO KHÁCH HÀNG: {registration.attendee.full_name}',
        'reg_id': registration.id,
        'ticket_number': registration.ticket_number,
        'registration_code': registration.registration_code,
        'attendee_name': registration.attendee.full_name,
        'email': registration.attendee.email,
        'phone': registration.attendee.phone or 'Chưa cập nhật',
        'organization': registration.attendee.organization or 'Khách mời tự do',
        'ticket_type': registration.ticket.name,
        'ticket_tier': registration.ticket.ticket_type,
        'event_title': registration.event.title,
        'checked_in_at': now_time.strftime('%H:%M:%S • %d/%m/%Y')
    }), 200


@checkin_bp.route('/api/event-attendees/<int:event_id>')
@login_required
@staff_required
def api_event_attendees(event_id):
    """Lấy danh sách chi tiết toàn bộ người tham dự của một sự kiện kèm trạng thái check-in và mã QR."""
    event = db.get_or_404(Event, event_id)
    registrations = Registration.query.filter_by(event_id=event.id).order_by(Registration.created_at.desc()).all()
    
    from app.routes.tickets import ensure_registration_qr
    
    attendees_data = []
    total_checked_in = 0
    total_valid = 0

    for r in registrations:
        qr_rel_path = ensure_registration_qr(r) or r.qr_code_path or ""
        if r.registration_status != 'cancelled':
            total_valid += 1
            if r.checked_in:
                total_checked_in += 1

        attendees_data.append({
            'reg_id': r.id,
            'registration_code': r.registration_code,
            'ticket_number': r.ticket_number,
            'attendee_name': r.attendee.full_name,
            'email': r.attendee.email,
            'phone': r.attendee.phone or '',
            'organization': r.attendee.organization or 'Khách mời tự do',
            'ticket_name': r.ticket.name,
            'ticket_type': r.ticket.ticket_type,
            'payment_status': r.payment_status,
            'registration_status': r.registration_status,
            'checked_in': r.checked_in,
            'checked_in_at': r.checked_in_at.strftime('%H:%M:%S • %d/%m/%Y') if r.checked_in_at else None,
            'checked_in_by': r.checked_in_by or '',
            'qr_code_url': f"/static/{qr_rel_path}" if qr_rel_path else ""
        })

    checkin_rate = round((total_checked_in / total_valid * 100), 1) if total_valid > 0 else 0.0

    return jsonify({
        'success': True,
        'event_id': event.id,
        'event_title': event.title,
        'total_registered': total_valid,
        'total_checked_in': total_checked_in,
        'total_remaining': total_valid - total_checked_in,
        'checkin_rate': checkin_rate,
        'attendees': attendees_data
    })

@checkin_bp.route('/api/quick-checkin/<int:reg_id>', methods=['POST'])
@login_required
@staff_required
def api_quick_checkin(reg_id):
    """Check-in nhanh 1 chạm cho nhân viên từ danh sách bảng."""
    registration = db.get_or_404(Registration, reg_id)
    
    if registration.registration_status == 'cancelled':
        return jsonify({
            'success': False,
            'message': 'Vé này đã bị hủy bởi người dùng, không thể check-in.'
        }), 400

    if registration.payment_status not in ('free', 'paid'):
        return jsonify({
            'success': False,
            'message': f'Vé chưa hoàn tất thanh toán (Trạng thái: {registration.payment_status}).'
        }), 400

    if registration.checked_in:
        time_str = registration.checked_in_at.strftime('%H:%M:%S %d/%m/%Y') if registration.checked_in_at else 'trước đó'
        return jsonify({
            'success': False,
            'message': f'Vé đã được check-in lúc {time_str} bởi {registration.checked_in_by or "hệ thống"}.'
        }), 409

    registration.checked_in = True
    registration.checked_in_at = utc_now()
    registration.checked_in_by = current_user.username
    db.session.commit()

    return jsonify({
        'success': True,
        'message': f'Check-in thành công cho khách hàng: {registration.attendee.full_name}',
        'attendee_name': registration.attendee.full_name,
        'ticket_number': registration.ticket_number,
        'checked_in_at': registration.checked_in_at.strftime('%H:%M:%S • %d/%m/%Y'),
        'checked_in_by': registration.checked_in_by
    })

@checkin_bp.route('/api/undo-checkin/<int:reg_id>', methods=['POST'])
@login_required
@staff_required
def api_undo_checkin(reg_id):
    """Hoàn tác trạng thái check-in trong trường hợp nhân viên bấm nhầm."""
    registration = db.get_or_404(Registration, reg_id)
    registration.checked_in = False
    registration.checked_in_at = None
    registration.checked_in_by = None
    db.session.commit()

    return jsonify({
        'success': True,
        'message': f'Đã hoàn tác trạng thái check-in cho vé {registration.ticket_number}.'
    })

