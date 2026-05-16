import streamlit as st
import json
import re
import os

# CONFIG GIAO DIỆN CYBERPUNK HUYẾT NGUYỆT V8.0
st.set_page_config(page_title="Vua PC Chatbot - Lê Văn Chung 10A4", page_icon="🖥️", layout="wide")

st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #020617, #0f172a, #1e1b4b); color: #f8fafc; }
.neon-title { text-align: center; font-size: 42px !important; font-weight: 900 !important; color: #ffffff; text-shadow: 0 0 10px #ef4444, 0 0 30px #b91c1c; }
.neon-subtitle { text-align: center; color: #fca5a5; font-size: 18px !important; font-weight: 500; }
[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) { background: linear-gradient(135deg, #b91c1c, #991b1b); border-radius: 16px; border-left: 5px solid #f87171; }
[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-assistant"]) { background: rgba(15, 23, 42, 0.8); border-radius: 16px; border: 1px solid #334155; border-left: 5px solid #ef4444; }
.stChatInput input { background-color: #0f172a !important; color: #ffffff !important; border: 2px solid #ef4444 !important; }
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
    st.markdown("<h2 style='color: #ef4444; text-align: center;'>🖥️ Control Panel V8</h2>", unsafe_allow_html=True)
    st.success("⚡ HỆ THỐNG: KHÓA CHẾT LỖI LOGIC")
    st.markdown("---")
    st.write("📊 **Trạng thái Engine:**")
    st.info("✔️ Bộ dò xung đột Mã số (ID Conflict Detector)")
    st.info("✔️ Bắt lỗi tuyệt đối các đuôi chip/main")
    st.info("✔️ Miễn nhiễm với hiện tượng vơ đũa cả nắm")
    st.markdown("---")
    st.warning("🤖 Phiên bản: Vua PC AI Engine v8.0")
    st.info("👨‍💻 Tác giả dự án STEM:\n\n**Lê Văn Chung - Lớp 10A4**")

st.markdown('<div class="neon-title">👑 VUA PC - BẢN KHÓA LỖI TỐI THƯỢNG</div>', unsafe_allow_html=True)
st.markdown('<div class="neon-subtitle">BỘ LÕI ĐA TẦNG PHÁT TRIỂN BỞI: LÊ VĂN CHUNG - LỚP 10A4</div>', unsafe_allow_html=True)
st.markdown("---")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

# ==========================================
# THUẬT TOÁN V8.0: BỘ DÒ XUNG ĐỘT MÃ SỐ CỐT LÕI
# ==========================================
def calculate_score(item, user_words):
    score = 0
    item_kws = [str(k).lower() for k in item.get("keywords", [])]
    
    for kw in item_kws:
        if kw in user_words:
            score += 1
            
    # LỌC NGƯỢC: Trích xuất các số định danh (từ 3 chữ số trở lên, ví dụ: 6500, 14400, 110, 3060)
    item_numbers = [re.sub(r'\D', '', kw) for kw in item_kws if re.search(r'\d{3,}', kw)]
    user_numbers = [re.sub(r'\D', '', w) for w in user_words if re.search(r'\d{3,}', w)]
    
    item_numbers = [n for n in item_numbers if n]
    user_numbers = [n for n in user_numbers if n]
    
    # NẾU thiết bị trong database có mã số, VÀ người dùng gõ mã số
    if item_numbers and user_numbers:
        # Kiểm tra xem có chung mã số nào không (Intersection). 
        # Nếu KHÔNG CÓ mã nào chung -> Tức là hỏi 1 đằng, database có 1 nẻo -> Lập tức đánh rớt (-1)
        if not set(item_numbers).intersection(set(user_numbers)):
            return -1
            
    return score

def engine_vua_pc(user_query):
    q_clean = user_query.lower().strip()
    
    # Chuẩn hóa từ lóng phần cứng
    if "xanh màn" in q_clean or "màn xanh" in q_clean: q_clean += " bsod xanh memory management"
    if "sập nguồn" in q_clean or "chạy sập" in q_clean: q_clean += " sập nguồn quá nhiệt tắt"

    user_words = re.sub(r'[^\w\s]', ' ', q_clean).split()
    if not user_words: return "🤖 Vui lòng nhập nội dung rõ ràng!"

    # Xác định luồng (Phần cứng hay Báo lỗi)
    hardware_signals = ["chạy", "được", "không", "ko", "so", "sánh", "mạnh", "hơn", "max", "hiệu", "năng", "tư", "vấn", "thông", "số", "main", "chip", "cpu", "vga", "card", "ram", "buss", "bus"]
    has_hw_name = any(re.search(r'(i3|i5|i7|i9|ryzen|gtx|rtx|rx|dimensity|snapdragon|h110|b660|h610)', w) for w in user_words)
    is_hardware = has_hw_name or any(sig in user_words for sig in hardware_signals)

    best_match = None
    max_score = 0
    match_type = ""

    # Quét theo luồng ưu tiên
    if is_hardware:
        for item in data_pc.get("linh_kien_pc", []):
            score = calculate_score(item, user_words)
            if score > max_score:
                max_score = score
                best_match = item
                match_type = "linh_kien"
    else:
        for item in data_pc.get("loi_he_thong", []):
            score = calculate_score(item, user_words)
            if score > max_score:
                max_score = score
                best_match = item
                match_type = "loi"

    # Xử lý kết quả trả về
    if max_score > 0 and best_match:
        if match_type == "loi":
            return f"### 🎯 Phân tích phát hiện lỗi: {best_match['ten']}\n⚠️ **Phân loại:** `{best_match['loai']}`\n\n❌ **Nguyên nhân cốt lõi:** {best_match['nguyen_nhan']}\n\n🛠️ **Phác đồ khắc phục:**\n{best_match['giai_phap']}"
        else:
            return f"### 📦 Thông tin linh kiện: {best_match['ten']}\n⚙️ **Thông số kỹ thuật:** {best_match['thong_so']}\n\n💡 **Tư vấn từ Chung 10A4:** *{best_match['chuyen_gia_tu_van']}*"

    # Từ chối phân luồng siêu chuẩn
    if is_hardware:
        return f"🤖 **Vua PC v8.0 phản hồi:**\n\nHệ thống nhận diện bạn đang hỏi thông số phần cứng.\n⚠️ Tuy nhiên, mã thiết bị này hiện **chưa được nạp** vào kho dữ liệu `linh_kien_pc` trong file JSON của hệ thống.\n💡 *Mẹo: Hãy bổ sung mã này vào database để bot học thêm kiến thức nhé!*"
    else:
        return "🤖 **Vua PC v8.0 phản hồi:**\n\nHệ thống chưa tìm thấy pan bệnh nào khớp với mô tả lỗi của bạn trong cơ sở dữ liệu.\n💡 *Mẹo: Hãy bổ sung kịch bản xử lý hiện tượng này vào danh mục `loi_he_thong`.*"

# THỰC THI NHẬP LIỆU CHAT
if prompt := st.chat_input("Nhập mã lỗi hoặc tên linh kiện cần chẩn đoán..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("💾 Bộ dò xung đột đang quét mã định danh thiết bị..."):
            answer = engine_vua_pc(prompt)
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
