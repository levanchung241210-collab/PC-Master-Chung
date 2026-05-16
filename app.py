import streamlit as st
import database_pc as db  # Nạp file dữ liệu database_pc.py
import re

# ==========================================
# CẤU HÌNH GIAO DIỆN DARK THEME NEON HÚT MẮT
# ==========================================
st.set_page_config(
    page_title="Chatbot PC - Lê Văn Chung 10A4",
    page_icon="🖥️",
    layout="wide"
)

st.markdown("""
<style>
/* ===== NỀN KHÔNG GIAN TỐI ===== */
.stApp {
    background: linear-gradient(135deg, #020617, #0f172a, #1e1b4b);
    color: #f8fafc;
}

/* ===== HIỆU ỨNG CHỮ NEON HÚT MẮT ===== */
.neon-title {
    text-align: center;
    font-size: 42px !important;
    font-weight: 900 !important;
    color: #ffffff;
    text-shadow: 
        0 0 5px #3b82f6,
        0 0 10px #3b82f6,
        0 0 20px #2563eb,
        0 0 40px #1d4ed8;
    margin-bottom: 5px;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.neon-subtitle {
    text-align: center;
    color: #38bdf8;
    font-size: 18px !important;
    font-weight: 500;
    letter-spacing: 1px;
    margin-bottom: 25px;
    text-shadow: 0 0 8px rgba(56, 189, 248, 0.5);
}

/* ===== KHUNG CHAT USER VÀ BOT CHUYÊN NGHIỆP ===== */
[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) {
    background: linear-gradient(135deg, #1d4ed8, #1e40af);
    border-radius: 16px;
    padding: 15px;
    margin-bottom: 12px;
    box-shadow: 0 4px 12px rgba(29, 78, 216, 0.3);
    border-left: 5px solid #60a5fa;
}

[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-assistant"]) {
    background: rgba(15, 23, 42, 0.8);
    border-radius: 16px;
    padding: 15px;
    margin-bottom: 12px;
    border: 1px solid #334155;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
    border-left: 5px solid #3b82f6;
}

/* ===== KHUNG NHẬP LIỆU ĐÈN LED TỰ PHÁT SÁNG ===== */
.stChatInput input {
    background-color: #0f172a !important;
    color: #ffffff !important;
    border-radius: 12px !important;
    border: 2px solid #3b82f6 !important;
    box-shadow: 0 0 10px rgba(59, 130, 246, 0.5) !important;
    font-size: 16px;
}

.stChatInput input:focus {
    border-color: #38bdf8 !important;
    box-shadow: 0 0 15px rgba(56, 189, 248, 0.8) !important;
}

/* ===== CẤU HÌNH THANH BÊN SIDEBAR ===== */
section[data-testid="stSidebar"] {
    background-color: #020617;
    border-right: 1px solid #1e293b;
}

/* ===== THANH CUỘN CÔNG NGHỆ ===== */
::-webkit-scrollbar {
    width: 8px;
}
::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #3b82f6, #38bdf8);
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# --- THANH BÊN SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='color: #3b82f6; text-align: center;'>🖥️ Control Panel</h2>", unsafe_allow_html=True)
    st.success("⚡ HỆ THỐNG: SIÊU TỐC ĐỘ (OFFLINE)")
    st.markdown("---")
    st.write("📊 **Dữ liệu nạp sẵn:**")
    st.info(f"✔️ {len(db.LOI_HE_THONG)} Mã lỗi hệ thống nâng cao")
    st.info(f"✔️ {len(db.BEEP_CODES)} Mã âm thanh phần cứng BIOS")
    st.info(f"✔️ {len(db.LINH_KIEN_PC)} Danh mục thông số linh kiện")
    st.markdown("---")
    st.warning("🤖 **Phiên bản:** Chatbot K-Matching v2.5")
    st.markdown("---")
    st.info("👨‍💻 **Tác giả dự án STEM:**\n\n**Lê Văn Chung - Lớp 10A4**")

# --- TIÊU ĐỀ ĐƯỢC THIẾT KẾ THEO YÊU CẦU ---
st.markdown('<div class="neon-title">🤖 CHATBOT CHUYÊN GIA PC</div>', unsafe_allow_html=True)
st.markdown('<div class="neon-subtitle">PHÁT TRIỂN BỞI: LÊ VĂN CHUNG - LỚP 10A4</div>', unsafe_allow_html=True)
st.markdown("---")

# --- KHỞI TẠO LỊCH SỬ CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- THUẬT TOÁN TÌM KIẾM CHUẨN HÓA LOGIC ---
def engine_chuyen_gia(user_query):
    q_raw = user_query.lower().strip()
    q_clean = re.sub(re.compile(r'[^\w\s\-]'), '', q_raw) 
    q_no_space = q_clean.replace(" ", "")
    
    ket_qua = []

    # 1. Khớp kho mã lỗi hệ thống
    for key, info in db.LOI_HE_THONG.items():
        key_clean = key.lower().replace(" ", "").replace("_", "")
        if key in q_clean or key_clean in q_no_space or q_clean in info["ten"].lower():
            res = f"### 🎯 Phát hiện lỗi: {info['ten']} (`{info['loai']}`)\n"
            res += f"❌ **Nguyên nhân chính:** {info['nguyen_nhan']}\n\n"
            res += "🛠️ *Phác đồ sửa chữa chuyên sâu từng bước:*\n"
            for step in info["giai_phap"]:
                res += f"{step}\n"
            ket_qua.append(res)
            break 

    # 2. Khớp tiếng kêu bíp BIOS
    if any(keyword in q_clean for keyword in ["tít", "bíp", "tit", "bip", "kêu"]):
        for key, info in db.BEEP_CODES.items():
            key_match = key.lower().replace(" ", "")
            if key_match in q_no_space or q_no_space in key_match:
                res = f"### 🔊 Giải mã âm thanh BIOS: {key.upper()}\n"
                res += f"🚨 **Tình trạng phần cứng:** {info['tinh_trang']}\n"
                if "xu_ly" in info:
                    res += f"🔧 **Hướng xử lý:** {info['xu_ly']}\n"
                ket_qua.append(res)
                break

    # 3. Khớp thông số linh kiện phần cứng
    for key, info in db.LINH_KIEN_PC.items():
        key_clean = key.lower().replace(" ", "").replace("-", "")
        if key_clean in q_no_space:
            res = f"### 📦 Linh kiện: {info['ten']}\n"
            res += f"⚙️ **Thông số cốt lõi:** {info['thong_so']}\n"
            if "socket" in info:
                res += f"🔌 **Chuẩn chân cắm (Socket):** `{info['socket']}`\n"
            if "main_tuong_thich" in info:
                res += f"📋 **Dòng Bo mạch chủ tương thích:** {', '.join(info['main_tuong_thich'])}\n"
            res += f"⚡ **Yêu cầu bộ nguồn (PSU):** {info['nguon_khuyen_nghi']}\n\n"
            res += f"💡 **Tư vấn từ Chuyên gia:** *{info['chuyen_gia_tu_van']}*"
            ket_qua.append(res)
            break

    if ket_qua:
        return "\n\n---\n\n".join(ket_qua)
    
    return ("🤖 **Chatbot phản hồi:** Tôi đã ghi nhận mô tả này. Tuy nhiên, mã hiệu/linh kiện này "
            "nằm ngoài danh sách được nạp sẵn trong cơ sở dữ liệu cục bộ.\n\n"
            "💡 *Mẹo cho bạn: Hãy thử nhập các từ khóa như: i5-6500, memory_management, gtx 1650, tít dài liên tục.*")

# --- XỬ LÝ NHẬP LIỆU ---
if prompt := st.chat_input("Nhập mã lỗi Windows, tiếng kêu máy tính hoặc tên linh kiện..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("💾 Đang truy xuất ma trận dữ liệu cục bộ..."):
            answer = engine_chuyen_gia(prompt)
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
p
