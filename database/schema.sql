-- =============================================================================
-- SQL SCHEMA DDL DEFINITION (9 TABLES - 3NF NORMALIZED)
-- Hệ Thống Quản Lý Sự Kiện Tích Hợp AI (Event Management AI System)
-- =============================================================================

-- 1. BẢNG USERS (Tài khoản người dùng & RBAC)
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(80) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'attendee', -- 'admin', 'staff', 'attendee'
    is_active BOOLEAN NOT NULL DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 2. BẢNG SPEAKERS (Hồ sơ diễn giả & chuyên gia)
CREATE TABLE IF NOT EXISTS speakers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(150) NOT NULL,
    title VARCHAR(150),
    organization VARCHAR(200),
    bio TEXT,
    photo_url VARCHAR(255),
    email VARCHAR(150),
    expertise VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 3. BẢNG VENUES (Địa điểm & phòng hội thảo)
CREATE TABLE IF NOT EXISTS venues (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(200) NOT NULL,
    address VARCHAR(255) NOT NULL,
    capacity INTEGER NOT NULL DEFAULT 100,
    room_name VARCHAR(100),
    status VARCHAR(20) DEFAULT 'available', -- 'available', 'maintenance'
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 4. BẢNG EVENTS (Thông tin sự kiện cốt lõi)
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_code VARCHAR(40) NOT NULL UNIQUE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(100) NOT NULL DEFAULT 'Technology',
    banner_url VARCHAR(255),
    start_date DATETIME NOT NULL,
    end_date DATETIME NOT NULL,
    location_type VARCHAR(20) DEFAULT 'offline', -- 'offline', 'online', 'hybrid'
    location_address VARCHAR(255),
    online_meeting_url VARCHAR(255),
    max_attendees INTEGER DEFAULT 500,
    status VARCHAR(20) DEFAULT 'published', -- 'draft', 'published', 'completed', 'cancelled'
    tags VARCHAR(255),
    created_by INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL
);

-- 5. BẢNG SCHEDULES (Lịch trình timeline & phân bổ phiên hội thảo)
CREATE TABLE IF NOT EXISTS schedules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER NOT NULL,
    speaker_id INTEGER,
    venue_id INTEGER,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    start_at DATETIME NOT NULL,
    end_at DATETIME NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
    FOREIGN KEY (speaker_id) REFERENCES speakers(id) ON DELETE SET NULL,
    FOREIGN KEY (venue_id) REFERENCES venues(id) ON DELETE SET NULL
);

-- 6. BẢNG ATTENDEES (Hồ sơ người tham dự & sở thích AI)
CREATE TABLE IF NOT EXISTS attendees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    attendee_code VARCHAR(40) NOT NULL UNIQUE,
    user_id INTEGER UNIQUE,
    full_name VARCHAR(150) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    phone VARCHAR(20),
    organization VARCHAR(200),
    job_title VARCHAR(100),
    interests TEXT, -- JSON/CSV sở thích công nghệ cho TF-IDF
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 7. BẢNG TICKETS (Hạng vé, mức giá & hạn ngạch Quota)
CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER NOT NULL,
    ticket_code VARCHAR(40) NOT NULL UNIQUE,
    ticket_type VARCHAR(30) NOT NULL, -- 'free', 'standard', 'vip'
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price FLOAT NOT NULL DEFAULT 0.0,
    quota INTEGER NOT NULL DEFAULT 100,
    sold_count INTEGER NOT NULL DEFAULT 0,
    status VARCHAR(20) DEFAULT 'active', -- 'active', 'sold_out', 'hidden'
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE
);

-- 8. BẢNG REGISTRATIONS (Đăng ký vé, thanh toán, mã QR check-in & khảo sát)
CREATE TABLE IF NOT EXISTS registrations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    registration_code VARCHAR(50) NOT NULL UNIQUE,
    event_id INTEGER NOT NULL,
    attendee_id INTEGER NOT NULL,
    ticket_id INTEGER NOT NULL,
    registration_status VARCHAR(20) DEFAULT 'confirmed', -- 'confirmed', 'cancelled', 'pending'
    payment_status VARCHAR(20) DEFAULT 'free', -- 'free', 'paid', 'pending', 'refunded'
    payment_ref VARCHAR(100),
    payment_amount FLOAT DEFAULT 0.0,
    paid_at DATETIME,
    refund_status VARCHAR(20) DEFAULT 'none',
    ticket_number VARCHAR(50) NOT NULL UNIQUE,
    qr_code_path VARCHAR(255),
    checked_in BOOLEAN DEFAULT 0,
    checked_in_at DATETIME,
    checked_in_by VARCHAR(100),
    feedback_rating INTEGER, -- 1 đến 5 sao
    feedback_text TEXT,
    sentiment VARCHAR(20), -- 'POSITIVE', 'NEUTRAL', 'NEGATIVE'
    sentiment_score FLOAT,
    feedback_submitted_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
    FOREIGN KEY (attendee_id) REFERENCES attendees(id) ON DELETE CASCADE,
    FOREIGN KEY (ticket_id) REFERENCES tickets(id) ON DELETE RESTRICT,
    CONSTRAINT uq_event_attendee UNIQUE (event_id, attendee_id)
);

-- 9. BẢNG AI_CHAT_HISTORY (Lịch sử hội thoại & nhật ký AI RAG)
CREATE TABLE IF NOT EXISTS ai_chat_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    event_id INTEGER,
    chat_type VARCHAR(30) NOT NULL DEFAULT 'rag_chat', -- 'rag_chat', 'generator', 'sentiment'
    user_message TEXT NOT NULL,
    ai_response TEXT NOT NULL,
    model_name VARCHAR(80) DEFAULT 'gemini-2.0-flash',
    response_mode VARCHAR(20) DEFAULT 'live', -- 'live', 'mock'
    latency_ms INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE
);

-- 10. BẢNG NOTIFICATIONS (Thông báo sự kiện, thư mời, nhắc lịch tích hợp AI)
CREATE TABLE IF NOT EXISTS notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER NOT NULL,
    title VARCHAR(200) NOT NULL,
    notification_type VARCHAR(30) NOT NULL DEFAULT 'reminder', -- 'invitation', 'reminder', 'thank_you', 'update'
    target_audience VARCHAR(50) NOT NULL DEFAULT 'all_registered', -- 'all_registered', 'checked_in', 'not_checked_in', 'vip'
    content TEXT NOT NULL,
    recipient_count INTEGER DEFAULT 0,
    status VARCHAR(20) DEFAULT 'sent', -- 'draft', 'sent'
    sent_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL
);

-- 11. BẢNG EVENT_FAQS (Hỏi đáp chính sách, cẩm nang sự kiện phục vụ RAG Grounding)
CREATE TABLE IF NOT EXISTS event_faqs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER NOT NULL,
    question VARCHAR(255) NOT NULL,
    answer TEXT NOT NULL,
    category VARCHAR(50) DEFAULT 'general', -- 'checkin', 'ticketing', 'venue', 'logistics', 'general'
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE
);

-- =============================================================================
-- INDEXES TỐI ƯU HÓA HIỆU NĂNG TRUY VẤN
-- =============================================================================
CREATE INDEX IF NOT EXISTS idx_events_category ON events(category);
CREATE INDEX IF NOT EXISTS idx_events_status ON events(status);
CREATE INDEX IF NOT EXISTS idx_events_start_date ON events(start_date);
CREATE INDEX IF NOT EXISTS idx_schedules_event ON schedules(event_id);
CREATE INDEX IF NOT EXISTS idx_tickets_event ON tickets(event_id);
CREATE INDEX IF NOT EXISTS idx_registrations_event ON registrations(event_id);
CREATE INDEX IF NOT EXISTS idx_registrations_attendee ON registrations(attendee_id);
CREATE INDEX IF NOT EXISTS idx_registrations_ticket_number ON registrations(ticket_number);
CREATE INDEX IF NOT EXISTS idx_registrations_checked_in ON registrations(checked_in);
CREATE INDEX IF NOT EXISTS idx_notifications_event ON notifications(event_id);
CREATE INDEX IF NOT EXISTS idx_notifications_type ON notifications(notification_type);
CREATE INDEX IF NOT EXISTS idx_event_faqs_event ON event_faqs(event_id);
CREATE INDEX IF NOT EXISTS idx_event_faqs_category ON event_faqs(category);

