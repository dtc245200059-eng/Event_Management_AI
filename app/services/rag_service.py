"""
RAG Service: Structured Context Retrieval from SQLite Database + Prompt Grounding.
Implements Question Analysis, Parameterized Event Retrieval, Context Building, and Grounded RAG.
"""
import os
import time
import re
import unicodedata
from datetime import datetime
from flask import current_app
from app.extensions import db
from app.models import Event, Speaker, Venue, Schedule, Ticket, EventFAQ
from app.services.gemini_service import call_gemini

def remove_accents(input_str):
    """Chuyển đổi chuỗi tiếng Việt có dấu thành không dấu để nhận diện ý định chuẩn xác."""
    if not input_str:
        return ""
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)]).lower()

def load_prompt_template(filename):
    """Đọc prompt template từ thư mục app/prompts/."""
    prompts_dir = os.path.join(current_app.root_path, 'prompts')
    filepath = os.path.join(prompts_dir, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    return ""

def analyze_question(query_text=""):
    """
    Question Analysis Module:
    Phân loại Ý định (Intent) và Trích xuất Thực thể (Entity Extraction)
    từ câu hỏi ngôn ngữ tự nhiên tiếng Việt của người dùng.
    """
    raw = (query_text or "").strip()
    q_lower = raw.lower()
    q_no_accents = remove_accents(q_lower)

    def has_any(keywords):
        return any(k in q_lower or k in q_no_accents for k in keywords)

    # 1. Intent Detection
    is_free_query = has_any(["mien phi", "0 dong", "0 vnd", "free", "khong mat tien", "khong ton tien"])
    is_ticket_query = has_any(["ve", "gia ve", "hang ve", "tien ve", "con ve", "mua ve", "dat ve", "ban ve", "thanh toan", "vietqr", "qr code", "huy ve", "hoan tien", "hoan quota"])
    is_schedule_query = has_any(["lich trinh", "agenda", "timeline", "may gio", "khi nao", "thoi gian", "bat dau", "ket thuc", "phien", "buoi"])
    is_speaker_query = has_any(["dien gia", "ai thuyet trinh", "chuyen gia", "speaker", "thay", "co", "tien si", "giao su", "bac si", "chu tri", "bao cao vien"])
    is_venue_query = has_any(["dia diem", "o dau", "hoi truong", "phong hop", "vi tri", "online", "truc tiep", "dia chi"])
    is_recommendation_query = has_any(["goi y", "nen tham gia", "phu hop", "de xuat", "thich hop", "su kien hot", "hay nhat", "danh cho"])

    # 2. Entity Extraction
    # Location entities
    location_filter = None
    if has_any(["thai nguyen", "ictu", "quyết thắng", "z115"]):
        location_filter = "Thái Nguyên"
    elif has_any(["ha noi", "hà nội", "hoan kiem", "hoàn kiếm", "hoa lac", "hòa lạc"]):
        location_filter = "Hà Nội"
    elif has_any(["ho chi minh", "hồ chí minh", "tphcm", "sai gon", "sài gòn"]):
        location_filter = "TP. Hồ Chí Minh"
    elif has_any(["online", "truc tuyen", "zoom", "google meet"]):
        location_filter = "Online"

    # Category entities
    category_filter = None
    categories_map = {
        "Trí tuệ nhân tạo": ["ai", "tri tue nhan tao", "genai", "machine learning", "deep learning", "rag", "llm"],
        "Khoa học dữ liệu": ["du lieu", "data", "tot nghiep", "be giang", "graduation"],
        "Cloud & DevOps": ["cloud", "devops", "docker", "kubernetes", "microservices"],
        "Startup & Đầu tư": ["startup", "khoi nghiep", "dau tu", "career", "viec lam", "tuyen dung", "doanh nghiep"],
        "An toàn thông tin": ["bao mat", "an ninh mang", "cyber", "zero trust", "hacker"],
        "Âm nhạc": ["am nhac", "acoustic", "concert", "ca nhac"],
        "Ẩm thực": ["am thuc", "ca phe", "coffee", "bakery", "banh"],
        "Y tế & Sức khỏe": ["y te", "suc khoe", "healthtech", "benh vien", "y khoa"],
        "Game & Đồ họa": ["game", "spatial", "unreal", "unity", "do hoa"],
        "Thể thao": ["marathon", "chay bo", "the thao", "night run"],
        "Nghệ thuật & Thiết kế": ["nhiep anh", "drone", "cinematic", "ui/ux", "thiet ke", "figma"]
    }
    for cat_name, kws in categories_map.items():
        if has_any(kws):
            category_filter = cat_name
            break

    # Time filter
    time_filter = None
    if has_any(["hom nay", "ngay mai", "sap toi", "tuan nay", "thang nay", "nam nay", "2026"]):
        time_filter = "upcoming"

    return {
        "is_free_query": is_free_query,
        "is_ticket_query": is_ticket_query,
        "is_schedule_query": is_schedule_query,
        "is_speaker_query": is_speaker_query,
        "is_venue_query": is_venue_query,
        "is_recommendation_query": is_recommendation_query,
        "location_filter": location_filter,
        "category_filter": category_filter,
        "time_filter": time_filter,
        "raw_query": raw,
        "query_lower": q_lower,
        "query_no_accents": q_no_accents
    }

def retrieve_events(intent_data, target_event_id=None):
    """
    Event Retrieval Module:
    Truy xuất dữ liệu có cấu trúc từ SQLite sử dụng SQLAlchemy ORM an toàn (chống SQLi).
    Lọc theo intent, entities và tính điểm phù hợp (relevance scoring).
    """
    # Nếu chỉ định rõ ID sự kiện (ví dụ trong trang chi tiết sự kiện hoặc workspace đã chọn)
    if target_event_id:
        evt = db.session.get(Event, target_event_id)
        if evt:
            return [evt]

    all_published = Event.query.filter(Event.status.in_(['published', 'ongoing'])).all()
    if not all_published:
        return []

    q_lower = intent_data["query_lower"]
    q_no_accents = intent_data["query_no_accents"]
    is_free = intent_data["is_free_query"]
    cat_filter = intent_data["category_filter"]
    loc_filter = intent_data["location_filter"]

    scored_events = []

    for e in all_published:
        score = 0
        e_title_lower = e.title.lower()
        e_title_no_acc = remove_accents(e_title_lower)
        e_desc_lower = (e.description or "").lower()
        e_desc_no_acc = remove_accents(e_desc_lower)
        e_cat_lower = (e.category or "").lower()
        e_loc_lower = (e.location_address or "").lower()
        e_tags_lower = (e.tags or "").lower()

        # 1. Khớp theo vé miễn phí
        if is_free:
            has_free_ticket = any(t.price == 0 and t.is_available for t in e.tickets)
            if has_free_ticket:
                score += 10
            else:
                score -= 3

        # 2. Khớp theo danh mục
        if cat_filter and e.category == cat_filter:
            score += 8

        # 3. Khớp theo địa điểm
        if loc_filter:
            if loc_filter == "Online" and e.location_type.lower() in ("online", "hybrid"):
                score += 8
            elif loc_filter.lower() in e_loc_lower:
                score += 8

        # 4. Khớp theo tiêu đề sự kiện (Exact & Substring match)
        if e_title_lower in q_lower or e_title_no_acc in q_no_accents:
            score += 15
        else:
            # Khớp từng từ khóa trong tiêu đề
            title_words = [w for w in e_title_no_acc.split() if len(w) > 2]
            matched_words = [w for w in title_words if w in q_no_accents]
            if matched_words:
                score += len(matched_words) * 2

        # 5. Khớp theo mã sự kiện
        if e.event_code and e.event_code.lower() in q_lower:
            score += 20

        # 6. Khớp theo Diễn giả trong lịch trình của sự kiện
        for s in e.schedules:
            if s.speaker:
                spk_name_lower = s.speaker.name.lower()
                spk_name_no_acc = remove_accents(spk_name_lower)
                if spk_name_lower in q_lower or spk_name_no_acc in q_no_accents:
                    score += 12

        # 7. Khớp theo mô tả & tags
        if any(w in e_desc_no_acc for w in q_no_accents.split() if len(w) > 3):
            score += 2
        if e_tags_lower:
            for tag in e_tags_lower.split(','):
                tag_str = tag.strip().lower()
                if tag_str and tag_str in q_lower:
                    score += 3

        if score > 0:
            scored_events.append((score, e))

    scored_events.sort(key=lambda x: x[0], reverse=True)

    if scored_events:
        top_events = [item[1] for item in scored_events[:6]]
        return top_events

    # Nếu câu hỏi quá tổng quát, trả về 6 sự kiện mới nhất/sắp diễn ra
    return sorted(all_published, key=lambda x: x.start_date)[:6]

def build_retrieved_context(query_text="", target_event_id=None):
    """
    Context Builder Module:
    Định dạng và làm giàu dữ liệu truy xuất thành Grounded Context có cấu trúc Markdown chuẩn,
    kiểm soát Token Budgeting và chuẩn bị sẵn các link điều hướng chi tiết.
    """
    intent_data = analyze_question(query_text)
    events = retrieve_events(intent_data, target_event_id=target_event_id)

    if not events:
        return "KHÔNG TÌM THẤY DỮ LIỆU SỰ KIỆN PHÙ HỢP TRONG CƠ SỞ DỮ LIỆU HỆ THỐNG."

    context_blocks = []

    # Block 1: Header hệ thống
    context_blocks.append("=== DANH SÁCH DỮ LIỆU SỰ KIỆN TRUY XUẤT TỪ CSDL (GROUND TRUTH) ===")

    for evt in events:
        evt_block = []
        evt_block.append(f"### [SỰ KIỆN ID {evt.id}]: {evt.title}")
        evt_block.append(f"- **Mã sự kiện:** {evt.event_code} | **Trạng thái:** {evt.status.upper()}")
        evt_block.append(f"- **Chủ đề / Danh mục:** {evt.category}")
        evt_block.append(f"- **Thời gian:** {evt.start_date.strftime('%H:%M • %d/%m/%Y')} đến {evt.end_date.strftime('%H:%M • %d/%m/%Y')}")
        evt_block.append(f"- **Hình thức & Địa điểm:** {evt.location_type.upper()} | {evt.location_address or 'Trực tuyến'}")
        evt_block.append(f"- **Mô tả vắn tắt:** {evt.description}")
        evt_block.append(f"- **Link chi tiết & Đặt vé:** [👉 Xem chi tiết & Đặt vé ngay](/events/{evt.id}#ticketSection)")

        # Bảng vé
        tickets = evt.tickets.all()
        if tickets:
            evt_block.append("\n  * BẢNG HẠNG VÉ & GIÁ TIỀN:")
            for t in tickets:
                price_str = "0 VNĐ (MIỄN PHÍ)" if t.price == 0 else f"{t.price:,.0f} VNĐ"
                status_str = "ĐANG MỞ BÁN (CÒN VÉ)" if t.is_available else "HẾT VÉ / TẠM ĐÓNG"
                evt_block.append(f"    + Hạng vé: {t.name} ({t.ticket_type.upper()}) | Giá: {price_str} | Quota: còn {t.remaining_quota}/{t.quota} suất ({status_str})")
        else:
            evt_block.append("  * Vé: Đang cập nhật danh sách vé.")

        # Lịch trình & Diễn giả
        schedules = evt.schedules.order_by(Schedule.start_at.asc()).all()
        if schedules:
            evt_block.append("\n  * LỊCH TRÌNH CÁC PHIÊN THẢO LUẬN (AGENDA):")
            for s in schedules:
                time_range = f"{s.start_at.strftime('%H:%M')} - {s.end_at.strftime('%H:%M')}"
                spk_name = s.speaker.name if s.speaker else "Ban tổ chức"
                spk_info = f" ({s.speaker.title or 'Chuyên gia'}, {s.speaker.organization or ''})" if s.speaker else ""
                vne_name = s.venue.name if s.venue else "Hội trường chính"
                evt_block.append(f"    + [{time_range}] {s.title}")
                evt_block.append(f"      - Diễn giả: {spk_name}{spk_info} | Phòng: {vne_name}")
                if s.description:
                    evt_block.append(f"      - Tóm tắt phiên: {s.description}")

        # Các câu hỏi thường gặp & Quy định sự kiện (FAQ)
        faqs = evt.faqs.all() if hasattr(evt, 'faqs') else []
        if faqs:
            evt_block.append("\n  * CÁC CÂU HỎI THƯỜNG GẶP (FAQ) & QUY ĐỊNH SỰ KIỆN:")
            for fq in faqs:
                evt_block.append(f"    + Q: {fq.question}")
                evt_block.append(f"      A: {fq.answer}")

        context_blocks.append("\n".join(evt_block))

    # Block 2: Danh sách Diễn giả nổi bật liên quan
    speakers = Speaker.query.limit(8).all()
    if speakers:
        spk_block = ["=== DANH SÁCH DIỄN GIẢ TIÊU BIỂU TRONG HỆ THỐNG ==="]
        for spk in speakers:
            spk_block.append(f"- **{spk.name}** ({spk.title or 'Chuyên gia'} - {spk.organization or 'Đơn vị đối tác'}): {spk.bio or 'Chuyên gia đầu ngành giàu kinh nghiệm.'}")
        context_blocks.append("\n".join(spk_block))

    # Block 3: Quy trình hệ thống chuẩn
    workflow_block = """=== QUY TRÌNH HỆ THỐNG EVENTAI PRO ===
1. **Quy trình Đặt vé & Thanh toán VietQR:**
   - Người dùng chọn sự kiện -> Chọn hạng vé phù hợp -> Bấm 'Tiến Hành Đặt Vé'.
   - Hệ thống tự động sinh Mã QR thanh toán chuẩn VietQR NAPAS 24/7 / MoMo / VNPAY đúng số tiền và cú pháp chuyển khoản.
   - Vé Miễn phí (0 VNĐ): Hệ thống duyệt cấp vé ngay lập tức không cần thanh toán.
2. **Quy trình Nhận vé & Check-in tại sự kiện:**
   - Sau khi có vé, người dùng vào mục 'Vé Của Tôi' (`/tickets/my-tickets`) để xem Thẻ vé điện tử kèm Mã QR Check-in cá nhân.
   - Tại cửa hội trường, nhân viên Ban tổ chức dùng camera quét mã QR để đối soát và cho vào trong 1 giây.
3. **Quy trình Hủy vé & Hoàn trả Quota:**
   - Người dùng vào 'Vé Của Tôi' -> Bấm nút 'Hủy vé' màu đỏ tại vé cần hủy -> Xác nhận Modal.
   - Suất vé sẽ tự động được hoàn trả về kho quota sự kiện cho người khác đăng ký."""
    context_blocks.append(workflow_block)

    return "\n\n".join(context_blocks)

def answer_event_query(user_message, event_id=None, history=None):
    """
    RAG Pipeline hoàn chỉnh:
    Query -> Question Analysis -> Event Retrieval -> Context Builder -> 5-part System Prompt -> Multi-turn Gemini / Local Fallback.
    """
    start_time = time.time()

    # 1. Trích xuất ngữ cảnh từ SQLite
    context = build_retrieved_context(query_text=user_message, target_event_id=event_id)

    # 2. Tải Prompt Template 5 thành phần
    system_template = load_prompt_template('chatbot_system.txt')
    if "{{retrieved_context}}" in system_template:
        system_instruction = system_template.replace("{{retrieved_context}}", context)
    else:
        system_instruction = f"{system_template}\n\n=== CONTEXT DỮ LIỆU SỰ KIỆN ===\n{context}"

    # 3. Gọi Gemini API (hỗ trợ hội thoại đa lượt history) hoặc Local Fallback Engine
    response_text, mode = call_gemini(
        prompt=user_message,
        system_instruction=system_instruction,
        history=history
    )

    latency_ms = int((time.time() - start_time) * 1000)
    return response_text, mode, latency_ms
