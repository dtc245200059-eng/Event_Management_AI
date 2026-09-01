---
name: rag-prompt
description: Skill thiết kế System Prompt và User Prompt có cấu trúc 5 thành phần (Instructions, Context, Constraints, Few-shot Examples, Output Format) nhằm chống Hallucination cho RAG LLM.
---

# RAG Prompt Engineering Skill

## Objective
Xây dựng chỉ dẫn có cấu trúc chuẩn 5 thành phần cho mô hình ngôn ngữ lớn (Gemini 2.0 Flash) nhằm đảm bảo 100% câu trả lời dựa trên dữ liệu thực tế (Grounded), ngăn chặn hiện tượng bịa đặt thông tin (Anti-Hallucination) và phòng chống tấn công Prompt Injection.

## Cấu Trúc 5 Thành Phần Chuẩn Của Prompt
1. **Instructions (Chỉ dẫn Vai trò & Mục tiêu)**:
   - "Bạn là Event AI Assistant - Trợ lý thông minh của Hệ thống Quản lý Sự kiện."
2. **Context (Khối Ngữ cảnh Dữ liệu)**:
   - Ngữ cảnh thực tế `{{retrieved_context}}` được truyền từ `context-builder`.
3. **Constraints (Ràng buộc Nghiêm ngặt & Chống Hallucination)**:
   - CHỈ ĐƯỢC PHÉP trả lời dựa trên thông tin có trong phần CONTEXT.
   - TUYỆT ĐỐI KHÔNG tự tạo tên diễn giả, tự bịa lịch trình hoặc tự sinh giá vé.
   - Nếu Context không chứa thông tin: Nói rõ ràng rằng hệ thống chưa có thông tin về nội dung này và hướng dẫn người dùng liên hệ Ban tổ chức.
   - Trả lời hoàn toàn bằng tiếng Việt lịch sự, súc tích.
4. **Few-shot Examples (Ví dụ Mẫu)**:
   - Cung cấp các cặp Question - Grounded Answer mẫu để định hình văn phong phản hồi.
5. **Output Format (Định dạng Phản hồi)**:
   - Trình bày định dạng Markdown sạch (in đậm, danh sách gạch đầu dòng, bảng biểu nếu cần).

## Rules & Constraints
- Tách biệt System Prompt và User Input để chống Prompt Injection.
- Quản lý các tệp prompt có cấu trúc trong thư mục `app/prompts/`.

## Outputs
- `app/prompts/chatbot_system.txt`
- `app/prompts/event_generator.txt`
- `app/prompts/sentiment_prompt.txt`
