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
    st.markdown("<h2 style='color: #3b82f6; text-align: center;'>🖥️ Vua PC Lab v10.0</h2>", unsafe_allow_html=True)
    st.success("⚡ ENGINE: KHÓA BẢO VỆ ĐA LỚP")
    st.markdown("---")
    st.write("📊 **Trạng thái cốt lõi:**")
    st.info("✔️ Quét Substring triệt để (Không sợ dính chữ)")
    st.info("✔️ Chặn nhận vơ mã số (i5-14400 vs i5-6500)")
    st.info("✔️ Giữ nguyên vẹn Data JSON của Chung")
    st.markdown("---")
    st.warning("🤖 Phiên bản: Tối ưu chấm giải STEM")
    st.info("👨‍💻 Tác giả:\n\n**Lê Văn Chung - Lớp 10A4**")

st.markdown('<div class="neon-title">👑 VUA PC - BẢN KHÓA LOGIC TỐI THƯỢNG V10.0</div>', unsafe_allow_html=True)
st.markdown('<div class="neon-subtitle">BỘ LÕI CHUẨN HÓA KHÔNG ĐỤNG DATA CỦA: LÊ VĂN CHUNG - LỚP 10A4</div>', unsafe_allow_html=True)
st.markdown("---")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

# ==========================================
# THUẬT TOÁN TÍNH ĐIỂM CHUẨN XÁC CAO (V10.0)
# ==========================================
def calculate_match_score(item, q_clean, user_numbers):
    score = 0
    item_kws = [str(kw).lower().strip() for kw in item.get("keywords", [])]
    
    # 1. Đếm điểm từ khóa bằng cách quét chuỗi con (Chống hoàn toàn lỗi gõ liền, gõ dính chữ)
    for kw in item_kws:
        if kw in q_clean:
            score += 1
            
    if score == 0:
        return 0

    # 2. KIỂM TRA XUNG ĐỘT MÃ SỐ (Ví dụ: Database có số 6500, user gõ số 14400 -> Trả về 0 luôn)
    item_numbers = [re.sub(r'\D', '', kw) for kw in item_kws if re.search(r'\d{3,}', kw)]
    item_numbers = [n for n in item_numbers if n]
    
    if item_numbers and user_numbers:
        # Nếu có gõ số nhưng không trùng bất kỳ số định danh nào trong item này -> Loại luôn
        if not set(item_numbers).intersection(set(user_numbers)):
            return 0
            
    return score

def engine_vua_pc(user_query):
    # Chuẩn hóa chuỗi đầu vào (Làm phẳng, xóa ký tự đặc biệt thừa nhưng giữ nguyên chữ số liền nhau)
    q_clean = user_query.lower().strip()
    q_clean = re.sub(r'[-–_,.\?!\(\)]', ' ', q_clean) # Biến gạch ngang thành khoảng trắng để dễ khớp
    q_clean_compact = q_clean.replace(" ", "") # Chuỗi viết liền để bắt các cụm gõ dính
    
    # Xử lý lời chào nhanh
    if any(w in q_clean.split() for w in ["hi", "hello", "chào", "alo"]):
        return "👋 **Xin chào! Tôi là Vua PC v10.0.** Hệ thống đã được tối ưu hóa bộ lọc tìm kiếm chuỗi con. Bạn cần chẩn đoán lỗi hay kiểm tra thông số thiết bị nào?"

    # Trích xuất toàn bộ số từ câu hỏi của user để check xung đột (ví dụ: 14400, 6500, 110)
    user_numbers = [re.sub(r'\D', '', w) for w in q_clean.split() if re.search(r'\d{3,}', w)]
    user_numbers = [n for n in user_numbers if n]

    best_match = None
    max_score = 0
    match_pool = ""

    # Quét đồng thời trên cả 2 kho bằng thuật toán khóa số
    for item in data_pc.get("linh_kien_pc", []):
        score = calculate_match_score(item, q_clean, user_numbers)
        # Quét thêm cả chuỗi viết liền phòng trường hợp user gõ dính
        score_compact = calculate_match_score(item, q_clean_compact, user_numbers)
        final_score = max(score, score_compact)
        
        if final_score > max_score:
            max_score = final_score
            best_match = item
            match_pool = "linh_kien"

    for item in data_pc.get("loi_he_thong", []):
        score = calculate_match_score(item, q_clean, user_numbers)
        score_compact = calculate_match_score(item, q_clean_compact, user_numbers)
        final_score = max(score, score_compact)
        
        if final_score > max_score:
            max_score = final_score
            best_match = item
            match_pool = "loi"

    # PHÂN PHỐI ĐẦU RA KHI CÓ KẾT QUẢ KHỚP UY TÍN
    if max_score >= 1 and best_match:
        if match_pool == "loi":
            return f"### 🎯 Phân tích phát hiện lỗi: {best_match['ten']}\n⚠️ **Phân loại:** `{best_match['loai']}`\n\n❌ **Nguyên nhân cốt lõi:** {best_match['nguyen_nhan']}\n\n🛠️ **Phác đồ khắc phục:**\n{best_match['giai_phap']}"
        else:
            return f"### 📦 Thông tin linh kiện: {best_match['ten']}\n⚙️ **Thông số kỹ thuật:** {best_hw_match if 'thong_so' not in best_match else best_match['thong_so']}\n\n💡 **Tư vấn từ Chung 10A4:** *{best_match['chuyen_gia_tu_van']}*"

    # TẦNG TỪ CHỐI THÔNG MINH DỰA TRÊN TỪ KHÓA BÁO HIỆU TẦNG SÂU
    hardware_keywords = ["i3", "i5", "i7", "i9", "ryzen", "gtx", "rtx", "rx", "h110", "b660", "h610", "main", "chip", "cpu", "vga", "card"]
    error_keywords = ["xanh", "sập", "đen", "lỗi", "bsod", "dump", "treo", "đơ", "bíp"]

    if any(kw in q_clean for kw in hardware_keywords):
        return f"🤖 **Vua PC v10.0 phản hồi:** Hệ thống nhận diện từ khóa liên quan đến phần cứng máy tính.\n\n⚠️ Tuy nhiên, mã linh kiện này hiện **chưa được nạp** vào kho dữ liệu `linh_kien_pc` trong file JSON hiện tại.\n💡 *Mẹo: Hãy giữ nguyên code và bổ sung thêm khối linh kiện này vào file JSON nhé!*"
        
    if any(kw in q_clean for kw in error_keywords):
        return f"🤖 **Vua PC v10.0 phản hồi:** Hệ thống nhận diện bạn đang báo lỗi máy tính.\n\n⚠️ Hiện tại pan bệnh này chưa khớp với kịch bản nào trong danh mục `loi_he_thong` của file JSON."

    return "🤖 **Vua PC v10.0 phản hồi:** Câu hỏi của bạn chưa chứa đủ từ khóa định danh để hệ thống đối chiếu với file JSON. Bạn vui lòng nhập rõ mã linh kiện (VD: i5 6500) hoặc mô tả lỗi (VD: máy bị xanh màn) nhé!"

# THỰC THI NHẬP LIỆU CHAT
if prompt := st.chat_input("Mô tả lỗi máy tính hoặc linh kiện bạn cần chẩn đoán tại đây..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("💾 Bộ lõi V10.0 đang dò quét file JSON của Chung..."):
            answer = engine_vua_pc(prompt)
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
