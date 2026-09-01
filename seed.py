"""
Database Seeder Script.
Fills the SQLite database with rich, realistic mock data for 10+ major tech & ICTU events, speakers, venues, schedules, tickets, registrations, and AI chat logs.
"""
from datetime import datetime, timedelta
import os
import sys
import qrcode
import qrcode.image.svg

sys.stdout.reconfigure(encoding='utf-8')
from app import create_app
from app.extensions import db
from app.models import (
    User, Speaker, Venue, Event, Schedule,
    Attendee, Ticket, Registration, AIChatHistory
)

app = create_app('development')

def generate_sample_qr(ticket_number):
    """Generates and saves a scalable SVG QR code for a given ticket number."""
    qr_dir = os.path.join(app.static_folder, 'qr_codes')
    os.makedirs(qr_dir, exist_ok=True)
    filename = f"{ticket_number}.svg"
    filepath = os.path.join(qr_dir, filename)
    
    factory = qrcode.image.svg.SvgImage
    img = qrcode.make(ticket_number, image_factory=factory)
    img.save(filepath)
    return f"qr_codes/{filename}"

def run_seed():
    with app.app_context():
        print("🌱 Đang làm sạch và khởi tạo lại Cơ sở Dữ liệu 9 bảng chuẩn 3NF...")
        db.drop_all()
        db.create_all()

        # ==========================================
        # 1. TẠO USERS
        # ==========================================
        print("👤 Đang tạo Users mẫu...")
        admin = User(
            username='admin',
            email='admin@eventai.vn',
            full_name='Quản Trị Viên Hệ Thống',
            role='admin',
            phone='0901234567',
            avatar_url='https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150'
        )
        admin.set_password('Admin@123')

        staff = User(
            username='staff1',
            email='staff@eventai.vn',
            full_name='Nguyễn Văn Điều Phối',
            role='staff',
            phone='0912345678',
            avatar_url='https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150'
        )
        staff.set_password('Staff@123')

        user1 = User(
            username='attendee1',
            email='tuan.nguyen@techcorp.vn',
            full_name='Nguyễn Quốc Tuấn',
            role='attendee',
            phone='0987654321',
            avatar_url='https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150'
        )
        user1.set_password('User@123')

        user2 = User(
            username='attendee2',
            email='mai.tran@datasol.ai',
            full_name='Trần Tuyết Mai',
            role='attendee',
            phone='0976543210',
            avatar_url='https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=150'
        )
        user2.set_password('User@123')

        user3 = User(
            username='attendee3',
            email='hoang.le@aiinnovate.org',
            full_name='Lê Huy Hoàng',
            role='attendee',
            phone='0965432109',
            avatar_url='https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?w=150'
        )
        user3.set_password('User@123')

        user4 = User(
            username='attendee4',
            email='quan.do@ictu.edu.vn',
            full_name='Đỗ Minh Quân',
            role='attendee',
            phone='0934567890',
            avatar_url='https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150'
        )
        user4.set_password('User@123')

        user5 = User(
            username='attendee5',
            email='linh.hoang@cybersec.vn',
            full_name='Hoàng Thùy Linh',
            role='attendee',
            phone='0945678901',
            avatar_url='https://images.unsplash.com/photo-1517841905240-472988babdf9?w=150'
        )
        user5.set_password('User@123')

        user6 = User(
            username='attendee6',
            email='dung.pham@startuphub.vn',
            full_name='Phạm Tiến Dũng',
            role='attendee',
            phone='0956789012',
            avatar_url='https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?w=150'
        )
        user6.set_password('User@123')

        db.session.add_all([admin, staff, user1, user2, user3, user4, user5, user6])
        db.session.commit()

        # ==========================================
        # 2. TẠO ATTENDEE PROFILES
        # ==========================================
        print("🏷️ Đang tạo Attendee Profiles...")
        att1 = Attendee(
            attendee_code='ATT-2026-001',
            user_id=user1.id,
            full_name=user1.full_name,
            email=user1.email,
            phone=user1.phone,
            organization='TechCorp Solutions Vietnam',
            job_title='Senior Software Engineer',
            interests='Trí tuệ nhân tạo, GenAI, Machine Learning, Python, Full-stack, Deep Learning, ICTU'
        )
        att2 = Attendee(
            attendee_code='ATT-2026-002',
            user_id=user2.id,
            full_name=user2.full_name,
            email=user2.email,
            phone=user2.phone,
            organization='Trường ĐH CNTT & Truyền Thông - ICTU',
            job_title='Sinh viên Khóa K20 - ICTU',
            interests='Big Data, LLM, Phân tích dữ liệu, RAG Chatbot, AI Agents, Python, Lễ tốt nghiệp ICTU'
        )
        att3 = Attendee(
            attendee_code='ATT-2026-003',
            user_id=user3.id,
            full_name=user3.full_name,
            email=user3.email,
            phone=user3.phone,
            organization='Global Cloud & DevOps Initiative',
            job_title='Cloud Solutions Architect',
            interests='Cloud Computing, DevOps, Kubernetes, AI Infrastructure, Microservices'
        )
        att4 = Attendee(
            attendee_code='ATT-2026-004',
            user_id=user4.id,
            full_name=user4.full_name,
            email=user4.email,
            phone=user4.phone,
            organization='CLB AI & Robotics - ICTU Thái Nguyên',
            job_title='Đội trưởng Đội Hackathon ICTU',
            interests='GenAI, Robotics, IoT, Python, Deep Learning, AI Hackathon'
        )
        att5 = Attendee(
            attendee_code='ATT-2026-005',
            user_id=user5.id,
            full_name=user5.full_name,
            email=user5.email,
            phone=user5.phone,
            organization='Trung tâm An toàn Thông tin Quốc gia',
            job_title='Chuyên gia Bảo mật & Zero Trust',
            interests='Cybersecurity, AI Fraud Detection, DevSecOps, Cloud Security'
        )
        att6 = Attendee(
            attendee_code='ATT-2026-006',
            user_id=user6.id,
            full_name=user6.full_name,
            email=user6.email,
            phone=user6.phone,
            organization='Vườn ươm Khởi nghiệp Đổi mới Sáng tạo',
            job_title='Founder & Giám đốc Điều hành',
            interests='Fintech, Startup, AI Product, Đầu tư mạo hiểm, ESG Tech'
        )
        db.session.add_all([att1, att2, att3, att4, att5, att6])
        db.session.commit()

        # ==========================================
        # 3. TẠO SPEAKERS (BAO GỒM DIỄN GIẢ ICTU & CHUYÊN GIA)
        # ==========================================
        print("🎤 Đang tạo Diễn giả chuyên gia & Thầy Cô ICTU...")
        spk1 = Speaker(
            name='TS. Lê Quang Dũng',
            title='Trưởng Viện Nghiên cứu Trí tuệ Nhân tạo',
            bio='Hơn 15 năm nghiên cứu và giảng dạy về Deep Learning, Transformer và Agentic AI tại các viện công nghệ hàng đầu.',
            organization='AI Innovation Hub Vietnam',
            avatar_url='https://images.unsplash.com/photo-1560250097-0b93528c311a?w=200',
            email='dung.le@aihub.vn'
        )
        spk2 = Speaker(
            name='Bà Phạm Phương Thảo',
            title='CTO & VP of Technology',
            bio='Chuyên gia hàng đầu về xây dựng hệ thống phân tán chịu tải lớn, bảo mật Zero Trust và tích hợp giải pháp AI vào doanh nghiệp.',
            organization='CloudScale Asia Pacific',
            avatar_url='https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=200',
            email='thao.pham@cloudscale.asia'
        )
        spk3 = Speaker(
            name='Ông Michael Hoàng',
            title='Principal Solutions Architect',
            bio='Tác giả nhiều cuốn sách về MLOps, RAG Pipeline và ứng dụng LLM trong tự động hóa kỹ nghệ phần mềm.',
            organization='Google Cloud Partner Network',
            avatar_url='https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=200',
            email='michael.hoang@gcloudpartners.com'
        )
        spk4 = Speaker(
            name='PGS.TS. Phùng Trung Nghĩa',
            title='Hiệu Trưởng Trường ĐH CNTT & Truyền Thông Thái Nguyên (ICTU)',
            bio='Nhà lãnh đạo giáo dục tiên phong trong đổi mới giảng dạy công nghệ số, trí tuệ nhân tạo và hợp tác đào tạo quốc tế tại ICTU.',
            organization='Trường ĐH CNTT & TT Thái Nguyên - ICTU',
            avatar_url='https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=200',
            email='ptnghia@ictu.edu.vn'
        )
        spk5 = Speaker(
            name='TS. Vũ Vinh Quang',
            title='Trưởng Khoa Công nghệ Thông tin - ICTU',
            bio='Chuyên gia đầu ngành về Khoa học Máy tính, xử lý ảnh y tế và các giải pháp phần mềm thông minh ứng dụng trong đời sống.',
            organization='Khoa CNTT - Trường ĐH CNTT & TT Thái Nguyên',
            avatar_url='https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=200',
            email='vvquang@ictu.edu.vn'
        )
        spk6 = Speaker(
            name='Ông Hoàng Nam Tiến',
            title='Chuyên gia Chiến Lược & Cố Vấn Khởi Nghiệp Công Nghệ',
            bio='Diễn giả truyền cảm hứng hàng đầu về Chuyển đổi số, Kỹ năng làm việc thời đại AI và định hướng tương lai cho thế hệ sinh viên IT.',
            organization='Tập đoàn Công nghệ FPT',
            avatar_url='https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=200',
            email='tien.hn@fpt.com.vn'
        )
        db.session.add_all([spk1, spk2, spk3, spk4, spk5, spk6])
        db.session.commit()

        # ==========================================
        # 4. TẠO VENUES (ĐỊA ĐIỂM TỔ CHỨC)
        # ==========================================
        print("🏢 Đang tạo Địa điểm tổ chức (Hà Nội, TP.HCM & ICTU Thái Nguyên)...")
        vne_ictu1 = Venue(
            venue_code='VNE-ICTU-C1',
            name='Hội trường Lớn C1 - Trường ĐH CNTT & TT Thái Nguyên (ICTU)',
            address='Đường Z115, Xã Quyết Thắng, Thành phố Thái Nguyên',
            capacity=1500,
            room_name='Hội trường Trọng thể C1',
            description='Hội trường quy mô lớn nhất ICTU với hệ thống âm thanh, ánh sáng chuyên nghiệp, màn hình LED kích thước lớn phục vụ các sự kiện trọng đại.'
        )
        vne_ictu2 = Venue(
            venue_code='VNE-ICTU-LAB',
            name='Trung tâm Đổi Mới Sáng Tạo & AI Lab Tòa nhà D - ICTU',
            address='Tòa nhà D, Trường ĐH CNTT & TT Thái Nguyên, TP. Thái Nguyên',
            capacity=300,
            room_name='Phòng Lab AI & Smart IoT Innovation',
            description='Không gian công nghệ hiện đại, trang bị máy trạm GPU cấu hình cao và internet tốc độ cao chuyên dụng cho Hackathon.'
        )
        vne_ictu3 = Venue(
            venue_code='VNE-ICTU-SQUARE',
            name='Quảng trường & Sảnh Tòa nhà Trung tâm ICTU',
            address='Khuôn viên Trường ĐH CNTT & TT Thái Nguyên, TP. Thái Nguyên',
            capacity=3000,
            room_name='Khu phức hợp Triển lãm & Ngày hội Việc làm',
            description='Không gian ngoài trời thoáng đãng, nơi diễn ra các gian hàng doanh nghiệp và hoạt động trải nghiệm công nghệ.'
        )
        vne1 = Venue(
            venue_code='VNE-NCC-01',
            name='Trung tâm Hội nghị Quốc gia Hà Nội',
            address='Số 57 Phạm Hùng, Mễ Trì, Nam Từ Liêm, Hà Nội',
            capacity=1200,
            room_name='Hội trường Grand Hall A',
            description='Hội trường hiện đại với màn hình LED 4K 500 inch, hệ thống âm thanh vòm tiêu chuẩn quốc tế.'
        )
        vne2 = Venue(
            venue_code='VNE-JWM-02',
            name='Khách sạn JW Marriott Hanoi',
            address='Số 8 Đỗ Đức Dục, Mễ Trì, Nam Từ Liêm, Hà Nội',
            capacity=450,
            room_name='Phòng Hội nghị Lotus Ballroom',
            description='Không gian hội thảo sang trọng, dịch vụ teabreak cao cấp, phù hợp cho networking VIP.'
        )
        vne3 = Venue(
            venue_code='VNE-GEM-03',
            name='Trung tâm Sự kiện GEM Center TP.HCM',
            address='Số 8 Nguyễn Bỉnh Khiêm, Đa Kao, Quận 1, TP. Hồ Chí Minh',
            capacity=800,
            room_name='Sảnh Castor & Pollux Hall',
            description='Không gian sự kiện đẳng cấp bậc nhất TP.HCM với ánh sáng lập trình thông minh.'
        )
        vne5 = Venue(
            venue_code='VNE-ONL-05',
            name='Nền tảng Trực tuyến Metaverse & Zoom High-Quality',
            address='Online Streaming URL: https://meet.eventai.vn/live',
            capacity=5000,
            room_name='Virtual Global Stage 01',
            description='Phát sóng trực tiếp với độ trễ siêu thấp (<200ms), tương tác hỏi đáp Q&A và dịch thuật AI.'
        )
        db.session.add_all([vne_ictu1, vne_ictu2, vne_ictu3, vne1, vne2, vne3, vne5])
        db.session.commit()

        # ==========================================
        # 5. TẠO CÁC SỰ KIỆN (BAO GỒM SỰ KIỆN ICTU)
        # ==========================================
        print("📅 Đang tạo các Sự kiện công nghệ & Sự kiện Trường ĐH CNTT & TT Thái Nguyên (ICTU)...")
        now = datetime.utcnow()
        
        # 1. ICTU Graduation 2026
        evt_ictu_grad = Event(
            event_code='EVT-ICTU-GRAD-2026',
            title='Lễ Bế Giảng & Trao Bằng Tốt Nghiệp Khóa 2022 - 2026 Trường ĐH CNTT & TT Thái Nguyên (ICTU)',
            description='Sự kiện trọng đại và ý nghĩa nhất năm học 2026 của Trường Đại học Công nghệ Thông tin và Truyền thông Thái Nguyên (ICTU). Vinh danh các tân Kỹ sư, Cử nhân xuất sắc; trao bằng tốt nghiệp và mở ra cánh cửa sự nghiệp công nghệ tương lai.',
            category='Khoa học dữ liệu',
            banner_url='https://images.unsplash.com/photo-1523240795612-9a054b0db644?w=800',
            start_date=now + timedelta(days=3, hours=7, minutes=30),
            end_date=now + timedelta(days=3, hours=12),
            location_type='offline',
            location_address='Hội trường Lớn C1, Trường ĐH CNTT & TT Thái Nguyên, Đường Z115, TP. Thái Nguyên',
            max_attendees=1500,
            status='published',
            tags='ICTU, Lễ tốt nghiệp, Trao bằng, Thái Nguyên, Đại học, Sinh viên',
            created_by=admin.id
        )

        # 2. ICTU Hackathon 2026
        evt_ictu_hack = Event(
            event_code='EVT-ICTU-HACKATHON-2026',
            title='ICTU AI Hackathon 2026: Lập Trình Ứng Dụng GenAI & Chuyển Đổi Số',
            description='Cuộc thi lập trình công nghệ 48 giờ liên tục dành cho sinh viên ICTU và các trường đại học thành viên Đại học Thái Nguyên. Thử thách xây dựng giải pháp AI Agent, RAG Chatbot và ứng dụng thông minh phục vụ cộng đồng.',
            category='Trí tuệ nhân tạo',
            banner_url='https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=800',
            start_date=now + timedelta(days=8, hours=8),
            end_date=now + timedelta(days=10, hours=18),
            location_type='offline',
            location_address='Trung tâm Đổi Mới Sáng Tạo Tòa nhà D - ICTU, TP. Thái Nguyên',
            max_attendees=300,
            status='published',
            tags='ICTU, Hackathon, AI, GenAI, Python, Coding, Sinh viên',
            created_by=admin.id
        )

        # 3. ICTU Career Fair 2026
        evt_ictu_career = Event(
            event_code='EVT-ICTU-CAREER-2026',
            title='Ngày Hội Việc Làm & Hướng Nghiệp ICTU Career Fair 2026: Kết Nối Doanh Nghiệp Công Nghệ',
            description='Quy tụ hơn 40 tập đoàn công nghệ hàng đầu (FPT Software, Viettel, VNPT, Samsung, CMC, MISA) mang đến hơn 1.500 cơ hội việc làm và thực tập cho sinh viên ICTU ngành Công nghệ Thông tin, Kỹ thuật Phần mềm, An toàn Thông tin và Trí tuệ Nhân tạo.',
            category='Startup & Đầu tư',
            banner_url='https://images.unsplash.com/photo-1515187029135-18ee286d815b?w=800',
            start_date=now + timedelta(days=14, hours=8),
            end_date=now + timedelta(days=14, hours=17),
            location_type='offline',
            location_address='Quảng trường & Sảnh Tòa nhà Trung tâm ICTU, TP. Thái Nguyên',
            max_attendees=3000,
            status='published',
            tags='ICTU, Career Fair, Tuyển dụng, Việc làm IT, Doanh nghiệp, Thái Nguyên',
            created_by=admin.id
        )

        # 4. AI Summit 2026
        evt1 = Event(
            event_code='EVT-AISUMMIT-2026',
            title='Vietnam AI Summit 2026: Kỷ Nguyên Agentic AI & RAG Thế Hệ Mới',
            description='Sự kiện công nghệ thường niên quy tụ hơn 1.000 chuyên gia, kỹ sư và nhà lãnh đạo công nghệ nhằm thảo luận về xu hướng AI tạo sinh (GenAI), giải pháp RAG tối ưu chống Hallucination, Agentic AI đa tác vụ và phương pháp ứng dụng thực tiễn trong phát triển phần mềm doanh nghiệp.',
            category='Trí tuệ nhân tạo',
            banner_url='https://images.unsplash.com/photo-1518770660439-4636190af475?w=800',
            start_date=now + timedelta(days=5, hours=8),
            end_date=now + timedelta(days=5, hours=17, minutes=30),
            location_type='hybrid',
            location_address='Trung tâm Hội nghị Quốc gia, Hà Nội & Zoom Live',
            max_attendees=1000,
            status='published',
            tags='AI, GenAI, RAG, Agentic AI, Python, Machine Learning',
            created_by=admin.id
        )

        # 5. Cloud & DevOps TechDay
        evt2 = Event(
            event_code='EVT-CLOUD-2026',
            title='Cloud & DevOps TechDay: Kiến Trúc Microservices & MLOps Triển Khai Thực Tế',
            description='Khám phá các phương pháp tốt nhất khi thiết kế hạ tầng đám mây hiện đại, tự động hóa CI/CD pipeline cho mô hình AI, quản trị cụm Kubernetes đa vùng và tối ưu hóa chi phí vận hành cho doanh nghiệp số.',
            category='Cloud & DevOps',
            banner_url='https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=800',
            start_date=now + timedelta(days=12, hours=9),
            end_date=now + timedelta(days=12, hours=16, minutes=30),
            location_type='offline',
            location_address='Khách sạn JW Marriott Hanoi, Đỗ Đức Dục, Hà Nội',
            max_attendees=400,
            status='published',
            tags='Cloud, DevOps, Kubernetes, MLOps, Microservices, Docker',
            created_by=admin.id
        )

        # 6. Data Science Masterclass
        evt3 = Event(
            event_code='EVT-DATASCI-2026',
            title='Data Science Masterclass: Khai Phá Dữ Liệu Lớn & Dự Báo Thời Gian Thực',
            description='Khóa hội thảo chuyên sâu dành cho Data Analyst và Data Scientist về khai thác dữ liệu phi cấu trúc, trực quan hóa insight kinh doanh và ứng dụng mô hình máy học dự báo hành vi khách hàng với độ chính xác cao.',
            category='Khoa học dữ liệu',
            banner_url='https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800',
            start_date=now + timedelta(days=18, hours=13, minutes=30),
            end_date=now + timedelta(days=18, hours=18),
            location_type='online',
            location_address='Trực tuyến qua Zoom & Google Meet',
            online_meeting_url='https://meet.eventai.vn/datascience-2026',
            max_attendees=500,
            status='published',
            tags='Data Science, Big Data, Predictive Analytics, Python, Visualization',
            created_by=admin.id
        )

        # 7. CyberSecurity DefCamp
        evt5 = Event(
            event_code='EVT-CYBERSEC-2026',
            title='CyberSecurity DefCamp: Chiến Lược Phòng Thủ Zero Trust & An Toàn AI 2026',
            description='Hội nghị an ninh mạng chuyên sâu tập trung vào phòng chống tấn công APT, bảo vệ chuỗi cung ứng phần mềm (Software Supply Chain), kiểm toán bảo mật ứng dụng LLM theo tiêu chuẩn OWASP Top 10 for GenAI.',
            category='Kỹ thuật phần mềm',
            banner_url='https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=800',
            start_date=now + timedelta(days=22, hours=8, minutes=30),
            end_date=now + timedelta(days=22, hours=17),
            location_type='offline',
            location_address='Trung tâm Sự kiện GEM Center, Quận 1, TP. Hồ Chí Minh',
            max_attendees=600,
            status='published',
            tags='CyberSecurity, Zero Trust, OWASP, Penetration Testing, Security',
            created_by=admin.id
        )

        # 8. Hands-on Workshop
        evt8 = Event(
            event_code='EVT-WORKSHOP-2026',
            title='Hands-on Deep Learning & LLM Fine-Tuning Workshop',
            description='Khóa huấn luyện kỹ thuật chuyên sâu 1 ngày dành cho các kỹ sư: Thực hành tinh chỉnh mô hình mã nguồn mở (Llama 3, Mistral), kỹ thuật LoRA, QLoRA, đánh giá benchmark và đóng gói API production.',
            category='Workshop',
            banner_url='https://images.unsplash.com/photo-1531482615713-2afd69097998?w=800',
            start_date=now + timedelta(days=28, hours=8, minutes=30),
            end_date=now + timedelta(days=28, hours=17),
            location_type='offline',
            location_address='Trung tâm Hội nghị Quốc gia, Phòng Hội thảo B, Hà Nội',
            max_attendees=120,
            status='published',
            tags='Workshop, Deep Learning, Fine-tuning, LoRA, LLM, Python',
            created_by=admin.id
        )

        db.session.add_all([evt_ictu_grad, evt_ictu_hack, evt_ictu_career, evt1, evt2, evt3, evt5, evt8])
        db.session.commit()

        # ==========================================
        # 6. TẠO SCHEDULES CHI TIẾT
        # ==========================================
        print("⏰ Đang tạo Lịch trình phiên họp chi tiết...")
        schedules = [
            # ICTU Graduation Schedules
            Schedule(
                event_id=evt_ictu_grad.id, speaker_id=spk4.id, venue_id=vne_ictu1.id,
                title='Khai mạc, Chào cờ & Diễn văn Chúc mừng của Hiệu trưởng ICTU',
                description='Báo cáo tổng kết chặng đường 4 năm học tập, nghiên cứu và rèn luyện của sinh viên khóa 2022-2026 tại ICTU.',
                start_at=evt_ictu_grad.start_date, end_at=evt_ictu_grad.start_date + timedelta(hours=1, minutes=30)
            ),
            Schedule(
                event_id=evt_ictu_grad.id, speaker_id=spk5.id, venue_id=vne_ictu1.id,
                title='Nghi thức Trao Bằng Tốt Nghiệp & Vinh Danh Thủ Khoa Các Ngành CNTT, An Toàn Thông Tin, Trí Tuệ Nhân Tạo',
                description='Trao bằng tốt nghiệp trực tiếp cho các tân kỹ sư, cử nhân và khen thưởng các sinh viên đạt thành tích xuất sắc toàn khóa.',
                start_at=evt_ictu_grad.start_date + timedelta(hours=1, minutes=30), end_at=evt_ictu_grad.start_date + timedelta(hours=3, minutes=30)
            ),
            Schedule(
                event_id=evt_ictu_grad.id, speaker_id=spk6.id, venue_id=vne_ictu1.id,
                title='Chia Sẻ Từ Doanh Nghiệp Liên Kết & Lời Tri Ân Từ Đại Diện Tân Cử Nhân',
                description='Đại diện doanh nghiệp chia sẻ cơ hội nghề nghiệp và đại diện sinh viên phát biểu tri ân thầy cô, cha mẹ.',
                start_at=evt_ictu_grad.start_date + timedelta(hours=3, minutes=30), end_at=evt_ictu_grad.start_date + timedelta(hours=4, minutes=30)
            ),

            # ICTU Hackathon Schedules
            Schedule(
                event_id=evt_ictu_hack.id, speaker_id=spk5.id, venue_id=vne_ictu2.id,
                title='Khai mạc ICTU Hackathon 2026 & Công Bố Đề Bài Lập Trình GenAI',
                description='Hướng dẫn thể lệ cuộc thi, các tiêu chí chấm điểm và giới thiệu hội đồng ban giám khảo.',
                start_at=evt_ictu_hack.start_date, end_at=evt_ictu_hack.start_date + timedelta(hours=2)
            ),
            Schedule(
                event_id=evt_ictu_hack.id, speaker_id=spk3.id, venue_id=vne_ictu2.id,
                title='Phiên Mentoring: Tối Ưu RAG Pipeline & Triển Khai AI Agent Trên Môi Trường Cloud',
                description='Các chuyên gia hỗ trợ kỹ thuật trực tiếp cho từng đội thi để hoàn thiện sản phẩm prototype.',
                start_at=evt_ictu_hack.start_date + timedelta(days=1, hours=2), end_at=evt_ictu_hack.start_date + timedelta(days=1, hours=5)
            ),

            # ICTU Career Fair Schedules
            Schedule(
                event_id=evt_ictu_career.id, speaker_id=spk6.id, venue_id=vne_ictu3.id,
                title='Tọa Đàm: Định Hướng Nghề Nghiệp IT & Bí Quyết Chinh Phục Nhà Tuyển Dụng Năm 2026',
                description='Chuyên gia chia sẻ về xu hướng tuyển dụng kỹ sư phần mềm, AI engineer, data analyst và kỹ năng cần có.',
                start_at=evt_ictu_career.start_date, end_at=evt_ictu_career.start_date + timedelta(hours=2)
            ),
            Schedule(
                event_id=evt_ictu_career.id, speaker_id=spk2.id, venue_id=vne_ictu3.id,
                title='Phỏng Vấn & Nhận CV Trực Tiếp Tại Các Gian Hàng Doanh Nghiệp Công Nghệ',
                description='Hơn 40 doanh nghiệp tiến hành phỏng vấn nhanh và tuyển chọn ứng viên tiềm năng ngay tại khuôn viên trường.',
                start_at=evt_ictu_career.start_date + timedelta(hours=2, minutes=30), end_at=evt_ictu_career.start_date + timedelta(hours=8)
            ),

            # AI Summit Schedules
            Schedule(
                event_id=evt1.id, speaker_id=spk1.id, venue_id=vne1.id,
                title='Khai mạc & Keynote: Xu hướng Agentic AI và Đột phá của RAG trong năm 2026',
                description='Tổng quan kiến trúc mô hình ngôn ngữ lớn, các mẫu thiết kế Agentic AI (Reflection, Tool Use, Planning).',
                start_at=evt1.start_date, end_at=evt1.start_date + timedelta(hours=1, minutes=30)
            ),
            Schedule(
                event_id=evt1.id, speaker_id=spk3.id, venue_id=vne1.id,
                title='Workshop Thực hành: Xây dựng RAG Chatbot doanh nghiệp chống Hallucination',
                description='Hướng dẫn chi tiết từ khâu xử lý tài liệu, embedding, vector store đến kỹ thuật prompt 5 thành phần.',
                start_at=evt1.start_date + timedelta(hours=2), end_at=evt1.start_date + timedelta(hours=4)
            )
        ]
        db.session.add_all(schedules)
        db.session.commit()

        # ==========================================
        # 7. TẠO HẠNG VÉ (TICKETS) CHO TOÀN BỘ SỰ KIỆN
        # ==========================================
        print("🎟️ Đang tạo các Hạng vé cho toàn bộ sự kiện...")
        tickets = [
            # ICTU Graduation Tickets
            Ticket(event_id=evt_ictu_grad.id, ticket_code='TCK-ICTU-GRAD-STUDENT', ticket_type='free', name='Vé Tân Cử Nhân / Kỹ Sư ICTU (Miễn Phí)', description='Dành cho sinh viên tốt nghiệp nhận bằng và quà lưu niệm từ Ban Giám Hiệu.', price=0.0, quota=1200, sold_count=350),
            Ticket(event_id=evt_ictu_grad.id, ticket_code='TCK-ICTU-GRAD-GUEST', ticket_type='vip', name='Vé Khách Mời & Phụ Huynh Danh Dự (VIP)', description='Khu vực ghế ngồi danh dự hàng đầu dành cho Phụ huynh và Khách quý.', price=0.0, quota=300, sold_count=120),

            # ICTU Hackathon Tickets
            Ticket(event_id=evt_ictu_hack.id, ticket_code='TCK-ICTU-HACK-TEAM', ticket_type='free', name='Vé Đội Thi Hackathon (Miễn Phí)', description='Bao gồm không gian làm việc 48h, tài nguyên AI Cloud, ăn trưa và áo thi đấu ICTU.', price=0.0, quota=60, sold_count=25),
            Ticket(event_id=evt_ictu_hack.id, ticket_code='TCK-ICTU-HACK-GUEST', ticket_type='standard', name='Vé Khán Giả Cổ Vũ & Demo Day', description='Tham quan các gian trưng bày sản phẩm AI của sinh viên và cổ vũ chung kết.', price=0.0, quota=200, sold_count=80),

            # ICTU Career Fair Tickets
            Ticket(event_id=evt_ictu_career.id, ticket_code='TCK-ICTU-CAREER-STD', ticket_type='free', name='Vé Tham Quan & Ứng Tuyển Việc Làm', description='Vào cửa tự do, nộp CV và phỏng vấn trực tiếp tại tất cả 40+ gian hàng.', price=0.0, quota=2500, sold_count=650),

            # Event AI Summit
            Ticket(event_id=evt1.id, ticket_code='TCK-AISUMMIT-FREE', ticket_type='free', name='Vé Tiêu Chuẩn (Miễn Phí)', description='Tham gia toàn bộ các phiên hội thảo chính, nhận tài liệu sự kiện dạng số.', price=0.0, quota=600, sold_count=150),
            Ticket(event_id=evt1.id, ticket_code='TCK-AISUMMIT-VIP', ticket_type='vip', name='Vé VIP All-Access & Gala Dinner', description='Vị trí ngồi hàng đầu, tham gia Workshop thực hành, tiệc giao lưu riêng cùng diễn giả và quà tặng độc quyền.', price=990000.0, quota=100, sold_count=45),
            
            # Event Cloud
            Ticket(event_id=evt2.id, ticket_code='TCK-CLOUD-STD', ticket_type='standard', name='Vé Tham Dự Tiêu Chuẩn', description='Tham gia tất cả các chuyên đề Cloud & DevOps, Teabreak cao cấp.', price=250000.0, quota=200, sold_count=85),
            Ticket(event_id=evt2.id, ticket_code='TCK-CLOUD-VIP', ticket_type='vip', name='Vé VIP Executive', description='Tham gia phiên thảo luận bàn tròn riêng và ăn trưa cùng diễn giả CTO.', price=850000.0, quota=50, sold_count=20),

            # Event Data Science
            Ticket(event_id=evt3.id, ticket_code='TCK-DATASCI-FREE', ticket_type='free', name='Vé Trực Tuyến Miễn Phí', description='Truy cập phòng Zoom chất lượng cao và nhận slide bài giảng sau sự kiện.', price=0.0, quota=500, sold_count=220),

            # Event CyberSecurity
            Ticket(event_id=evt5.id, ticket_code='TCK-CYBER-STD', ticket_type='standard', name='Vé Tiêu Chuẩn DefCamp', description='Tham dự phiên phân tích tình huống mã độc và nhận chứng nhận tham dự điện tử.', price=300000.0, quota=300, sold_count=110),
            
            # Event Workshop
            Ticket(event_id=evt8.id, ticket_code='TCK-WS-PRO', ticket_type='standard', name='Vé Tham Dự Workshop Chuyên Sâu', description='Bao gồm tài nguyên GPU Cloud, máy tính thực hành tại phòng Lab và tài liệu huấn luyện.', price=500000.0, quota=120, sold_count=60)
        ]
        db.session.add_all(tickets)
        db.session.commit()

        # ==========================================
        # 8. TẠO REGISTRATIONS MẪU CÓ MÃ QR VECTOR SVG ĐỘC NHẤT
        # ==========================================
        print("📋 Đang tạo Registrations & QR Codes mẫu cho nhiều sự kiện...")
        
        # 1. User 1 đăng ký VIP Event 1 (AI Summit) - ĐÃ CHECK-IN
        t_vip1 = tickets[6]
        t_num1 = 'TCK-NUM-2026-001-AI'
        qr1_path = generate_sample_qr(t_num1)
        reg1 = Registration(
            registration_code='REG-2026-0001',
            event_id=evt1.id,
            attendee_id=att1.id,
            ticket_id=t_vip1.id,
            registration_status='confirmed',
            payment_status='paid',
            payment_ref='TRANS-VNPAY-98765432',
            payment_amount=t_vip1.price,
            paid_at=now - timedelta(days=2),
            ticket_number=t_num1,
            qr_code_path=qr1_path,
            checked_in=True,
            checked_in_at=now - timedelta(days=1, hours=2),
            checked_in_by='staff1',
            feedback_rating=5,
            feedback_text='Sự kiện cực kỳ chất lượng! Diễn giả chia sẻ rất sâu về Agentic AI, hệ thống check-in quét mã QR siêu nhanh dưới 1 giây.',
            sentiment='positive',
            sentiment_score=0.92,
            feedback_submitted_at=now - timedelta(hours=10)
        )

        # 2. User 2 (Trần Tuyết Mai) đăng ký Lễ Tốt Nghiệp ICTU 2026 - CHƯA CHECK-IN
        t_grad = tickets[0]
        t_num2 = 'TCK-NUM-2026-ICTU-001'
        qr2_path = generate_sample_qr(t_num2)
        reg2 = Registration(
            registration_code='REG-2026-ICTU-0001',
            event_id=evt_ictu_grad.id,
            attendee_id=att2.id,
            ticket_id=t_grad.id,
            registration_status='confirmed',
            payment_status='free',
            payment_amount=0.0,
            ticket_number=t_num2,
            qr_code_path=qr2_path,
            checked_in=False,
            feedback_rating=5,
            feedback_text='Em rất tự hào là sinh viên Trường ĐH CNTT & TT Thái Nguyên - ICTU! Buổi lễ tốt nghiệp được tổ chức trang trọng và chuyên nghiệp.',
            sentiment='positive',
            sentiment_score=0.98,
            feedback_submitted_at=now - timedelta(hours=3)
        )

        # 3. User 3 (Lê Huy Hoàng) đăng ký Standard Event 2 (Cloud) - CHƯA CHECK-IN
        t_std2 = tickets[7]
        t_num3 = 'TCK-NUM-2026-003-CL'
        qr3_path = generate_sample_qr(t_num3)
        reg3 = Registration(
            registration_code='REG-2026-0003',
            event_id=evt2.id,
            attendee_id=att3.id,
            ticket_id=t_std2.id,
            registration_status='confirmed',
            payment_status='paid',
            payment_ref='TRANS-MOMO-11223344',
            payment_amount=t_std2.price,
            paid_at=now - timedelta(days=1),
            ticket_number=t_num3,
            qr_code_path=qr3_path,
            checked_in=False
        )

        # 4. User 4 (Đỗ Minh Quân) đăng ký VIP Phụ huynh & Khách mời Lễ Tốt Nghiệp ICTU - CHƯA CHECK-IN
        t_grad_vip = tickets[1]
        t_num4 = 'TCK-NUM-2026-ICTU-002-VIP'
        qr4_path = generate_sample_qr(t_num4)
        reg4 = Registration(
            registration_code='REG-2026-ICTU-0002',
            event_id=evt_ictu_grad.id,
            attendee_id=att4.id,
            ticket_id=t_grad_vip.id,
            registration_status='confirmed',
            payment_status='free',
            payment_amount=0.0,
            ticket_number=t_num4,
            qr_code_path=qr4_path,
            checked_in=False
        )

        # 5. User 5 (Hoàng Thùy Linh) đăng ký Tân Cử Nhân Lễ Tốt Nghiệp ICTU - ĐÃ CHECK-IN
        t_num5 = 'TCK-NUM-2026-ICTU-003'
        qr5_path = generate_sample_qr(t_num5)
        reg5 = Registration(
            registration_code='REG-2026-ICTU-0003',
            event_id=evt_ictu_grad.id,
            attendee_id=att5.id,
            ticket_id=t_grad.id,
            registration_status='confirmed',
            payment_status='free',
            payment_amount=0.0,
            ticket_number=t_num5,
            qr_code_path=qr5_path,
            checked_in=True,
            checked_in_at=now - timedelta(minutes=45),
            checked_in_by='staff1'
        )

        # 6. User 6 (Phạm Tiến Dũng) đăng ký Khách mời Lễ Tốt Nghiệp ICTU - CHƯA CHECK-IN
        t_num6 = 'TCK-NUM-2026-ICTU-004-VIP'
        qr6_path = generate_sample_qr(t_num6)
        reg6 = Registration(
            registration_code='REG-2026-ICTU-0004',
            event_id=evt_ictu_grad.id,
            attendee_id=att6.id,
            ticket_id=t_grad_vip.id,
            registration_status='confirmed',
            payment_status='free',
            payment_amount=0.0,
            ticket_number=t_num6,
            qr_code_path=qr6_path,
            checked_in=False
        )

        # 7. User 4 (Đỗ Minh Quân) đăng ký ICTU Hackathon 2026 - CHƯA CHECK-IN
        t_hack = tickets[2]
        t_num7 = 'TCK-NUM-2026-HACK-001'
        qr7_path = generate_sample_qr(t_num7)
        reg7 = Registration(
            registration_code='REG-2026-HACK-0001',
            event_id=evt_ictu_hack.id,
            attendee_id=att4.id,
            ticket_id=t_hack.id,
            registration_status='confirmed',
            payment_status='free',
            payment_amount=0.0,
            ticket_number=t_num7,
            qr_code_path=qr7_path,
            checked_in=False
        )

        # 8. User 6 (Phạm Tiến Dũng) đăng ký AI Summit (Free Pass) - CHƯA CHECK-IN
        t_ai_free = tickets[5]
        t_num8 = 'TCK-NUM-2026-AI-FREE-001'
        qr8_path = generate_sample_qr(t_num8)
        reg8 = Registration(
            registration_code='REG-2026-AI-0008',
            event_id=evt1.id,
            attendee_id=att6.id,
            ticket_id=t_ai_free.id,
            registration_status='confirmed',
            payment_status='free',
            payment_amount=0.0,
            ticket_number=t_num8,
            qr_code_path=qr8_path,
            checked_in=False
        )

        db.session.add_all([reg1, reg2, reg3, reg4, reg5, reg6, reg7, reg8])
        db.session.commit()

        # ==========================================
        # 9. TẠO AI CHAT HISTORY MẪU
        # ==========================================
        print("🤖 Đang tạo Lịch sử AI Chat mẫu...")
        chat1 = AIChatHistory(
            user_id=user2.id,
            event_id=evt_ictu_grad.id,
            chat_type='rag_chat',
            user_message='Lễ tốt nghiệp 2026 của trường Đại học CNTT & TT Thái Nguyên (ICTU) diễn ra ở đâu và vào lúc nào?',
            ai_response='**Lễ Bế Giảng & Trao Bằng Tốt Nghiệp Khóa 2022 - 2026** của Trường Đại học Công nghệ Thông tin và Truyền thông Thái Nguyên (ICTU) diễn ra tại **Hội trường Lớn C1 - ICTU** (Đường Z115, Xã Quyết Thắng, TP. Thái Nguyên) vào lúc **07:30 sáng**.\n\nChương trình có sự chủ trì của **PGS.TS. Phùng Trung Nghĩa** (Hiệu trưởng ICTU) cùng sự tham gia của các thầy cô lãnh đạo Khoa và các doanh nghiệp đối tác.\n\nBạn có thể đăng ký vé Tân cử nhân/kỹ sư hoặc vé khách mời miễn phí ngay trên hệ thống!',
            model_name='gemini-2.0-flash',
            response_mode='live',
            latency_ms=1150
        )

        db.session.add(chat1)
        db.session.commit()

        print("✅ Hoàn tất Seed CSDL 9 bảng chuẩn 3NF với các sự kiện trường ĐH CNTT & TT Thái Nguyên (ICTU) và các hội thảo công nghệ lớn!")

if __name__ == '__main__':
    run_seed()
