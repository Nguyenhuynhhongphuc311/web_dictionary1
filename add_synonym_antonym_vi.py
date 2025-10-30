import sqlite3
from nltk.corpus import wordnet

# --- Kết nối đến CSDL SQLite ---
db_path = "dictionary.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# --- Kiểm tra nếu bảng chưa có cột synonym và antonym thì thêm ---
try:
    cursor.execute("ALTER TABLE words ADD COLUMN synonym TEXT;")
    cursor.execute("ALTER TABLE words ADD COLUMN antonym TEXT;")
    print("✅ Đã thêm cột synonym và antonym.")
except:
    print("⚙️ Cột synonym và antonym đã tồn tại.")

# --- Lấy danh sách từ vựng ---
cursor.execute("SELECT id, word FROM words")
rows = cursor.fetchall()

count = 0
for row in rows:
    word_id, word = row
    syns = set()
    ants = set()

    for synset in wordnet.synsets(word):
        for lemma in synset.lemmas():
            syns.add(lemma.name().replace("_", " "))
            if lemma.antonyms():
                for ant in lemma.antonyms():
                    ants.add(ant.name().replace("_", " "))

    synonym_text = ", ".join(list(syns)[:5]) if syns else None
    antonym_text = ", ".join(list(ants)[:5]) if ants else None

    cursor.execute("""
        UPDATE words
        SET synonym = ?, antonym = ?
        WHERE id = ?
    """, (synonym_text, antonym_text, word_id))

    count += 1
    if count % 100 == 0:
        print(f"Đã xử lý {count} từ...")

conn.commit()
conn.close()
print(f"🎉 Hoàn tất! Đã thêm synonym và antonym cho {count} từ.")
