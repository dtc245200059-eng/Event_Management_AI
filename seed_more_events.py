"""
Comprehensive Diversity Events Seeder for Event Management AI System.
Adds events across:
- Cybersecurity & Zero Trust
- Indie Acoustic Music & Visual Art
- ICTU Innovation & Startup Expo
- Cloud Native, Kubernetes & DevOps
- Vietnamese Game Creators & 3D Spatial
- AI in Healthcare & Smart Life
- Fintech, Banking 4.0 & Open Finance
- UI/UX Design & Human-Centered AI
- Robotics & Smart Manufacturing Expo
- Vietnam University Esports Championship (VEC)
- Green Tech & ESG Sustainability Forum
- Data Science, Big Data & PyData Vietnam
"""
from datetime import datetime, timedelta
from app import create_app
from app.extensions import db
from app.models import User, Event, Ticket, Schedule, Speaker, Venue

app = create_app('development')

with app.app_context():
    admin = User.query.filter_by(role='admin').first()
    admin_id = admin.id if admin else 1

    diverse_events = [
        {
            "event_code": "EVT-2026-FINTECH-001",
            "title": "Vietnam Fintech & Open Banking Summit 2026: Tương Lai Tài Chính Số",
            "description": "Diễn đàn công nghệ tài chính thường niên lớn nhất Việt Nam. Thảo luận về ngân hàng mở (Open Banking), thanh toán không tiếp xúc qua QR/NFC, định danh điện tử eKYC và ứng dụng AI phát hiện gian lận giao dịch theo thời gian thực.",
            "category": "Kinh doanh & Khởi nghiệp",
            "location_type": "offline",
            "location_address": "Trung tâm Hội nghị GEM Center, Số 8 Nguyễn Bỉnh Khiêm, Đa Kao, Quận 1, TP. Hồ Chí Minh",
            "start_date": datetime(2026, 11, 12, 8, 30),
            "end_date": datetime(2026, 11, 12, 17, 30),
            "banner_url": "https://images.unsplash.com/photo-1559526324-4b87b5e36e44?w=800",
            "max_attendees": 450,
            "tags": "Fintech, Open Banking, eKYC, AI Fraud Detection, Thanh toán số",
            "tickets": [
                {"name": "Vé Tham Dự Hội Thảo (Standard)", "ticket_type": "standard", "price": 350000, "quota": 300},
                {"name": "Vé VIP Executive & Tiệc Tối Networking", "ticket_type": "vip", "price": 1500000, "quota": 150}
            ],
            "speakers": [
                {"name": "Ông Trần Quốc Bảo", "title": "Phó Tổng Giám Đốc Công Nghệ", "bio": "Hơn 20 năm dẫn dắt chuyển đổi số ngân hàng lõi (Core Banking).", "organization": "VietBank Digital"},
                {"name": "Bà Jennifer Wong", "title": "Head of Fintech Innovation APAC", "bio": "Chuyên gia tư vấn khung pháp lý Sandbox và Open Finance.", "organization": "Fintech Asia Partners"}
            ],
            "schedules": [
                {"title": "Keynote: Xu hướng Open Banking và Kiến trúc Ngân hàng tương lai", "start_at": datetime(2026, 11, 12, 8, 45), "end_at": datetime(2026, 11, 12, 10, 15), "description": "Chia sẻ kinh nghiệm kết nối API ngân hàng mở an toàn."},
                {"title": "Tọa đàm: Phòng chống lừa đảo trực tuyến bằng Machine Learning", "start_at": datetime(2026, 11, 12, 10, 30), "end_at": datetime(2026, 11, 12, 12, 0), "description": "Giải pháp AI phát hiện tài khoản rác và giao dịch bất thường."},
                {"title": "Triển lãm Demo: Giải pháp Thanh toán một chạm & Sinh trắc học", "start_at": datetime(2026, 11, 12, 13, 30), "end_at": datetime(2026, 11, 12, 16, 30), "description": "Trải nghiệm các máy POS sinh trắc khuôn mặt và lòng bàn tay."}
            ]
        },
        {
            "event_code": "EVT-2026-UIUX-DESIGN-001",
            "title": "UI/UX Design & Human-Centered AI Conference 2026: Kiến Tạo Trải Nghiệm",
            "description": "Hội nghị thường niên dành cho Product Designers, UX Researchers và Design Leads. Khám phá cách kết hợp tư duy thiết kế lấy con người làm trung tâm (Human-Centered) với các công cụ Generative AI, xây dựng Design System quy mô lớn và tối ưu Micro-Interactions.",
            "category": "Thiết kế & Sáng tạo",
            "location_type": "offline",
            "location_address": "Không gian Sáng tạo Complex 01, Số 29 Ngách 31 Ngõ 167 Tây Sơn, Đống Đa, Hà Nội",
            "start_date": datetime(2026, 11, 20, 9, 0),
            "end_date": datetime(2026, 11, 20, 17, 30),
            "banner_url": "https://images.unsplash.com/photo-1581291518857-4e27b48ff24e?w=800",
            "max_attendees": 250,
            "tags": "UI/UX, Product Design, Design System, Figma, AI Co-design, UX Research",
            "tickets": [
                {"name": "Vé Designer Pass (Standard)", "ticket_type": "standard", "price": 280000, "quota": 180},
                {"name": "Vé VIP Masterclass & Portfolio Review", "ticket_type": "vip", "price": 750000, "quota": 70}
            ],
            "speakers": [
                {"name": "Nguyễn Hoàng Minh", "title": "Lead Product Designer", "bio": "Tác giả của Design System phục vụ hơn 15 triệu người dùng ứng dụng di động.", "organization": "Grab Vietnam"},
                {"name": "Bà Đặng Phương Thảo", "title": "Senior UX Researcher", "bio": "Chuyên gia nghiên cứu hành vi người dùng số và khảo sát khả năng tiếp cận (Accessibility).", "organization": "Design Lab Hanoi"}
            ],
            "schedules": [
                {"title": "Keynote: Thiết kế giao diện trong kỷ nguyên AI đàm thoại & Trợ lý ảo", "start_at": datetime(2026, 11, 20, 9, 15), "end_at": datetime(2026, 11, 20, 10, 45), "description": "Tư duy thiết kế giao diện không chạm và đàm thoại tự nhiên."},
                {"title": "Hands-on Workshop: Xây dựng Tokens & Auto Layout nâng cao trên Figma", "start_at": datetime(2026, 11, 20, 11, 0), "end_at": datetime(2026, 11, 20, 12, 30), "description": "Thực hành đồng bộ Design Tokens từ Figma sang Code CSS."},
                {"title": "Portfolio Review trực tiếp 1:1 cùng các Design Director", "start_at": datetime(2026, 11, 20, 14, 0), "end_at": datetime(2026, 11, 20, 16, 30), "description": "Nhận xét và định hướng nghề nghiệp cho các nhà thiết kế trẻ."}
            ]
        },
        {
            "event_code": "EVT-2026-ROBOTICS-001",
            "title": "Vietnam Robotics & Smart Automation Expo 2026: Kỷ Nguyên Robot Hình Người",
            "description": "Triển lãm và trình diễn công nghệ Robot thông minh, Cánh tay robot công nghiệp tự hành AGV/AMR, Robot hình người ứng dụng AI và dây chuyền nhà máy thông minh Smart Factory 4.0.",
            "category": "Kỹ thuật phần mềm",
            "location_type": "offline",
            "location_address": "Trung tâm Hội chợ và Triển lãm Sài Gòn (SECC), 799 Nguyễn Văn Linh, Tân Phú, Quận 7, TP. Hồ Chí Minh",
            "start_date": datetime(2026, 12, 5, 8, 30),
            "end_date": datetime(2026, 12, 5, 17, 30),
            "banner_url": "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=800",
            "max_attendees": 600,
            "tags": "Robotics, Automation, AI Robot, Smart Factory, AGV, Humanoid",
            "tickets": [
                {"name": "Vé Khách Tham Quan Triển Lãm (Miễn Phí)", "ticket_type": "free", "price": 0, "quota": 400},
                {"name": "Vé Hội Thảo Chuyên Gia & B2B Matchmaking", "ticket_type": "vip", "price": 600000, "quota": 200}
            ],
            "speakers": [
                {"name": "TS. Phạm Quang Dũng", "title": "Giám đốc Viện Công nghệ Robot", "bio": "Chuyên gia nghiên cứu thuật toán điều khiển chuyển động Robot bipedal.", "organization": "Viện Hàn lâm KH&CN"},
                {"name": "Mr. Hans Schneider", "title": "VP of Automation Systems", "bio": "Hơn 25 năm tư vấn triển khai dây chuyền tự động hóa nhà máy thông minh tại Đức.", "organization": "KUKA Robotics APAC"}
            ],
            "schedules": [
                {"title": "Khai mạc Expo & Màn trình diễn Robot Hình Người đồng diễn", "start_at": datetime(2026, 12, 5, 9, 0), "end_at": datetime(2026, 12, 5, 10, 0), "description": "Trình diễn khả năng giữ thăng bằng và thao tác tay tinh xảo của Robot AI."},
                {"title": "Hội thảo: Tự động hóa kho vận thông minh với bầy Robot AGV/AMR", "start_at": datetime(2026, 12, 5, 10, 30), "end_at": datetime(2026, 12, 5, 12, 0), "description": "Tối ưu hóa logistics kho hàng với điều phối thuật toán đám mây."},
                {"title": "Cuộc thi Sáng tạo Robot Sinh viên Toàn quốc: Robot Arena 2026", "start_at": datetime(2026, 12, 5, 13, 30), "end_at": datetime(2026, 12, 5, 16, 30), "description": "Tranh tài gay cấn giữa 16 đội Robot tự hành sinh viên các trường đại học."}
            ]
        },
        {
            "event_code": "EVT-2026-ESPORTS-001",
            "title": "Vietnam University Esports Championship 2026 (VEC): Đại Chiến Thể Thao Điện Tử",
            "description": "Vòng Chung Kết Quốc Gia Giải Thể Thao Điện Tử Sinh Viên Toàn Quốc 2026. Nơi hội tụ các đội tuyển sinh viên xuất sắc nhất tranh tài ở các bộ môn Valorant, Liên Minh Huyền Thoại và FC Online cùng các hoạt động Cosplay Festival.",
            "category": "Thể thao & Giải trí",
            "location_type": "offline",
            "location_address": "Nhà thi đấu Thể thao Cầu Giấy, 35 Trần Quý Kiên, Dịch Vọng, Cầu Giấy, Hà Nội",
            "start_date": datetime(2026, 12, 12, 10, 0),
            "end_date": datetime(2026, 12, 12, 21, 0),
            "banner_url": "https://images.unsplash.com/photo-1542751371-adc38448a05e?w=800",
            "max_attendees": 1000,
            "tags": "Esports, Game, Valorant, LMHT, Sinh viên, Cosplay Festival",
            "tickets": [
                {"name": "Vé Khán Đài Cổ Vũ (Standard)", "ticket_type": "standard", "price": 100000, "quota": 700},
                {"name": "Vé VIP Sân Khấu + Áo Đấu & Quà Tặng Độc Quyền", "ticket_type": "vip", "price": 350000, "quota": 300}
            ],
            "speakers": [
                {"name": "Bình luận viên Hoàng Luân", "title": "Esports Caster & Host", "bio": "Bình luận viên thể thao điện tử kỳ cựu với hơn 12 năm kinh nghiệm.", "organization": "Vietnam Esports Federation"},
                {"name": "Tuyển thủ Đỗ Duy Khánh (Levi)", "title": "Đội trưởng Đội tuyển Quốc gia Esports", "bio": "Vận động viên thể thao điện tử chuyên nghiệp nhiều lần vô địch Đông Nam Á.", "organization": "GAM Esports"}
            ],
            "schedules": [
                {"title": "Lễ khai mạc & Chung kết Nhánh Thắng Bộ môn Valorant", "start_at": datetime(2026, 12, 12, 10, 30), "end_at": datetime(2026, 12, 12, 13, 30), "description": "Trận đấu Bo3 kịch tính giữa Đại học Bách Khoa và ICTU Thái Nguyên."},
                {"title": "Cosplay Grand Contest & Giao lưu cùng Streamer nổi tiếng", "start_at": datetime(2026, 12, 12, 14, 0), "end_at": datetime(2026, 12, 12, 16, 0), "description": "Trình diễn hóa trang 50+ nhân vật game và anime ấn tượng."},
                {"title": "Đại Chung Kết Liên Minh Huyền Thoại & Lễ Trao Cúp Vô Địch", "start_at": datetime(2026, 12, 12, 16, 30), "end_at": datetime(2026, 12, 12, 20, 30), "description": "Trận chung kết Bo5 nảy lửa tìm ra nhà vô địch sinh viên toàn quốc 2026."}
            ]
        },
        {
            "event_code": "EVT-2026-GREENTECH-001",
            "title": "Green Tech & ESG Sustainability Forum 2026: Công Nghệ Cho Tương Lai Xanh",
            "description": "Diễn đàn công nghệ xanh và phát triển bền vững ESG. Giới thiệu các giải pháp lưu trữ năng lượng mặt trời, pin thể rắn, cảm biến IoT giám sát chất lượng không khí và chuyển đổi số giảm phát thải ròng Net-Zero.",
            "category": "Môi trường & Công nghệ Xanh",
            "location_type": "hybrid",
            "location_address": "Khách sạn Pan Pacific Hanoi, Số 1 Thanh Niên, Ba Đình, Hà Nội & Livestream",
            "start_date": datetime(2026, 12, 18, 8, 30),
            "end_date": datetime(2026, 12, 18, 17, 0),
            "banner_url": "https://images.unsplash.com/photo-1497435334941-8c899ee9e8e9?w=800",
            "max_attendees": 300,
            "tags": "Green Tech, ESG, Net Zero, Năng lượng sạch, IoT Môi trường, Bền vững",
            "tickets": [
                {"name": "Vé Hội Thảo Xanh (Standard)", "ticket_type": "standard", "price": 200000, "quota": 200},
                {"name": "Vé VIP Doanh Nghiệp ESG & Báo Cáo Chuyên Sâu", "ticket_type": "vip", "price": 800000, "quota": 100}
            ],
            "speakers": [
                {"name": "TS. Lê Thu Hương", "title": "Chuyên gia Kinh tế Môi trường", "bio": "Cố vấn chính sách chuyển dịch năng lượng và thị trường tín chỉ carbon.", "organization": "Viện Chiến lược Môi trường"},
                {"name": "Mr. Eric Lindqvist", "title": "Director of Clean Energy Solutions", "bio": "Hơn 15 năm phát triển dự án điện gió ngoài khơi và lưới điện thông minh tại Bắc Âu.", "organization": "Nordic Green Energy"}
            ],
            "schedules": [
                {"title": "Toàn cảnh Thị trường Tín chỉ Carbon & Lộ trình Net-Zero 2050", "start_at": datetime(2026, 12, 18, 8, 45), "end_at": datetime(2026, 12, 18, 10, 15), "description": "Cách doanh nghiệp công nghệ áp dụng báo cáo ESG theo chuẩn quốc tế."},
                {"title": "Công nghệ Lưu trữ Năng lượng & Ứng dụng IoT trong Giám sát Môi trường", "start_at": datetime(2026, 12, 18, 10, 30), "end_at": datetime(2026, 12, 18, 12, 0), "description": "Giải pháp pin thế hệ mới và mạng lưới sensor quan trắc không khí."},
                {"title": "Tọa đàm: Thúc đẩy Startup Công nghệ Xanh và Quỹ Đầu tư Khí hậu", "start_at": datetime(2026, 12, 18, 13, 30), "end_at": datetime(2026, 12, 18, 16, 0), "description": "Cơ hội nhận tài trợ từ các quỹ đầu tư mạo hiểm xanh quốc tế."}
            ]
        },
        {
            "event_code": "EVT-2026-PYDATA-001",
            "title": "PyData & Big Data Engineering Vietnam 2026: Khai Phóng Dữ Liệu Lớn",
            "description": "Hội nghị kỹ thuật chuyên sâu về Lập trình Python, Khoa học Dữ liệu (Data Science), Kỹ thuật Dữ liệu (Data Engineering) và MLOps. Chia sẻ kinh nghiệm thực chiến xử lý hàng tỷ dòng dữ liệu với Polars, DuckDB, Apache Spark và LLMOps.",
            "category": "Kỹ thuật phần mềm",
            "location_type": "offline",
            "location_address": "Hội trường Đại học Bách Khoa Hà Nội, Số 1 Đại Cồ Việt, Hai Bà Trưng, Hà Nội",
            "start_date": datetime(2026, 12, 22, 8, 30),
            "end_date": datetime(2026, 12, 22, 17, 30),
            "banner_url": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=800",
            "max_attendees": 400,
            "tags": "Python, PyData, Big Data, Data Science, MLOps, DuckDB, Polars",
            "tickets": [
                {"name": "Vé Sinh Viên & Lập Trình Viên (Standard)", "ticket_type": "standard", "price": 200000, "quota": 300},
                {"name": "Vé VIP Tech Lead + MLOps Workshop Chuyên Sâu", "ticket_type": "vip", "price": 650000, "quota": 100}
            ],
            "speakers": [
                {"name": "Kỹ sư Vũ Thành Nam", "title": "Principal Data Engineer", "bio": "Kiến trúc sư hệ thống Data Lakehouse xử lý hơn 10TB dữ liệu/ngày.", "organization": "VNG Corporation"},
                {"name": "TS. Đỗ Hải Đăng", "title": "Data Science Director", "bio": "Tác giả thư viện mã nguồn mở Python về phân tích chuỗi thời gian.", "organization": "PyData Vietnam Community"}
            ],
            "schedules": [
                {"title": "Keynote: Tăng tốc Data Pipeline với Polars và DuckDB thay thế Pandas", "start_at": datetime(2026, 12, 22, 9, 0), "end_at": datetime(2026, 12, 22, 10, 30), "description": "Kỹ thuật tối ưu hóa CPU đa luồng và vectorization trong Python."},
                {"title": "Xây dựng Hệ thống MLOps & Đánh giá LLM (LLMEval) trong Doanh nghiệp", "start_at": datetime(2026, 12, 22, 10, 45), "end_at": datetime(2026, 12, 22, 12, 15), "description": "Tự động hóa chu trình CI/CD cho mô hình Machine Learning."},
                {"title": "Workshop Hands-on: Xây dựng Real-time Data Streaming với Apache Kafka", "start_at": datetime(2026, 12, 22, 13, 30), "end_at": datetime(2026, 12, 22, 16, 30), "description": "Thực hành trực tiếp xử lý luồng dữ liệu thời gian thực không độ trễ."}
            ]
        }
    ]

    added = 0
    for data in diverse_events:
        existing = Event.query.filter_by(event_code=data["event_code"]).first()
        if not existing:
            existing = Event.query.filter_by(title=data["title"]).first()

        if existing:
            print(f"Skipping existing: {data['event_code']}")
            continue

        evt = Event(
            event_code=data["event_code"],
            title=data["title"],
            description=data["description"],
            category=data["category"],
            location_type=data["location_type"],
            location_address=data["location_address"],
            start_date=data["start_date"],
            end_date=data["end_date"],
            banner_url=data["banner_url"],
            max_attendees=data["max_attendees"],
            status="published",
            tags=data.get("tags", ""),
            created_by=admin_id
        )
        db.session.add(evt)
        db.session.flush()

        for idx, t_info in enumerate(data["tickets"], 1):
            t_code = f"TCK-{evt.id:03d}-{idx:02d}-{t_info['ticket_type'].upper()}"
            t = Ticket(
                event_id=evt.id,
                ticket_code=t_code,
                name=t_info["name"],
                ticket_type=t_info["ticket_type"],
                price=t_info["price"],
                quota=t_info["quota"],
                sold_count=0,
                status="active"
            )
            db.session.add(t)

        created_speakers = []
        for s_info in data["speakers"]:
            spk = Speaker.query.filter_by(name=s_info["name"]).first()
            if not spk:
                spk = Speaker(
                    name=s_info["name"],
                    title=s_info["title"],
                    bio=s_info["bio"],
                    organization=s_info.get("organization", "")
                )
                db.session.add(spk)
                db.session.flush()
            created_speakers.append(spk)

        for idx, sch_info in enumerate(data["schedules"]):
            spk_id = created_speakers[idx % len(created_speakers)].id if created_speakers else None
            sch = Schedule(
                event_id=evt.id,
                title=sch_info["title"],
                start_at=sch_info["start_at"],
                end_at=sch_info["end_at"],
                description=sch_info.get("description", ""),
                speaker_id=spk_id
            )
            db.session.add(sch)

        added += 1

    db.session.commit()
    total = Event.query.count()
    print(f"Hoan tat! Da them thanh cong {added} su kien moi da dang. Tong so su kien hien tai: {total}")

