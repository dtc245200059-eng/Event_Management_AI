import sqlite3
from pathlib import Path

db_path = Path("instance_staging/staging.db")
if not db_path.exists():
    print(f"Error: {db_path} does not exist.")
    exit(1)

conn = sqlite3.connect(str(db_path))
c = conn.cursor()
tables = [row[0] for row in c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'").fetchall()]
print(f"Tables in staging.db: {len(tables)}")
for t in sorted(tables):
    count = c.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
    print(f"  {t}: {count}")
conn.close()

