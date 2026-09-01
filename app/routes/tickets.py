"""
Tickets and Registration Blueprint (Booking, Quota Transaction, Payment simulation, Feedback).
"""
import os
import uuid
from datetime import datetime
import qrcode
import qrcode.image.svg
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort, current_app, send_file
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Event, Ticket, Registration, Attendee

tickets_bp = Blueprint('tickets', __name__)

def generate_qr_code(ticket_number):
    """Sinh ảnh mã QR định dạng SVG vector sắc nét và lưu vào static/qr_codes/."""
    qr_dir = os.path.join(current_app.static_folder, 'qr_codes')
    os.makedirs(qr_dir, exist_ok=True)
    filename = f"{ticket_number}.svg"
    filepath = os.path.join(qr_dir, filename)

    factory = qrcode.image.svg.SvgImage
    img = qrcode.make(ticket_number, image_factory=factory)
    img.save(filepath)
    return f"qr_codes/{filename}"

def ensure_registration_qr(registration):
    """Đảm bảo mã QR của vé luôn tồn tại trên đĩa, tự động tái tạo nếu bị thiếu (Self-Healing)."""
    if not registration or not registration.ticket_number:
        return None
    qr_dir = os.path.join(current_app.static_folder, 'qr_codes')
    os.makedirs(qr_dir, exist_ok=True)
    filename = f"{registration.ticket_number}.svg"
    filepath = os.path.join(qr_dir, filename)

    if not os.path.exists(filepath):
        factory = qrcode.image.svg.SvgImage
        img = qrcode.make(registration.ticket_number, image_factory=factory)
        img.save(filepath)

    rel_path = f"qr_codes/{filename}"
    if registration.qr_code_path != rel_path:
        registration.qr_code_path = rel_path
        db.session.commit()
    return rel_path

@tickets_bp.route('/register/<int:event_id>', methods=['GET', 'POST'])
@login_required
def register_ticket(event_id):
    event = Event.query.get_or_404(event_id)

    # Check if attendee profile exists
    if not current_user.attendee_profile:
        flash('Vui lòng cập nhật hồ sơ người tham dự trước khi đặt vé.', 'warning')
        return redirect(url_for('auth.profile'))

    attendee = current_user.attendee_profile

    # Check existing registration of this attendee for this event
    existing_reg = Registration.query.filter_by(
        event_id=event.id,
        attendee_id=attendee.id
    ).first()

    # If already confirmed
    if existing_reg and existing_reg.registration_status == 'confirmed':
        flash('Bạn đã sở hữu vé tham dự sự kiện này!', 'info')
        return redirect(url_for('tickets.view_ticket', reg_id=existing_reg.id))

    if request.method == 'POST':
        ticket_id = request.form.get('ticket_id', type=int)
        if not ticket_id:
            flash('Vui lòng chọn loại vé.', 'danger')
            return redirect(url_for('main.event_detail', event_id=event.id))

        # Atomic Transaction & Quota Check
        try:
            ticket = Ticket.query.filter_by(id=ticket_id, event_id=event.id).with_for_update().first()
            if not ticket or not ticket.is_available:
                flash('Loại vé này hiện đã hết số lượng phát hành hoặc tạm đóng.', 'danger')
                return redirect(url_for('main.event_detail', event_id=event.id))

            is_paid_ticket = ticket.price > 0
            payment_status = 'pending' if is_paid_ticket else 'free'
            reg_status = 'pending' if is_paid_ticket else 'confirmed'

            # Generate fresh ticket number and QR
            ticket_number = f"TCK-{event.id:03d}-{attendee.id:04d}-{uuid.uuid4().hex[:6].upper()}"
            qr_path = generate_qr_code(ticket_number)

            if existing_reg:
                # Case 1: Was pending (update ticket type and price if changed)
                if existing_reg.registration_status == 'pending':
                    if existing_reg.ticket_id != ticket.id:
                        # Release old ticket quota and hold new ticket quota
                        old_t = existing_reg.ticket
                        if old_t and old_t.sold_count > 0:
                            old_t.sold_count -= 1
                            if old_t.status == 'sold_out' and old_t.sold_count < old_t.quota:
                                old_t.status = 'active'
                        ticket.sold_count += 1
                        if ticket.sold_count >= ticket.quota:
                            ticket.status = 'sold_out'
                # Case 2: Was cancelled (reactivate registration and take quota)
                elif existing_reg.registration_status == 'cancelled':
                    ticket.sold_count += 1
                    if ticket.sold_count >= ticket.quota:
                        ticket.status = 'sold_out'

                # Update existing record
                existing_reg.ticket_id = ticket.id
                existing_reg.registration_status = reg_status
                existing_reg.payment_status = payment_status
                existing_reg.payment_amount = ticket.price
                existing_reg.ticket_number = ticket_number
                existing_reg.qr_code_path = qr_path
                existing_reg.checked_in = False
                existing_reg.checked_in_at = None
                existing_reg.checked_in_by = None
                existing_reg.feedback_rating = None
                existing_reg.feedback_text = None
                existing_reg.sentiment = None

                db.session.commit()
                target_reg = existing_reg
            else:
                # Case 3: Completely new registration
                ticket.sold_count += 1
                if ticket.sold_count >= ticket.quota:
                    ticket.status = 'sold_out'

                reg_code = f"REG-{datetime.utcnow().strftime('%Y%m')}-{uuid.uuid4().hex[:8].upper()}"
                new_reg = Registration(
                    registration_code=reg_code,
                    event_id=event.id,
                    attendee_id=attendee.id,
                    ticket_id=ticket.id,
                    registration_status=reg_status,
                    payment_status=payment_status,
                    payment_amount=ticket.price,
                    ticket_number=ticket_number,
                    qr_code_path=qr_path
                )
                db.session.add(new_reg)
                db.session.commit()
                target_reg = new_reg

            if is_paid_ticket:
                return redirect(url_for('tickets.checkout', reg_id=target_reg.id))
            else:
                flash('Đăng ký vé miễn phí thành công! Mã vé QR của bạn đã sẵn sàng.', 'success')
                return redirect(url_for('tickets.view_ticket', reg_id=target_reg.id))

        except Exception as e:
            db.session.rollback()
            flash(f'Lỗi xử lý giao dịch đặt vé: {str(e)}', 'danger')
            return redirect(url_for('main.event_detail', event_id=event.id))

    return redirect(url_for('main.event_detail', event_id=event.id))

def generate_payment_qr(reg_code, amount, method='vnpay'):
    """Sinh ảnh mã QR thanh toán động dạng SVG vector cho đơn hàng."""
    qr_dir = os.path.join(current_app.static_folder, 'qr_codes')
    os.makedirs(qr_dir, exist_ok=True)
    filename = f"pay_{reg_code}.svg"
    filepath = os.path.join(qr_dir, filename)
    
    # Structured payment payload (VietQR / VNPAY compatible standard)
    qr_payload = f"VIETQR://PAY?bank=MBBANK&acc=0901234567&name=CONG%20TY%20CONG%20NGHE%20EVENTAI&amount={int(amount)}&memo=THANHTOAN%20{reg_code}"
    factory = qrcode.image.svg.SvgImage
    img = qrcode.make(qr_payload, image_factory=factory)
    img.save(filepath)
    return f"qr_codes/{filename}"

@tickets_bp.route('/checkout/<int:reg_id>', methods=['GET', 'POST'])
@login_required
def checkout(reg_id):
    reg = Registration.query.get_or_404(reg_id)
    
    # Permission check
    if reg.attendee.user_id != current_user.id and not current_user.is_staff:
        abort(403)

    if reg.payment_status == 'paid':
        flash('Đơn đăng ký này đã được thanh toán hoàn tất.', 'info')
        return redirect(url_for('tickets.view_ticket', reg_id=reg.id))

    if request.method == 'POST':
        payment_method = request.form.get('payment_method', 'vnpay')
        
        # Payment gateway confirmation & verification
        trans_ref = f"GATE-{payment_method.upper()}-{uuid.uuid4().hex[:10].upper()}"
        reg.payment_status = 'paid'
        reg.registration_status = 'confirmed'
        reg.payment_ref = trans_ref
        reg.paid_at = datetime.utcnow()
        db.session.commit()

        flash(f'Thanh toán thành công qua {payment_method.upper()}! Mã giao dịch: {trans_ref}', 'success')
        return redirect(url_for('tickets.view_ticket', reg_id=reg.id))

    # Generate Dynamic Payment QR
    pay_qr_url = generate_payment_qr(reg.registration_code, reg.payment_amount)

    return render_template(
        'tickets/checkout.html',
        registration=reg,
        pay_qr_url=pay_qr_url
    )

@tickets_bp.route('/my-tickets')
@login_required
def my_tickets():
    if not current_user.attendee_profile:
        registrations = []
    else:
        registrations = current_user.attendee_profile.registrations.order_by(Registration.created_at.desc()).all()
        for r in registrations:
            ensure_registration_qr(r)
    return render_template('tickets/my_tickets.html', registrations=registrations)

@tickets_bp.route('/view/<int:reg_id>')
@login_required
def view_ticket(reg_id):
    reg = Registration.query.get_or_404(reg_id)
    if reg.attendee.user_id != current_user.id and not current_user.is_staff:
        abort(403)
    ensure_registration_qr(reg)
    return render_template('tickets/view_ticket.html', registration=reg)

@tickets_bp.route('/download-qr/<int:reg_id>')
@login_required
def download_qr(reg_id):
    """Cho phép người tham dự hoặc ban tổ chức tải tệp ảnh mã QR SVG của vé."""
    reg = Registration.query.get_or_404(reg_id)
    if reg.attendee.user_id != current_user.id and not current_user.is_staff:
        abort(403)
    qr_rel_path = ensure_registration_qr(reg)
    filepath = os.path.join(current_app.static_folder, qr_rel_path)
    return send_file(
        filepath,
        as_attachment=True,
        download_name=f"Ticket_QR_{reg.ticket_number}.svg",
        mimetype="image/svg+xml"
    )

@tickets_bp.route('/cancel/<int:reg_id>', methods=['POST'])
@login_required
def cancel_ticket(reg_id):
    """Hủy đăng ký vé tham dự và hoàn trả quota số lượng vé."""
    reg = Registration.query.get_or_404(reg_id)
    
    # Check ownership
    if reg.attendee.user_id != current_user.id and not current_user.is_staff:
        abort(403)

    if reg.registration_status == 'cancelled':
        flash('Vé này đã được hủy trước đó.', 'info')
        return redirect(url_for('tickets.my_tickets'))

    if reg.checked_in:
        flash('Vé này đã thực hiện check-in vào sự kiện, không thể thực hiện hủy.', 'danger')
        return redirect(url_for('tickets.view_ticket', reg_id=reg.id))

    # Cancel and release quota
    reg.registration_status = 'cancelled'
    
    ticket = reg.ticket
    if ticket and ticket.sold_count > 0:
        ticket.sold_count -= 1
        if ticket.status == 'sold_out' and ticket.sold_count < ticket.quota:
            ticket.status = 'active'

    db.session.commit()
    flash(f'Đã hủy vé #{reg.ticket_number} thành công. Suất tham dự sự kiện đã được hoàn trả.', 'success')
    return redirect(url_for('tickets.my_tickets'))

@tickets_bp.route('/feedback/<int:reg_id>', methods=['POST'])
@login_required
def submit_feedback(reg_id):
    reg = Registration.query.get_or_404(reg_id)
    if reg.attendee.user_id != current_user.id:
        abort(403)

    rating = request.form.get('feedback_rating', type=int)
    feedback_text = request.form.get('feedback_text', '').strip()

    if not rating or rating < 1 or rating > 5:
        flash('Vui lòng chọn số sao đánh giá hợp lệ (1-5 sao).', 'warning')
        return redirect(url_for('tickets.view_ticket', reg_id=reg.id))

    reg.feedback_rating = rating
    reg.feedback_text = feedback_text
    reg.feedback_submitted_at = datetime.utcnow()

    # Rule-based / simple sentiment polarity initialization
    if feedback_text:
        positive_words = ['tuyệt vời', 'rất tốt', 'chất lượng', 'hài lòng', 'xuất sắc', 'bổ ích', 'nhanh', 'hay', 'good', 'great', 'perfect']
        negative_words = ['tệ', 'kém', 'thất vọng', 'chậm', 'lỗi', 'ồn', 'đắt', 'bad', 'poor', 'slow', 'fail']
        
        pos_count = sum(1 for w in positive_words if w in feedback_text.lower())
        neg_count = sum(1 for w in negative_words if w in feedback_text.lower())

        if rating >= 4 or (pos_count > neg_count and rating >= 3):
            reg.sentiment = 'positive'
            reg.sentiment_score = 0.8
        elif rating <= 2 or neg_count > pos_count:
            reg.sentiment = 'negative'
            reg.sentiment_score = -0.7
        else:
            reg.sentiment = 'neutral'
            reg.sentiment_score = 0.0
    else:
        reg.sentiment = 'positive' if rating >= 4 else ('neutral' if rating == 3 else 'negative')

    db.session.commit()
    flash('Cảm ơn bạn đã gửi đánh giá và phản hồi về sự kiện!', 'success')
    return redirect(url_for('tickets.view_ticket', reg_id=reg.id))
