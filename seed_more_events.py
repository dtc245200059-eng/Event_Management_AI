"""
Comprehensive Diversity Events Seeder for Event Management AI System.
Seeds 10 Diverse High-Quality Events Across Different Topic Verticals:
1. Âm nhạc & Nghệ thuật Thị giác (Acoustic Music & Digital Art)
2. Ẩm thực & Cà phê Đặc sản (Specialty Coffee & Artisan Bakery)
3. Y tế Số & Trí tuệ Nhân tạo Y khoa (HealthTech & AI Healthcare)
4. Game Development & Đồ họa 3D Spatial (Game Dev & Spatial Computing)
5. An toàn Thông tin & Tác chiến Zero Trust (Cybersecurity Summit)
6. Thể thao Marathon & Chạy bộ Tiếp sức (City Night Run Marathon)
7. Nhiếp ảnh Điện ảnh & Drone Flycam (Cinematography & Aerial Arts)
8. Công nghệ Xanh & Phát triển Bền vững (Green Tech & ESG Forum)
9. UI/UX Design & Human-Centered AI (Product Design & Interaction)
10. Fintech & Ngân hàng Số 4.0 (Open Banking & Digital Finance)
"""
import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from datetime import datetime, timedelta
from app import create_app
from app.extensions import db
from app.models import User, Event, Ticket, Schedule, Speaker, Venue

app = create_app('development')

with app.app_context():
    admin = User.query.filter_by(role='admin').first()
    admin_id = admin.id if admin else 1

    now = datetime.now()

    diverse_events = [
        # 1. ÂM NHẠC & NGHỆ THUẬT
        {
            "event_code": "EVT-2026-ACOUSTIC-ART-001",
            "title": "Đêm Nhạc Acoustic & Triển Lãm Nghệ Thuật Ánh Sáng: Giai Điệu Chữa Lành 2026",
            "description": "Không gian thưởng thức âm nhạc mộc acoustic kết hợp trình chiếu nghệ thuật ánh sáng 3D Mapping và sắp đặt thị giác tương tác. Đêm nhạc mang đến trải nghiệm thư giãn tâm hồn cùng những giọng ca Indie tài năng và ban nhạc thính phòng trẻ trung.",
            "category": "Âm nhạc & Nghệ thuật",
            "location_type": "offline",
            "location_address": "Không gian Nghệ thuật Phố đi bộ Hồ Gươm & L’Espace, 24 Tràng Tiền, Hoàn Kiếm, Hà Nội",
            "start_date": now + timedelta(days=12, hours=19),
            "end_date": now + timedelta(days=12, hours=22, minutes=30),
            "banner_url": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=800",
            "max_attendees": 350,
            "tags": "Âm nhạc, Acoustic, Indie, Triển lãm ánh sáng, Nghệ thuật thị giác, Chữa lành",
            "tickets": [
                {"name": "Vé Thưởng Thức Nghệ Thuật (Standard)", "ticket_type": "standard", "price": 250000, "quota": 250},
                {"name": "Vé VIP Ghế Ngồi Hàng Đầu & Thưởng Rượu Vang", "ticket_type": "vip", "price": 600000, "quota": 100}
            ],
            "speakers": [
                {"name": "Nhạc sĩ Trần Hải Đăng", "title": "Giám đốc Nghệ thuật & Nhà sản xuất Âm nhạc", "bio": "Nhà soạn nhạc đoạt nhiều giải thưởng sáng tạo âm nhạc thể nghiệm và phim ảnh.", "organization": "Hanoi Indie Art Studio"},
                {"name": "Nghệ sĩ Thị giác Mai Lan Chi", "title": "Visual Light Artist", "bio": "Chuyên gia nghệ thuật ánh sáng số và sắp đặt công nghệ tương tác tương lai.", "organization": "Visual Arts Collective"}
            ],
            "schedules": [
                {"title": "Khai mạc Triển lãm Ánh sáng & Trải nghiệm Không gian Thị giác Tương tác", "start_at": now + timedelta(days=12, hours=19), "end_at": now + timedelta(days=12, hours=19, minutes=45), "description": "Khách mời tự do tham quan không gian sắp đặt ánh sáng và chụp hình lưu niệm."},
                {"title": "Phần 1: Những Bản Tình Ca Acoustic Mộc Mạc & Hòa Âm Thính Phòng", "start_at": now + timedelta(days=12, hours=19, minutes=45), "end_at": now + timedelta(days=12, hours=21, minutes=0), "description": "Biểu diễn trực tiếp các bản phối acoustic guitar, cello và piano êm dịu."},
                {"title": "Phần 2: Giao Lưu Cùng Nghệ Sĩ & Thưởng Thức Đêm Nhạc Ánh Sáng Gala", "start_at": now + timedelta(days=12, hours=21, minutes=15), "end_at": now + timedelta(days=12, hours=22, minutes=30), "description": "Kết hợp trình chiếu 3D Mapping rực rỡ và những khúc ca cao trào ấm áp."}
            ]
        },

        # 2. ẨM THỰC & CÀ PHÊ ĐẶC SẢN
        {
            "event_code": "EVT-2026-COFFEE-BAKERY-001",
            "title": "Vietnam Specialty Coffee & Bakery Expo 2026: Hương Vị Cà Phê Di Sản",
            "description": "Lễ hội văn hóa cà phê đặc sản và nghệ thuật làm bánh thủ công lớn nhất trong năm. Quy tụ hơn 80 thương hiệu rang xay trứ danh, hạt Arabica Cầu Đất, Robusta Gia Lai, cuộc thi Barista Championship và workshop ghép vị cà phê - bánh ngọt.",
            "category": "Ẩm thực & Đời sống",
            "location_type": "offline",
            "location_address": "Trung tâm Triển lãm Quốc tế I.C.E Hà Nội, 91 Trần Hưng Đạo, Hoàn Kiếm, Hà Nội",
            "start_date": now + timedelta(days=15, hours=8, minutes=30),
            "end_date": now + timedelta(days=17, hours=17, minutes=30),
            "banner_url": "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=800",
            "max_attendees": 1200,
            "tags": "Cà phê, Coffee, Bakery, Barista, Ẩm thực, Thử nếm Cupping, Rang xay",
            "tickets": [
                {"name": "Vé Khách Tham Quan & Thử Nếm Cà Phê (1 Ngày)", "ticket_type": "standard", "price": 150000, "quota": 900},
                {"name": "Vé VIP Trọn Gói 3 Ngày & Tham Gia Barista Masterclass", "ticket_type": "vip", "price": 550000, "quota": 300}
            ],
            "speakers": [
                {"name": "Chuyên gia Thử Nếm Q-Grader Lê Hữu Trí", "title": "Head of Sensory & Green Coffee", "bio": "Chuyên gia Q-Grader quốc tế với hơn 15 năm đánh giá chất lượng hạt cà phê đặc sản.", "organization": "Vietnam Specialty Coffee Association"},
                {"name": "Chef Patissier Sophie Nguyễn", "title": "Bếp trưởng Bánh Nghệ Thuật", "bio": "Tốt nghiệp Học viện Le Cordon Bleu Paris, chuyên gia bánh ngọt phong cách Pháp đương đại.", "organization": "Maison Douce Bakery"}
            ],
            "schedules": [
                {"title": "Khai Mạc Triển Lãm & Trải Nghiệm Cupping Hạt Cà Phê Đặc Sản 3 Miền", "start_at": now + timedelta(days=15, hours=9, minutes=0), "end_at": now + timedelta(days=15, hours=11, minutes=30), "description": "Thử nếm và chấm điểm 20+ mẫu cà phê Arabica và Robusta tuyển chọn."},
                {"title": "Chung Kết Cuộc Thi Pha Chế Nghệ Thuật Vietnam Latte Art Championship", "start_at": now + timedelta(days=15, hours=13, minutes=30), "end_at": now + timedelta(days=15, hours=16, minutes=30), "description": "Màn tranh tài tạo hình bọt sữa điêu luyện của các Barista hàng đầu."},
                {"title": "Masterclass: Kỹ Thuật Ghép Vị Cà Phê Lên Men Cùng Bánh Tart Trái Cây", "start_at": now + timedelta(days=16, hours=10, minutes=0), "end_at": now + timedelta(days=16, hours=12, minutes=0), "description": "Khám phá nguyên lý cân bằng độ chua thanh và vị béo ngậy tinh tế."}
            ]
        },

        # 3. Y TẾ SỐ & AI Y KHOA
        {
            "event_code": "EVT-2026-HEALTHTECH-001",
            "title": "Hội Nghị Y Tế Số & Ứng Dụng AI Trong Chẩn Đoán Y Khoa (HealthTech Summit 2026)",
            "description": "Diễn đàn y tế kỹ thuật số quốc gia về chuyển đổi số bệnh viện thông minh, hồ sơ sức khỏe điện tử (EHR) liên thông, ứng dụng Trí tuệ Nhân tạo trong phân tích ảnh X-quang/CT và phát hiện sớm tế bào ung thư.",
            "category": "Y tế & Sức khỏe",
            "location_type": "hybrid",
            "location_address": "Khách sạn Lotte Hotel Hanoi, 54 Liễu Giai, Ba Đình, Hà Nội & Livestream Trực Tuyến",
            "start_date": now + timedelta(days=19, hours=8, minutes=0),
            "end_date": now + timedelta(days=19, hours=17, minutes=0),
            "banner_url": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=800",
            "max_attendees": 450,
            "tags": "Y tế số, HealthTech, AI Y khoa, Chẩn đoán hình ảnh, Bệnh viện thông minh, EHR",
            "tickets": [
                {"name": "Vé Tham Dự Trực Tuyến (Online Pass)", "ticket_type": "standard", "price": 200000, "quota": 250},
                {"name": "Vé Đại Biểu Trực Tiếp & Kỷ Yếu Báo Cáo Khoa Học (VIP)", "ticket_type": "vip", "price": 950000, "quota": 200}
            ],
            "speakers": [
                {"name": "GS.TS. Bác sĩ Nguyễn Văn Cường", "title": "Viện trưởng Viện Y học Số", "bio": "Chuyên gia đầu ngành ứng dụng công nghệ vi phẫu và chuẩn đoán hình ảnh y sinh.", "organization": "Bệnh viện Bạch Mai & ĐH Y Hà Nội"},
                {"name": "TS. Elena Rostova", "title": "Chief AI Healthcare Scientist", "bio": "Tác giả mô hình Deep Learning chuẩn đoán sớm tổn thương võng mạc tiểu đường.", "organization": "MedTech Europe Research"}
            ],
            "schedules": [
                {"title": "Keynote: Bệnh Viện Thông Minh và Mô Hình Hồ Sơ Bệnh Án Điện Tử Không Giấy Tờ", "start_at": now + timedelta(days=19, hours=8, minutes=30), "end_at": now + timedelta(days=19, hours=10, minutes=0), "description": "Kinh nghiệm thực tiễn số hóa 100% quy trình khám chữa bệnh tại các bệnh viện lớn."},
                {"title": "Tọa đàm: Đột Phá AI Trong Phân Tích Hình Ảnh Cắt Lớp Vi Tính và MRI", "start_at": now + timedelta(days=19, hours=10, minutes=15), "end_at": now + timedelta(days=19, hours=12, minutes=0), "description": "Tăng độ chính xác chuẩn đoán sớm khối u và giảm tải cho bác sĩ X-quang."},
                {"title": "Triển Lãm Thiết Bị Y Tế Đeo Tay IoT Theo Dõi Nhịp Tim và Cảnh Báo Đột Quỵ", "start_at": now + timedelta(days=19, hours=13, minutes=30), "end_at": now + timedelta(days=19, hours=16, minutes=30), "description": "Trải nghiệm cảm biến sinh trắc học liên tục truyền dữ liệu về đám mây."}
            ]
        },

        # 4. GAME DEV & 3D SPATIAL COMPUTING
        {
            "event_code": "EVT-2026-GAMEDEV-3D-001",
            "title": "Vietnam Game Creators & 3D Spatial Computing Conference 2026: Sáng Tạo Thế Giới Ảo",
            "description": "Hội thảo chuyên sâu dành cho lập trình viên Game, họa sĩ 3D Concept, Technical Artists và các Studio game độc lập. Khám phá quy trình dựng thế giới ảo trên Unreal Engine 5.5, Unity 6, công nghệ Spatial Computing và AI tạo tài nguyên game.",
            "category": "Game & Đồ họa 3D",
            "location_type": "offline",
            "location_address": "Trung tâm Đổi mới Sáng tạo Quốc gia (NIC Hòa Lạc), Khu CNC Hòa Lạc, Thạch Thất, Hà Nội",
            "start_date": now + timedelta(days=22, hours=9, minutes=0),
            "end_date": now + timedelta(days=22, hours=18, minutes=0),
            "banner_url": "https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=800",
            "max_attendees": 500,
            "tags": "Game Dev, 3D Spatial, Unreal Engine, Unity, Virtual Reality, Game Studio, Indie Game",
            "tickets": [
                {"name": "Vé Indie Developer Pass (Standard)", "ticket_type": "standard", "price": 200000, "quota": 350},
                {"name": "Vé VIP Studio Leader & Buổi Kết Nối Nhà Phát Hành Quốc Tế", "ticket_type": "vip", "price": 800000, "quota": 150}
            ],
            "speakers": [
                {"name": "Kỹ sư Lê Minh Quang", "title": "Lead Technical Artist & Shader Expert", "bio": "Hơn 10 năm tối ưu hóa đồ họa thời gian thực cho các tựa game AAA quốc tế.", "organization": "Virtuos Vietnam"},
                {"name": "Nhà thiết kế Game Vũ Hà Trang", "title": "Principal Game Designer", "bio": "Tác giả tựa game Indie đạt hơn 5 triệu lượt tải trên Steam và Nintendo Switch.", "organization": "Skyline Game Studio"}
            ],
            "schedules": [
                {"title": "Keynote: Tối Ưu Hóa Ánh Sáng Lumen & Nanite Trong Unreal Engine 5", "start_at": now + timedelta(days=22, hours=9, minutes=15), "end_at": now + timedelta(days=22, hours=10, minutes=45), "description": "Bí quyết dựng bối cảnh hàng triệu đa giác mượt mà 60 FPS trên PC và Console."},
                {"title": "Workshop: Quy Trình Dùng AI Hỗ Trợ Tạo Texture & Rigging Nhân Vật 3D Tự Động", "start_at": now + timedelta(days=22, hours=11, minutes=0), "end_at": now + timedelta(days=22, hours=12, minutes=30), "description": "Rút ngắn 70% thời gian sản xuất tài nguyên đồ họa cho đội ngũ nhỏ."},
                {"title": "Pitching Arena: 10 Đội Game Indie Thuyết Trình Trước Quỹ Đầu Tư Thiên Thần", "start_at": now + timedelta(days=22, hours=14, minutes=0), "end_at": now + timedelta(days=22, hours=17, minutes=30), "description": "Cơ hội nhận gói tài trợ phát hành lên tới 100.000 USD từ các Publisher."}
            ]
        },

        # 5. AN TOÀN THÔNG TIN & ZERO TRUST
        {
            "event_code": "EVT-2026-CYBERSECURITY-001",
            "title": "Vietnam Cyber Security Summit 2026: Tác Chiến Phòng Thủ Số & Zero Trust",
            "description": "Hội nghị cấp cao về an ninh mạng và bảo vệ hạ tầng trọng yếu. Phân tích các mối đe dọa từ tấn công chuỗi cung ứng, mã độc tống tiền Ransomware thế hệ mới, kiến trúc Zero Trust và ứng dụng AI trong điều phối an ninh tự động (SOAR).",
            "category": "An toàn Thông tin",
            "location_type": "offline",
            "location_address": "Trung tâm Hội nghị Quốc gia NCC, Cổng 1 Đại Lộ Thăng Long, Mễ Trì, Nam Từ Liêm, Hà Nội",
            "start_date": now + timedelta(days=25, hours=8, minutes=0),
            "end_date": now + timedelta(days=25, hours=17, minutes=30),
            "banner_url": "https://images.unsplash.com/photo-1563986768609-322da13575f3?w=800",
            "max_attendees": 600,
            "tags": "An ninh mạng, Cybersecurity, Zero Trust, SOC, Ransomware, Phòng thủ số, Bảo mật",
            "tickets": [
                {"name": "Vé Kỹ Sư An Toàn Thông Tin (Standard)", "ticket_type": "standard", "price": 300000, "quota": 400},
                {"name": "Vé VIP CISO Leadership & Tiệc Trưa Kết Nối Cấp Cao", "ticket_type": "vip", "price": 1200000, "quota": 200}
            ],
            "speakers": [
                {"name": "Chuyên gia Vũ Ngọc Sơn", "title": "Giám đốc Công nghệ An ninh Mạng", "bio": "Hơn 20 năm phân tích mã độc và chỉ huy ứng cứu sự cố an ninh mạng cấp quốc gia.", "organization": "Hiệp hội An ninh Mạng Quốc gia"},
                {"name": "Mr. David Miller", "title": "Zero Trust Security Architect", "bio": "Cố vấn kiến trúc bảo mật đám mây và danh tính cho các tập đoàn Fortune 500.", "organization": "Global Cyber Defense Corp"}
            ],
            "schedules": [
                {"title": "Báo Cáo Toàn Cảnh An Ninh Mạng Việt Nam & Xu Hướng Tấn Công Có Chủ Đích (APT)", "start_at": now + timedelta(days=25, hours=8, minutes=45), "end_at": now + timedelta(days=25, hours=10, minutes=15), "description": "Thống kê dữ liệu thực tế về các vụ rò rỉ dữ liệu và bài học đắt giá cho doanh nghiệp."},
                {"title": "Mô Phỏng Trực Tiếp Diễn Tập Tác Chiến Phòng Thủ: Red Team vs Blue Team", "start_at": now + timedelta(days=25, hours=10, minutes=30), "end_at": now + timedelta(days=25, hours=12, minutes=0), "description": "Tấn công và phòng thủ trực tiếp vào hệ sinh thái máy chủ mô phỏng."},
                {"title": "Xây Dựng Trung Tâm Điều Hành An Ninh Mạng Thế Hệ Mới Ứng Dụng AI & SOAR", "start_at": now + timedelta(days=25, hours=13, minutes=30), "end_at": now + timedelta(days=25, hours=16, minutes=30), "description": "Tự động hóa phát hiện và cô lập máy tính nhiễm độc trong vòng dưới 60 giây."}
            ]
        },

        # 6. THỂ THAO & MARATHON ĐÊM
        {
            "event_code": "EVT-2026-NIGHTRUN-001",
            "title": "Thái Nguyên City Night Run 2026: Bước Chạy Kết Nối Di Sản Xứ Trà",
            "description": "Giải chạy đêm quy mô lớn tại Thành phố Thái Nguyên với cung đường lung linh ánh đèn qua các địa danh lịch sử, Quảng trường Võ Nguyên Giáp, Bảo tàng Văn hóa các Dân tộc và Đồi chè Tân Cương thơ mộng.",
            "category": "Thể thao & Giải trí",
            "location_type": "offline",
            "location_address": "Quảng trường Võ Nguyên Giáp, Phường Trưng Vương, TP. Thái Nguyên",
            "start_date": now + timedelta(days=28, hours=18, minutes=0),
            "end_date": now + timedelta(days=28, hours=23, minutes=30),
            "banner_url": "https://images.unsplash.com/photo-1530549387789-4c1017266635?w=800",
            "max_attendees": 2000,
            "tags": "Marathon, Night Run, Chạy bộ, Thể thao, Thái Nguyên, Rèn luyện sức khỏe, Xứ Trà",
            "tickets": [
                {"name": "Vé Cự Ly 5KM Fun Run (Sinh Viên & Gia Đình)", "ticket_type": "standard", "price": 180000, "quota": 1000},
                {"name": "Vé Cự Ly 10KM Thử Thách", "ticket_type": "standard", "price": 280000, "quota": 600},
                {"name": "Vé Cự Ly 21KM Half Marathon & Bộ Racekit VIP Mạ Vàng", "ticket_type": "vip", "price": 500000, "quota": 400}
            ],
            "speakers": [
                {"name": "VĐV Nguyễn Thị Oanh", "title": "Kỷ Lục Gia Điền Kinh Đông Nam Á", "bio": "Vận động viên nhiều lần giành HCV SEA Games, đại sứ tinh thần lối sống năng động lành mạnh.", "organization": "Đội Tuyển Điền Kinh Quốc Gia"},
                {"name": "HLV Bùi Tuấn Anh", "title": "Huấn Luyện Viên Marathon Trưởng", "bio": "Chuyên gia hướng dẫn kỹ thuật chạy bền tránh chấn thương và dinh dưỡng thể thao đỉnh cao.", "organization": "Vietnam Running Club"}
            ],
            "schedules": [
                {"title": "Khai Mạc Giải Chạy, Phát Racekit & Khởi Động Đồng Diễn Âm Nhạc Sôi Động", "start_at": now + timedelta(days=28, hours=18, minutes=30), "end_at": now + timedelta(days=28, hours=19, minutes=30), "description": "Nhận áo chạy, BIB gắn chip đo giờ điện tử và làm nóng cơ thể cùng HLV."},
                {"title": "Xuất Phát Cự Ly 21KM & 10KM Cùng Cơn Mưa Pháo Sáng Lung Linh", "start_at": now + timedelta(days=28, hours=20, minutes=0), "end_at": now + timedelta(days=28, hours=22, minutes=0), "description": "Khởi tranh cung đường chạy đêm rực rỡ sắc màu qua trung tâm thành phố."},
                {"title": "Lễ Bế Mạc & Trao Kỷ Niệm Chương Cho Toàn Bộ Vận Động Viên Hoàn Thành", "start_at": now + timedelta(days=28, hours=22, minutes=15), "end_at": now + timedelta(days=28, hours=23, minutes=30), "description": "Tôn vinh nỗ lực kiên cường và trao thưởng cho các VĐV về nhất các nhóm tuổi."}
            ]
        },

        # 7. NHIẾP ẢNH & ĐIỆN ẢNH DRONE
        {
            "event_code": "EVT-2026-CINEMATIC-DRONE-001",
            "title": "Vietnam Cinematic & Drone Photography Workshop 2026: Kể Chuyện Bằng Khung Hình",
            "description": "Khóa tập huấn và thực hành chuyên sâu về nghệ thuật quay phim điện ảnh, kỹ thuật bay Flycam FPV an toàn và quy trình chỉnh màu chuyên nghiệp (Color Grading) trên DaVinci Resolve với các Đạo diễn hình ảnh (DOP) nổi tiếng.",
            "category": "Nhiếp ảnh & Điện ảnh",
            "location_type": "offline",
            "location_address": "Trung tâm Nghệ thuật Đương đại VCCA, Tầng B1-R3 Royal City, 72A Nguyễn Trãi, Thanh Xuân, Hà Nội",
            "start_date": now + timedelta(days=32, hours=9, minutes=0),
            "end_date": now + timedelta(days=32, hours=17, minutes=30),
            "banner_url": "https://images.unsplash.com/photo-1508614589041-895b88991e3e?w=800",
            "max_attendees": 280,
            "tags": "Nhiếp ảnh, Drone, Flycam, Cinematic, DaVinci Resolve, Làm phim, DOP, Color Grading",
            "tickets": [
                {"name": "Vé Tham Dự Hội Thảo (Standard)", "ticket_type": "standard", "price": 220000, "quota": 200},
                {"name": "Vé VIP Thực Hành Studio Kèm Bộ LUTs Bản Quyền Điện Ảnh", "ticket_type": "vip", "price": 650000, "quota": 80}
            ],
            "speakers": [
                {"name": "Đạo diễn hình ảnh Trịnh Đình Lê Minh", "title": "Director of Photography (DOP)", "bio": "Đạo diễn của nhiều tác phẩm điện ảnh chiếu rạp đạt giải thưởng Bông Sen Vàng.", "organization": "Vietnam Cinema Guild"},
                {"name": "Phi công FPV Drone Đỗ Duy Hoàng", "title": "Lead Aerial Cinematographer", "bio": "Chuyên gia bay FPV ghi hình các MV ca nhạc và quảng cáo quốc tế tại Việt Nam.", "organization": "Skyview Films"}
            ],
            "schedules": [
                {"title": "Bố Cục Điện Ảnh & Kỹ Năng Đặt Ánh Sáng Tạo Chiều Sâu Cho Khung Hình", "start_at": now + timedelta(days=32, hours=9, minutes=30), "end_at": now + timedelta(days=32, hours=11, minutes=30), "description": "Tư duy kể chuyện bằng góc máy, tiêu cự ống kính và chuyển động máy quay mềm mại."},
                {"title": "Hướng Dẫn Làm Chủ Thiết Bị Bay Không Người Lái (Drone) & Kỹ Thuật Bay Cinematic", "start_at": now + timedelta(days=32, hours=13, minutes=0), "end_at": now + timedelta(days=32, hours=15, minutes=0), "description": "Kỹ thuật bay một shot mượt mà và các biện pháp bảo đảm an toàn bay."},
                {"title": "Thực Hành Color Grading: Tái Tạo Tone Màu Điện Ảnh Trong DaVinci Resolve Studio", "start_at": now + timedelta(days=32, hours=15, minutes=15), "end_at": now + timedelta(days=32, hours=17, minutes=15), "description": "Quản lý Color Space, Color Management ACES và cân bằng màu da tự nhiên."}
            ]
        },

        # 8. CÔNG NGHỆ XANH & ESG
        {
            "event_code": "EVT-2026-GREENTECH-001",
            "title": "Green Tech & ESG Sustainability Forum 2026: Công Nghệ Cho Tương Lai Xanh",
            "description": "Diễn đàn công nghệ xanh và phát triển bền vững ESG. Giới thiệu các giải pháp lưu trữ năng lượng mặt trời, pin thể rắn, cảm biến IoT giám sát chất lượng không khí và chuyển đổi số giảm phát thải ròng Net-Zero.",
            "category": "Môi trường & Công nghệ Xanh",
            "location_type": "hybrid",
            "location_address": "Khách sạn Pan Pacific Hanoi, Số 1 Thanh Niên, Ba Đình, Hà Nội & Trực Tuyến",
            "start_date": now + timedelta(days=36, hours=8, minutes=30),
            "end_date": now + timedelta(days=36, hours=17, minutes=0),
            "banner_url": "https://images.unsplash.com/photo-1497435334941-8c899ee9e8e9?w=800",
            "max_attendees": 350,
            "tags": "Green Tech, ESG, Net Zero, Năng lượng sạch, Môi trường, Bền vững, IoT",
            "tickets": [
                {"name": "Vé Hội Thảo Xanh (Standard)", "ticket_type": "standard", "price": 200000, "quota": 250},
                {"name": "Vé VIP Doanh Nghiệp ESG & Báo Cáo Phân Tích Chuyên Sâu", "ticket_type": "vip", "price": 800000, "quota": 100}
            ],
            "speakers": [
                {"name": "TS. Lê Thu Hương", "title": "Chuyên gia Kinh tế Môi trường", "bio": "Cố vấn chính sách chuyển dịch năng lượng và thị trường tín chỉ carbon.", "organization": "Viện Chiến lược Môi trường"},
                {"name": "Mr. Eric Lindqvist", "title": "Director of Clean Energy Solutions", "bio": "Hơn 15 năm phát triển dự án điện gió ngoài khơi và lưới điện thông minh tại Bắc Âu.", "organization": "Nordic Green Energy"}
            ],
            "schedules": [
                {"title": "Toàn Cảnh Thị Trường Tín Chỉ Carbon & Lộ Trình Net-Zero 2050", "start_at": now + timedelta(days=36, hours=8, minutes=45), "end_at": now + timedelta(days=36, hours=10, minutes=15), "description": "Cách doanh nghiệp công nghệ áp dụng báo cáo ESG theo chuẩn quốc tế."},
                {"title": "Công Nghệ Lưu Trữ Năng Lượng & Ứng Dụng IoT Trong Giám Sát Môi Trường", "start_at": now + timedelta(days=36, hours=10, minutes=30), "end_at": now + timedelta(days=36, hours=12, minutes=0), "description": "Giải pháp pin thế hệ mới và mạng lưới sensor quan trắc không khí."},
                {"title": "Tọa Đàm: Thúc Đẩy Startup Công Nghệ Xanh và Quỹ Đầu Tư Khí Hậu", "start_at": now + timedelta(days=36, hours=13, minutes=30), "end_at": now + timedelta(days=36, hours=16, minutes=0), "description": "Cơ hội nhận tài trợ từ các quỹ đầu tư mạo hiểm xanh quốc tế."}
            ]
        },

        # 9. UI/UX DESIGN & HUMAN-CENTERED AI
        {
            "event_code": "EVT-2026-UIUX-DESIGN-001",
            "title": "UI/UX Design & Human-Centered AI Conference 2026: Kiến Tạo Trải Nghiệm Đột Phá",
            "description": "Hội nghị thường niên dành cho Product Designers, UX Researchers và Design Leads. Khám phá cách kết hợp tư duy thiết kế lấy con người làm trung tâm (Human-Centered) với các công cụ Generative AI, xây dựng Design System quy mô lớn và tối ưu Micro-Interactions.",
            "category": "Thiết kế & Sáng tạo",
            "location_type": "offline",
            "location_address": "Không gian Sáng tạo Complex 01, Số 29 Ngách 31 Ngõ 167 Tây Sơn, Đống Đa, Hà Nội",
            "start_date": now + timedelta(days=40, hours=9, minutes=0),
            "end_date": now + timedelta(days=40, hours=17, minutes=30),
            "banner_url": "https://images.unsplash.com/photo-1581291518857-4e27b48ff24e?w=800",
            "max_attendees": 300,
            "tags": "UI/UX, Product Design, Design System, Figma, AI Co-design, UX Research, Trải nghiệm người dùng",
            "tickets": [
                {"name": "Vé Designer Pass (Standard)", "ticket_type": "standard", "price": 280000, "quota": 220},
                {"name": "Vé VIP Masterclass & Đánh Giá Portfolio 1:1 Cùng Giám Đốc Sáng Tạo", "ticket_type": "vip", "price": 750000, "quota": 80}
            ],
            "speakers": [
                {"name": "Nguyễn Hoàng Minh", "title": "Lead Product Designer", "bio": "Tác giả của Design System phục vụ hơn 15 triệu người dùng ứng dụng di động.", "organization": "Grab Vietnam"},
                {"name": "Bà Đặng Phương Thảo", "title": "Senior UX Researcher", "bio": "Chuyên gia nghiên cứu hành vi người dùng số và khả năng tiếp cận (Accessibility).", "organization": "Design Lab Hanoi"}
            ],
            "schedules": [
                {"title": "Keynote: Thiết Kế Giao Diện Trong Kỷ Nguyên AI Đàm Thoại & Trợ Lý Ảo", "start_at": now + timedelta(days=40, hours=9, minutes=15), "end_at": now + timedelta(days=40, hours=10, minutes=45), "description": "Tư duy thiết kế giao diện không chạm và đàm thoại tự nhiên."},
                {"title": "Hands-on Workshop: Xây Dựng Tokens & Auto Layout Nâng Cao Trên Figma", "start_at": now + timedelta(days=40, hours=11, minutes=0), "end_at": now + timedelta(days=40, hours=12, minutes=30), "description": "Thực hành đồng bộ Design Tokens từ Figma sang Code CSS."},
                {"title": "Portfolio Review Trực Tiếp 1:1 Cùng Các Design Director", "start_at": now + timedelta(days=40, hours=14, minutes=0), "end_at": now + timedelta(days=40, hours=16, minutes=30), "description": "Nhận xét và định hướng nghề nghiệp cho các nhà thiết kế trẻ."}
            ]
        },

        # 10. FINTECH & NGÂN HÀNG SỐ
        {
            "event_code": "EVT-2026-FINTECH-001",
            "title": "Vietnam Fintech & Open Banking Summit 2026: Tương Lai Tài Chính Số",
            "description": "Diễn đàn công nghệ tài chính thường niên lớn nhất Việt Nam. Thảo luận về ngân hàng mở (Open Banking), thanh toán không tiếp xúc qua QR/NFC, định danh điện tử eKYC và ứng dụng AI phát hiện gian lận giao dịch theo thời gian thực.",
            "category": "Kinh doanh & Khởi nghiệp",
            "location_type": "offline",
            "location_address": "Trung tâm Hội nghị GEM Center, Số 8 Nguyễn Bỉnh Khiêm, Đa Kao, Quận 1, TP. Hồ Chí Minh",
            "start_date": now + timedelta(days=45, hours=8, minutes=30),
            "end_date": now + timedelta(days=45, hours=17, minutes=30),
            "banner_url": "https://images.unsplash.com/photo-1559526324-4b87b5e36e44?w=800",
            "max_attendees": 500,
            "tags": "Fintech, Open Banking, eKYC, AI Fraud Detection, Thanh toán số, Ngân hàng mở",
            "tickets": [
                {"name": "Vé Tham Dự Hội Thảo (Standard)", "ticket_type": "standard", "price": 350000, "quota": 350},
                {"name": "Vé VIP Executive & Tiệc Tối Networking Lãnh Đạo Tài Chính", "ticket_type": "vip", "price": 1500000, "quota": 150}
            ],
            "speakers": [
                {"name": "Ông Trần Quốc Bảo", "title": "Phó Tổng Giám Đốc Công Nghệ", "bio": "Hơn 20 năm dẫn dắt chuyển đổi số ngân hàng lõi (Core Banking).", "organization": "VietBank Digital"},
                {"name": "Bà Jennifer Wong", "title": "Head of Fintech Innovation APAC", "bio": "Chuyên gia tư vấn khung pháp lý Sandbox và Open Finance.", "organization": "Fintech Asia Partners"}
            ],
            "schedules": [
                {"title": "Keynote: Xu Hướng Open Banking và Kiến Trúc Ngân Hàng Tương Lai", "start_at": now + timedelta(days=45, hours=8, minutes=45), "end_at": now + timedelta(days=45, hours=10, minutes=15), "description": "Chia sẻ kinh nghiệm kết nối API ngân hàng mở an toàn."},
                {"title": "Tọa Đàm: Phòng Chống Lừa Đảo Trực Tuyến Bằng Machine Learning", "start_at": now + timedelta(days=45, hours=10, minutes=30), "end_at": now + timedelta(days=45, hours=12, minutes=0), "description": "Giải pháp AI phát hiện tài khoản rác và giao dịch bất thường."},
                {"title": "Triển Lãm Demo: Giải Pháp Thanh Toán Một Chạm & Sinh Trắc Học", "start_at": now + timedelta(days=45, hours=13, minutes=30), "end_at": now + timedelta(days=45, hours=16, minutes=30), "description": "Trải nghiệm các máy POS sinh trắc khuôn mặt và lòng bàn tay."}
            ]
        }
    ]

    added = 0
    updated = 0
    for data in diverse_events:
        evt = Event.query.filter_by(event_code=data["event_code"]).first()
        if not evt:
            evt = Event.query.filter_by(title=data["title"]).first()

        if not evt:
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
            added += 1
        else:
            evt.title = data["title"]
            evt.description = data["description"]
            evt.category = data["category"]
            evt.location_type = data["location_type"]
            evt.location_address = data["location_address"]
            evt.start_date = data["start_date"]
            evt.end_date = data["end_date"]
            evt.banner_url = data["banner_url"]
            evt.max_attendees = data["max_attendees"]
            evt.tags = data.get("tags", "")
            evt.status = "published"
            db.session.flush()
            updated += 1

        # Add or refresh tickets
        for idx, t_info in enumerate(data["tickets"], 1):
            t_code = f"TCK-{evt.id:03d}-{idx:02d}-{t_info['ticket_type'].upper()}"
            existing_t = Ticket.query.filter_by(ticket_code=t_code).first()
            if not existing_t:
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

        # Add or find speakers
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

        # Add schedules if none exist
        if evt.schedules.count() == 0:
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

    db.session.commit()
    total = Event.query.count()
    print(f"✅ Hoàn tất! Đã thêm {added} sự kiện mới, cập nhật {updated} sự kiện. Tổng số sự kiện trên hệ thống: {total}")
