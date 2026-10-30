# BÁO CÁO KIỂM KÊ THAY ĐỔI MÃ NGUỒN (CHANGE INVENTORY)
## KỸ NĂNG: AGENTIC SEO SKILL (`.agents/skills/seo`)

---

- **Dự án**: `EventAI Pro` (`D:\Event_Management_AI`)
- **Đối tượng**: Kỹ năng Agentic SEO (`.agents/skills/seo`)
- **Vị trí lưu trữ bản sao lưu độc lập (Standalone Backup)**:
  `D:\EventAI_Security_Backups\seo-skill-before-hardening`
- **Mã băm lưu trữ bản sao lưu gốc**: Đã đối chiếu 188/188 tệp khớp 100% SHA-256 (`seo-baseline-hashes.xml`).
- **Thời điểm hoàn thành gia cố**: Ngày 29 tháng 10 năm 2026

---

## 1. TỔNG QUAN PHẠM VI THAY ĐỔI

Mọi sửa đổi đều được kiểm soát nghiêm ngặt và giới hạn tuyệt đối bên trong:
- Thư mục kỹ năng: `D:\Event_Management_AI\.agents\skills\seo\`
- Thư mục tài liệu bảo mật: `D:\Event_Management_AI\docs\seo\`

**TUYỆT ĐỐI KHÔNG CÓ THAY ĐỔI NÀO NGOÀI PHẠM VI:**
- Mã nguồn ứng dụng Flask (`app/`), routes, views, models, templates, CSS, JS: **NGUYÊN VẸN 100%**.
- 39 kỹ năng nội bộ khác trong `.agents/skills/`: **NGUYÊN VẸN 100%**.
- Cơ sở dữ liệu SQLite, file migrations: **NGUYÊN VẸN 100%**.
- Tài liệu học thuật (`tailieu/`), file Word (`.docx`), file PowerPoint (`.pptx`): **NGUYÊN VẸN 100%**.

---

## 2. BẢNG ĐỐI CHIẾU MÃ BĂM SHA-256 TRƯỚC VÀ SAU KHI GIA CỐ (BEFORE & AFTER HASHES)

| STT | Trạng thái | Tệp thay đổi | SHA-256 Trước gia cố (Baseline) | SHA-256 Sau gia cố (Hardened) | Mục đích thay đổi kỹ thuật |
|:---:|:---:|:---|:---|:---|:---|
| 1 | MODIFIED | `SKILL.md` | `A274EAF6A1562D497E5F23DE7836108F864337320FF3544276226889AAE4FF8A` | `8AF8E862BF3962DA24C3BAE63C3F8F5772CC1FCDDA32D2099A88CA7732EEA90A` | Cập nhật quy chế an toàn: cấm quét `.env` tự động, bổ sung Rule 14 về rào chắn SSRF và thực thi offline. |
| 2 | MODIFIED | `install.ps1` | `B55FAB745AD3A0E0E05331C85E4F3B56B24DA2E70CECDA08847716138E333ECE` | `B83C9FF1A804D6509A7279E7AE523BCA692240759745DCF5667831EAA4021F4E` | Vô hiệu hóa chế độ tải zip từ xa không xác thực (`--online`) nếu thiếu biến môi trường cho phép tường minh. |
| 3 | MODIFIED | `install.sh` | `B40FE9501A7295D6DDB55A3BF8F50184FFF42F2A80D9F92F507834444EAEBC96` | `9FCE7D4ED67B115A876D56D561D9F8AEC314892ACE756AA9D141985AB2BBFFB4` | Khóa chế độ `--online` tải tệp nén từ GitHub nếu chưa được quản trị viên cấp phép tường minh. |
| 4 | MODIFIED | `scripts/lib/safe_http.py` | `85235FC83E69C8149B71E9820F6E3A4BAE9908CB7337FEA68F8D478E8BC82509` | `5F26691CFF97A657ED3776B3112C79EFC894C08B24797541FED37E681E83ADE4` | Tích hợp `SafeAdapter` kết nối socket trực tiếp tới IP đã xác thực (chống DNS Rebinding); tước bỏ header nhạy cảm khi chuyển hướng chéo miền; chặn hạ cấp HTTPS->HTTP; phát hiện vòng lặp redirect. |
| 5 | MODIFIED | `scripts/env_loader.py` | `0ADC5AED692D6DB2AE54C1A946CF0FFB8E5D65AB4AEE5DC16F4B01A286324FDC` | `EDEFFF4978EA63DC6914D94C5C8BC02F18ADE821AA9517E2D61DB9FD0567F2FE` | Xóa bỏ quét tự động `cwd/.env` và thư mục cha; thiết lập danh sách cho phép nghiêm ngặt `ALLOWED_SEO_KEYS`; ngăn ngừa thu thập bí mật ứng dụng EventAI Pro. |
| 6 | MODIFIED | `scripts/pagespeed.py` | `BACD0A3E47D0E63E9700ACD2E1295BF572804E0EF2A2E8B5F856959D3F7D92A6` | `373EEA6A1B9F49C39250A48603032A60CA82643A5FE9C93B7AC487AE189E35E5` | Xóa bỏ cơ chế tự động lấy `GOOGLE_API_KEY` (Gemini API key của ứng dụng) gửi lên query parameter của PageSpeed API. |
| 7 | MODIFIED | `scripts/entity_checker.py` | `14EC84D9136A2A149C6F6C67708CC995DDFE93306F83C9226452BAAD7912C58B` | `E57468425EE97F5771391DE51B7644E0A03F4CD9F953817939ABF5FC86994A7A` | Xóa bỏ fallback tự lấy `GOOGLE_API_KEY` của ứng dụng gửi ra Knowledge Graph API. |
| 8 | MODIFIED | `scripts/github_seo_report.py` | `B930B9DF28F91C32C529FF31E03D67F4B89DEC6AB5DA2C1EDBAA3F45E3E2FCD2` | `F1C2E42DBD369465424291B45D687CB04D2DB447554375E1F48912578C259542` | Loại bỏ việc truyền `--token <secret>` qua tham số dòng lệnh CLI; chuyển token qua biến môi trường con cách ly; làm sạch môi trường tiến trình con; che giấu token trong thông báo lỗi. |
| 9 | MODIFIED | `scripts/generate_report.py` | `40006377E227BD9CCF8B2931EC4D54BFC326EFA1BDEB660561792060041372AB` | `9C6D6FF0A0C01A591E7858A86C211BAB341C5709D0104EDC55326A8E8A2ADE01` | Rào chắn danh sách kịch bản được phép thực thi (`ALLOWED_REPORT_SCRIPTS`); làm sạch môi trường tiến trình con; gỡ bỏ liên kết Google Fonts CDN ngoài; escape HTML chống XSS toàn bộ trường dữ liệu đầu vào. |
| 10 | MODIFIED | `scripts/analyze_visual.py` | `AD52CC8D94A20D09A8AAE4E992C8FCA3BDA0952EB74D541E4C8291E648AA9415` | `CA2C82C797598535A8520239D7F451A9D0EC6CDA6FE76BADB552A9131C11C93D` | Chuẩn hóa rào chắn URL qua `assert_safe_url` trước khi khởi tạo ngữ cảnh Playwright. |
| 11 | MODIFIED | `scripts/capture_screenshot.py` | `1E3B4B150642613B6EEF9957E9ED7F0CF730F93C2AC4C0AFC84E468B74C8A1BD` | `C54A17878F89457870C27259F14001CFD17475E7D55546D9FF7464C981FCB7CB` | Bổ sung kiểm tra `assert_safe_url` ngăn chặn Playwright mở các địa chỉ loopback/metadata. |
| 12 | MODIFIED | `scripts/javascript_render_audit.py` | `EFF7BD37F8510A25BC8C62959B6CBE8D2DC549874692864238B71B5E58EC0998` | `A3FDE73F79C096303FA87414E86B32FAD46DFE4C49D15FC733628C22FFE28167` | Bổ sung kiểm tra `assert_safe_url` ngăn chặn Playwright render tài nguyên nội bộ. |
| 13 | MODIFIED | `scripts/mobile_render_checker.py` | `C42B4E8E87F3226F528E63CB6802CA791D3982F70E1B2A600C18668FA6E787E8` | `7CDACC6EB94296F25FE0C6E69F57604D3C26CDCFF24E92EF271DEAB3E3D78A46` | Bổ sung kiểm tra `assert_safe_url` trước khi chạy mobile viewport render. |
| 14 | MODIFIED | `scripts/visual_regression_snapshot.py` | `130F647186A81660A72681595C1A8AA4072F71C45E1EE08720C11C1D0940334B` | `5C076588B65B8136DC282EBCA881EEAA2859F399A2399C257CED8B8166939673` | Bổ sung kiểm tra `assert_safe_url` ngăn chặn snapshot các URL nội bộ. |
| 15 | **NEW** | `tests/test_security_hardening.py` | *NONE (Tệp mới)* | `8EAE1ED4EE884954CFDC181EC29DAFE3292D765A016DAEC29CC69412ED1C0562` | Bộ 45 ca kiểm thử hồi quy bảo mật độc lập, chạy offline 100%, kiểm chứng mọi rào chắn bảo vệ. |

---

## 3. TỔNG KẾT THAY ĐỔI
- **Tổng số tệp được sửa đổi (Modified)**: 14 tệp
- **Tổng số tệp tạo mới (New)**: 1 tệp kiểm thử (`tests/test_security_hardening.py`)
- **Tổng số tệp giữ nguyên không đổi**: 174 tệp
- **Tỷ lệ ảnh hưởng mã nguồn kỹ năng**: ~7.9% số tệp (tập trung chính xác vào các điểm nóng bảo mật mạng và nạp cấu hình)
- **Tác động lên mã nguồn ứng dụng**: **0% (Hoàn toàn cách ly)**

