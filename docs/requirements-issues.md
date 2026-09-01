# Requirements Issues, Ambiguities & Human Gate 1 Verification
**Dự Án**: Hệ Thống Quản Lý Sự Kiện Tích Hợp AI (Event Management AI System)  
**Tài Liệu Tham Chiếu**: `docs/customer-requirement.md`, `docs/requirements.md`  
**Giai Đoạn**: Requirements Engineering (Human Gate 1)

---

## 1. Mục Đích & Bối Cảnh
Trong mô hình **AI-Augmented SDLC**, việc sử dụng AI Agent để phân tích yêu cầu có thể dẫn đến hai nguy cơ lớn:
1. **AI Hallucination / Requirement Invention**: AI tự ý bổ sung các tính năng ngoài tầm kiểm soát và ngoài ngân sách dự án.
2. **Ambiguities & Implicit Assumptions**: Các yêu cầu ban đầu của khách hàng còn mơ hồ, thiếu số liệu định lượng hoặc có mâu thuẫn nghiệp vụ.

Tài liệu này ghi nhận toàn bộ quá trình phát hiện, làm rõ các điểm mơ hồ và biên bản kiểm duyệt con người (Human Gate 1).

---

## 2. Nhật Ký Rà Soát Điểm Mơ Hồ & Thiếu Sót (Ambiguity & Defect Log)

| Mã Vấn Đề | Mô Tả Mơ Hồ / Thiếu Sót | Nguy Cơ Kỹ Thuật | Quyết Định / Giải Pháp Xử Lý | Trạng Thái |
| :--- | :--- | :--- | :--- | :---: |
| **ISSUE-01** | Khách hàng yêu cầu "Thanh toán vé" nhưng chưa nêu rõ cổng thanh toán trung gian (MoMo, VNPay hay Stripe). | Gây phình to phạm vi phát triển (Scope Creep) và phụ thuộc vào tài khoản sandbox bên thứ ba. | **Quyết định**: Xây dựng module **Mô phỏng Thanh toán Nội bộ (Payment Simulation)** sinh mã giao dịch duy nhất và lưu trạng thái `paid`/`pending`/`free`. | **RESOLVED** |
| **ISSUE-02** | Xung đột khi nhiều người cùng bấm đặt vé vào mili-giây cuối cùng (Race Condition / Overselling). | Bán vượt quá số lượng chỗ ngồi thực tế của hội trường. | **Quyết định**: Áp dụng Database Transaction với khóa logic kiểm tra `sold_count < quota` ngay trước khi commit (`FR-04`, `BR-03`). | **RESOLVED** |
| **ISSUE-03** | Khách hàng chụp màn hình mã QR gửi cho bạn bè để cùng vào cổng (Check-in gian lận). | 1 vé được sử dụng nhiều lần tại các cửa soát vé khác nhau. | **Quyết định**: Thiết lập cờ `checked_in = True` ngay trong lần quét đầu tiên; mọi lần quét sau trả về lỗi HTTP 409 Duplicate (`FR-06`, `BR-05`). | **RESOLVED** |
| **ISSUE-04** | Chatbot AI tự bịa đặt thời gian hội thảo hoặc tên diễn giả nổi tiếng khi không tìm thấy trong CSDL (Hallucination). | Gây nhầm lẫn nghiêm trọng cho khách tham dự, làm mất uy tín Ban tổ chức. | **Quyết định**: Thiết kế System Prompt bắt buộc trả lời dựa trên CONTEXT truy xuất từ CSDL; nếu không có dữ liệu phải từ chối lịch sự (`FR-AI-01`, `NFR-09`). | **RESOLVED** |
| **ISSUE-05** | Mạng Internet tại địa điểm tổ chức hội nghị bị nghẽn khiến API Gemini bị Timeout hoặc mất kết nối. | Chatbot AI bị treo cứng hoặc ném lỗi crash màn hình người dùng. | **Quyết định**: Cài đặt **Offline Fallback Mock Engine** tự động kích hoạt khi có lỗi mạng/API Key, đảm bảo hệ thống phản hồi 100% thời gian. | **RESOLVED** |

---

## 3. Các Giả Định Kỹ Thuật (Assumptions)
1. **Môi trường Cơ sở dữ liệu**: SQLite được chấp nhận cho môi trường phát triển (Development) và kiểm thử tự động (Unit Test), CSDL MySQL / PostgreSQL sẵn sàng cho môi trường Production.
2. **Khung thời gian sự kiện**: Thời gian bắt đầu (`start_date`) luôn nhỏ hơn thời gian kết thúc (`end_date`).
3. **Mã vé QR**: Mã định danh vé là duy nhất trên toàn hệ thống (Format: `TCK-YYYYMM-<HEX8>`).
4. **Ngôn ngữ phản hồi**: Hệ thống giao diện và Trợ lý AI giao tiếp chính bằng Tiếng Việt.

---

## 4. Biên Bản Kiểm Chứng Chống AI Hallucination (Human Gate 1)

```
=============================================================================
             BIÊN BẢN KIỂM CHỨNG YÊU CẦU NGHIỆP VỤ (HUMAN GATE 1)
=============================================================================
Dự Án: Hệ Thống Quản Lý Sự Kiện Tích Hợp AI (Event Management AI System)
Người Kiểm Duyệt (Reviewer): Kỹ Sư Trưởng / Trưởng Nhóm Sinh Viên
Thời Điểm: Tháng 10/2026

DANH MỤC KIỂM TRA (VERIFICATION CHECKLIST):
 [X] Đã giải quyết triệt để 4 điểm nghẽn vận hành của bài toán thực tế.
 [X] 100% Yêu cầu Chức năng (FR-01..08, FR-AI-01..04) có ID và mô tả I/O rõ ràng.
 [X] 100% Yêu cầu Phi Chức năng (NFR-01..09) có chỉ số đo lường kiểm thử được.
 [X] Tất cả User Stories tuân thủ định dạng chuẩn As a... I want... so that...
 [X] Toàn bộ Acceptance Criteria tuân thủ chuẩn Given-When-Then.
 [X] KHÔNG PHÁT HIỆN "AI Hallucination" (AI không tự ý thêm các chức năng ngoài phạm vi).
 [X] Các điểm mơ hồ trong ISSUE-01 đến ISSUE-05 đã được thống nhất giải pháp.

KẾT LUẬN & PHÊ DUYỆT:
 Trạng Thái: [ APPROVED ] - ĐÃ PHÊ DUYỆT
 Quyết Định: Chuyển giao toàn bộ tài liệu Yêu cầu sang Giai đoạn Thiết Kế Kiến Trúc (Architecture Design).
=============================================================================
```
