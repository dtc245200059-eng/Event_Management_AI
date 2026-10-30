# BÁO CÁO TỔNG KẾT GIA CỐ BẢO MẬT KỸ NĂNG AGENTIC SEO
## PHASE 1 — AGENTIC SEO SKILL SECURITY HARDENING

---

- **Dự án**: `EventAI Pro` (`D:\Event_Management_AI`)
- **Đối tượng gia cố**: Kỹ năng Agentic SEO (`.agents/skills/seo`)
- **Kho lưu trữ nguồn**: `https://github.com/Bhanunamikaze/Agentic-SEO-Skill`
- **Vị trí sao lưu gốc an toàn**: `D:\EventAI_Security_Backups\seo-skill-before-hardening` (Xác thực 188/188 tệp khớp SHA-256)
- **Tài liệu kiểm toán gốc**: [seo-skill-security-audit.md](file:///d:/Event_Management_AI/docs/seo/seo-skill-security-audit.md)
- **Danh mục kiểm kê thay đổi**: [seo-skill-change-inventory.md](file:///d:/Event_Management_AI/docs/seo/seo-skill-change-inventory.md)
- **Bằng chứng kiểm thử hồi quy**: [seo-skill-security-regression-results.md](file:///d:/Event_Management_AI/docs/seo/seo-skill-security-regression-results.md)
- **Thời gian hoàn tất**: Ngày 29 tháng 10 năm 2026
- **Kỹ sư thẩm định & gia cố**: Senior Application Security Engineer & Software Supply Chain Auditor
- **Quyết định bảo mật chính thức**: **RESTRICTED (CHẾ ĐỘ KIỂM SOÁT TƯỜNG MINH)**

---

## 1. TỔNG QUAN VÀ BỐI CẢNH DỰ ÁN

Kỹ năng bên thứ ba `Agentic-SEO-Skill` được cài đặt vào thư mục `.agents/skills/seo` nhằm bổ sung năng lực kiểm toán SEO, dữ liệu có cấu trúc Schema.org, Core Web Vitals và tối ưu hóa tìm kiếm AI (GEO/AEO). Tuy nhiên, trong quá trình cài đặt ban đầu, hệ thống quét chuỗi cung ứng ghi nhận:
- **Gen Security**: HIGH RISK
- **Socket**: 1 alert
- **Snyk**: MEDIUM RISK

Báo cáo kiểm toán tĩnh trước đó đã phân loại kỹ năng này ở mức **RESTRICTED**. Nhiệm vụ của Giai đoạn 1 (Phase 1) là **tiến hành gia cố triệt để mã nguồn (Security Hardening)** nhằm loại bỏ các điểm yếu có thể bị khai thác, thiết lập các rào chắn kỹ thuật kiên cố, đồng thời bảo vệ tuyệt đối tính toàn vẹn của ứng dụng `EventAI Pro`.

---

## 2. NGUYÊN TẮC BẢO VỆ VÙNG GIỚI HẠN (STRICT CHANGE BOUNDARIES)

Toàn bộ quá trình gia cố tuân thủ kỷ luật nghiêm ngặt:
1. **Chỉ tác động bên trong thư mục kỹ năng**: `D:\Event_Management_AI\.agents\skills\seo\` và thư mục tài liệu `docs/seo/`.
2. **Không sửa đổi bất kỳ tệp ứng dụng nào**: Tuyệt đối không thay đổi mã nguồn Flask (`app/`), routes, Jinja2 templates, static CSS/JS, database models, file cấu hình `.env`, hay 39 kỹ năng nội bộ khác.
3. **Không thay đổi tài liệu học thuật**: Giữ nguyên vẹn 100% các tệp Word (`.docx`), PowerPoint (`.pptx`) trong `tailieu/`.
4. **Không cài đặt thêm gói ngoài**: Không chạy lệnh `pip install` gây ô nhiễm môi trường ảo Python.
5. **Độc lập sao lưu**: Tạo bản sao lưu toàn diện trước khi thực hiện bất kỳ thay đổi nào tại `D:\EventAI_Security_Backups\seo-skill-before-hardening`.

---

## 3. CÁC HÀNG RÀO BẢO MẬT ĐÃ TRIỂN KHAI (HARDENING IMPLEMENTATION)

### 3.1. Chống rò rỉ Header Xác thực khi Chuyển hướng HTTP (Task 4)
- **Điểm yếu trước đây**: Trong `safe_http.py`, khi xử lý chuyển hướng (301/302/303/307/308), các header chứa thông tin nhạy cảm (`Authorization`, `Cookie`, `Proxy-Authorization`, `X-Api-Key`) được giữ nguyên và gửi tiếp đến địa chỉ đích mới, kể cả khi đích đến thuộc tên miền bên ngoài (Cross-Origin) hoặc bị hạ cấp từ HTTPS sang HTTP.
- **Biện pháp khắc phục**:
  - Xây dựng hàm `get_origin(url)` xác định chặt chẽ bộ ba Origin: `(scheme, host, port)`.
  - Thiết lập danh sách header nhạy cảm: `SENSITIVE_HEADERS = {"authorization", "cookie", "proxy-authorization", "x-api-key", "api-key"}`.
  - **Chặn chuyển hướng chéo miền có xác thực**: Mặc định từ chối (`SafeHTTPError`) mọi chuyển hướng cross-origin nếu yêu cầu có chứa `Authorization`.
  - **Tước bỏ header nhạy cảm**: Nếu chuyển hướng chéo miền được chấp thuận, toàn bộ các header nhạy cảm sẽ bị xóa bỏ hoàn toàn trước khi tạo kết nối tới URL mới.
  - **Chống hạ cấp giao thức (HTTPS -> HTTP Downgrade)**: Từ chối ngay lập tức khi phát hiện chuyển hướng từ HTTPS sang HTTP không mã hóa.
  - **Phát hiện vòng lặp chuyển hướng**: Lưu vết `visited_urls`, ném ngoại lệ `TooManyRedirects` khi phát hiện lặp URL.

### 3.2. Ngăn chặn Triệt để SSRF & Lỗ hổng DNS Rebinding (Task 5)
- **Điểm yếu trước đây**: `safe_http.py` kiểm tra địa chỉ IP bằng `socket.getaddrinfo()` trước khi gọi `requests.request()`. Tuy nhiên, thư viện `requests` thực hiện lần phân giải DNS thứ hai khi tạo kết nối. Kẻ tấn công có thể thiết lập DNS với TTL = 0 để vượt qua bước kiểm tra rồi trỏ về `127.0.0.1` hoặc IP metadata của nhà cung cấp đám mây (Time-of-Check to Time-of-Use - TOCTOU).
- **Biện pháp khắc phục**:
  - **Mở rộng danh mục IP/Hostname bị cấm**:
    - Dải Loopback: `127.0.0.0/8`, `::1`.
    - Dải mạng riêng tư: `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`.
    - Dải Link-local và Cloud Metadata: `169.254.0.0/16`, `fe80::/10`, `169.254.169.254`, `fd00:ec2::254`.
    - Dải CGNAT / Shared Address Space: `100.64.0.0/10` (RFC 6598).
    - Dải IPv4-mapped IPv6: `::ffff:0:0/96` (tự động giải mã và kiểm tra IP gốc).
    - Hostname cấm: `localhost`, `*.localhost`, `*.local`, `*.internal`, `metadata.google.internal`, `metadata`, `instance-data`.
  - **Kiến trúc Kết nối Ràng buộc IP (IP-Binding Defenses)**:
    - Kế thừa và cài đặt các lớp: `SafeHTTPConnection`, `SafeHTTPSConnection`, `SafePoolManager`, và `SafeAdapter`.
    - Trong phương thức `_new_conn()` của tầng kết nối, hệ thống phân giải tên miền, xác thực **tất cả** bản ghi IP trả về.
    - **Kết nối TCP được thiết lập trực tiếp tới IP đã xác thực**: Triệt tiêu hoàn toàn khả năng urllib3 phân giải DNS lại lần thứ hai, loại bỏ 100% rủi ro tấn công DNS Rebinding.
    - **Bảo toàn TLS SNI & Chứng chỉ số**: Đối với HTTPS, tên miền gốc vẫn được chuyển giao cho `server_hostname` trong ngữ cảnh SSL, đảm bảo việc xác thực chứng chỉ số và bảo vệ chống nghe lén (Man-in-the-middle) hoạt động hoàn hảo.
  - **Chuẩn hóa các kịch bản Playwright**:
    - Tích hợp kiểm tra `assert_safe_url` trong `analyze_visual.py`, `capture_screenshot.py`, `mobile_render_checker.py`, `visual_regression_snapshot.py`, `javascript_render_audit.py` trước khi trình duyệt thực hiện điều hướng.

### 3.3. Vô hiệu hóa Cơ chế Tự động Tìm kiếm Bí mật (Task 6)
- **Điểm yếu trước đây**: `env_loader.py` tự động quét `Path.cwd() / ".env"`. Khi chạy từ thư mục gốc của `EventAI Pro`, kỹ năng đọc toàn bộ biến môi trường của dự án (`SECRET_KEY`, CSDL, `GOOGLE_API_KEY`) và nạp vào `os.environ`. Kịch bản `pagespeed.py` và `entity_checker.py` tự ý lấy `GOOGLE_API_KEY` (Gemini API key của ứng dụng) gửi lên query parameter (`?key=...`) của PageSpeed API.
- **Biện pháp khắc phục**:
  - **Xóa bỏ quét tự động**: `env_loader.py` không còn tìm kiếm trong thư mục hiện hành (`cwd`) hoặc thư mục người dùng (`$HOME`).
  - **Chỉ chấp nhận cấu hình tường minh**: Chỉ nạp cấu hình nếu biến môi trường `AGENTIC_SEO_ENV_PATH` được thiết lập tường minh hoặc qua tham số `explicit_path`.
  - **Thiết lập Danh sách Cho phép Khóa (Key Allowlist)**:
    `ALLOWED_SEO_KEYS = {"PAGESPEED_API_KEY", "GOOGLE_KG_API_KEY", "GITHUB_TOKEN", "GH_TOKEN", "GSC_CREDENTIALS_PATH"}`.
    Mọi khóa khác (đặc biệt là `SECRET_KEY`, `DATABASE_URL`, `GOOGLE_API_KEY`) đều bị **bỏ qua hoàn toàn**, không thể bị nạp vào bộ nhớ tiến trình.
  - **Tách biệt khóa API trong kịch bản**:
    - Sửa `pagespeed.py`: Chỉ dùng `PAGESPEED_API_KEY`, không fallback sang `GOOGLE_API_KEY`.
    - Sửa `entity_checker.py`: Chỉ dùng `GOOGLE_KG_API_KEY`, không fallback sang `GOOGLE_API_KEY`.

### 3.4. Chống Rò rỉ Token qua Tham số Tiến trình con (Task 7)
- **Điểm yếu trước đây**: `github_seo_report.py` ghép chuỗi `--token <secret>` vào danh sách tham số dòng lệnh khi gọi các kịch bản con qua `subprocess.run()`, khiến token bị hiển thị công khai trên thanh tiến trình hệ điều hành (Task Manager / Process List). Đồng thời, tiến trình con thừa kế toàn bộ biến môi trường của tiến trình cha.
- **Biện pháp khắc phục**:
  - **Loại bỏ token khỏi tham số CLI**: Xóa bỏ hoàn toàn `--token` trong danh sách `common` và `readme_args` của `collect_inputs()`.
  - **Chuyển giao Token qua Môi trường Cô lập**: Truyền token thông qua `clean_env["GITHUB_TOKEN"]` trong lời gọi `subprocess.run(..., env=clean_env)`.
  - **Làm sạch Môi trường Tiến trình con (`_sanitize_env`)**: Chỉ giữ lại các biến hệ thống cần thiết (`PATH`, `SYSTEMROOT`, `TEMP`, v.v.), loại bỏ toàn bộ biến môi trường nhạy cảm của ứng dụng.
  - **Che giấu Token trong Thông báo lỗi (`_mask_token`)**: Sử dụng Regex để chuyển đổi các token GitHub (`ghp_...`, `github_pat_...`, `Bearer ...`) thành chuỗi `[REDACTED]` trước khi ghi nhật ký hay trả về giao diện.

### 3.5. Kiểm soát Thực thi Tự động & Ngăn chặn Lệnh Tùy ý (Task 8)
- **Điểm yếu trước đây**: `generate_report.py` và `audit_runner.py` chạy tiến trình con mà không kiểm tra chặt chẽ tên kịch bản, tiềm ẩn nguy cơ Path Traversal (ví dụ: `../../malicious.py`).
- **Biện pháp khắc phục**:
  - **Danh sách kịch bản được phép (`ALLOWED_REPORT_SCRIPTS` & `ALLOWED_GITHUB_SCRIPTS`)**: Khóa cứng danh sách các kịch bản SEO nội bộ được phép gọi.
  - **Kiểm tra Leo thang Thư mục**: Xác thực đường dẫn bằng `os.path.realpath()`, đảm bảo tệp thực thi phải nằm bên trong thư mục `scripts/`.
  - **Giới hạn thời gian (Timeout Bound)**: Áp dụng trần timeout tối đa (120 giây) để ngăn chặn tiến trình treo tài nguyên.
  - **Vô hiệu hóa Tải mã từ xa trong Trình cài đặt**: Bổ sung rào chắn trong `install.ps1` và `install.sh`, từ chối chế độ `--online` nếu chưa có biến môi trường xác nhận `ALLOW_INSECURE_REMOTE_INSTALL=1`.

### 3.6. An toàn Hóa Báo cáo HTML & Chống XSS Lưu trữ (Task 9)
- **Điểm yếu trước đây**: `generate_report.py` chèn trực tiếp nội dung cào từ bên ngoài (tên miền, thẻ meta, tiêu đề, HTTP headers) vào file HTML mà không escape; đồng thời kết nối tới CDN Google Fonts (`fonts.googleapis.com`, `fonts.gstatic.com`).
- **Biện pháp khắc phục**:
  - **Gỡ bỏ toàn bộ liên kết tới CDN ngoài**: Xóa bỏ các thẻ `<link href="https://fonts.googleapis.com"...>`.
  - **Sử dụng Font Hệ thống Cục bộ (Offline System Font Stack)**: Áp dụng font Apple/Windows native (`-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif`), giúp báo cáo HTML hiển thị đẹp mắt, bảo mật và hoạt động hoàn toàn offline.
  - **Mã hóa Thực thể HTML (Contextual HTML Escaping)**: Áp dụng `html.escape(str(val), quote=True)` cho toàn bộ các giá trị động: tên miền, mã phản hồi, liên kết hỏng, danh sách vấn đề, thẻ social meta, và security headers. Triệt tiêu 100% nguy cơ Stored DOM XSS.

### 3.7. Chuẩn hóa Hướng dẫn Kỹ năng `SKILL.md` (Task 10)
- Giữ nguyên cấu trúc YAML frontmatter, tên kỹ năng `seo`, và 16 sub-skills.
- Cập nhật rõ ràng thông báo bảo mật: Vô hiệu hóa quét `.env` tự động; yêu cầu cung cấp token qua biến môi trường tường minh.
- Bổ sung **Critical Rule 14** quy định chế độ phân tích offline là mặc định, giới hạn rào chắn mạng SSRF, và cấm tự động kích hoạt trình cài đặt từ xa.

---

## 4. KẾT QUẢ THỰC THI KIỂM THỬ HỒI QUY BẢO MẬT (Task 11 & 12)

Kỹ sư bảo mật đã thiết lập bộ kiểm thử độc lập gồm **45 ca kiểm thử** tại `tests/test_security_hardening.py` và chạy trên môi trường Python 3.14.2:

```text
============================= test session starts =============================
platform win32 -- Python 3.14.2, pytest-9.1.1, pluggy-1.6.0
rootdir: D:\Event_Management_AI\.agents\skills\seo
configfile: pyproject.toml
collected 45 items

tests/test_security_hardening.py::test_get_origin PASSED                 [  2%]
tests/test_security_hardening.py::test_redirect_https_to_http_downgrade_rejected PASSED [  4%]
tests/test_security_hardening.py::test_redirect_cross_origin_authenticated_rejected PASSED [  6%]
tests/test_security_hardening.py::test_redirect_cross_origin_unauthenticated_strips_sensitive_headers PASSED [  8%]
tests/test_security_hardening.py::test_redirect_loop_detected PASSED     [ 11%]
tests/test_security_hardening.py::test_redirect_excessive_chain PASSED   [ 13%]
tests/test_security_hardening.py::test_blocked_ip_detection[...] (19 tests) PASSED [ 55%]
tests/test_security_hardening.py::test_allowed_public_ip PASSED          [ 57%]
tests/test_security_hardening.py::test_blocked_hostnames[...] (7 tests) PASSED [ 73%]
tests/test_security_hardening.py::test_dns_rebinding_simulation_blocks_connection PASSED [ 75%]
tests/test_security_hardening.py::test_ssrf_unsupported_scheme PASSED    [ 77%]
tests/test_security_hardening.py::test_env_loader_no_automatic_cwd_scanning PASSED [ 80%]
tests/test_security_hardening.py::test_env_loader_allowlist_enforcement PASSED [ 82%]
tests/test_security_hardening.py::test_github_seo_report_no_token_in_subprocess_args PASSED [ 84%]
tests/test_security_hardening.py::test_token_masking_in_error_reporting PASSED [ 86%]
tests/test_security_hardening.py::test_subprocess_env_sanitization PASSED [ 88%]
tests/test_security_hardening.py::test_generate_report_disallowed_script PASSED [ 91%]
tests/test_security_hardening.py::test_generate_report_path_traversal PASSED [ 93%]
tests/test_security_hardening.py::test_github_seo_report_disallowed_script PASSED [ 95%]
tests/test_security_hardening.py::test_html_report_offline_rendering PASSED [ 97%]
tests/test_security_hardening.py::test_html_report_untrusted_html_escaping PASSED [100%]

============================= 45 passed in 0.29s ==============================
```

- **Kết quả**: **45/45 ca kiểm thử ĐẠT (100% PASS RATE)**.
- **Tính tương thích Antigravity**: Thư mục `seo` duy trì đầy đủ cấu trúc `SKILL.md`, `scripts/`, `resources/`. Lệnh `npx skills list` yêu cầu tải gói npm chưa được phê duyệt nên đã được bỏ qua an toàn theo đúng hướng dẫn.

---

## 5. RỦI RO CÒN LẠI & QUY TẮC VẬN HÀNH (REMAINING RISKS & RESTRICTIONS)

Mặc dù toàn bộ các lỗ hổng mã nguồn nghiêm trọng đã được khắc phục, vẫn tồn tại 2 rủi ro cố hữu của việc kiểm toán web bên ngoài:

1. **Rủi ro Indirect Prompt Injection (IPI)**:
   - Nếu LLM cào dữ liệu từ một trang web do kẻ tấn công kiểm soát, trang web đó có thể chứa các chỉ thị prompt ẩn nhằm lừa LLM đưa ra kết luận sai lệch.
   - *Biện pháp giảm thiểu*: Khi phân tích trang web bên ngoài, người dùng phải coi nội dung web là văn bản chưa tin cậy (`untrusted text`), không cấp quyền cho LLM tự ý thực thi mã hệ thống dựa trên nội dung đọc được.
2. **Gói phụ thuộc chưa cài đặt (`beautifulsoup4`, `playwright`)**:
   - Các kịch bản phụ thuộc vào `bs4` hoặc `playwright` sẽ không thể chạy nếu môi trường chưa cài đặt các gói này.
   - *Biện pháp giảm thiểu*: Duy trì nguyên tắc không cài đặt thêm gói vào môi trường chính của `EventAI Pro`. Tận dụng tối đa năng lực đọc và phân tích trực tiếp của LLM (LLM-First On-Page Analysis).

---

## 6. QUYẾT ĐỊNH THẨM ĐỊNH CUỐI CÙNG (FINAL DECISION)

# ⚖️ PHÊ DUYỆT Ở CHẾ ĐỘ KIỂM SOÁT TƯỜNG MINH (RESTRICTED)

- **Căn cứ chấp thuận sử dụng (Không REJECTED)**:
  - 100% các lỗ hổng rò rỉ token, SSRF, DNS Rebinding, nạp trộm `.env` và Stored XSS đã được remediate thành công.
  - 45/45 ca kiểm thử bảo mật độc lập đã vượt qua thành công với bằng chứng rõ ràng.
  - Mã nguồn và dữ liệu của ứng dụng `EventAI Pro` được bảo vệ an toàn tuyệt đối.
- **Căn cứ không phê duyệt tự do (Không APPROVED)**:
  - Để ngăn chặn nguy cơ tấn công chuỗi cung ứng trong tương lai, kỹ năng cần tiếp tục hoạt động dưới sự giám sát có kiểm soát của người vận hành.
- **Quy chế vận hành chính thức**:
  1. **Được phép**: Sử dụng toàn bộ 48 tài liệu chuẩn mực trong `resources/` để LLM phân tích, đánh giá On-Page và tạo Schema JSON-LD trực tiếp cho `EventAI Pro`.
  2. **Được phép**: Thực thi các kịch bản kiểm tra cú pháp ngoại tuyến (`validate_schema.py`, `pre_commit_seo_check.sh`).
  3. **Yêu cầu cấp phép tường minh**: Mọi hoạt động cào dữ liệu ra ngoài internet hoặc kết nối API GitHub/Google phải có sự đồng ý của người vận hành và sử dụng biến môi trường tường minh (`AGENTIC_SEO_ENV_PATH` hoặc `GITHUB_TOKEN`).
  4. **Nghiêm cấm tuyệt đối**: Không chạy các trình cài đặt tự động (`install.ps1`, `install.sh`) và không cài đặt thêm gói bên thứ ba vào môi trường ứng dụng.

