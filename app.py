import streamlit as st
import json
import re
import os

# CẤU HÌNH GIAO DIỆN NEON CYBERPUNK
st.set_page_config(page_title="Vua PC Chatbot - Lê Văn Chung 10A4", page_icon="🖥️", layout="wide")

st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #020617, #0f172a, #1e1b4b); color: #f8fafc; }
.neon-title { text-align: center; font-size: 42px !important; font-weight: 900 !important; color: #ffffff; text-shadow: 0 0 10px #3b82f6, 0 0 30px #1d4ed8; }
.neon-subtitle { text-align: center; color: #38bdf8; font-size: 18px !important; font-weight: 500; }
[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) { background: linear-gradient(135deg, #1d4ed8, #1e40af); border-radius: 16px; border-left: 5px solid #60a5fa; }
[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-assistant"]) { background: rgba(15, 23, 42, 0.8); border-radius: 16px; border: 1px solid #334155; border-left: 5px solid #3b82f6; }
.stChatInput input { background-color: #0f172a !important; color: #ffffff !important; border: 2px solid #3b82f6 !important; }
section[data-testid="stSidebar"] { background-color: #020617; border-right: 1px solid #1e293b; }
</style>
""", unsafe_allow_html=True)

# ĐỌC CƠ SỞ DỮ LIỆU JSON KHỔNG LỒ
def load_database():
    if os.path.exists("database_pc.json"):
        with open("database_pc.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {"loi_he_thong": [], "linh_kien_pc": []}

data_pc = load_database()

# THANH SIDEBAR PANEL
with st.sidebar:
    st.markdown("<h2 style='color: #3b82f6; text-align: center;'>🖥️ Control Panel</h2>", unsafe_allow_html=True)
    st.success("⚡ HỆ THỐNG: SIÊU TỐC ĐỘ VUA PC")
    st.markdown("---")
    st.write("📊 **Bộ nhớ Hệ chuyên gia:**")
    st.info(f"✔️ Thuật toán phân tách ý định")
    st.info(f"✔️ Quản lý danh mục qua JSON dữ liệu lớn")
    st.markdown("---")
    st.warning("🤖 Phiên bản: Vua PC AI Engine v5.0")
    st.info("👨‍💻 Tác giả dự án STEM:\n\n**Lê Văn Chung - Lớp 10A4**")

st.markdown('<div class="neon-title">👑 VUA PC - CHATBOT HỆ CHUYÊN GIA NÂNG CAO</div>', unsafe_allow_html=True)
st.markdown('<div class="neon-subtitle">BỘ LÕI ĐA TẦNG PHÁT TRIỂN BỞI: LÊ VĂN CHUNG - LỚP 10A4</div>', unsafe_allow_html=True)
st.markdown("---")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

# ==========================================
# THUẬT TOÁN TƯ DUY PHÂN TÁCH Ý ĐỊNH VÀ CHẤM ĐIỂM
# ==========================================
def engine_vua_pc(user_query):
    q_clean = user_query.lower().strip()
    user_words = re.sub(r'[^\w\s]', ' ', q_clean).split()
    
    if not user_words:
        return "🤖 Vui lòng nhập nội dung câu hỏi rõ ràng để tôi chẩn đoán nhé!"

    # 1. XỬ LÝ CHÀO HỎI
    if any(w in ["hi", "hello", "chào", "xin chào", "alo"] for w in user_words):
        return ("👋 **Xin chào! Tôi là Vua PC - Hệ chuyên gia trợ lý máy tính lớp 10A4.**\n\n"
                "Tôi đã được nâng cấp bộ lọc ý định tránh nhận diện sai. Bạn cần tôi kiểm tra lỗi hệ thống hay tư vấn thông số linh kiện phần cứng?")

    # 2. PHÂN TÍCH Ý ĐỊNH (INTENT CLASSIFICATION)
    tu_van_keywords = ["chạy", "được", "không", "ko", "so", "sánh", "mạnh", "hơn", "max", "hiệu", "năng", "tư", "vấn", "thông", "số"]
    is_tu_van_hardware = any(w in tu_van_keywords for w in user_words)

    best_match = None
    max_score = 0

    # TẦNG LUẬT 1: NẾU LÀ Ý ĐỊNH HỎI THÔNG SỐ/TƯ VẤN -> CHỈ QUÉT KHO LINH KIỆN
    if is_tu_van_hardware:
        for item in data_pc.get("linh_kien_pc", []):
            score = 0
            for word in user_words:
                if word in item["keywords"]:
                    score += 1
            if score > max_score:
                max_score = score
                best_match = {"type": "linh_kien", "data": item}
                
    # TẦNG LUẬT 2: NẾU KHÔNG CÓ TỪ KHÓA TƯ VẤN -> TIẾN HÀNH QUÉT KHO LỖI TRƯỚC, LINH KIỆN SAU
    else:
        for item in data_pc.get("loi_he_thong", []):
            score = 0
            for word in user_words:
                if word in item["keywords"]:
                    score += 1
            if score > max_score:
                max_score = score
                best_match = {"type": "loi", "data": item}
                
        if max_score == 0: # Nếu kho lỗi không trùng, quét thử kho linh kiện
            for item in data_pc.get("linh_kien_pc", []):
                score = 0
                for word in user_words:
                    if word in item["keywords"]:
                        score += 1
                if score > max_score:
                    max_score = score
                    best_match = {"type": "linh_kien", "data": item}

    # 3. ĐÁNH GIÁ CHẤT LƯỢNG ĐẦU RA VÀ PHẢN HỒI
    # Thiết lập ngưỡng: Phải trùng ít chơi là 2 từ khóa hoặc từ khóa mang tính định danh cao thì mới xuất kết quả
    if max_score >= 2 and best_match:
        res_data = best_match["data"]
        if best_match["type"] == "loi":
            response = f"### 🎯 Phân tích phát hiện lỗi: {res_data['ten']}\n"
            response += f"⚠️ **Phân loại:** `{res_data['loai']}`\n\n"
            response += f"❌ **Nguyên nhân cốt lõi:** {res_data['nguyen_nhan']}\n\n"
            response += f"🛠 **Phác đồ khắc phục chuyên sâu:**\n{res_data['giai_phap']}"
            return response
        else:
            response = f"### 📦 Thông tin linh kiện: {res_data['ten']}\n"
            response += f"⚙️ **Thông số kỹ thuật:** {res_data['thong_so']}\n\n"
            response += f"💡 **Tư vấn cấu hình từ Chung 10A4:** *{res_data['chuyen_gia_tu_van']}*"
            return response

    # 4. TẦNG TỪ CHỐI THÔNG MINH (KHI KHÔNG ĐỦ ĐIỂM HOẶC KHÔNG TÌM THẤY TRONG DATABASE)
    if is_tu_van_hardware:
        return ("🤖 **Vua PC phản hồi:** Tôi nhận thấy bạn đang muốn tư vấn hoặc so sánh thông số linh kiện phần cứng.\n\n"
                "Tuy nhiên, linh kiện này (hoặc cặp linh kiện đối đầu này) hiện chưa được nạp dữ liệu thông số vào file `database_pc.json` cục bộ của hệ thống.\n"
                "💡 *Mẹo cho Chung: Hãy mở file JSON ra và bổ sung thêm từ khóa của thiết bị này vào danh mục `linh_kien_pc` nhé!*")
    else:
        return ("🤖 **Vua PC phản hồi:** Hệ thống đã bóc tách từ khóa mô tả của bạn nhưng chưa tìm thấy mã lỗi nào có phác đồ sửa chữa tương ứng trong cơ sở dữ liệu.\n\n"
                "💡 *Mẹo: Bạn có thể kiểm tra lại chính tả hoặc bổ sung thêm kịch bản sửa lỗi này vào kho lưu trữ `loi_he_thong` trong file JSON.*")

# XỬ LÝ NHẬP LIỆU CHAT
if prompt := st.chat_input("Mô tả lỗi máy tính hoặc linh kiện bạn cần chẩn đoán tại đây..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("💾 Thuật toán đang bóc tách ý định và chấm điểm ma trận..."):
            answer = engine_vua_pc(prompt)
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
