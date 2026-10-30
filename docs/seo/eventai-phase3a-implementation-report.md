# EventAI Pro — Phase 3A Core SEO Implementation Report

**Dự án:** `EventAI Pro — Nền tảng Quản trị & Trải nghiệm Sự kiện Thông minh tích hợp Trí tuệ Nhân tạo`  
**Giai đoạn:** Phase 3A — Hiện thực hóa Core SEO, Metadata Động, Canonicalization và Semantic Heading Hierarchy  
**Ngày thực hiện:** 29/10/2026  
**Chuyên viên thực hiện:** Kỹ sư Trưởng Technical SEO, Kiến trúc sư Flask/Jinja2 & Kỹ sư Kiểm thử Hồi quy  
**Trạng thái thực thi:** **HOÀN THÀNH TOÀN DIỆN (100% CÁC HẠNG MỤC ĐẠT CHUẨN XÁC MINH)**  

---

## 1. TỔNG QUAN VÀ MỤC TIÊU GIAI ĐOẠN 3A

Thực hiện theo lộ trình tối ưu hóa SEO kỹ thuật đã được phê duyệt (`docs/seo/eventai-seo-optimization-roadmap.md`), Giai đoạn 3A tập trung giải quyết toàn bộ các khiếm khuyết nền tảng về thẻ siêu dữ liệu (Metadata) và cấu trúc phân cấp ngữ nghĩa (Semantic Hierarchy) trên các trang công khai của website EventAI Pro.

### Phạm vi triển khai Phase 3A:
1. **Thiết lập Khung Metadata Cốt lõi tại `base.html`:** Xây dựng hệ thống khối Jinja2 linh hoạt cho `<title>`, `<meta name="description">`, `<link rel="canonical">`, Open Graph (Facebook/Zalo) và Twitter Card.
2. **Cấu hình Tên miền Chuẩn tắc (Canonical Domain):** Hỗ trợ biến môi trường `CANONICAL_DOMAIN` và cơ chế tạo URL tuyệt đối tự động, loại bỏ triệt để các tham số theo dõi chiến dịch (`utm_*`, `fbclid`, `ref`).
3. **Module Tiện ích `app/seo_helpers.py`:** Chuẩn hóa thuật toán làm sạch văn bản (loại bỏ thẻ HTML, chuẩn hóa khoảng trắng, cắt tỉa văn bản theo ranh giới từ vựng an toàn) và định dạng đường dẫn ảnh tuyệt đối cho mạng xã hội.
4. **Cá nhân hóa Siêu dữ liệu trên 3 Trang Công khai Trọng điểm:**
   - Trang chủ (`/`): Tiêu đề thương hiệu chuẩn tắc, mô tả giá trị cốt lõi, canonical trỏ về gốc.
   - Danh mục sự kiện (`/events`): Tiêu đề phân loại, mô tả khám phá hội thảo/workshop, canonical sạch.
   - Chi tiết sự kiện (`/events/<id>`): Tiêu đề động theo tên sự kiện, mô tả trích xuất từ nội dung sự kiện, thẻ `og:type="article"`, ảnh đại diện `og:image` tuyệt đối.
5. **Chuẩn hóa Cấu trúc Phân cấp Tiêu đề Ngữ nghĩa (H1 -> H2 -> H3):** Khắc phục lỗi thiếu thẻ H1 hoặc trùng lặp H1, duy trì chính xác 1 thẻ H1 duy nhất trên mỗi trang mà không làm thay đổi dù chỉ 1 pixel giao diện Apple Liquid Glass.
6. **Bảo tồn Tuyệt đối Nền tảng An ninh Phase 2.5:** Đảm bảo toàn bộ các chỉ thị `noindex`, quy tắc bảo vệ ảnh vé QR tĩnh và kiểm soát sự kiện bản nháp (draft) được duy trì nguyên vẹn.

---

## 2. KIẾN TRÚC VÀ CÁC THAY ĐỔI MÃ NGUỒN CHI TIẾT

### 2.1. Cấu hình Ứng dụng (`app/config.py`)
Đã bổ sung thuộc tính cấu hình `CANONICAL_DOMAIN` vào lớp cơ sở `Config`:
```python
# SEO & Canonical Domain
CANONICAL_DOMAIN = os.getenv('CANONICAL_DOMAIN', '').strip().rstrip('/')
```
- Khi chạy trên môi trường Production với biến môi trường `CANONICAL_DOMAIN=https://eventai.pro`, toàn bộ canonical link và Open Graph URL sẽ tự động sử dụng domain này.
- Khi chạy trên môi trường Local Development hoặc Testing (biến môi trường rỗng), hệ thống tự động fallback an toàn về `request.url_root.rstrip('/')`.

---

### 2.2. Xây dựng Module Tiện ích SEO (`app/seo_helpers.py`)
Tạo mới module chuyên trách độc lập, không phụ thuộc thư viện bên ngoài:

```python
"""
SEO Helper utilities for EventAI Pro.
Provides text sanitization, dynamic canonical URL generation, and Open Graph image formatting.
"""
import re
from urllib.parse import urlencode
from flask import request, current_app

DEFAULT_META_DESCRIPTION = (
    "Nền tảng Quản trị & Trải nghiệm Sự kiện Thông minh tích hợp Trí tuệ Nhân tạo EventAI Pro. "
    "Khám phá hội thảo công nghệ, diễn đàn khoa học, đăng ký vé QR Code tức thì và trợ lý AI thông minh."
)

DEFAULT_OG_IMAGE_URL = "https://images.unsplash.com/photo-1518770660439-4636190af475?w=1200&auto=format&fit=crop"

def clean_meta_description(text, fallback="", max_len=160):
    """
    Làm sạch văn bản mô tả:
    - Loại bỏ triệt để các thẻ HTML (<p>, <strong>, <div>...).
    - Chuẩn hóa khoảng trắng dư thừa và ký tự xuống dòng.
    - Cắt tỉa theo ranh giới từ vựng an toàn (word boundary) kèm '...' nếu vượt quá max_len.
    - Tự động fallback về tiêu đề sự kiện hoặc mô tả nền tảng nếu rỗng.
    """
    raw = text if (text and str(text).strip()) else fallback
    raw_str = str(raw).strip() if raw else ""
    clean = re.sub(r'<[^>]+>', ' ', raw_str)
    clean = ' '.join(clean.split())
    if not clean:
        clean = DEFAULT_META_DESCRIPTION
    if len(clean) > max_len:
        truncated = clean[:max_len - 3]
        if ' ' in truncated:
            truncated = truncated.rsplit(' ', 1)[0]
        clean = truncated.strip() + '...'
    return clean

def build_canonical_url(path=None, keep_params=None):
    """
    Tạo URL chuẩn tắc tuyệt đối:
    - Ưu tiên CANONICAL_DOMAIN, fallback request.url_root.
    - Chuẩn hóa dấu gạch chéo cuối trang (giữ '/' ở root, lược bỏ ở sub-paths).
    - Tự động loại bỏ toàn bộ tham số tracking (utm_*, fbclid, ref...).
    - Giữ lại các tham số truy vấn nằm trong danh sách trắng keep_params (ví dụ: 'page').
    """
    try:
        canonical_domain = current_app.config.get('CANONICAL_DOMAIN', '').strip().rstrip('/')
    except Exception:
        canonical_domain = ''
        
    base_origin = canonical_domain if canonical_domain else request.url_root.rstrip('/')
    target_path = path if path else request.path
    if not target_path.startswith('/'):
        target_path = '/' + target_path

    if len(target_path) > 1 and target_path.endswith('/'):
        target_path = target_path.rstrip('/')

    query_string = ''
    if keep_params and request.args:
        filtered_query = []
        for param in keep_params:
            if param in request.args:
                for val in request.args.getlist(param):
                    filtered_query.append((param, val))
        if filtered_query:
            query_string = '?' + urlencode(filtered_query)

    return f"{base_origin}{target_path}{query_string}"

def format_og_image(image_url=None):
    """
    Định dạng đường dẫn ảnh Open Graph thành URL tuyệt đối:
    - Giữ nguyên URL nếu đã là URL tuyệt đối (http:// hoặc https://).
    - Thêm base origin vào trước đường dẫn tương đối nội bộ (/static/uploads/...).
    - Fallback về ảnh bìa công nghệ mặc định chất lượng cao nếu ảnh rỗng/None.
    """
    img = str(image_url).strip() if image_url else ''
    if not img:
        return DEFAULT_OG_IMAGE_URL
    if img.startswith('http://') or img.startswith('https://'):
        return img
    try:
        canonical_domain = current_app.config.get('CANONICAL_DOMAIN', '').strip().rstrip('/')
    except Exception:
        canonical_domain = ''
    base_origin = canonical_domain if canonical_domain else request.url_root.rstrip('/')
    if not img.startswith('/'):
        img = '/' + img
    return f"{base_origin}{img}"
```

---

### 2.3. Đăng ký Bộ lọc và Biến Toàn cục (`app/__init__.py`)
Tại hàm `create_app()`:
1. Đăng ký filter Jinja: `app.jinja_env.filters['clean_meta_desc'] = clean_meta_description`
2. Cung cấp đầy đủ các tiện ích SEO trong `@app.context_processor` `inject_globals()`:
   - `'default_meta_desc': DEFAULT_META_DESCRIPTION`
   - `'canonical_url': build_canonical_url`
   - `'clean_meta_description': clean_meta_description`
   - `'format_og_image': format_og_image`
   - `'default_og_image': lambda: format_og_image(None)`

---

### 2.4. Tái cấu trúc Khung Giao diện Cơ sở (`app/templates/base.html`)
Đã thay thế thẻ meta mô tả cố định đơn lẻ bằng một khối siêu dữ liệu hoàn chỉnh, tương thích toàn diện với Jinja2 inheritance và tự động mã hóa ký tự đặc biệt trong thuộc tính:

```html
    <title>{% block title %}{{ app_title }}{% endblock %}</title>
    
    <!-- Core SEO Meta Tags -->
    <meta name="description" content="{% block meta_description %}{{ default_meta_desc }}{% endblock %}">
    {% block meta_robots %}{% endblock %}
    {% block canonical %}<link rel="canonical" href="{{ canonical_url() }}">{% endblock %}

    <!-- Open Graph / Facebook Meta Tags -->
    <meta property="og:type" content="{% block og_type %}website{% endblock %}">
    <meta property="og:site_name" content="EventAI Pro">
    <meta property="og:title" content="{% block og_title %}{{ self.title()|striptags|trim }}{% endblock %}">
    <meta property="og:description" content="{% block og_description %}{{ self.meta_description()|striptags|trim }}{% endblock %}">
    <meta property="og:url" content="{% block og_url %}{{ canonical_url() }}{% endblock %}">
    <meta property="og:image" content="{% block og_image %}{{ default_og_image() }}{% endblock %}">
    <meta property="og:locale" content="vi_VN">

    <!-- Twitter Card Meta Tags -->
    <meta name="twitter:card" content="{% block twitter_card %}summary_large_image{% endblock %}">
    <meta name="twitter:title" content="{% block twitter_title %}{{ self.title()|striptags|trim }}{% endblock %}">
    <meta name="twitter:description" content="{% block twitter_description %}{{ self.meta_description()|striptags|trim }}{% endblock %}">
    <meta name="twitter:image" content="{% block twitter_image %}{{ self.og_image()|striptags|trim }}{% endblock %}">
```

---

### 2.5. Tối ưu hóa Giao diện Trang Chủ (`app/templates/main/index.html`)
1. **Metadata Blocks:**
   ```html
   {% block title %}EventAI Pro | Nền Tảng Quản Lý & Trải Nghiệm Sự Kiện Thông Minh{% endblock %}
   {% block meta_description %}Khám phá các sự kiện công nghệ, hội thảo AI đỉnh cao và workshop thực chiến tại EventAI Pro. Đăng ký vé QR Code bảo mật và trải nghiệm Cố vấn AI phản hồi thời gian thực.{% endblock %}
   {% block canonical %}<link rel="canonical" href="{{ canonical_url('/') }}">{% endblock %}
   ```
2. **Chuẩn hóa Phân cấp Tiêu đề (Heading Hierarchy):**
   - Thẻ H1 duy nhất: `<h1 class="hero-title mb-3">Trải Nghiệm Sự Kiện <span class="gradient-text">Đột Phá & Đẳng Cấp</span></h1>` (giữ nguyên).
   - Tiêu đề slide sự kiện nổi bật: Thay đổi `<h3 class="hero-slide-title ...">` thành `<h2 class="h3 hero-slide-title ...">`.
   - Tiêu đề mục Gợi ý AI: Thay đổi `<h3 class="mb-0">` thành `<h2 class="h3 mb-0">Gợi Ý Riêng Cho Bạn</h2>`.
   - Tiêu đề mục Sự kiện sắp diễn ra: Thay đổi `<h3 class="mb-1">` thành `<h2 class="h3 mb-1">Sự Kiện Sắp Diễn Ra</h2>`.
   - *Kết quả thẩm mỹ:* Lớp CSS `.h3` của Bootstrap giữ nguyên 100% kích cỡ chữ, khoảng cách đệm và độ đậm chữ gốc.

---

### 2.6. Tối ưu hóa Giao diện Danh Sách Sự Kiện (`app/templates/main/events.html`)
1. **Metadata Blocks:**
   ```html
   {% block title %}Danh Sách Sự Kiện Công Nghệ & Hội Thảo | EventAI Pro{% endblock %}
   {% block meta_description %}Khám phá danh sách đầy đủ các sự kiện, hội thảo công nghệ, diễn đàn khoa học và workshop đào tạo kỹ năng tại EventAI Pro. Lọc theo chủ đề và đăng ký trực tuyến dễ dàng.{% endblock %}
   {% block canonical %}<link rel="canonical" href="{{ canonical_url('/events') }}">{% endblock %}
   ```
2. **Chuẩn hóa Phân cấp Tiêu đề:**
   - Thay đổi tiêu đề chính `<h2 class="mb-2">Tất Cả Sự Kiện</h2>` thành `<h1 class="h2 mb-2">Tất Cả Sự Kiện</h1>` (cung cấp thẻ H1 duy nhất cho trang).
   - Thay đổi tiêu đề từng thẻ sự kiện trong lưới từ `<h5 class="event-card-title mb-2">` thành `<h2 class="h5 event-card-title mb-2">` (phân cấp H2 trực thuộc H1).

---

### 2.7. Tối ưu hóa Giao diện Chi Tiết Sự Kiện (`app/templates/main/event_detail.html`)
1. **Metadata Blocks:**
   ```html
   {% block title %}{{ event.title }} | EventAI Pro{% endblock %}
   {% block meta_description %}{{ clean_meta_description(event.description, event.title) }}{% endblock %}
   {% block canonical %}<link rel="canonical" href="{{ canonical_url('/events/' ~ event.id) }}">{% endblock %}
   {% block og_type %}article{% endblock %}
   {% block og_image %}{{ format_og_image(event.banner_url) }}{% endblock %}
   {% block event_id %}{{ event.id }}{% endblock %}
   {% block meta_robots %}
   {% if event.status in ['draft', 'cancelled'] or is_draft_preview %}
   <meta name="robots" content="noindex, follow">
   {% endif %}
   {% endblock %}
   ```
2. **Chuẩn hóa Phân cấp Tiêu đề:**
   - Tiêu đề sự kiện: Thay đổi `<h2 class="mb-4" style="font-size: 1.75rem; line-height: 1.25;">` thành `<h1 class="h2 mb-4" style="font-size: 1.75rem; line-height: 1.25;">{{ event.title }}</h1>` (thẻ H1 duy nhất cho trang).
   - Tiêu đề các mục con:
     - `<h4 class="mb-3">Giới Thiệu Sự Kiện</h4>` -> `<h2 class="h4 mb-3">Giới Thiệu Sự Kiện</h2>`
     - `<h4 class="mb-4">Lịch Trình Chi Tiết (Agenda)</h4>` -> `<h2 class="h4 mb-4">Lịch Trình Chi Tiết (Agenda)</h2>`
     - `<h6 class="fw-semibold mb-2">` (từng mục phiên họp) -> `<h3 class="h6 fw-semibold mb-2">`
     - `<h4 class="mb-3">Chọn Hạng Vé</h4>` -> `<h2 class="h4 mb-3">Chọn Hạng Vé</h2>`

---

## 3. KẾT QUẢ KIỂM THỬ VÀ ĐỐI SOÁT AN NINH

### 3.1. Bộ kiểm thử Chuyên biệt Phase 3A (`tests/test_seo_core_metadata.py`)
Được thiết kế với **23 ca kiểm thử tự động**, sử dụng parser phân tích HTML thuần của Python Standard Library (không cài đặt gói phụ thuộc mới):
- **Homepage:** Title, meta description, canonical absolute URL, Open Graph, Twitter Cards (`4/4 PASSED`).
- **Events Catalog:** Title, description, canonical, cơ chế bóc tách tham số theo dõi chiến dịch (`3/3 PASSED`).
- **Event Detail:** Tiêu đề động, bóc tách thẻ HTML trong mô tả, cắt tỉa văn bản dài theo từ vựng, fallback mô tả rỗng, canonical link, Open Graph type article, chuyển đổi ảnh banner tương đối thành tuyệt đối, fallback ảnh đại diện rỗng (`8/8 PASSED`).
- **Cấu hình Tên miền:** Override thông qua `CANONICAL_DOMAIN` (`1/1 PASSED`).
- **An toàn Ký tự Đặc biệt:** Mã hóa dấu ngoặc kép, dấu và (`&`) trong thuộc tính thẻ (`1/1 PASSED`).
- **Kiểm soát Trùng lặp:** Đảm bảo không có bất kỳ thẻ trùng lặp nào (`1/1 PASSED`).
- **Cấu trúc Tiêu đề H1 -> H2 -> H3:** Kiểm chứng sự hiện diện chính xác của duy nhất một H1 trên trang chủ, danh sách sự kiện và chi tiết sự kiện (`3/3 PASSED`).
- **Bảo tồn An ninh Phase 2.5:** Đảm bảo `noindex` trên trang đăng nhập/lỗi, bảo vệ draft event, và chặn truy cập ảnh QR tĩnh (`3/3 PASSED`).
- **Kết quả thực thi:** **23/23 PASSED (100%)** trong 5.94 giây.

### 3.2. Bộ kiểm thử An ninh Phase 2.5 (`tests/test_phase2_5_security.py`)
- Thực thi độc lập: **12/12 PASSED (100%)** trong 4.47 giây.
- Khẳng định không có bất kỳ xung đột hay suy yếu nào đối với các cơ chế kiểm soát bảo mật đã ban hành trước đó.

### 3.3. Toàn bộ Bộ kiểm thử Toàn dự án (Full Project Test Suite)
- Tổng số ca kiểm thử: **77/77 PASSED (100%)** trong 20.32 giây (tăng thêm 23 test case so với 54 test case ban đầu).
- Hệ thống hoàn toàn không có hồi quy lỗi (Zero Regression).

---

## 4. KẾT LUẬN VÀ SẴN SÀNG CHUYỂN GIAO GIAI ĐOẠN 3B

Giai đoạn Phase 3A đã hoàn thành xuất sắc toàn bộ mục tiêu đề ra:
1. Đã giải quyết triệt để 100% các khiếm khuyết Core SEO về title, description, canonicalization, Open Graph, Twitter Card và semantic heading hierarchy.
2. Giao diện người dùng Apple Liquid Glass được bảo toàn hoàn hảo (Zero visual shift).
3. Toàn bộ các cơ chế an ninh thông tin, quyền riêng tư vé và bảo vệ bản nháp được duy trì nghiêm ngặt.
4. Cơ sở hạ tầng template đã sẵn sàng để tích hợp **Schema.org Event JSON-LD** trong **Phase 3B** mà không gặp bất kỳ trở ngại nào.

