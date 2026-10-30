"""
EventAI Pro — Windows Staging Database Seeder (Hardened & Secure).
Populates instance_staging/staging.db with synthetic users, events, tickets, and FAQs.
Completely isolated from the production database.
Uses cryptographically secure random passwords stored in instance_staging/.staging_secrets.json.
NEVER prints secrets to stdout or commits them to Git.
"""
import os
import sys
import json
import secrets
import string
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Enforce staging environment
os.environ['FLASK_ENV'] = 'staging'
staging_dir = BASE_DIR / 'instance_staging'
staging_dir.mkdir(parents=True, exist_ok=True)
staging_db_path = staging_dir / 'staging.db'
secrets_file = staging_dir / '.staging_secrets.json'

os.environ['DATABASE_URI'] = f"sqlite:///{staging_db_path}"
os.environ['CANONICAL_DOMAIN'] = 'http://127.0.0.1:5001'

from app import create_app
from app.extensions import db
from app.models import (
    User, Speaker, Venue, Event, Schedule,
    Attendee, Ticket, Registration, AIChatHistory,
    Notification, EventFAQ
)
import qrcode
import qrcode.image.svg
from datetime import datetime, timedelta, timezone

app = create_app('staging')

def get_or_generate_staging_secrets():
    """Retrieves or securely generates unique credentials for staging personas."""
    if secrets_file.exists():
        try:
            with open(secrets_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if all(k in data for k in ['admin', 'staff', 'organizer', 'attendee']):
                    return data
        except Exception:
            pass

    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    def gen_pwd():
        while True:
            pwd = ''.join(secrets.choice(alphabet) for _ in range(18))
            if (any(c.islower() for c in pwd) and
                any(c.isupper() for c in pwd) and
                any(c.isdigit() for c in pwd) and
                any(c in "!@#$%^&*" for c in pwd)):
                return pwd

    credentials = {
        'admin': {
            'username': 'admin_staging',
            'email': 'admin@staging.eventai.local',
            'full_name': 'Quản Trị Viên Staging',
            'role': 'admin',
            'password': gen_pwd()
        },
        'staff': {
            'username': 'staff_staging',
            'email': 'staff@staging.eventai.local',
            'full_name': 'Nhân Viên Soát Vé Staging',
            'role': 'staff',
            'password': gen_pwd()
        },
        'organizer': {
            'username': 'organizer_staging',
            'email': 'organizer@staging.eventai.local',
            'full_name': 'Ban Tổ Chức Staging',
            'role': 'organizer',
            'password': gen_pwd()
        },
        'attendee': {
            'username': 'attendee_staging',
            'email': 'attendee@staging.eventai.local',
            'full_name': 'Khách Mời Staging',
            'role': 'attendee',
            'password': gen_pwd()
        }
    }

    with open(secrets_file, 'w', encoding='utf-8') as f:
        json.dump(credentials, f, indent=2)

    return credentials

def seed_staging_database(force_reseed=False):
    qr_dir = BASE_DIR / 'app' / 'static' / 'qr_codes'
    qr_dir.mkdir(parents=True, exist_ok=True)

    creds = get_or_generate_staging_secrets()

    with app.app_context():
        print(f"[STAGING SEED] Initializing isolated staging tables in: {staging_db_path}")
        db.create_all()

        # Idempotency check: if user table has data and not forcing reseed
        if User.query.first() and not force_reseed:
            print("[STAGING SEED] Staging database already populated. Skipping re-seed.")
            print("[STAGING SEED] Credentials stored safely in: instance_staging\\.staging_secrets.json")
            return

        if force_reseed:
            db.drop_all()
            db.create_all()

        print("[STAGING SEED] Seeding synthetic personas with high-entropy unique credentials...")
        users = {}
        for role_key, udata in creds.items():
            user = User(
                username=udata['username'],
                email=udata['email'],
                full_name=udata['full_name'],
                role=udata['role'],
                phone='0900000000'
            )
            user.set_password(udata['password'])
            db.session.add(user)
            users[role_key] = user

        db.session.commit()

        # Synthetic Attendee Profile
        att_profile = Attendee(
            attendee_code='ATT-STG-2026-001',
            user_id=users['attendee'].id,
            full_name=users['attendee'].full_name,
            email=users['attendee'].email,
            phone=users['attendee'].phone,
            organization='Staging Academic Lab',
            job_title='QA Test Engineer'
        )
        db.session.add(att_profile)

        # Synthetic Venue
        venue = Venue(
            venue_code='VNE-STG-001',
            name='Trung Tâm Hội Thảo Quốc Gia Staging',
            address='Tầng 5, Tòa Nhà Thử Nghiệm, Hà Nội',
            capacity=500
        )
        db.session.add(venue)
        db.session.commit()

        # Synthetic Event
        now = datetime.now(timezone.utc)
        event = Event(
            event_code='EVT-STG-2026',
            title='Hội Thảo Công Nghệ EventAI Pro 2026 (Staging)',
            description='Sự kiện kiểm thử staging bản địa Windows 11 phục vụ nghiệm thu học thuật và đánh giá chất lượng.',
            category='Trí tuệ nhân tạo',
            banner_url='https://images.unsplash.com/photo-1518770660439-4636190af475?w=800',
            start_date=now + timedelta(days=7),
            end_date=now + timedelta(days=7, hours=4),
            location_type='offline',
            location_address='Tầng 5, Tòa Nhà Thử Nghiệm, Hà Nội',
            status='published',
            max_attendees=300,
            tags='AI, Staging, Windows11, Flask'
        )
        db.session.add(event)
        db.session.commit()

        # Synthetic Speaker
        speaker = Speaker(
            name='TS. Nguyễn Văn AI',
            title='Kiến Trúc Sư Trưởng Hệ Thống',
            bio='Tiến sĩ Khoa học Máy tính với các công trình nghiên cứu về Multi-Agent và RAG LLM.',
            organization='Viện Đổi Mới Sáng Tạo',
            email='speaker@staging.eventai.local'
        )
        db.session.add(speaker)
        db.session.commit()

        # Synthetic Schedule
        schedule = Schedule(
            event_id=event.id,
            speaker_id=speaker.id,
            venue_id=venue.id,
            title='Keynote: Ứng Dụng Multi-Agent Trong Quản Trị Sự Kiện',
            description='Phiên thuyết trình chuyên sâu về Critic Guardrail và Local RAG Fallback Engine.',
            start_at=event.start_date,
            end_at=event.start_date + timedelta(hours=2)
        )
        db.session.add(schedule)

        # Synthetic FAQs
        faq1 = EventFAQ(
            event_id=event.id,
            question='Quy trình check-in tại hội thảo staging diễn ra như thế nào?',
            answer='Người tham dự xuất trình mã QR trên vé điện tử trong ứng dụng để nhân viên check-in quét qua camera hoặc mã vé.',
            category='checkin'
        )
        faq2 = EventFAQ(
            event_id=event.id,
            question='Tôi có thể hủy vé và hoàn tiền không?',
            answer='Vé hội thảo miễn phí có thể hủy trực tiếp tại mục Vé Của Tôi trước giờ khai mạc 24 giờ.',
            category='ticketing'
        )
        db.session.add_all([faq1, faq2])
        db.session.commit()

        # Synthetic Ticket
        ticket = Ticket(
            event_id=event.id,
            ticket_code='TCK-STG-001',
            name='Vé Tham Dự Tiêu Chuẩn',
            ticket_type='standard',
            price=0,
            quota=100
        )
        db.session.add(ticket)
        db.session.commit()

        # Synthetic Registration with QR
        ticket_number = f"TCK-{event.id:03d}-0001-STG"
        qr_filename = f"{ticket_number}.svg"
        qr_filepath = qr_dir / qr_filename
        factory = qrcode.image.svg.SvgImage
        img = qrcode.make(ticket_number, image_factory=factory)
        img.save(str(qr_filepath))

        registration = Registration(
            event_id=event.id,
            ticket_id=ticket.id,
            attendee_id=att_profile.id,
            ticket_number=ticket_number,
            qr_code_path=f"qr_codes/{qr_filename}",
            registration_code='REG-STG-202610-001',
            registration_status='confirmed',
            payment_status='free',
            checked_in=False
        )
        db.session.add(registration)
        db.session.commit()

        print("[STAGING SEED] Staging database seeded successfully with synthetic data!")
        print(f"  - Event: {event.title} (ID: {event.id})")
        print(f"  - Ticket Number: {ticket_number} (QR: {qr_filename})")
        print("  - Personas: admin_staging, staff_staging, organizer_staging, attendee_staging")
        print("  - Credentials status: SECURED in instance_staging\\.staging_secrets.json")
        print("  - Local retrieval: Run '.\\.venv\\Scripts\\python.exe scripts\\get_staging_credentials.py'")

if __name__ == '__main__':
    force = '--reseed' in sys.argv
    seed_staging_database(force_reseed=force)
