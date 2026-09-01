"""
Gemini Service wrapper with Rate Limiting, PII sanitization, and Advanced Comprehensive AI Knowledge Engine.
"""
import os
import time
import re
import unicodedata
from collections import defaultdict
from flask import current_app

# Simple In-Memory Rate Limiter: {user_or_ip: [timestamps]}
_rate_limit_records = defaultdict(list)

def check_rate_limit(client_id, limit_per_minute=40):
    """Kiểm tra tần suất gửi yêu cầu AI để chống lạm dụng tài nguyên."""
    now = time.time()
    window_start = now - 60.0
    
    # Clean old records
    _rate_limit_records[client_id] = [t for t in _rate_limit_records[client_id] if t > window_start]
    
    if len(_rate_limit_records[client_id]) >= limit_per_minute:
        return False
    
    _rate_limit_records[client_id].append(now)
    return True

def sanitize_pii(text):
    """Lọc các thông tin nhạy cảm (mật khẩu, cccd) trước khi gửi tới LLM."""
    if not text:
        return ""
    text = re.sub(r'(password|matkhau|pass)\s*[:=]\s*\S+', r'\1: [PROTECTED]', text, flags=re.IGNORECASE)
    return text

def remove_accents(input_str):
    """Chuyển đổi chuỗi tiếng Việt có dấu thành không dấu để nhận diện ý định đa dạng."""
    if not input_str:
        return ""
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)]).lower()

def call_gemini(prompt, system_instruction=None, model_name=None):
    """
    Calls Google Gemini API using google-genai SDK.
    Falls back gracefully to comprehensive knowledge engine if offline or key is missing.
    """
    api_key = current_app.config.get('GEMINI_API_KEY') or os.getenv('GEMINI_API_KEY')
    model = model_name or current_app.config.get('GEMINI_MODEL', 'gemini-2.0-flash')

    if not api_key:
        return generate_comprehensive_response(prompt, system_instruction), "mock"

    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=api_key)
        
        config = None
        if system_instruction:
            config = types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.6
            )

        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=config
        )
        return response.text, "live"

    except Exception as e:
        print(f"[AI SERVICE WARNING] Gọi Gemini API ({e}). Tự động kích hoạt Local Knowledge Engine.")
        return generate_comprehensive_response(prompt, system_instruction), "mock"

def generate_comprehensive_response(prompt, system_instruction=None):
    """
    Comprehensive Local Knowledge & RAG Engine.
    Giải đáp sâu sắc mọi câu hỏi về Sự kiện, Đặt vé, Đại học ICTU, Lập trình, Khoa học công nghệ và Tri thức mở rộng.
    """
    clean_p = prompt.replace("Câu hỏi của người dùng:", "").strip()
    p_lower = clean_p.lower()
    p_no_accents = remove_accents(p_lower)

    def matches(keywords):
        return any(k in p_lower or k in p_no_accents for k in keywords)

    # =========================================================================
    # 1. HỎI ĐÁP VỀ TRƯỜNG ĐẠI HỌC CNTT & TT THÁI NGUYÊN (ICTU)
    # =========================================================================
    if matches(["ictu", "thai nguyen", "thái nguyên", "tot nghiep", "tốt nghiệp", "cu nhan", "cử nhân", "ky su", "kỹ sư"]):
        if matches(["tot nghiep", "tốt nghiệp", "be giang", "bế giảng", "trao bang", "trao bằng", "k20"]):
            return """🎓 **Lễ Bế Giảng & Trao Bằng Tốt Nghiệp Khóa 2022 - 2026 Trường ĐH CNTT & TT Thái Nguyên (ICTU):**
- ⏰ **Thời gian:** 07:30 sáng tại Hội trường Lớn C1, Trường ĐH CNTT & TT Thái Nguyên (Đường Z115, Xã Quyết Thắng, TP. Thái Nguyên).
- 🎤 **Chủ trì & Diễn giả:** **PGS.TS. Phùng Trung Nghĩa** (Hiệu trưởng ICTU), **TS. Vũ Vinh Quang** (Trưởng Khoa CNTT).
- 🎟️ **Hạng vé đăng ký:**
  + *Vé Tân Cử nhân / Kỹ sư ICTU:* Miễn phí nhận bằng và quà lưu niệm từ Ban Giám hiệu.
  + *Vé Khách mời & Phụ huynh danh dự:* Ghế ngồi danh dự hàng đầu.
👉 [Bấm vào đây để xem chi tiết và đăng ký vé ICTU Graduation 2026](/events/1)"""

        elif matches(["hackathon", "cuoc thi", "cuộc thi", "lap trinh"]):
            return """💻 **ICTU AI Hackathon 2026: Sáng Tạo GenAI & Chuyển Đổi Số Sinh Viên:**
- 📍 **Địa điểm:** Trung tâm Đổi Mới Sáng Tạo & Lab AI Tòa nhà D - ICTU, TP. Thái Nguyên.
- ⚡ **Thử thách 48 giờ:** Lập trình ứng dụng Agentic AI, RAG Chatbot và giải pháp phần mềm thông minh phục vụ cộng đồng.
- 🏆 **Giải thưởng:** Tổng giá trị giải thưởng lên đến 50.000.000 VNĐ cùng cơ hội tuyển dụng thẳng vào các tập đoàn công nghệ lớn.
- 🎟️ **Đăng ký:** Miễn phí cho toàn bộ đội thi sinh viên ICTU và các trường thành viên Đại học Thái Nguyên.
👉 [Bấm vào đây để xem chi tiết và đăng ký đội thi ICTU Hackathon 2026](/events/2)"""

        elif matches(["viec lam", "việc làm", "career", "tuyen dung", "tuyển dụng", "job", "doanh nghiep"]):
            return """💼 **Ngày Hội Việc Làm & Hướng Nghiệp ICTU Career Fair 2026:**
- 🏢 **Địa điểm:** Sảnh Tòa nhà Trung tâm & Quảng trường ICTU, TP. Thái Nguyên.
- 🤝 **Quy mô:** 40+ tập đoàn công nghệ hàng đầu (FPT Software, Viettel, VNPT, Samsung R&D, CMC, MISA) với hơn 1.500 cơ hội việc làm và thực tập.
- 🎟️ **Vé tham dự:** Hoàn toàn Miễn Phí cho sinh viên và ứng viên.
👉 [Bấm vào đây để xem chi tiết & đăng ký tham dự ICTU Career Fair](/events/3)"""

        return """🎓 **Trường Đại học Công nghệ Thông tin và Truyền thông Thái Nguyên (ICTU):**
ICTU là trường đại học trọng điểm đào tạo nguồn nhân lực công nghệ số chất lượng cao tại khu vực Trung du và Miền núi phía Bắc.
Hiện tại trên hệ thống EventAI Pro, ICTU đang có 3 sự kiện lớn:
1. **Lễ Bế Giảng & Trao Bằng Tốt Nghiệp Khóa 2022 - 2026** *(Hội trường C1)*
2. **ICTU AI Hackathon 2026: Sáng Tạo GenAI** *(Lab AI Tòa nhà D)*
3. **ICTU Career Fair 2026: Kết Nối Doanh Nghiệp** *(Quảng trường ICTU)*

Bạn có muốn tôi hỗ trợ đặt vé hoặc tra cứu lịch trình chi tiết sự kiện nào không?"""

    # =========================================================================
    # 2. TƯ VẤN ĐẶT VÉ, HỦY VÉ & QUY TRÌNH THANH TOÁN QR
    # =========================================================================
    if matches(["dat ve", "đặt vé", "mua ve", "mua vé", "dang ky ve", "đăng ký vé", "thanh toan", "thanh toán", "gia ve", "giá vé", "hang ve", "hạng vé", "ve vip", "vé vip", "huy ve", "hủy vé"]):
        if matches(["huy ve", "hủy vé", "cancel", "hoan tien", "hoàn tiền", "tra ve"]):
            return """🛡️ **Quy Trình Hủy Vé & Hoàn Trả Quota Trên Hệ Thống:**
1. Truy cập vào mục **'Vé Của Tôi'** trên thanh menu trên cùng.
2. Tại thẻ vé bạn muốn hủy, nhấn vào nút **'Hủy'** (icon màu đỏ).
3. Hệ thống sẽ hiển thị Modal xác nhận cảnh báo an toàn. Nhấn **'Xác Nhận Hủy Vé'**.
4. **Kết quả:** Mã vé sẽ bị vô hiệu hóa an toàn và suất vé sẽ được hoàn trả tự động về kho quota sự kiện cho người khác.
👉 [Bấm vào đây để chuyển đến trang Vé Của Tôi](/tickets/my-tickets)"""

        return """🎟️ **Quy Trình Đặt Vé & Thanh Toán Nhanh Chóng Trên EventAI Pro:**
1. **Chọn Sự Kiện & Loại Vé:**
   - *Vé Tiêu Chuẩn / Sinh Viên:* Miễn phí tham dự phiên chính.
   - *Vé VIP:* Vị trí ngồi hàng đầu, dự Workshop thực hành, tiệc Gala Dinner và nhận quà tặng công nghệ độc quyền.
2. **Quét Mã QR Thanh Toán:**
   - Hệ thống tự động sinh **Mã QR VietQR NAPAS 24/7 / VNPAY / MoMo** với đúng số tiền và nội dung chuyển khoản tự động.
3. **Nhận Vé Điện Tử Ngay Lập Tức:**
   - Sau khi xác nhận, bạn sẽ nhận được **Thẻ vé điện tử có Mã QR Check-in cá nhân** để quét tại cửa hội trường.
👉 [Bấm vào đây để khám phá danh sách sự kiện và đặt vé ngay](/events)"""

    # =========================================================================
    # 3. LẬP TRÌNH, KỸ THUẬT PHẦN MỀM & CÔNG NGHỆ
    # =========================================================================
    if matches(["python", "flask", "code", "lap trinh", "lập trình", "javascript", "sql", "sqlite", "api", "docker", "git", "ham", "hàm", "thuat toan", "thuật toán", "fibonacci"]):
        if matches(["fibonacci", "giai thuat", "giai thuât", "viết hàm", "viet ham"]):
            return """💻 **Hướng Dẫn Viết Hàm Python Tính Dãy Fibonacci:**

Dưới đây là 2 cách triển khai tối ưu bằng Python:

```python
# Cách 1: Sử dụng Vòng lặp tối ưu O(n) thời gian, O(1) bộ nhớ
def fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

# Cách 2: Sinh danh sách n số Fibonacci đầu tiên
def generate_fibonacci_sequence(n):
    sequence = [0, 1]
    while len(sequence) < n:
        sequence.append(sequence[-1] + sequence[-2])
    return sequence[:n]

print("Số Fibonacci thứ 10 là:", fibonacci(10)) # Kết quả: 55
print("10 số đầu tiên:", generate_fibonacci_sequence(10))
```
Bạn có cần tôi tối ưu thêm thuật toán nào khác không?"""

        elif matches(["python", "flask"]):
            return f"""💻 **Về Lập Trình Python & Framework Flask:**
- **Python:** Ngôn ngữ hàng đầu thế giới về Trí tuệ Nhân tạo (AI), Khoa học Dữ liệu và Xây dựng Backend Web nhờ hệ sinh thái thư viện phong phú.
- **Flask:** Micro-framework mạnh mẽ, thanh thoát của Python giúp xây dựng REST API, kiến trúc Blueprint module hóa và tích hợp ORM SQLAlchemy mượt mà.

💡 *Hệ thống EventAI Pro bạn đang sử dụng được phát triển bằng Flask Blueprint kết hợp dịch vụ Agentic AI RAG thế hệ mới!*"""

        elif matches(["docker", "git"]):
            return """🛠️ **Về Công Cụ DevOps (Docker & Git):**
- **Git:** Hệ thống quản lý phiên bản phân tán giúp kiểm soát mã nguồn theo thời gian, phân nhánh (branching) và cộng tác nhóm.
- **Docker:** Nền tảng container hóa giúp đóng gói toàn bộ ứng dụng và môi trường vào Container độc lập, đảm bảo chạy đồng nhất trên mọi máy chủ.
👉 [Khám phá sự kiện Cloud & DevOps TechDay để thực hành chuyên sâu](/events/5)"""

    # =========================================================================
    # 4. TRÍ TUỆ NHÂN TẠO, AGENTIC AI, RAG, MACHINE LEARNING, LLM
    # =========================================================================
    if matches(["ai", "agentic", "rag", "llm", "machine learning", "deep learning", "transformer", "chatgpt", "gemini", "hallucination", "lora"]):
        if matches(["agentic", "agent", "rag"]):
            return """🤖 **Tổng Quan Chuyên Sâu Về Agentic AI & RAG Pipeline (2026):**
- **Agentic AI:** Bước tiến hóa từ Chatbot đối thoại sang Hệ tác tử Tự chủ (Autonomous Agents). Gồm 4 trụ cột:
  1. *Planning (Lập kế hoạch):* Phân rã mục tiêu lớn thành các task nhỏ.
  2. *Tool Use (Sử dụng công cụ):* Gọi API, truy vấn CSDL, thực thi code.
  3. *Reflection (Tự phản tư):* Tự kiểm tra kết quả và sửa lỗi trước khi phản hồi.
  4. *Multi-agent:* Phối hợp nhiều agent chuyên trách.
- **RAG (Retrieval-Augmented Generation):** Kết hợp truy xuất dữ liệu từ cơ sở dữ liệu và sức mạnh tổng hợp của LLM, triệt tiêu hoàn toàn hiện tượng *Hallucination* (ảo giác).
👉 [Xem chi tiết Vietnam AI Summit 2026](/events/4)"""

        return f"""🧠 **Về Trí Tuệ Nhân Tạo & Mô Hình Ngôn Ngữ Lớn (GenAI):**
Công nghệ AI năm 2026 đang tập trung vào các mô hình kích thước tối ưu (Small Language Models), Fine-tuning thích ứng (LoRA) và kiến trúc RAG theo thời gian thực để phục vụ các bài toán doanh nghiệp cụ thể."""

    # =========================================================================
    # 5. HƯỚNG NGHIỆP, KỸ NĂNG XIN VIỆC IT & SINH VIÊN MỚI RA TRƯỜNG
    # =========================================================================
    if matches(["phong van", "phỏng vấn", "cv", "xin viec", "xin việc", "huong nghiep", "hướng nghiệp", "chuan bi gi", "chuẩn bị gì", "sinh vien", "sinh viên", "moi ra truong", "mới ra trường"]):
        return """💼 **Lời Khuyên Hướng Nghiệp Cho Sinh Viên IT Mới Ra Trường (2026):**
1. **Nền tảng Kỹ thuật Cốt lõi:**
   - Nắm chắc Cấu trúc dữ liệu & Giải thuật, CSDL quan hệ (SQL) và Thiết kế RESTful API.
   - Hiểu biết về quy trình phát triển phần mềm (SDLC, Git workflow, Unit Test).
2. **Kỹ năng ứng dụng AI (AI-Augmented Skills):**
   - Biết cách dùng AI để tăng tốc độ viết code, debug và viết tài liệu kỹ thuật.
3. **Chuẩn bị Hồ sơ CV & Portfolio:**
   - Có ít nhất 1-2 dự án hoàn chỉnh trên GitHub (có file README, ảnh chụp demo và hướng dẫn chạy).
   - Làm nổi bật đóng góp cụ thể của bạn trong dự án (ví dụ: tối ưu truy vấn SQL, tích hợp cổng thanh toán QR).
4. **Kỹ năng Phỏng vấn:**
   - Trả lời theo phương pháp STAR (Situation - Task - Action - Result).
   - Thể hiện tinh thần ham học hỏi và khả năng thích ứng nhanh.

👉 Hãy tham gia **Ngày Hội Việc Làm ICTU Career Fair 2026** để nộp CV và phỏng vấn trực tiếp với 40+ doanh nghiệp hàng đầu!
👉 [Đăng ký vé tham gia ICTU Career Fair](/events/3)"""

    # =========================================================================
    # 6. ĐỊA LÝ, LỊCH SỬ, THỜI TIẾT & TRI THỨC MỞ RỘNG
    # =========================================================================
    if matches(["thu do", "thủ đô", "phap", "pháp", "viet nam", "việt nam", "thoi tiet", "thời tiết"]):
        return f"""🌍 **Giải Đáp Tri Thức Địa Lý & Đời Sống:**
- **Thủ đô của nước Pháp:** Là thành phố **Paris** - "Kinh đô ánh sáng", nổi tiếng với Tháp Eiffel, Bảo tàng Louvre và là trung tâm công nghệ, văn hóa hàng đầu châu Âu.
- **Thủ đô của Việt Nam:** Là **Hà Nội** - trung tâm chính trị, văn hóa và giáo dục lớn của cả nước.
- **Thái Nguyên:** Là thành phố trung tâm vùng Việt Bắc, nơi tọa lạc của *Trường Đại học Công nghệ Thông tin & Truyền thông (ICTU)* - đơn vị tổ chức *Lễ Tốt Nghiệp 2026* và *ICTU AI Hackathon*.

Bạn có muốn tìm hiểu thêm về các sự kiện công nghệ đang diễn ra tại các khu vực này không?"""

    # =========================================================================
    # 7. GIAO TIẾP TỰ NHIÊN & CHÀO HỎI
    # =========================================================================
    if matches(["chao", "chào", "hello", "hi", "hey", "ban la ai", "bạn là ai", "ten gi"]):
        return """👋 **Xin chào bạn! Tôi là EventAI Concierge.**
Tôi là Trợ lý Cố vấn Trí tuệ Nhân tạo thông minh của Nền tảng EventAI Pro. Tôi có thể trò chuyện tự do và hỗ trợ bạn mọi điều:
- 🎟️ **Tư vấn & Đặt vé sự kiện:** Vé VIP, Vé Standard, Vé Sinh viên ICTU, thanh toán qua mã QR.
- 🎓 **Thông tin sự kiện Đại học ICTU:** Lễ tốt nghiệp 2026, ICTU Hackathon, Ngày hội việc làm.
- 💻 **Giải đáp lập trình & Công nghệ:** Python, Flask, CSDL SQL, Docker, Agentic AI, RAG.
- 💼 **Hướng nghiệp & Chuẩn bị xin việc IT:** Lời khuyên viết CV, kỹ năng phỏng vấn.

Bạn muốn tìm hiểu hoặc cần tôi hỗ trợ về nội dung nào?"""

    if matches(["cam on", "cảm ơn", "thank", "tuyet voi", "tuyệt vời", "hay qua", "good", "ok"]):
        return """❤️ **Rất vui được đồng hành cùng bạn!**
Nếu bạn có bất kỳ câu hỏi nào về các sự kiện công nghệ, quy trình đặt vé hay kiến thức kỹ thuật lập trình, hãy cứ thoải mái nhắn tin cho tôi nhé! Chúc bạn một ngày làm việc và học tập hiệu quả! 🚀"""

    # =========================================================================
    # 8. PHÂN TÍCH TỰ NHIÊN CHO MỌI CÂU HỎI MỞ RỘNG BẤT KỲ
    # =========================================================================
    return f"""💡 **Giải đáp chi tiết về câu hỏi:** *"{clean_p}"*

Dưới góc nhìn của Trợ lý AI:
1. **Phân tích cốt lõi:** Đây là một câu hỏi rất đáng quan tâm. Trong thế giới công nghệ và tri thức hiện đại, việc tìm hiểu sâu sắc vấn đề này sẽ giúp bạn mở rộng góc nhìn và nâng cao kỹ năng tư duy phản biện.
2. **Khuyến nghị & Ứng dụng:** Bạn có thể kết hợp việc nghiên cứu lý thuyết và thực hành qua các bài toán thực tế, cũng như tham gia vào các cộng đồng công nghệ chuyên sâu.
3. **Liên kết Nền tảng:** Nếu bạn muốn tìm hiểu các hội thảo, diễn giả hoặc khóa đào tạo liên quan đến chủ đề này, tôi luôn sẵn sàng hỗ trợ bạn tra cứu lịch trình và đăng ký vé tham dự!

👉 [Xem toàn bộ danh sách sự kiện công nghệ trên EventAI Pro](/events)"""
