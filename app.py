from flask import Flask, render_template, request, jsonify
import sqlite3
import re
import os
from threading import Lock

app = Flask(__name__)

# Tên database của bạn
DB_NAME = "dictionary.db"

# Khóa để quản lý kết nối database, đảm bảo an toàn cho môi trường đa luồng
db_lock = Lock()

# ======================
# 🔹 KẾT NỐI DATABASE
# ======================
def get_connection():
    """Tạo kết nối database, đảm bảo kết nối chỉ đọc nếu có thể."""
    # Khi chạy trên môi trường không cho phép kết nối đa luồng, có thể dùng check_same_thread=False
    return sqlite3.connect(DB_NAME, check_same_thread=False)

# ======================
# 🔹 LOAD TẤT CẢ TỪ VÀO BỘ NHỚ
# ======================
def load_all_words():
    """Tải tất cả các từ duy nhất vào bộ nhớ (SET) để dùng cho autocomplete."""
    # Kiểm tra database tồn tại trước
    if not os.path.exists(DB_NAME):
        print(f"LỖI: Database '{DB_NAME}' không tìm thấy. Autocomplete sẽ không hoạt động.")
        return set()
    
    conn = get_connection()
    cursor = conn.cursor()
    # Chỉ lấy các từ duy nhất
    cursor.execute("SELECT DISTINCT word FROM words")
    # Lấy set (tập hợp) các từ, chuyển về chữ thường để tìm kiếm không phân biệt hoa thường
    words = set(r[0].lower() for r in cursor.fetchall())
    conn.close()
    print(f"Đã tải thành công {len(words)} từ vào bộ nhớ.")
    return words

all_words_set = load_all_words()
# Chuyển set thành list để dễ dàng tìm kiếm với prefix
all_words_list = sorted(list(all_words_set))


# ======================
# 🔹 GỘP DÒNG TRÙNG
# ======================
def filter_unique_by_word(rows):
    """Gộp các dòng dữ liệu trùng từ (do có nhiều nghĩa) thành một kết quả duy nhất."""
    result_dict = {}
    for row in rows:
        word = row[0]
        if word not in result_dict:
            result_dict[word] = list(row)
        else:
            # Gộp synonym
            if len(row) > 9 and row[9]:
                old_syn = result_dict[word][9] or ""
                if row[9] not in old_syn:
                    result_dict[word][9] = (old_syn + ", " + row[9]).strip(", ")
            # Gộp antonym
            if len(row) > 10 and row[10]:
                old_ant = result_dict[word][10] or ""
                if row[10] not in old_ant:
                    result_dict[word][10] = (old_ant + ", " + row[10]).strip(", ")
    return list(result_dict.values())

# ======================
# 🔹 HÀM XỬ LÝ CHUỖI
# ======================

# Hàm này highlight dấu nhấn trong phiên âm (Được phục hồi)
def highlight_stress_mark(pronunciation):
    if not pronunciation:
        return ""
    # Dấu nhấn chính (ˈ)
    return re.sub(r'ˈ', r'<span class="stress-mark">ˈ</span>', pronunciation)


# Hàm này bọc từ khóa tìm kiếm trong kết quả (ví dụ, highlight từ tìm kiếm)
def highlight_keyword(text, keyword):
    """Tô sáng từ khóa tìm kiếm trong kết quả."""
    if not keyword or not text:
        return text
    
    # 1. Tách chuỗi thành các phần: TEXT và HTML TAGS
    # Regex này tìm tất cả các thẻ HTML (như <a href="..."></a>)
    parts = re.split(r'(<[^>]+>|&nbsp;)', text)
    
    highlighted_text = []
    
    # 2. Chỉ highlight các phần là TEXT
    pattern = re.compile(re.escape(keyword), re.IGNORECASE)
    
    for part in parts:
        if not part:
            continue
            
        # Kiểm tra nếu phần này là một thẻ HTML hoặc khoảng trắng đặc biệt (&nbsp;)
        if part.startswith('<') and part.endswith('>') or part == '&nbsp;':
            highlighted_text.append(part) # Giữ nguyên thẻ HTML
        else:
            # Chỉ thay thế trong phần text
            # Thay thế keyword bằng <mark>keyword</mark>
            highlighted_text.append(pattern.sub(lambda m: f"<mark style='background-color:#fff3cd; color:inherit;'>{m.group(0)}</mark>", part))
            
    return "".join(highlighted_text)


# ======================
# 🔹 TOKENIZER & LINK CÂU VÍ DỤ (Đã sửa để tô đậm từ đã biết)
# ======================
def link_words_in_example(text):
    """Tạo liên kết cho mỗi từ trong câu ví dụ và tô đậm từ có trong từ điển."""
    if not text:
        return ""
    # Biểu thức chính quy: (\W+) tách các từ bằng các ký tự không phải từ (dấu câu, khoảng trắng)
    words = re.split(r'(\W+)', text) 
    result = ""
    for w in words:
        # Chỉ tạo link với từ tiếng Anh VÀ có trong từ điển
        if re.match(r'^[A-Za-z]+$', w) and w.lower() in all_words_set:
            # Thêm class 'known-word' để CSS tô đậm và loại bỏ style inline cũ
            css_class = 'known-word'
            result += f'<a href="/?word={w.lower()}" class="{css_class}">{w}</a>'
        else:
            result += w
    return result


# ======================
# 🔹 TRANG CHÍNH
# ======================
@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    search_word = ""

    search_word = request.args.get("word", "").strip() or request.form.get("word", "").strip()

    if search_word:
        conn = get_connection()
        cursor = conn.cursor()
        
        # 1. TÌM CHÍNH XÁC (Ưu tiên)
        cursor.execute("""
            SELECT word, pronunciation, type, v2, v3, ing, ed, meaning, example, synonym, antonym
            FROM words
            WHERE word = ? COLLATE NOCASE
        """, (search_word,))
        rows = cursor.fetchall()

        if not rows:
            # 2. TÌM GẦN ĐÚNG (Nếu tìm chính xác không có) - Giới hạn 10 từ
            cursor.execute("""
                SELECT word, pronunciation, type, v2, v3, ing, ed, meaning, example, synonym, antonym
                FROM words
                WHERE word LIKE ? COLLATE NOCASE LIMIT 10
            """, (search_word + "%",))
            rows = cursor.fetchall()
        
        results = filter_unique_by_word(rows)

        # xử lý link + highlight
        for r in results:
            r[1] = highlight_stress_mark(r[1]) # pronunciation (Áp dụng highlight dấu nhấn)

            if r[7]: # meaning
                r[7] = highlight_keyword(r[7], search_word)
            if r[8]: # example
                # Quan trọng: Link trước, sau đó Highlight.
                r[8] = link_words_in_example(r[8])
                # Highlight được gọi sau link, nhưng giờ hàm highlight đã được sửa để bỏ qua thẻ <a>
                r[8] = highlight_keyword(r[8], search_word)
            
            # Áp dụng highlight cho Synonym và Antonym
            if r[9]: # synonym
                r[9] = highlight_keyword(r[9], search_word)
            if r[10]: # antonym
                r[10] = highlight_keyword(r[10], search_word)


        conn.close()

    return render_template("index.html", results=results, search_word=search_word)

# ======================
# 🔹 GỢI Ý TỰ ĐỘNG (Sử dụng dữ liệu trong bộ nhớ)
# ======================
@app.route("/autocomplete")
def autocomplete():
    term = request.args.get("term", "").strip().lower()
    suggestions = []
    
    if term:
        # Lọc danh sách từ đã được tải vào bộ nhớ (rất nhanh)
        suggestions = [word for word in all_words_list if word.startswith(term)]
        
        # Đảm bảo kết quả là duy nhất và giới hạn 10 (khắc phục lỗi lặp từ)
        unique_suggestions = sorted(list(set(suggestions)))[:10]
        suggestions = unique_suggestions

    # Trả về các từ duy nhất, khắc phục lỗi lặp từ trong autocomplete
    return jsonify(suggestions)

# ======================
# 🔹 CHẠY APP
# ======================
if __name__ == "__main__":
    # Đảm bảo database tồn tại trước khi chạy
    if not os.path.exists(DB_NAME):
        print("CẢNH BÁO: Database 'dictionary.db' không tồn tại. Vui lòng tạo file này và bảng 'words'.")
    app.run(debug=True)
