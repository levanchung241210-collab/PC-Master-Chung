import streamlit as st
import json
import re
import os

# CONFIG GIAO DIỆN CYBERPUNK CHUẨN STEM LỚP 10A4
st.set_page_config(page_title="Vua PC Chatbot - Lê Văn Chung 10A4", page_icon="🖥️", layout="wide")

st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #020617, #0b1329, #1c1a27); color: #f8fafc; }
.neon-title { text-align: center; font-size: 42px !important; font-weight: 900 !important; color: #ffffff; text-shadow: 0 0 10px #3b82f6, 0 0 30px #1d4ed8; }
.neon-subtitle { text-align: center; color: #38bdf8; font-size: 18px !important; font-weight: 500; }
[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) { background: linear-gradient(135deg, #1d4ed8, #1e40af); border-radius: 16px; border-left: 5px solid #60a5fa; }
[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-assistant"]) { background: rgba(15, 23, 42, 0.8); border-radius: 16px; border: 1px solid #334155; border-left: 5px solid #3b82f6; }
.stChatInput input { background-color: #0f172a !important; color: #ffffff !important; border: 2px solid #3b82f6 !important; }
section[data-testid="stSidebar"] { background-color: #020617; border-right: 1px solid #1e293b; }
</style>
""", unsafe_allow_html=True)

# LOAD DATABASE JSON
def load_database():
    if os.path.exists("database_pc.json"):
        with open("database_pc.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {"loi_he_thong": [], "linh_kien_pc": []}

data_pc = load_database()

# SIDEBAR CONTROL PANEL
with st.sidebar:
    st.markdown("<h2 style='color: #3b82f6; text-align: center;'>🖥️ Vua PC Lab v11.0</h2>", unsafe_allow_html=True)
    st.success("⚡ ENGINE: ĐÓNG BĂNG LOGIC")
    st.markdown("---")
    st.write("📊 **Trạng thái hệ thống:**")
    st.info("✔️ Cơ chế chặn bắt chữ đơn lẻ (Anti-Single Keyword)")
    st.info("✔️ Yêu cầu tối thiểu 2 điểm trùng khớp")
    st.info("✔️ Không chỉnh sửa dữ liệu JSON gốc")
    st.markdown("---")
    st.warning("🤖 Phiên bản: Bản vá lỗi tối hậu")
    st.info("👨‍💻 Tác giả:\n\n**Lê Văn Chung - Lớp 10A4**")

st.markdown('<div class="neon-title">👑 VUA PC - BẢN KHÓA LOGIC TỐI HẬU V11.0</div>', unsafe_allow_html=True)
st.markdown('<div class="neon-subtitle">BỘ LÕI HOÀN THIỆN XỬ LÝ KHÔNG ĐỤNG DATA CỦA: LÊ VĂN CHUNG - LỚP 10A4</div>', unsafe_allow_html=True)
st.markdown("---")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

# ==========================================
# THUẬT TOÁN TÍNH ĐIỂM CHUẨN XÁC CAO (V11.0)
# ==========================================
def calculate_match_score(item, q_clean, user_numbers):
    score = 0
    item_kws = [str(kw).lower().strip() for kw in item.get("keywords", [])]
    
    # Chỉ đếm từ khóa nếu nó đứng tách biệt hoặc khớp chính xác để tránh dính chữ bậy
    user_words = q_clean.split()
    for kw in item_kws:
        if kw in user_words or (kw.isdigit() and kw in q_clean):
            score += 1
            
    if score == 0:
        return 0

    # KIỂM TRA XUNG ĐỘT MÃ SỐ (Chặn đứng i5-14400 ăn theo i5-6500)
    item_numbers = [re.sub(r'\D', '', kw) for kw in item_kws if re.search(r'\d{3,}', kw)]
    item_numbers = [n for n in item_numbers if n]
    
    if item_numbers and user_numbers:
        if not set(item_numbers).intersection(set(user_numbers)):
            return 0 # Mã số không khớp -> Hủy kết quả lập tức
            
    return score

def engine_vua_pc(user_query):
    # Tiền xử lý xóa ký tự đặc biệt, giữ lại khoảng trắng
    q_clean = user_query.lower().strip()
    q_clean = re.sub(r'[-–_,.\?!\(\)]', ' ', q_clean)
    
    # Xử lý lời chào nhanh
    if any(w in q_clean.split() for w in ["hi", "hello", "chào", "alo"]):
        return "👋 **Xin chào! Tôi là Vua PC v11.0.** Hệ thống đã được cấu hình lại bộ lọc từ khóa. Bạn cần chẩn đoán lỗi hay kiểm tra thông số thiết bị nào?"

    # Trích xuất toàn bộ số từ câu hỏi để check xung đột
    user_numbers = [re.sub(r'\D', '', w) for w in q_clean.split() if re.search(r'\d{3,}', w)]
    user_numbers = [n for n in user_numbers if n]

    best_match = None
    max_score = 0
    match_pool = ""

    # Quét kho linh kiện
    for item in data_pc.get("linh_kien_pc", []):
        final_score = calculate_match_score(item, q_clean, user_numbers)
        if final_score > max_score:
            max_score = final_score
            best_match = item
            match_pool = "linh_kien"

    # Quét kho lỗi
    for item in data_pc.get("loi_he_thong", []):
        final_score = calculate_match_score(item, q_clean, user_numbers)
        if final_score > max_score:
            max_score = final_score
            best_match = item
            match_pool = "loi"

    # ĐIỀU KIỆN ĐẦU RA NGHIÊM NGẶT (CHỐNG BẮT CHỮ CHUNG CHUNG)
    # Nếu khớp linh kiện phần cứng, yêu cầu phải trùng từ 2 từ khóa trở lên (Ví dụ: phải có cả 'i5' và '6500')
    if max_score >= 2 and best_match:
        if match_pool == "loi":
            return f"### 🎯 Phân tích phát hiện lỗi: {best_match['ten']}\n⚠️ **Phân loại:** `{best_match['loai']}`\n\n❌ **Nguyên nhân cốt lõi:** {best_match['nguyen_nhan']}\n\n🛠️ **Phác đồ khắc phục:**\n{best_match['giai_phap']}"
        else:
            return f"### 📦 Thông tin linh kiện: {best_match['ten']}\n⚙️ **Thông số kỹ thuật:** {best_match.get('thong_so', 'Chưa có thông số')}\n\n💡 **Tư vấn từ Chung 10A4:** *{best_match.get('chuyen_gia_tu_van', '')}*"

    # TẦNG TỪ CHỐI VÀ PHÂN LUỒNG THÔNG MINH KHI KHÔNG ĐỦ ĐIỂM SÀN
    hardware_keywords = ["i3", "i5", "i7", "i9", "ryzen", "gtx", "rtx", "rx", "h110", "b660", "h610", "main", "chip", "cpu", "vga", "card"]
    error_keywords = ["xanh", "sập", "đen", "lỗi", "bsod", "dump", "treo", "đơ", "bíp"]

    if any(kw in q_clean.split() for kw in hardware_keywords):
        # Nếu gõ cụ thể mã chip mới (ví dụ i5 12400f) mà không có trong JSON thì thông báo chưa nạp
        if user_numbers:
            return f"🤖 **Vua PC v11.0 phản hồi:** Hệ thống nhận diện mã phần cứng liên quan đến dòng số `{user_numbers[0]}`.\n\n⚠️ Thiết bị này hiện **chưa được nạp** vào danh mục `linh_kien_pc` trong file `database_pc.json`."
        # Nếu chỉ gõ vu vơ câu có chữ i5 như "Sao biết mỗi i5 vậy" -> Trả về câu hướng dẫn chứ không nhận vơ linh kiện
        return "🤖 **Vua PC v11.0 phản hồi:** Bạn đang nhắc đến từ khóa phần cứng chung chung. Để xem chi tiết, vui lòng nhập đầy đủ mã (Ví dụ: `i5 6500`)."
        
    if any(kw in q_clean.split() for kw in error_keywords):
        return "🤖 **Vua PC v11.0 phản hồi:** Hệ thống nhận diện câu hỏi liên quan đến báo lỗi, nhưng thông tin chưa đủ chi tiết để đối chiếu với file JSON."

    return "🤖 **Vua PC v11.0 phản hồi:** Câu hỏi của bạn nằm ngoài phạm vi phân tích. Hãy nhập mã linh kiện cụ thể (VD: i5 6500) hoặc lỗi hệ thống để kiểm tra chính xác."

# THỰC THI NHẬP LIỆU CHAT
if prompt := st.chat_input("Mô tả lỗi máy tính hoặc linh kiện bạn cần chẩn đoán tại đây..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("💾 Bộ lõi V11.0 đang kiểm tra điều kiện điểm sàn..."):
            answer = engine_vua_pc(prompt)
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
