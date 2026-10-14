"""
Database Service (SQL Tool) for Multi-Agent Event System.
Executes parameterized SQL queries against the relational Event Management database.
Guarantees protection against SQL injection and matches exact schema tables.
"""
import os
import sqlite3
from pathlib import Path
from typing import List, Dict, Any, Optional

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
DEFAULT_SQLITE_PATH = BASE_DIR / "instance" / "event_management.db"
if not DEFAULT_SQLITE_PATH.exists():
    ALT_PATH = BASE_DIR / "event_management.db"
    if ALT_PATH.exists():
        DEFAULT_SQLITE_PATH = ALT_PATH

def get_connection():
    """
    Returns an active database connection with dictionary cursor support.
    Defaults to SQLite, but allows MySQL if configured in environment.
    """
    db_uri = os.getenv("DATABASE_URI", "")
    if db_uri.startswith("mysql") or os.getenv("MYSQL_HOST"):
        try:
            import mysql.connector
            return mysql.connector.connect(
                host=os.getenv("MYSQL_HOST", "localhost"),
                port=int(os.getenv("MYSQL_PORT", "3306")),
                user=os.getenv("MYSQL_USER", "root"),
                password=os.getenv("MYSQL_PASSWORD", ""),
                database=os.getenv("MYSQL_DATABASE", "event_management")
            )
        except Exception:
            pass

    conn = sqlite3.connect(str(DEFAULT_SQLITE_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def search_events_sql(criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    SQL Tool: Searches events based on structured criteria using safe parameterized queries.
    Matches schema: location_type, location_address, max_attendees, start_date, end_date.
    """
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT DISTINCT
            e.id,
            e.event_code,
            e.title,
            e.category,
            e.location_type AS format,
            e.location_address AS venue_address,
            e.location_address AS venue_city,
            e.max_attendees AS venue_capacity,
            e.status,
            e.start_date,
            e.end_date,
            e.banner_url AS banner_image,
            e.description,
            MIN(t.price) AS min_ticket_price,
            MAX(t.price) AS max_ticket_price
        FROM events e
        LEFT JOIN tickets t ON e.id = t.event_id
        WHERE e.status IN ('published', 'ongoing')
    """
    params = []

    # Category filter
    category = criteria.get("category")
    if category and str(category).lower() not in ("all", "none", "null", ""):
        query += " AND LOWER(e.category) LIKE ?"
        params.append(f"%{str(category).lower()}%")

    # Format filter (online, offline, in_person, hybrid)
    fmt = criteria.get("format")
    if fmt and str(fmt).lower() not in ("all", "none", "null", ""):
        fmt_val = "offline" if str(fmt).lower() == "in_person" else str(fmt).lower()
        query += " AND (LOWER(e.location_type) = ? OR LOWER(e.location_type) = 'hybrid')"
        params.append(fmt_val)

    # City / Location filter
    city = criteria.get("city") or criteria.get("location")
    if city and str(city).lower() not in ("all", "none", "null", ""):
        query += " AND LOWER(e.location_address) LIKE ?"
        params.append(f"%{str(city).lower()}%")

    # Minimum capacity filter
    min_capacity = criteria.get("min_capacity")
    if min_capacity and isinstance(min_capacity, (int, float)) and min_capacity > 0:
        query += " AND e.max_attendees >= ?"
        params.append(min_capacity)

    # Keyword / Topic search
    keyword = criteria.get("keyword") or criteria.get("topic")
    if keyword and str(keyword).lower() not in ("all", "none", "null", ""):
        query += " AND (LOWER(e.title) LIKE ? OR LOWER(e.description) LIKE ? OR LOWER(e.tags) LIKE ?)"
        params.append(f"%{str(keyword).lower()}%")
        params.append(f"%{str(keyword).lower()}%")
        params.append(f"%{str(keyword).lower()}%")

    query += " GROUP BY e.id"

    # Max Price filter (HAVING clause)
    max_price = criteria.get("max_price")
    if max_price is not None and isinstance(max_price, (int, float)) and max_price >= 0:
        query += " HAVING (MIN(t.price) <= ? OR MIN(t.price) IS NULL)"
        params.append(max_price)

    query += " ORDER BY e.start_date ASC LIMIT 10"

    cursor.execute(query, params)
    rows = cursor.fetchall()
    
    results = []
    for r in rows:
        results.append(dict(r))

    cursor.close()
    conn.close()
    return results

def get_event_full_details_sql(event_id: int) -> Optional[Dict[str, Any]]:
    """
    SQL Tool: Retrieves comprehensive ground truth details for a specific event
    including tickets, schedules, speakers, and venues.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Event details
    cursor.execute("""
        SELECT e.id, e.event_code, e.title, e.category, e.description,
               e.location_type AS format, e.location_address, e.online_meeting_url,
               e.max_attendees AS capacity, e.start_date, e.end_date, e.status, e.tags
        FROM events e
        WHERE e.id = ?
    """, (event_id,))
    event_row = cursor.fetchone()
    if not event_row:
        cursor.close()
        conn.close()
        return None

    event_data = dict(event_row)
    event_data["venue_name"] = event_data.get("location_address") or "Hội trường sự kiện"
    event_data["venue_city"] = event_data.get("location_address") or "Toàn quốc"

    # Tickets
    cursor.execute("""
        SELECT id, ticket_code, name, ticket_type, price, quota, sold_count,
               (quota - sold_count) as remaining_quota
        FROM tickets
        WHERE event_id = ?
        ORDER BY price ASC
    """, (event_id,))
    event_data["tickets"] = [dict(t) for t in cursor.fetchall()]

    # Schedules, Speakers & Venues
    cursor.execute("""
        SELECT s.id, s.title AS session_title, s.description, s.start_at AS start_time,
               s.end_at AS end_time,
               sp.name AS speaker_name, sp.title AS speaker_title, sp.organization AS speaker_org,
               sp.bio AS speaker_expertise,
               v.name AS venue_name, v.room_name AS room
        FROM schedules s
        LEFT JOIN speakers sp ON s.speaker_id = sp.id
        LEFT JOIN venues v ON s.venue_id = v.id
        WHERE s.event_id = ?
        ORDER BY s.start_at ASC
    """, (event_id,))
    event_data["schedules"] = [dict(s) for s in cursor.fetchall()]

    # FAQs
    cursor.execute("""
        SELECT id, question, answer, category
        FROM event_faqs
        WHERE event_id = ?
    """, (event_id,))
    event_data["faqs"] = [dict(f) for f in cursor.fetchall()]

    cursor.close()
    conn.close()
    return event_data

def get_all_events_summary_sql(limit: int = 15) -> List[Dict[str, Any]]:
    """SQL Tool: Returns high-level summary of active events."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT e.id, e.title, e.category, e.location_type AS format,
               e.location_address AS venue_name, e.location_address AS venue_city,
               e.start_date, e.end_date,
               MIN(t.price) as min_price, MAX(t.price) as max_price
        FROM events e
        LEFT JOIN tickets t ON e.id = t.event_id
        WHERE e.status IN ('published', 'ongoing')
        GROUP BY e.id
        ORDER BY e.start_date ASC
        LIMIT ?
    """, (limit,))
    rows = [dict(r) for r in cursor.fetchall()]
    cursor.close()
    conn.close()
    return rows
