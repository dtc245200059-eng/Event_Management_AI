# BÁO CÁO KIỂM TOÁN BẢO MẬT TĨNH — AGENTIC SEO SKILL

**Dự án đích:** `D:\Event_Management_AI`  
**Nguồn người dùng cung cấp:** `seo-skill-audit.zip` (bản sao thư mục cài đặt `.agents/skills/seo`)  
**Kho nguồn được khai báo:** `https://github.com/Bhanunamikaze/Agentic-SEO-Skill`  
**Phương pháp:** chỉ đọc các byte trong ZIP; phân tích tĩnh Python AST, PowerShell/Shell bằng cách đọc văn bản; không chạy mã của Skill, không cài phụ thuộc, không kết nối mạng, không đọc bất cứ file `.env` nào ngoài ZIP.  
**Kết luận cuối cùng:** **RESTRICTED — CHƯA CHO PHÉP CHẠY TỰ ĐỘNG / CHẠY CÓ TOKEN.** Một vài bộ phân tích dữ liệu cục bộ có thể được cân nhắc thử trong môi trường cách ly sau khi phê duyệt từng lệnh.

## 1. Thống kê và độ tin cậy

- ZIP có **190 mục**, trong đó **188 tệp có dữ liệu** và 2 mục thư mục/không có dữ liệu. Tổng kích thước giải nén theo metadata: **1,565,160 bytes**.
- **89 tệp `.py` ở cấp `scripts/`** (gồm 1 `__init__.py`, tức 88 tệp `.py` còn lại; README tự mô tả 89 scripts — đây là cách đếm chưa đối chiếu đầy đủ), **2 file Python hỗ trợ** tại `scripts/lib/`; **10** tài liệu tác tử, **16** tài liệu nhóm tác vụ con.
- **100 tệp Python** (bao gồm tests) đã được phân tích cú pháp tĩnh bằng `ast.parse`; **100/100 hợp lệ**, **không thực thi Python từ ZIP**.
- `SKILL.md` có frontmatter `name: seo` và `description` hợp lệ; tài liệu yêu cầu các luồng audit có thể tự chạy những script bổ trợ, nên **không cho Agent tự kích hoạt mặc định** trước khi giới hạn quyền.
- `pyproject.toml` báo **version 3.0.1**, Python >= 3.10, giấy phép **MIT**; phụ thuộc nền: BeautifulSoup4, lxml, requests. Tùy chọn: Google API SDK, Playwright, pytest/ruff. Không cài bất kỳ phụ thuộc nào trong lần kiểm toán.
- SHA-256 của ZIP: `0a35c2f08c63ac31784f516c2d0d460fa41551b3570e278e14d4abd8964fedaa`.
- **Không có lịch sử Git/commit ID trong ZIP**; vì vậy **chưa thể đối chiếu commit đã cài với một revision upstream đã ký/xác thực**.
- Các nhãn **Gen High Risk / Socket 1 alert / Snyk Medium Risk** là thông tin từ nhật ký cài đặt do người dùng đưa; ZIP **không chứa báo cáo chi tiết của ba scanner**. Do đó **chưa thể định danh chính xác alert gốc, cũng chưa thể kết luận chúng là false positive**.

## 2. Kết luận phân tích hành vi

- Không phát hiện `os.system`, `subprocess(..., shell=True)`, lệnh `eval()`/`exec()` thực thi tùy ý hay `verify=False` trong **mã Python ứng dụng của ZIP** qua việc rà soát các call site. Các kết quả tìm theo chuỗi `re.compile` không phải thực thi mã động. Một số bài test dùng `importlib.util.spec_from_file_location`/`exec_module` để nạp module cục bộ: đây vẫn là hành vi thực thi code nếu chạy test, nhưng **chưa chạy**.
- Có **những subprocess thực sự**: `generate_report.py`, `github_seo_report.py` chạy script Python con; `lighthouse_runner.py` gọi Lighthouse/Chromium; `github_api.py` gọi `gh` và `git`; `repo_release_seo.py` gọi `git` để đọc tag.
- Có **những lệnh yêu cầu mạng thực sự**: website crawling, PageSpeed Insights, GitHub API/CLI, Google Knowledge Graph/Search Console, Wikipedia/Wikidata, Google Suggestions, IndexNow; Playwright có thể truy cập bất kỳ trang/tài nguyên mạng mà browser tải.
- Có **đường đọc credentials được thiết kế công khai** (`scripts/env_loader.py`): tự động đọc `.env` từ thư mục hiện hành, root Skill và `$HOME/.agentic-seo/.env`, sau đó đưa mọi biến vào `os.environ`. `github_api.py` lấy `GITHUB_TOKEN`/`GH_TOKEN`; các script GSC có thể đọc đường dẫn tới JSON service account. Đây là quyền truy cập nhạy cảm, **không phải bằng chứng có chủ đích đánh cắp dữ liệu**.
- Có **ghi file** theo lựa chọn CLI hoặc mặc định: `fetch_page.py` (HTML), `generate_report.py`/`audit_runner.py` (HTML/MD), `github_seo_report.py` (Markdown/JSON), `github_traffic_archiver.py` (`.github-seo-data`), scripts sitemap/report/ảnh. Không coi đây là công cụ chỉ đọc khi vận hành thông thường.
- Installer `install.sh` và `install.ps1` có chế độ tải mã từ GitHub, cài pip/Playwright, chép/ghi đè tệp và dọn thư mục đích khi có các lựa chọn phù hợp. **Không dùng installer repo để kiểm toán hoặc vận hành SEO**, vì `npx skills` đã cài Skill.

## 3. Phát hiện cụ thể và mức độ rủi ro

### R-01 — HIGH: Token GitHub có thể đi theo redirect sang host khác

**Bằng chứng:** `scripts/github_api.py:176–185, 212–225` thêm `Authorization: Bearer <token>` vào header; `scripts/lib/safe_http.py:144–160, 181–191` tái sử dụng nguyên `request_headers` sau mỗi redirect; chuyển hướng chỉ kiểm tra IP nội bộ, **không chặn host ngoài danh sách hoặc xóa Authorization khi đổi origin**.

**Nguy cơ:** Nếu phản hồi URL được gọi có redirect liên miền tới host công khai khác, header chứa token có thể được gửi cho host mới. Đây là **lỗ hổng thiết kế xác nhận bằng mã nguồn**, nhưng chưa có bằng chứng từng xảy ra sự cố ngoài thực tế.

**Giảm thiểu:** Không cấp GitHub token/gh authenticated cho Skill lúc này. Vá `safe_request` để không chuyển header nhạy cảm khi đổi origin; với GitHub API, giới hạn host đích `api.github.com`, chặn redirect liên miền và giới hạn chặt `path`.

### R-02 — MEDIUM/HIGH (tùy môi trường): bảo vệ SSRF chưa hoàn chỉnh

**Bằng chứng:** `scripts/lib/safe_http.py:79–104` dùng `socket.getaddrinfo` kiểm tra IP, nhưng ở `:152–160` `requests` lại thực hiện DNS/kết nối theo tên host; không ghim IP đã kiểm tra, không phát hiện hostname sau DNS change ở thời điểm kết nối. `:91–94` vẫn trả về URL khi DNS lookup báo `socket.gaierror`. `requests.Session()` theo mặc định còn có thể sử dụng proxy từ môi trường.

**Nguy cơ:** DNS rebinding / thay đổi kết quả DNS / proxy có thể khiến ràng buộc ban đầu không còn bảo đảm; trình duyệt Playwright gọi `page.goto` tại `capture_screenshot.py`, `analyze_visual.py`, `javascript_render_audit.py`, `mobile_render_checker.py`, `visual_regression_snapshot.py` mà không dùng `safe_http.py` để chặn mạng nội bộ.

**Giảm thiểu:** Cấm quét URL chưa tin cậy hoặc hệ thống nội bộ; chỉ chạy trong sandbox với egress allowlist, không có quyền truy cập mạng nội bộ/metadata/credential; kiểm thử bảo vệ SSRF trên môi trường riêng trước khi cấp quyền mạng.

### R-03 — MEDIUM: đọc `.env` từ workspace/nhà người dùng, quyền rộng

**Bằng chứng:** `scripts/env_loader.py:31–45, 78–94, 97–129` tự nạp mọi biến từ `.env`; `scripts/github_api.py:32–45` kích hoạt loader khi xử lý GitHub token. `.env.example` có hướng dẫn `PAGESPEED_API_KEY`, `GOOGLE_KG_API_KEY`, `GITHUB_TOKEN`, `GSC_CREDENTIALS_PATH`.

**Nguy cơ:** Skill có thể truy cập thông tin cấu hình vượt nhu cầu SEO, kể cả secrets của ứng dụng khi chạy từ project root. Không có bằng chứng script cố ý thu thập toàn bộ tệp `.env` và gửi đi; nhưng việc đưa tất cả biến vào môi trường tiến trình làm tăng bề mặt rò rỉ.

**Giảm thiểu:** Chạy từ thư mục sandbox **không chứa** `.env`; không sao chép secrets sang đó; dùng token hạn chế quyền nếu có bước bắt buộc cần GitHub API; trước đó ưu tiên audit offline không token.

### R-04 — MEDIUM: truyền token cho tiến trình con bằng đối số CLI

**Bằng chứng:** `scripts/github_seo_report.py:161–172` tạo `common = ... + ['--token', token]`; `:45–59` gọi các script con bằng `subprocess.run`. Các đối số tiến trình có thể bị quan sát thông qua danh sách process trong một số môi trường.

**Giảm thiểu:** Không dùng `--token`, không chạy bộ `github_seo_report.py` với credential cho đến khi sửa thành cách truyền token an toàn, có kiểm soát.

### R-05 — MEDIUM: mạng và ghi file tự động theo luồng full audit

**Bằng chứng:** `SKILL.md` khuyến nghị chạy nhiều script khi full audit; `scripts/generate_report.py:83–99` gọi script con, `:104–113` tải HTML vào temp file; `github_traffic_archiver.py:133–161` mặc định lưu traffic history trừ `--no-write`; `indexnow_checker.py:133–164` có thể **POST** URL tới máy tìm kiếm (chỉ khi người dùng bật ping).

**Giảm thiểu:** Cấm chế độ full audit tự động, GitHub traffic archival, IndexNow ping, crawler rộng, browser-based crawling; hạn chế mọi đường ghi kết quả vào thư mục báo cáo đã phê duyệt.

### R-06 — LOW/MEDIUM: báo cáo HTML tạo kết nối tới Google Fonts khi mở

**Bằng chứng:** `scripts/generate_report.py:1294–1296` chứa CSS link `fonts.googleapis.com` và `fonts.gstatic.com`. Đây không phải bằng chứng tống xuất secrets, nhưng mở report khi đang online có thể gửi request/metadata đến bên thứ ba.

**Giảm thiểu:** dùng font hệ thống, không mở HTML report nhạy cảm khi có mạng, hoặc loại bỏ external font links trước khi phân phối.

### R-07 — UNRESOLVED: cảnh báo Gen/Socket/Snyk và tính toàn vẹn nguồn

**Bằng chứng:** chỉ có nhãn High Risk/1 alert/Medium Risk từ CLI; không có chi tiết finding / CVE / dependency tree / revision. Không có `.git` để đối chiếu lịch sử hoặc commit. Mã nguồn có giấy phép MIT, test, và security policy, nhưng các tín hiệu này **không phải chứng nhận mã an toàn**.

**Giảm thiểu:** Xuất đầy đủ báo cáo của Gen/Socket/Snyk từ trang kiểm tra; so sánh SHA-256 của bản đã cài với bản upstream đã khóa commit; phân loại từng cảnh báo từ bằng chứng chi tiết trước khi nâng mức phê duyệt.

## 4. Kiểm tra khả năng nghi vấn mã độc / exfiltration

**Không tìm thấy bằng chứng trực tiếp** về một endpoint bí mật chuyên thu thập dữ liệu hoặc đoạn mã tự ý gửi toàn bộ files/secrets đến một domain ngoài mục đích SEO trong những tệp đã đọc. Những nơi dùng mạng được liệt kê trong chính code và phần lớn khớp chức năng: `api.github.com`, Google APIs, `kgsearch.googleapis.com`, `www.wikidata.org`, `en.wikipedia.org`, các máy chủ IndexNow, các URL website/đối thủ do người vận hành cung cấp; script report tham chiếu Google Fonts.

**Giới hạn:** Đây là kiểm toán tĩnh; không thực thi dependency, không chụp packet, không chứng minh không có side effect runtime. Phần lớn script phụ thuộc thư viện bên ngoài nên chưa thể khẳng định an toàn toàn hệ thống.

## 5. Danh sách chạy hạn chế đề xuất (CHƯA PHẢI PHÊ DUYỆT TỰ ĐỘNG)

| Script | Điều kiện nếu muốn thử nghiệm | Quyết định |
|---|---|---|
| `validate_schema.py` | Chỉ file HTML mẫu **không chứa secrets**; script chỉ đọc nội dung cục bộ, kiểm tra JSON-LD, không tải mạng | Có thể cho thử **sau khi phê duyệt cụ thể** |
| `finding_verifier.py` | JSON input do người dùng chuẩn bị, không chứa private data; không nhập URL; stdout/file output trong sandbox | Có thể cho thử sau khi phê duyệt cụ thể |
| `validate_skill_inventory.py` | Chạy ở thư mục sao chép Skill cô lập, chỉ để đối chiếu danh sách SKILL/README; không cần mạng | Có thể cho thử sau khi phê duyệt cụ thể |
| `parse_html.py` | **Chỉ** dùng chế độ tệp HTML đã sao chép vào sandbox; **cấm `--fetch`**; không dùng session/secret | Hạn chế, chỉ cho thử sau khi phê duyệt cụ thể |
| `readability.py` | Chỉ truyền tệp HTML local, **không dùng `--url`**; phụ thuộc kiểm tra trước | Hạn chế, chỉ cho thử sau khi phê duyệt cụ thể |
| `fetch_page.py`, `robots_checker.py`, `sitemap_checker.py`, `pagespeed.py`, `broken_links.py` | Các luồng có egress/crawl, có thể tải site ngoài và gây lộ metadata | **Chưa duyệt** |
| `generate_report.py`, `audit_runner.py`, `github_seo_report.py`, `github_traffic_archiver.py` | Gọi nhiều script, ghi file, đọc token/có mạng | **Chưa duyệt** |
| `indexnow_checker.py` | Có chức năng POST/ping tới bên thứ ba | **Chưa duyệt** |
| `capture_screenshot.py`, `analyze_visual.py`, `javascript_render_audit.py` và script Playwright khác | Browser có thể mở URL và request mạng ngoài | **Chưa duyệt** |
| `install.sh`, `install.ps1` | Tải mã, cài phụ thuộc, tạo/ghi đè và dọn file | **Không chạy lại** |

**Danh sách trên được rút ra từ đường thực thi và import được quan sát; vẫn phải xem dòng lệnh chính xác trước khi thử.**

## 6. Đề xuất áp dụng cho EventAI Pro

1. Giữ `.agents/skills/seo` nhưng **không tự động kích hoạt workflow** của `SKILL.md` khi chưa được phê duyệt.
2. Nếu cần audit trước, ưu tiên **đọc tĩnh** các Flask templates công khai và cấu trúc route bằng Agent đã tin cậy hoặc bộ công cụ SEO offline không chạy script bên thứ ba.
3. Không cho scan admin, hồ sơ tài khoản, vé/QR cá nhân, dữ liệu check-in, API nội bộ hoặc `.env`; tránh bất kỳ URL chứa access token hoặc session.
4. Vá/đổi cách xử lý redirect token và DNS SSRF trước khi cho phép crawler có quyền mạng; với Playwright cần network isolation riêng.
5. Chỉ khi audit an toàn mới triển khai SEO cho trang chủ, danh sách sự kiện, chi tiết sự kiện công khai: metadata/canonical, `Event` JSON-LD, sitemap, robots, accessibility, tốc độ mobile.
6. Không thêm quyền Github token, GSC service account hoặc Google Cloud credentials vào Skill ở giai đoạn này.

## 7. Đánh giá rủi ro và hạn chế xác minh

| Lĩnh vực | Trạng thái |
|---|---|
| Đã kiểm tra inventory ZIP | **VERIFIED** |
| YAML `SKILL.md` name/description | **VERIFIED** |
| Python AST syntax (100 tệp) | **VERIFIED — không chạy** |
| Giấy phép và dependencies theo bản copy | **VERIFIED FROM ARCHIVE** |
| Không có bằng chứng exfiltration chủ đích | **NOT OBSERVED STATICALLY**, không phải chứng nhận an toàn |
| Gen High Risk / Socket alert / Snyk Med | **REPORTED ONLY — chi tiết chưa có** |
| Commit upstream trùng bản cài | **UNVERIFIED** |
| Existing custom Skills không bị ghi đè | **UNVERIFIED** — chỉ nhận ZIP SEO, không có snapshot các thư mục khác |
| Kiểm tra runtime/sandbox/netflow | **NOT RUN** theo ràng buộc READ-ONLY |

**QUYẾT ĐỊNH: RESTRICTED.** Không dùng trực tiếp `seo audit <url>` với toàn quyền trong Antigravity; chỉ được cân nhắc chức năng local sau khi kiểm tra lại từng lệnh trong môi trường hạn chế. Chưa đủ chứng cứ để gán nhãn `REJECTED` cho toàn bộ repository và chưa đủ căn cứ để `APPROVED`.

---

## Phụ lục A — Toàn bộ 188 tệp có nội dung trong ZIP

> Tên dưới đây chuẩn hóa dấu `\` của ZIP Windows thành `/`. Những thư mục thực tế được liệt kê ở phụ lục này dưới dạng đường dẫn của các tệp con; không có nội dung tệp bí mật từ máy người dùng được sao chép.

- `seo/.env.example`
- `seo/.gitignore`
- `seo/CHANGELOG.md`
- `seo/CITATION.cff`
- `seo/CODE_OF_CONDUCT.md`
- `seo/CONTRIBUTING.md`
- `seo/improvements.md`
- `seo/install.ps1`
- `seo/install.sh`
- `seo/LICENSE`
- `seo/pyproject.toml`
- `seo/README.md`
- `seo/requirements.txt`
- `seo/SECURITY.md`
- `seo/SKILL.md`
- `seo/SUPPORT.md`
- `seo/.github/CODEOWNERS`
- `seo/.github/dependabot.yml`
- `seo/.github/pull_request_template.md`
- `seo/.github/ISSUE_TEMPLATE/bug_report.md`
- `seo/.github/ISSUE_TEMPLATE/feature_request.md`
- `seo/.github/workflows/ci.yml`
- `seo/.github/workflows/package-on-tag.yml`
- `seo/docs/images/example-prompt-output.png`
- `seo/docs/images/report-dashboard.png`
- `seo/resources/agents/seo-content.md`
- `seo/resources/agents/seo-github-analyst.md`
- `seo/resources/agents/seo-github-benchmark.md`
- `seo/resources/agents/seo-github-data.md`
- `seo/resources/agents/seo-performance.md`
- `seo/resources/agents/seo-schema.md`
- `seo/resources/agents/seo-sitemap.md`
- `seo/resources/agents/seo-technical.md`
- `seo/resources/agents/seo-verifier.md`
- `seo/resources/agents/seo-visual.md`
- `seo/resources/config/scoring.json`
- `seo/resources/references/cwv-thresholds.md`
- `seo/resources/references/eeat-framework.md`
- `seo/resources/references/github-api-ops.md`
- `seo/resources/references/github-ranking-factors.md`
- `seo/resources/references/google-seo-reference.md`
- `seo/resources/references/link-building.md`
- `seo/resources/references/llm-audit-rubric.md`
- `seo/resources/references/quality-gates.md`
- `seo/resources/references/readme-audit-rubric.md`
- `seo/resources/references/schema-types.md`
- `seo/resources/schema/templates.json`
- `seo/resources/skills/seo-aeo.md`
- `seo/resources/skills/seo-article.md`
- `seo/resources/skills/seo-audit.md`
- `seo/resources/skills/seo-competitor-pages.md`
- `seo/resources/skills/seo-content.md`
- `seo/resources/skills/seo-geo.md`
- `seo/resources/skills/seo-github.md`
- `seo/resources/skills/seo-hreflang.md`
- `seo/resources/skills/seo-images.md`
- `seo/resources/skills/seo-links.md`
- `seo/resources/skills/seo-page.md`
- `seo/resources/skills/seo-plan.md`
- `seo/resources/skills/seo-programmatic.md`
- `seo/resources/skills/seo-schema.md`
- `seo/resources/skills/seo-sitemap.md`
- `seo/resources/skills/seo-technical.md`
- `seo/resources/templates/agency.md`
- `seo/resources/templates/blog-post.md`
- `seo/resources/templates/ecommerce.md`
- `seo/resources/templates/generic.md`
- `seo/resources/templates/github-seo-report.md`
- `seo/resources/templates/github-weekly-scorecard.md`
- `seo/resources/templates/local-service.md`
- `seo/resources/templates/news-article.md`
- `seo/resources/templates/publisher.md`
- `seo/resources/templates/saas.md`
- `seo/resources/templates/technical-article.md`
- `seo/scripts/a11y_seo_checker.py`
- `seo/scripts/ai_crawler_policy_matrix.py`
- `seo/scripts/analyze_visual.py`
- `seo/scripts/anchor_text_audit.py`
- `seo/scripts/answer_block_scanner.py`
- `seo/scripts/article_seo.py`
- `seo/scripts/audit_runner.py`
- `seo/scripts/broken_links.py`
- `seo/scripts/cache_compression_checker.py`
- `seo/scripts/canonical_checker.py`
- `seo/scripts/capture_screenshot.py`
- `seo/scripts/citation_readiness.py`
- `seo/scripts/collection_page_checker.py`
- `seo/scripts/competitor_gap.py`
- `seo/scripts/content_decay_detector.py`
- `seo/scripts/content_intent_matcher.py`
- `seo/scripts/crawl_audit.py`
- `seo/scripts/critical_request_chain.py`
- `seo/scripts/duplicate_content.py`
- `seo/scripts/eeat_signal_checker.py`
- `seo/scripts/entity_checker.py`
- `seo/scripts/env_loader.py`
- `seo/scripts/external_link_quality.py`
- `seo/scripts/faceted_nav_audit.py`
- `seo/scripts/fetch_page.py`
- `seo/scripts/finding_verifier.py`
- `seo/scripts/font_audit.py`
- `seo/scripts/freshness_checker.py`
- `seo/scripts/generate_report.py`
- `seo/scripts/github_api.py`
- `seo/scripts/github_community_health.py`
- `seo/scripts/github_competitor_research.py`
- `seo/scripts/github_readme_lint.py`
- `seo/scripts/github_repo_audit.py`
- `seo/scripts/github_search_benchmark.py`
- `seo/scripts/github_seo_report.py`
- `seo/scripts/github_traffic_archiver.py`
- `seo/scripts/github_weekly_scorecard.py`
- `seo/scripts/gsc_checker.py`
- `seo/scripts/hreflang_checker.py`
- `seo/scripts/hreflang_sitemap_validator.py`
- `seo/scripts/image_inventory.py`
- `seo/scripts/image_weight_audit.py`
- `seo/scripts/indexability_matrix.py`
- `seo/scripts/indexnow_checker.py`
- `seo/scripts/internal_links.py`
- `seo/scripts/javascript_render_audit.py`
- `seo/scripts/lcp_subparts.py`
- `seo/scripts/lighthouse_runner.py`
- `seo/scripts/link_profile.py`
- `seo/scripts/llms_txt_checker.py`
- `seo/scripts/llms_txt_generator.py`
- `seo/scripts/local_seo_checker.py`
- `seo/scripts/log_file_analyzer.py`
- `seo/scripts/mobile_render_checker.py`
- `seo/scripts/orphan_pages_from_sitemap.py`
- `seo/scripts/pagespeed.py`
- `seo/scripts/parse_html.py`
- `seo/scripts/pre_commit_seo_check.sh`
- `seo/scripts/product_schema_checker.py`
- `seo/scripts/readability.py`
- `seo/scripts/redirect_backlink_reclaim.py`
- `seo/scripts/redirect_checker.py`
- `seo/scripts/reference_freshness.py`
- `seo/scripts/repo_docs_site_checker.py`
- `seo/scripts/repo_file_inventory.py`
- `seo/scripts/repo_release_seo.py`
- `seo/scripts/repo_social_preview_checker.py`
- `seo/scripts/repo_topic_suggester.py`
- `seo/scripts/review_schema_checker.py`
- `seo/scripts/rich_results_guard.py`
- `seo/scripts/robots_checker.py`
- `seo/scripts/robots_path_tester.py`
- `seo/scripts/schema_diff.py`
- `seo/scripts/schema_required_props.py`
- `seo/scripts/schema_template_generator.py`
- `seo/scripts/security_headers.py`
- `seo/scripts/seo_common.py`
- `seo/scripts/sitemap_checker.py`
- `seo/scripts/sitemap_generator.py`
- `seo/scripts/social_meta.py`
- `seo/scripts/third_party_script_audit.py`
- `seo/scripts/topical_cluster_mapper.py`
- `seo/scripts/url_quality.py`
- `seo/scripts/validate_schema.py`
- `seo/scripts/validate_skill_inventory.py`
- `seo/scripts/video_schema_checker.py`
- `seo/scripts/visual_regression_snapshot.py`
- `seo/scripts/x_robots_header_checker.py`
- `seo/scripts/__init__.py`
- `seo/scripts/lib/safe_http.py`
- `seo/scripts/lib/__init__.py`
- `seo/tests/test_content_ai_scripts.py`
- `seo/tests/test_core_seo_scripts.py`
- `seo/tests/test_duplicate_content.py`
- `seo/tests/test_link_and_github_depth_scripts.py`
- `seo/tests/test_pagespeed.py`
- `seo/tests/test_performance_scripts.py`
- `seo/tests/test_readability.py`
- `seo/tests/test_reporting.py`
- `seo/tests/test_schema_local_ecommerce_scripts.py`
- `seo/tests/fixtures/pagespeed_field_data.json`
- `seo/tests/fixtures/pagespeed_lab_data.json`
- `seo/tests/fixtures/report_data.json`
- `seo/wiki/Audit-Workflow.md`
- `seo/wiki/Command-Reference.md`
- `seo/wiki/Example-Prompts.md`
- `seo/wiki/Home.md`
- `seo/wiki/Installation.md`
- `seo/wiki/Release-and-Packaging.md`
- `seo/wiki/Reports-and-Outputs.md`
- `seo/wiki/Script-Inventory.md`
- `seo/wiki/Troubleshooting.md`
- `seo/wiki/_Sidebar.md`
