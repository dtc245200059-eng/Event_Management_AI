Hệ thống quản lý sự kiện có tích hợp AI
1. Mô tả bài toán

Đơn vị tổ chức sự kiện cần quản lý sự kiện, lịch trình, vé, người tham dự, check-in, phản hồi và truyền thông. Nếu dữ liệu phân tán, ban tổ chức khó kiểm soát số lượng khách, gửi thông báo và tổng hợp phản hồi sau sự kiện. Đề tài yêu cầu xây dựng hệ thống quản lý sự kiện có tích hợp AI sinh nội dung thông báo, tóm tắt phản hồi và hỗ trợ hỏi đáp thông tin sự kiện.
2. Mục tiêu

- Xây dựng hệ thống quản lý sự kiện, vé/đăng ký, người tham dự, check-in, lịch trình và phản hồi.
- Tích hợp AI để sinh thông báo, tóm tắt phản hồi và chatbot hỏi đáp thông tin sự kiện.
- Sử dụng AI trong SDLC để phân tích nghiệp vụ sự kiện, sinh mã, kiểm thử và tài liệu.
- Hỗ trợ ban tổ chức vận hành sự kiện hiệu quả và rút kinh nghiệm sau sự kiện.
3. Yêu cầu chức năng
3.1. Chức năng quản lý
1. Đăng nhập và phân quyền quản trị viên, ban tổ chức, nhân viên check-in.
2. Quản lý sự kiện: tên, thời gian, địa điểm, mô tả, trạng thái.
3. Quản lý lịch trình, diễn giả, phiên nội dung.
4. Quản lý đăng ký/vé và thông tin người tham dự.
5. Check-in người tham dự bằng mã đăng ký hoặc QR code ở mức demo.
6. Gửi/thống kê thông báo cho người tham dự.
7. Thu thập phản hồi sau sự kiện.
8. Thống kê số đăng ký, check-in, tỷ lệ tham dự, phản hồi.
3.2. Chức năng AI
1. AI sinh nội dung email/thông báo mời tham dự, nhắc lịch hoặc cảm ơn sau sự kiện.
2. AI tóm tắt phản hồi người tham dự thành các nhóm ý kiến chính.
3. Chatbot hỏi đáp thông tin sự kiện dựa trên mô tả, lịch trình và FAQ.
4. Yêu cầu kỹ thuật

- Backend: FastAPI/Flask/Django.
- Frontend: React/Vue/HTML template.
- CSDL: SQLite/MySQL/PostgreSQL.
- AI Engine: OpenAI/Gemini/Claude/Hugging Face/Ollama.
- Khuyến khích dùng RAG nhẹ cho chatbot lịch trình/FAQ.
- Có test cho đăng ký, check-in, phản hồi và AI tóm tắt.
5. Dữ liệu đầu vào, đầu ra và dữ liệu hệ thống

- Dữ liệu chính: sự kiện, lịch trình, diễn giả, người tham dự, vé/đăng ký, check-in, phản hồi, thông báo.
- Đầu vào quản lý: thông tin sự kiện, lịch trình, đăng ký, phản hồi.
- Đầu vào AI: nội dung sự kiện, nhóm người nhận, phản hồi dạng văn bản, FAQ.
- Đầu ra quản lý: danh sách đăng ký, trạng thái check-in, báo cáo phản hồi.
- Đầu ra AI: thông báo, tóm tắt phản hồi, câu trả lời chatbot.

Ví dụ dữ liệu mẫu: `Sự kiện: Ngày hội AI 2026, 200 khách, 4 phiên, phản hồi: "Nội dung hay nhưng phần check-in hơi chậm"`.

Prompt mẫu:

System: Bạn là trợ lý truyền thông sự kiện. Viết nội dung rõ ràng, lịch sự, đúng thông tin được cung cấp. Không tự thêm thời gian, địa điểm hoặc diễn giả.
User: Hãy sinh email nhắc lịch tham dự dựa trên thông tin sau: {{event_info}}. Đối tượng nhận: sinh viên đã đăng ký.

Không gửi email/số điện thoại hàng loạt cho AI nếu chỉ cần sinh nội dung mẫu.
6. Hướng dẫn sử dụng AI trong từng giai đoạn SDLC

 Giai đoạn 1: Phân tích yêu cầu và thiết kế hệ thống (Bài KT1)

- Dùng AI phân tích quy trình tạo sự kiện, đăng ký, check-in, phản hồi.
- Dùng AI thiết kế actor, use case và ERD.
- Dùng AI xác định chức năng AI sinh thông báo, tóm tắt phản hồi, hỏi đáp sự kiện.
- Dùng AI sinh wireframe trang sự kiện, check-in và dashboard phản hồi.
- Dùng AI gợi ý yêu cầu phi chức năng về tốc độ check-in.

 Giai đoạn 2: Xây dựng chức năng quản lý (Bài KT2)

- Dùng AI sinh model/API cho sự kiện, người tham dự, check-in, phản hồi.
- Dùng AI sinh giao diện danh sách sự kiện và form đăng ký.
- Dùng AI sinh logic thống kê tỷ lệ tham dự.
- Dùng AI debug lỗi trùng đăng ký hoặc check-in nhiều lần.

 Giai đoạn 3: Tích hợp AI, tối ưu prompt và kiểm thử (Bài KT3)

- Dùng AI thiết kế prompt sinh thông báo không tự bịa thông tin.
- Dùng AI sinh code tóm tắt phản hồi theo nhóm vấn đề.
- Dùng AI tạo test case cho phản hồi tiêu cực, dữ liệu thiếu, câu hỏi ngoài phạm vi.
- Tối ưu prompt chatbot để chỉ trả lời theo dữ liệu sự kiện.

 Giai đoạn 4: Hoàn thiện, triển khai và báo cáo (Bài thi cuối kỳ)

- Dùng AI sinh README, dữ liệu mẫu và kịch bản demo sự kiện.
- Dùng AI review bảo mật dữ liệu người tham dự.
- Dùng AI tạo báo cáo kỹ thuật và slide.
- Dùng AI hỗ trợ triển khai và tạo bản hướng dẫn vận hành.
7. Mức độ khó

Trung bình: Hệ thống có nhiều luồng nghiệp vụ nhưng không quá nặng về dữ liệu nhạy cảm. Chức năng AI đa dạng và cần kiểm soát không bịa thông tin sự kiện.
