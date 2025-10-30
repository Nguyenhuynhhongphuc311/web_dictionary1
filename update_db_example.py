import sqlite3
import os

# Tên database
DB_NAME = "dictionary.db"

def update_pronunciation(word, new_pronunciation):
    """
    Cập nhật phiên âm (pronunciation) cho một từ cụ thể trong database và kiểm tra lại.
    """
    if not os.path.exists(DB_NAME):
        print(f"LỖI: Database '{DB_NAME}' không tìm thấy.")
        return

    conn = None
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # 1. Kiểm tra từ tồn tại
        cursor.execute("SELECT word FROM words WHERE word = ? COLLATE NOCASE", (word,))
        if cursor.fetchone() is None:
            print(f"CẢNH BÁO: Từ '{word}' không tồn tại trong database.")
            return

        # 2. Thực hiện cập nhật
        cursor.execute("""
            UPDATE words
            SET pronunciation = ?
            WHERE word = ? COLLATE NOCASE
        """, (new_pronunciation, word))
        
        # 3. Commit (Lưu thay đổi)
        conn.commit()
        
        # 4. Kiểm tra lại dữ liệu vừa cập nhật (DEBUG)
        cursor.execute("SELECT pronunciation, meaning FROM words WHERE word = ? COLLATE NOCASE LIMIT 1", (word,))
        updated_row = cursor.fetchone()
        
        if updated_row and updated_row[0] == new_pronunciation:
            print(f"✅ THÀNH CÔNG: Đã xác nhận cập nhật cho từ: {word}")
            print(f"   -> Pronunciation: /{updated_row[0]}/")
            print(f"   -> Meaning (ví dụ): {updated_row[1]}")
        else:
            print(f"❌ LỖI GHI DỮ LIỆU: Cập nhật cho từ {word} có thể không thành công.")


    except sqlite3.Error as e:
        print(f"❌ LỖI DATABASE: {e}")
    finally:
        if conn:
            conn.close()

# =======================================================
# 📌 CÁCH SỬ DỤNG
# =======================================================

# 1. Từ 'ability': Phiên âm chính xác: /əˈbɪləti/
update_pronunciation("ability", "əˈbɪləti")

# 2. Từ 'account': Phiên âm chính xác: /əˈkaʊnt/
update_pronunciation("account", "əˈkaʊnt")

# 3. Từ 'my': Phiên âm chính xác: /maɪ/
update_pronunciation("my", "maɪ")

# 4. Từ 'abortion': Phiên âm chính xác: /əˈbɔːʃən/
update_pronunciation("abortion", "əˈbɔːʃən")

print("\n--- Vui lòng kiểm tra log trên Console. Nếu thấy '❌ LỖI GHI DỮ LIỆU' hoặc '❌ LỖI DATABASE', database của bạn đang có vấn đề. ---")
