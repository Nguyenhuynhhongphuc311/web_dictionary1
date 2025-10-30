# init_db_full.py
import sqlite3
from import_word import data

DB_PATH = "dictionary.db"
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# Tạo bảng av
c.execute("""
CREATE TABLE IF NOT EXISTS av (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word TEXT NOT NULL,
    pronunciation TEXT,
    type TEXT,
    v2 TEXT,
    v3 TEXT,
    ving TEXT,
    ved TEXT,
    meaning TEXT,
    example TEXT,
    synonym TEXT,
    antonym TEXT
)
""")
conn.commit()

insert_query = """
INSERT OR IGNORE INTO av
(word, pronunciation, type, v2, v3, ving, ved, meaning, example, synonym, antonym)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

for row in data:
    # Nếu tuple chưa đủ 11 phần tử -> bổ sung None
    if len(row) < 11:
        row = tuple(list(row) + [None] * (11 - len(row)))
    c.execute(insert_query, row)

conn.commit()
conn.close()
print("✅ Đã chèn tất cả từ vào bảng av với dấu nhấn IPA đầy đủ!")
