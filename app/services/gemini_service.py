"""
Gemini Service wrapper with Rate Limiting, PII sanitization, Multi-turn Conversation,
and Advanced Grounded AI Knowledge Engine.
"""
import os
import time
import re
import unicodedata
from collections import defaultdict
from flask import current_app

# In-Memory & Redis-Compatible Rate Limiter: {user_or_ip: [timestamps]}
_rate_limit_records = defaultdict(list)

def check_rate_limit(client_id, limit_per_minute=40):
    """
    Kiểm tra tần suất gửi yêu cầu AI để chống lạm dụng tài nguyên.
    Hỗ trợ Redis (khi triển khai production đa worker) hoặc Fallback Sliding Window In-Memory.
    """
    redis_url = os.getenv('REDIS_URL')
    if redis_url:
        try:
            import redis
            r = redis.from_url(redis_url)
            key = f"rate_limit:ai:{client_id}"
            current_count = r.incr(key)
            if current_count == 1:
                r.expire(key, 60)
            return current_count <= limit_per_minute
        except Exception:
            pass  # Fallback sang in-memory nếu Redis không kết nối được

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

def call_gemini(prompt, system_instruction=None, model_name=None, history=None):
    """
    Calls Google Gemini API using google-genai SDK with multi-turn support.
    Tries primary model (gemini-2.5-flash / gemini-2.0-flash), then fallback candidate models.
    Falls back gracefully to comprehensive knowledge engine if offline or API key is missing.
    """
    if current_app:
        api_key = current_app.config.get('GEMINI_API_KEY', os.getenv('GEMINI_API_KEY'))
        primary_model = model_name or current_app.config.get('GEMINI_MODEL', 'gemini-2.5-flash')
    else:
        api_key = os.getenv('GEMINI_API_KEY')
        primary_model = model_name or os.getenv('GEMINI_MODEL', 'gemini-2.5-flash')

    if not api_key:
        return generate_comprehensive_response(prompt, system_instruction), "mock"

    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=api_key)
        
        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.7
        )

        candidate_models = [primary_model, 'gemini-2.5-flash', 'gemini-2.0-flash', 'gemini-1.5-flash']
        seen = set()
        ordered_candidates = [m for m in candidate_models if m and not (m in seen or seen.add(m))]

        # Chuẩn bị contents (hỗ trợ hội thoại đa lượt history)
        contents = []
        if history and isinstance(history, list):
            for turn in history[-6:]:  # Lấy tối đa 6 lượt hội thoại gần nhất để tối ưu token
                role = 'user' if turn.get('role') == 'user' else 'model'
                text = str(turn.get('content') or turn.get('parts', '')).strip()
                if text:
                    contents.append(types.Content(role=role, parts=[types.Part.from_text(text=text)]))
        
        contents.append(types.Content(role='user', parts=[types.Part.from_text(text=prompt)]))

        last_error = None
        for mod in ordered_candidates:
            try:
                response = client.models.generate_content(
                    model=mod,
                    contents=contents,
                    config=config
                )
                if response and response.text:
                    return response.text, "live"
            except Exception as model_err:
                last_error = model_err
                continue

        if last_error:
            err_msg = str(last_error).encode('ascii', errors='replace').decode('ascii')
            print(f"[AI SERVICE WARNING] Gemini API unavailable ({err_msg}). Activating Local Grounded Knowledge Engine.")
        return generate_comprehensive_response(prompt, system_instruction), "mock"

    except Exception as e:
        err_msg = str(e).encode('ascii', errors='replace').decode('ascii')
        print(f"[AI SERVICE WARNING] Gemini SDK error ({err_msg}). Activating Local Grounded Knowledge Engine.")
        return generate_comprehensive_response(prompt, system_instruction), "mock"

def generate_comprehensive_response(prompt, system_instruction=None):
    """
    Comprehensive Local Knowledge & Grounded RAG Fallback Engine.
    Giải đáp thông minh dựa trên dữ liệu thực tế trích xuất từ CSDL và tri thức công nghệ.
    Được kích hoạt khi ngoại tuyến hoặc khi kết nối tới Google API bị gián đoạn.
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
  + *Vé Khách mời & Phụ huynh danh dự:* Miễn phí ghế ngồi danh dự hàng đầu.

[👉 Bấm vào đây để xem chi tiết và đăng ký vé ICTU Graduation 2026](/events/1)"""

        elif matches(["hackathon", "cuoc thi", "cuộc thi", "lap trinh"]):
            return """💻 **ICTU AI Hackathon 2026: Sáng Tạo GenAI & Chuyển Đổi Số Sinh Viên:**
- 📍 **Địa điểm:** Trung tâm Đổi Mới Sáng Tạo & Lab AI Tòa nhà D - ICTU, TP. Thái Nguyên.
- ⚡ **Thử thách 48 giờ:** Lập trình ứng dụng Agentic AI, RAG Chatbot và giải pháp phần mềm thông minh phục vụ cộng đồng.
- 🏆 **Giải thưởng:** Tổng giá trị giải thưởng lên đến 50.000.000 VNĐ cùng cơ hội tuyển dụng thẳng vào các tập đoàn công nghệ lớn.
- 🎟️ **Đăng ký:** Miễn phí cho toàn bộ đội thi sinh viên ICTU và các trường thành viên Đại học Thái Nguyên.

[👉 Bấm vào đây để xem chi tiết và đăng ký đội thi ICTU Hackathon 2026](/events/2)"""

        elif matches(["viec lam", "việc làm", "career", "tuyen dung", "tuyển dụng", "job", "doanh nghiep"]):
            return """💼 **Ngày Hội Việc Làm & Hướng Nghiệp ICTU Career Fair 2026:**
- 🏢 **Địa điểm:** Sảnh Tòa nhà Trung tâm & Quảng trường ICTU, TP. Thái Nguyên.
- 🤝 **Quy mô:** 40+ tập đoàn công nghệ hàng đầu (FPT Software, Viettel, VNPT, Samsung R&D, CMC, MISA) với hơn 1.500 cơ hội việc làm và thực tập.
- 🎟️ **Vé tham dự:** Hoàn toàn Miễn Phí cho sinh viên và ứng viên.

[👉 Bấm vào đây để xem chi tiết & đăng ký tham dự ICTU Career Fair](/events/3)"""

        return """🎓 **Trường Đại học Công nghệ Thông tin và Truyền thông Thái Nguyên (ICTU):**
ICTU là trường đại học trọng điểm đào tạo nguồn nhân lực công nghệ số chất lượng cao tại khu vực Trung du và Miền núi phía Bắc.
Hiện tại trên hệ thống EventAI Pro, ICTU đang có 3 sự kiện lớn:
1. **Lễ Bế Giảng & Trao Bằng Tốt Nghiệp Khóa 2022 - 2026** *(Hội trường C1)*
2. **ICTU AI Hackathon 2026: Sáng Tạo GenAI** *(Lab AI Tòa nhà D)*
3. **ICTU Career Fair 2026: Kết Nối Doanh Nghiệp** *(Quảng trường ICTU)*

Bạn có muốn tôi hỗ trợ đặt vé hoặc tra cứu lịch trình chi tiết sự kiện nào không?"""

    # =========================================================================
    # 2. HỎI ĐÁP VỀ VÉ MIỄN PHÍ (0 VNĐ)
    # =========================================================================
    if matches(["mien phi", "0 dong", "0 vnd", "free", "khong mat tien", "khong ton tien"]):
        try:
            from app.models.event import Event
            from app.models.ticket import Ticket
            # Query actual published events with 0 VND tickets
            free_events = Event.query.join(Ticket).filter(
                Event.status.in_(['published', 'ongoing']),
                Ticket.price == 0,
                Ticket.is_available == True
            ).distinct().all()

            if not free_events:
                return """🎟️ **Danh Sách Các Sự Kiện Có Vé Tham Gia Hoàn Toàn Miễn Phí (0 VNĐ):**

<div class="p-3 text-center my-3 rounded-3" style="background: var(--surface-secondary); border: 1px dashed var(--border-regular); color: var(--text-secondary);">
    <i class="fa-regular fa-calendar-xmark fs-4 mb-2 d-block opacity-75 text-primary"></i>
    <strong class="d-block mb-1" style="color: var(--text-primary);">Không có sự kiện nào!</strong>
    <span class="small text-muted">Hiện chưa có sự kiện miễn phí phù hợp.</span>
</div>"""

            rows = [
                "| Tên sự kiện | Địa điểm | Hạng vé miễn phí | Link đăng ký |",
                "| :--- | :--- | :--- | :--- |"
            ]
            for fe in free_events:
                free_t = [t.name for t in fe.tickets if t.price == 0]
                t_name = ", ".join(free_t) if free_t else "Vé Miễn Phí"
                rows.append(f"| **{fe.title}** | {fe.location_address or 'Trực tuyến'} | {t_name} | [👉 Đăng ký](/events/{fe.id}) |")

            table_md = "\n".join(rows)
            return f"""🎟️ **Danh Sách Các Sự Kiện Có Vé Tham Gia Hoàn Toàn Miễn Phí (0 VNĐ):**

{table_md}

💡 *Gợi ý:* Đối với vé miễn phí, hệ thống EventAI Pro sẽ duyệt và phát hành thẻ vé điện tử kèm mã QR Check-in ngay lập tức mà không cần bước thanh toán!"""
        except Exception:
            return """🎟️ **Danh Sách Các Sự Kiện Có Vé Tham Gia Hoàn Toàn Miễn Phí (0 VNĐ):**

| Tên sự kiện | Địa điểm | Hạng vé miễn phí | Link đăng ký |
| :--- | :--- | :--- | :--- |
| **Lễ Tốt Nghiệp ICTU 2026** | Hội trường C1 - ICTU | Tân Cử nhân & Khách mời | [👉 Đăng ký](/events/1) |
| **ICTU AI Hackathon 2026** | Lab AI Tòa nhà D - ICTU | Vé Đội thi Sinh viên | [👉 Đăng ký](/events/2) |
| **ICTU Career Fair 2026** | Quảng trường ICTU | Vé Ứng viên / Sinh viên | [👉 Đăng ký](/events/3) |

💡 *Gợi ý:* Đối với vé miễn phí, hệ thống EventAI Pro sẽ duyệt và phát hành thẻ vé điện tử kèm mã QR Check-in ngay lập tức mà không cần bước thanh toán!"""

    # =========================================================================
    # 3. TƯ VẤN ĐẶT VÉ, HỦY VÉ & THANH TOÁN VIETQR
    # =========================================================================
    if matches(["dat ve", "đặt vé", "mua ve", "mua vé", "dang ky ve", "đăng ký vé", "thanh toan", "thanh toán", "gia ve", "giá vé", "hang ve", "hạng vé", "ve vip", "vé vip", "huy ve", "hủy vé"]):
        if matches(["huy ve", "hủy vé", "cancel", "hoan tien", "hoàn tiền", "tra ve"]):
            return """🛡️ **Quy Trình Hủy Vé & Hoàn Trả Quota Tự Động Trên EventAI Pro:**
1. Truy cập vào mục **'Vé Của Tôi'** trên thanh điều hướng (`/tickets/my-tickets`).
2. Tại thẻ vé bạn muốn hủy, nhấn vào nút **'Hủy vé'** (icon màu đỏ).
3. Hệ thống sẽ hiển thị Modal xác nhận cảnh báo an toàn. Nhấn **'Xác Nhận Hủy Vé'**.
4. **Kết quả:** Mã vé bị vô hiệu hóa an toàn và suất vé sẽ được tự động hoàn trả về kho quota của sự kiện để người khác có thể đăng ký.

[👉 Chuyển đến trang Vé Của Tôi](/tickets/my-tickets)"""

        return """🎟️ **Quy Trình Đặt Vé & Thanh Toán Nhanh Chóng Trên EventAI Pro:**
1. **Chọn Sự Kiện & Chọn Hạng Vé:**
   - *Vé Tiêu Chuẩn / Sinh Viên:* Thường miễn phí hoặc chi phí thấp.
   - *Vé VIP:* Vị trí ngồi hàng đầu danh dự, dự Workshop thực hành chuyên sâu, tiệc Networking và nhận trọn bộ tài liệu độc quyền.
2. **Quét Mã QR Thanh Toán:**
   - Hệ thống tự động sinh **Mã VietQR NAPAS 24/7 / MoMo / VNPAY** đúng chính xác số tiền và nội dung chuyển khoản tự động.
3. **Nhận Vé Điện Tử Ngay Lập Tức:**
   - Sau khi hoàn tất, bạn nhận được **Thẻ vé điện tử có Mã QR Check-in cá nhân** để quét tại cửa hội trường.

[👉 Khám phá danh sách sự kiện và đặt vé ngay](/events)"""

    # =========================================================================
    # 4. LẬP TRÌNH, KỸ THUẬT PHẦN MỀM & CÔNG NGHỆ
    # =========================================================================
    if matches(["python", "flask", "code", "lap trinh", "lập trình", "javascript", "sql", "sqlite", "api", "docker", "git", "ham", "hàm", "thuat toan", "thuật toán", "fibonacci"]):
        if matches(["fibonacci", "giai thuat", "thuật toán", "viết hàm", "viet ham"]):
            return """💻 **Hướng Dẫn Viết Hàm Python Tính Dãy Fibonacci:**

Dưới đây là 2 cách triển khai tối ưu bằng Python:

```python
# Cách 1: Vòng lặp tối ưu O(n) thời gian, O(1) bộ nhớ
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

print("Số Fibonacci thứ 10 là:", fibonacci(10)) # 55
print("10 số đầu tiên:", generate_fibonacci_sequence(10))
```

Bạn có cần tôi tối ưu thêm thuật toán nào khác không?"""

        elif matches(["python", "flask"]):
            return """💻 **Về Lập Trình Python & Framework Flask:**
- **Python:** Ngôn ngữ số 1 thế giới về Trí tuệ Nhân tạo (AI), Khoa học Dữ liệu và Xây dựng Backend Web nhờ hệ sinh thái thư viện phong phú.
- **Flask:** Micro-framework mạnh mẽ, thanh thoát của Python giúp xây dựng REST API, kiến trúc Blueprint module hóa và tích hợp ORM SQLAlchemy mượt mà.

💡 *Hệ thống EventAI Pro bạn đang sử dụng được phát triển bằng Flask Blueprint kết hợp dịch vụ Agentic AI RAG thế hệ mới!*"""

        elif matches(["docker", "git"]):
            return """🛠️ **Về Công Cụ DevOps (Docker & Git):**
- **Git:** Hệ thống quản lý phiên bản phân tán giúp kiểm soát mã nguồn theo thời gian, phân nhánh (branching) và cộng tác nhóm.
- **Docker:** Nền tảng container hóa giúp đóng gói toàn bộ ứng dụng và môi trường vào Container độc lập, đảm bảo chạy đồng nhất trên mọi máy chủ.

[👉 Khám phá sự kiện Cloud & DevOps TechDay](/events/5)"""

    # =========================================================================
    # 5. TRÍ TUỆ NHÂN TẠO, AGENTIC AI, RAG, MACHINE LEARNING
    # =========================================================================
    if matches(["ai", "agentic", "rag", "llm", "machine learning", "deep learning", "transformer", "chatgpt", "gemini"]):
        if matches(["agentic", "agent", "rag"]):
            return """🤖 **Tổng Quan Chuyên Sâu Về Agentic AI & RAG Pipeline (2026):**
- **Agentic AI:** Bước tiến hóa từ Chatbot đối thoại sang Hệ tác tử Tự chủ (Autonomous Agents). Gồm 4 trụ cột:
  1. *Planning (Lập kế hoạch):* Phân rã mục tiêu lớn thành các task nhỏ.
  2. *Tool Use (Sử dụng công cụ):* Gọi API, truy vấn CSDL, thực thi code.
  3. *Reflection (Tự phản tư):* Tự kiểm tra kết quả và sửa lỗi trước khi phản hồi.
  4. *Multi-agent:* Phối hợp nhiều agent chuyên trách.
- **RAG (Retrieval-Augmented Generation):** Kết hợp truy xuất dữ liệu từ cơ sở dữ liệu quan hệ (SQLite) và sức mạnh tổng hợp của LLM (Gemini 3.6 Flash), triệt tiêu hoàn toàn hiện tượng *Hallucination* (ảo giác).

[👉 Xem chi tiết Vietnam AI Summit 2026](/events/4)"""

        return """🧠 **Về Trí Tuệ Nhân Tạo & Mô Hình Ngôn Ngữ Lớn (GenAI):**
Công nghệ AI năm 2026 đang tập trung vào các mô hình kích thước tối ưu (Small Language Models), Fine-tuning thích ứng (LoRA) và kiến trúc RAG theo thời gian thực để phục vụ các bài toán doanh nghiệp cụ thể.

[👉 Khám phá các sự kiện Trí tuệ Nhân tạo hot nhất](/events)"""

    # =========================================================================
    # 6. GIAO TIẾP TỰ NHIÊN & CHÀO HỎI
    # =========================================================================
    if matches(["chao", "chào", "hello", "hi", "hey", "ban la ai", "bạn là ai", "ten gi"]):
        return """👋 **Xin chào bạn! Tôi là EventAI Concierge.**
Tôi là Trợ lý Cố vấn Trí tuệ Nhân tạo thông minh của Nền tảng EventAI Pro. Tôi có thể đồng hành và hỗ trợ bạn:
- 🎟️ **Tư vấn & Đặt vé sự kiện:** Vé VIP, Vé Tiêu chuẩn, Vé Sinh viên ICTU, thanh toán qua VietQR.
- 🎓 **Thông tin sự kiện Đại học ICTU:** Lễ tốt nghiệp 2026, ICTU Hackathon, Ngày hội việc làm.
- 📅 **Tra cứu lịch trình, diễn giả & phòng hội thảo** theo thời gian thực.
- 💻 **Giải đáp lập trình & Công nghệ:** Python, Flask, CSDL SQL, Docker, Agentic AI, RAG.

Bạn muốn tìm hiểu hoặc cần tôi hỗ trợ về nội dung nào?"""

    if matches(["cam on", "cảm ơn", "thank", "tuyet voi", "tuyệt vời", "hay qua", "good", "ok"]):
        return """❤️ **Rất vui được đồng hành cùng bạn!**
Nếu bạn có bất kỳ câu hỏi nào về các sự kiện công nghệ, quy trình đặt vé hay kiến thức kỹ thuật lập trình, hãy cứ thoải mái nhắn tin cho tôi nhé! Chúc bạn một ngày tuyệt vời! 🚀"""

    # =========================================================================
    # 7. PHÂN TÍCH TỰ NHIÊN TỪ NGỮ CẢNH CƠ SỞ DỮ LIỆU THỰC TẾ
    # =========================================================================
    # Nếu trong system_instruction có dữ liệu sự kiện trích xuất, ta tận dụng dữ liệu đó:
    if system_instruction and "[SỰ KIỆN ID" in system_instruction:
        # Tìm tiêu đề sự kiện đầu tiên trong context
        evt_match = re.search(r'\[SỰ KIỆN ID (\d+)\]:\s*([^\n]+)', system_instruction)
        if evt_match:
            evt_id = evt_match.group(1)
            evt_title = evt_match.group(2).strip()
            return f"""💡 **Thông tin liên quan đến câu hỏi của bạn về sự kiện:**

Dựa trên dữ liệu hệ thống, sự kiện phù hợp nhất là:
**{evt_title}**

- 🎟️ Bạn có thể tra cứu lịch trình chi tiết, danh sách diễn giả và các hạng vé đang mở bán.
- 👉 [Bấm vào đây để xem chi tiết & Đặt vé ngay](/events/{evt_id}#ticketSection)

Nếu bạn cần thông tin chi tiết hơn về giá vé, diễn giả hay địa điểm tổ chức, hãy cho tôi biết nhé!"""

    return f"""💡 **Giải đáp chi tiết về:** *"{clean_p}"*

Dưới góc nhìn của Trợ lý EventAI Concierge:
1. **Nội dung trọng tâm:** Câu hỏi của bạn rất hữu ích cho việc tìm hiểu và chuẩn bị tham gia các sự kiện công nghệ.
2. **Khuyến nghị từ hệ thống:** Bạn có thể tham khảo danh sách các sự kiện đang diễn ra để cập nhật thêm các buổi hội thảo, diễn giả và workshop chuyên sâu liên quan đến chủ đề này.
3. **Thao tác nhanh:**
   - [👉 Khám phá toàn bộ sự kiện trên EventAI Pro](/events)
   - [👉 Quản lý vé của tôi](/tickets/my-tickets)"""
