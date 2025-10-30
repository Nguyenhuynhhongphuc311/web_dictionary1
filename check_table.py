import sqlite3
import os

DB_NAME = "dictionary.db"

def check_word_data(word):
    """Kiểm tra dữ liệu thô của một từ trong database."""
    if not os.path.exists(DB_NAME):
        print(f"LỖI: Database '{DB_NAME}' không tìm thấy.")
        return

    conn = None
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        print(f"--- Dữ liệu thô cho từ: '{word}' (Không phân biệt hoa thường) ---")
        
        cursor.execute("""
            SELECT word, pronunciation, type, meaning
            FROM words
            WHERE word = ? COLLATE NOCASE
        """, (word,))
        
        rows = cursor.fetchall()
        
        if rows:
            for row in rows:
                print(f"  Word: {row[0]}")
                print(f"  Pronunciation: {row[1] if row[1] else '!!! THIẾU DỮ LIỆU !!!'}")
                print(f"  Type: {row[2]}")
                print(f"  Meaning: {row[3]}")
                print("-" * 20)
        else:
            print("Không tìm thấy từ này.")

    except sqlite3.Error as e:
        print(f"LỖI DATABASE: {e}")
    finally:
        if conn:
            conn.close()

# Kiểm tra các từ bạn đang gặp vấn đề
check_word_data("ability")
check_word_data("abortion")
check_word_data("my")

print("--- Hoàn tất kiểm tra ---")
