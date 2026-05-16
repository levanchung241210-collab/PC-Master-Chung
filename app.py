import streamlit as st
import json
import re
import os
import random
from groq import Groq

# Cấu hình layout chuẩn của trang
st.set_page_config(
    page_title="PC Solving System — Lê Văn Chung 10A4",
    page_icon="⚡",
    layout="centered"
)

# ══════════════════════════════════════
# GIAO DIỆN HÌNH KHỐI ĐỒNG BỘ CSS NÂNG CAO
# ══════════════════════════════════════
st.markdown("""
<style>
/* Tải các font chữ chuyên dụng: Bebas Neue và Oswald mô phỏng font chữ hẹp, góc vuông của Valorant */
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Oswald:wght@600;700&family=Barlow+Condensed:wght@700;800&family=Barlow:wght@400;500;600&display=swap');

:root {
    --valo-red:       #ff4655;
    --valo-red-dim:   #2a1618;
    --valo-teal:      #00d4bf;
    --valo-teal-dim:  #0b1e1d;
    --valo-bg:        #0f141c;
    --valo-card:      #161d28;
    --valo-border:    #242e3d;
    --white:          #ffffff;
    --muted:          #7e8591;
}

/* Định dạng nền ứng dụng */
html, body, .stApp {
    background-color: var(--valo-bg) !important;
    color: #ece8e1 !important;
    font-family: 'Barlow', sans-serif !important;
}

/* Nền họa tiết lưới mờ đặc trưng */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 0;
    background: 
        linear-gradient(rgba(15, 20, 28, 0.95), rgba(15, 20, 28, 0.95)),
        repeating-linear-gradient(0deg, transparent, transparent 30px, rgba(255,70,85,0.012) 30px, rgba(255,70,85,0.012) 31px),
        repeating-linear-gradient(90deg, transparent, transparent 30px, rgba(0,212,191,0.01) 30px, rgba(0,212,191,0.01) 31px);
}

/* ÉP ĐỒNG BỘ ĐỘ RỘNG KHUNG - SỬA LỖI LỆCH GIỮA PC VÀ ĐIỆN THOẠI */
.block-container {
    max-width: 780px !important;
    margin: 0 auto !important;
    padding-top: 2rem !important;
    padding-bottom: 6rem !important;
}

/* Ép thanh Chat Input mặc định khớp khít với khung hiển thị phía trên trên PC */
[data-testid="stChatInput"] {
    max-width: 780px !important;
    margin: 0 auto !important;
    left: 0 !important;
    right: 0 !important;
    background: transparent !important;
}

[data-testid="stChatInput"] > div {
    background-color: #1c2432 !important;
    border: 1px solid var(--valo-border) !important;
    border-bottom: 2px solid var(--valo-red) !important;
    border-radius: 2px !important;
}

[data-testid="stChatInput"] textarea {
    color: var(--white) !important;
}

/* Ép container chứa các dòng tin nhắn không bị tràn sọc ngang */
[data-testid="stChatMessageContainer"] {
    max-width: 780px !important;
    margin: 0 auto !important;
    padding: 0 !important;
}

/* THIẾT KẾ TIÊU ĐỀ TÁC GIẢ SẮC NÉT (CÓ MÀU TRÊN CẢ PC/MOBILE) */
.valo-author-title {
    font-family: 'Barlow Condensed', sans-serif !important;
    font-size: 15px !important;
    font-weight: 800 !important;
    letter-spacing: 3px !important;
    text-transform: uppercase !important;
    color: var(--valo-teal) !important;
    text-shadow: 0 0 10px rgba(0, 212, 191, 0.5), 2px 2px 0px #000000 !important;
    text-align: center;
    margin-bottom: 4px;
}

.valo-eyebrow {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 5px;
    color: var(--muted);
    text-align: center;
    text-transform: uppercase;
    margin-bottom: 12px;
}

/* THIẾT KẾ FONT VALORANT SẮC CẠNH CHO TIÊU ĐỀ CHÍNH */
.valo-main-heading {
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: clamp(26px, 5.5vw, 38px) !important;
    font-weight: 400 !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    color: var(--white) !important;
    text-align: center !important;
    line-height: 1.1 !important;
    margin: 10px 0 18px 0 !important;
    text-shadow: 2px 2px 0px rgba(0, 0, 0, 0.6) !important;
}

/* KHỐI GREETING PANEL CỐ ĐỊNH */
.valo-greeting-box {
    background: var(--valo-card) !important;
    border: 1px solid var(--valo-border) !important;
    border-left: 4px solid var(--valo-red) !important;
    padding: 22px !important;
    border-radius: 2px !important;
    box-shadow: 0 8px 24px rgba(0,0,0,0.3) !important;
    margin-bottom: 20px !important;
}

.valo-status-indicator {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 10px;
    font-weight: 700;
    color: var(--valo-teal);
    letter-spacing: 1.5px;
    text-transform: uppercase;
    background: rgba(0, 212, 191, 0.06);
    padding: 3px 10px;
    border: 1px solid rgba(0, 212, 191, 0.15);
    border-radius: 2px;
    margin-bottom: 10px;
}

.valo-greeting-text {
    color: #b5b9c0;
    font-size: 14px;
    line-height: 1.6;
    text-align: center;
}

.valo-counter-row {
    display: flex;
    justify-content: center;
    gap: 35px;
    margin-top: 15px;
    padding-top: 12px;
    border-top: 1px solid rgba(255,255,255,0.05);
}
.valo-counter-item { text-align: center; }
.valo-counter-val { font-family: 'Bebas Neue', sans-serif; font-size: 24px; color: var(--valo-red); line-height: 1; }
.valo-counter-lbl { font-family: 'Barlow Condensed', sans-serif; font-size: 10px; color: var(--muted); letter-spacing: 1px; }

/* KHUNG NHÃN CHỌN NHANH VẤN ĐỀ VÁT GÓC */
.valo-section-tag {
    background: var(--valo-red) !important;
    color: var(--white) !important;
    font-family: 'Barlow Condensed', sans-serif !important;
    font-size: 13px !important;
    font-weight: 700 !important;
    letter-spacing: 1.5px !important;
    padding: 5px 18px !important;
    display: inline-block !important;
    clip-path: polygon(8px 0%, 100% 0%, calc(100% - 8px) 100%, 0% 100%) !important;
    margin: 10px 0 15px 0 !important;
}

/* ĐỊNH DẠNG KHUNG ĐOẠN CHAT (AN TOÀN - ĐẬM CHẤT ESPORTS) */
[data-testid="stChatMessage"] {
    border-radius: 2px !important;
    padding: 15px 18px !important;
    margin: 12px 0 !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
}

/* Ép toàn bộ chữ trong khung chat thành màu TRẮNG SÁNG hiển thị rõ trên mọi thiết bị */
[data-testid="stChatMessage"] p, [data-testid="stChatMessage"] li {
    font-size: 15px !important;
    line-height: 1.65 !important;
    color: #ffffff !important;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.9) !important;
}

/* KHUNG CHAT USER (Phe Tiến Công - Đỏ) */
[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) {
    background: linear-gradient(90deg, var(--valo-red-dim) 0%, #150e10 100%) !important;
    border: 1px solid rgba(255, 70, 85, 0.25) !important;
    border-right: 4px solid var(--valo-red) !important;
}

/* KHUNG CHAT BOT (Phe Phòng Thủ - Xanh Teal) */
[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-assistant"]) {
    background: linear-gradient(90deg, var(--valo-teal-dim) 0%, #0d1217 100%) !important;
    border: 1px solid rgba(0, 212, 191, 0.18) !important;
    border-left: 4px solid var(--valo-teal) !important;
}

/* Tiêu đề linh kiện/lỗi bên trong cấu trúc bot */
[data-testid="stChatMessage"] h3 {
    font-family: 'Oswald', sans-serif !important;
    font-size: 18px !important;
    font-weight: 700 !important;
    color: var(--valo-teal) !important;
    text-transform: uppercase !important;
    margin-top: 4px !important;
    border-bottom: 1px solid rgba(255,255,255,0.08) !important;
    padding-bottom: 4px !important;
}

/* KHUNG NÚT BẤM GỢI Ý */
.stButton > button {
    background: #19212c !important;
    color: var(--white) !important;
    border: 1px solid var(--valo-border) !important;
    border-left: 3px solid var(--valo-teal) !important;
    font-family: 'Barlow Condensed', sans-serif !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    padding: 10px 14px !important;
    border-radius: 0px !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
    text-align: left !important;
}
.stButton > button:hover {
    background: var(--valo-border) !important;
    border-color: var(--valo-teal) !important;
    box-shadow: 0 0 12px rgba(0, 212, 191, 0.2) !important;
}

/* Ẩn bớt các thanh header thừa của Streamlit */
#MainMenu, footer, header { visibility: hidden !important; }
</style>
""", unsafe_allow_html=True)

# ========================
# KẾT NỐI API GROQ
# ========================
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except KeyError:
    st.error("❌ Hệ thống phát hiện thiếu cấu hình GROQ_API_KEY trong Secrets!")
    st.stop()
except Exception as e:
    st.error(f"❌ Trục trặc cổng kết nối: {str(e)}")
    st.stop()

# ========================
# TRÍCH XUẤT DATABASE CỤC BỘ
# ========================
def load_database():
    if os.path.exists("database_pc.json"):
        with open("database_pc.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {"loi_he_thong": [], "linh_kien_pc": []}

def load_raw_json():
    if os.path.exists("database_pc.json"):
        with open("database_pc.json", "r", encoding="utf-8") as f:
            return f.read()
    return "{}"

data_pc = load_database()
raw_json_context = load_raw_json()
db_loi = len(data_pc.get("loi_he_thong", []))
db_lk = len(data_pc.get("linh_kien_pc", []))

# ========================
# SIDEBAR ĐIỀU HƯỚNG BÊN TRÁI
# ========================
with st.sidebar:
    st.markdown("### ⚡ PC SOLVING SYSTEM")
    st.markdown("---")
    st.markdown("Hệ thống tự động tra cứu, chẩn đoán pan bệnh máy tính và tư vấn đồng bộ linh kiện.")
    st.markdown("---")
    if st.button("⟳ PHIÊN MỚI", use_container_width=True):
        st.session_state.messages = []
        st.session_state.greeted = False
        st.session_state.suggestions = []
        st.rerun()
    st.markdown("---")
    st.markdown("<span style='color:#00d4bf; font-weight:bold;'>Tác giả: Lê Văn Chung - 10A4</span>", unsafe_allow_html=True)

# ========================
# KHU VỰC TIÊU ĐỀ GIAO DIỆN CHÍNH
# ========================
st.markdown("""
<div style="text-align: center;">
    <div class="valo-author-title">LÊ VĂN CHUNG — LỚP 10A4</div>
    <div class="valo-eyebrow">DỰ ÁN STEM ỨNG DỤNG CÔNG NGHỆ HOÀN CHỈNH</div>
    <div class="valo-main-heading">HỆ THỐNG PHÂN TÍCH PHẦN CỨNG MÁY TÍNH</div>
</div>
""", unsafe_allow_html=True)

# ========================
# KHỞI TẠO BỘ LƯU TRỮ KHÔNG GIAN BỘ NHỚ
# ========================
if "messages" not in st.session_state: st.session_state.messages = []
if "greeted" not in st.session_state: st.session_state.greeted = False
if "suggestions" not in st.session_state: st.session_state.suggestions = []
if "pending_query" not in st.session_state: st.session_state.pending_query = None

# 4 câu hỏi gợi ý nhanh ban đầu
ALL_SUGGESTIONS = [
    ("⚠ Màn hình xanh chết BSOD", "Máy tính bị màn hình xanh chết, phải làm gì?"),
    ("▪ Màn hình đen không hiển thị", "Máy lên nguồn nhưng màn hình đen, không lên gì"),
    ("◈ PC bíp liên tục khi bật", "Máy tính bíp nhiều tiếng khi khởi động, lỗi gì?"),
    ("◉ Máy chạy chậm bất thường", "Máy tính đột nhiên chạy rất chậm, khắc phục thế nào?"),
    ("🌡 CPU overheat — quá nóng", "CPU bị overheat, nhiệt độ lên đến 95 độ C"),
    ("◆ RAM có tương thích mainboard không", "Làm sao biết RAM có tương thích với mainboard không?"),
    ("⚡ Cần bao nhiêu W nguồn điện", "Cấu hình PC của tôi cần bao nhiêu W nguồn là đủ?"),
    ("🎮 Card đồ họa GTX 1650", "Card GTX 1650 chơi được những game nào mượt?"),
]

if not st.session_state.suggestions:
    st.session_state.suggestions = random.sample(ALL_SUGGESTIONS, 4)

# ========================
# KHỐI GREETING PANEL (LUÔN CỐ ĐỊNH Ở ĐẦU)
# ========================
st.markdown(f"""
<div class="valo-greeting-box">
    <div style="text-align:center;">
        <div class="valo-status-indicator">● LIVE OPERATION READY</div>
    </div>
    <div class="valo-greeting-text">
        Chào mừng đến với hệ thống kiểm tra phần cứng tự động. Vui lòng nhập thông số linh kiện, 
        mã hiệu thiết bị hoặc mô tả chi tiết dấu hiệu hư hỏng phần cứng để bắt đầu chẩn đoán kỹ thuật.
    </div>
    <div class="valo-counter-row">
        <div class="valo-counter-item">
            <div class="valo-counter-val">{db_loi}</div>
            <div class="valo-counter-lbl">PAN BỆNH LỖI</div>
        </div>
        <div class="valo-counter-item" style="border-left: 1px dashed rgba(255,255,255,0.1); padding-left: 25px;">
            <div class="valo-counter-val">{db_lk}</div>
            <div class="valo-counter-lbl">LINH KIỆN PC</div>
        </div>
        <div class="valo-counter-item" style="border-left: 1px dashed rgba(255,255,255,0.1); padding-left: 25px;">
            <div class="valo-counter-val" style="color:var(--valo-teal)">ONLINE</div>
            <div class="valo-counter-lbl">TRẠNG THÁI</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Chỉ hiển thị danh sách gợi ý khi chưa có hội thoại
if not st.session_state.messages:
    st.markdown('<div class="valo-section-tag">CHỌN NHANH VẤN ĐỀ</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="small")
    for i, (label, query) in enumerate(st.session_state.suggestions):
        with (col1 if i % 2 == 0 else col2):
            if st.button(label, key=f"sug_{i}"):
                st.session_state.greeted = True
                st.session_state.pending_query = query
                st.rerun()

# ========================
# HIỂN THỊ LỊCH SỬ CHAT TRỰC QUAN
# ========================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ========================
# THUẬT TOÁN ĐỐI CHIẾU DATABASE CỤC BỘ
# ========================
def calculate_match_score(item, q_clean, user_numbers):
    score = 0
    item_kws = [str(kw).lower().strip() for kw in item.get("keywords", [])]
    user_words = q_clean.split()
    for kw in item_kws:
        if kw in user_words or (kw.isdigit() and kw in q_clean):
            score += 1
    if score == 0: return 0
    item_nums = [re.sub(r'\D','',kw) for kw in item_kws if re.search(r'\d{3,}',kw)]
    item_nums = [n for n in item_nums if n]
    if item_nums and user_numbers:
        if not set(item_nums).intersection(set(user_numbers)):
            return 0
    return score

def search_database(user_query):
    q_clean = re.sub(r'[-–_,.\?!\(\)]',' ', user_query.lower().strip())
    user_numbers = [re.sub(r'\D','',w) for w in q_clean.split() if re.search(r'\d{3,}',w)]
    user_numbers = [n for n in user_numbers if n]
    best_match, max_score, match_pool = None, 0, ""
    
    for item in data_pc.get("linh_kien_pc", []):
        s = calculate_match_score(item, q_clean, user_numbers)
        if s > max_score: max_score, best_match, match_pool = s, item, "linh_kien"
    for item in data_pc.get("loi_he_thong", []):
        s = calculate_match_score(item, q_clean, user_numbers)
        if s > max_score: max_score, best_match, match_pool = s, item, "loi"
        
    if max_score >= 2 and best_match:
        if match_pool == "loi":
            return (f"### ✕ {best_match['ten']}\n"
                    f"*Phân loại dữ liệu: Lỗi Hệ Thống*\n\n"
                    f"**⚠ Nguyên nhân:** {best_match['nguyen_nhan']}\n\n"
                    f"**◈ Phác đồ sửa chữa:**\n{best_match['giai_phap']}")
        else:
            return (f"### ◆ {best_match['ten']}\n"
                    f"*Phân loại dữ liệu: Thiết Bị Linh Kiện*\n\n"
                    f"**⚙ Thông số kỹ thuật:** {best_match.get('thong_so','')}\n\n"
                    f"**◉ Socket:** `{best_match.get('socket','')}`\n\n"
                    f"**▶ Tư vấn cấu hình:** {best_match.get('chuyen_gia_tu_van','')}")
    return None

# ========================
# XỬ LÝ DỮ LIỆU QUA AI
# ========================
def ask_engine(user_query, chat_history):
    system_prompt = f"""Bạn là mô hình trí tuệ nhân tạo tích hợp sâu trong Hệ thống Phân tích Phần cứng Máy tính của tác giả học sinh Lê Văn Chung lớp 10A4.
Nghiêm cấm tự xưng là mô hình ngôn ngữ lớn, không nhắc đến Meta, Llama hay Groq.
Khi giải đáp các câu hỏi kỹ thuật, hãy tận dụng tối đa kho tri thức gốc sau đây nếu có dữ liệu phù hợp: {raw_json_context}.
Trình bày mạch lạc bằng tiếng Việt, ngắn gọn, phân chia đề mục rõ ràng."""
    
    messages = [{"role": "system", "content": system_prompt}]
    for msg in chat_history[-6:]:
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": user_query})
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        max_tokens=650,
        temperature=0.4
    )
    return response.choices[0].message.content

# ========================
# LUỒNG TIẾP NHẬN TIN NHẮN CHAT
# ========================
def handle_message(prompt):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        
    with st.chat_message("assistant"):
        with st.spinner("HỆ THỐNG ĐANG QUÉT TOÀN BỘ KHỐI LOGIC..."):
            try:
                answer = search_database(prompt) or ask_engine(prompt, st.session_state.messages)
                final_answer = f"""{answer}\n\n---\n*— Kỹ sư phân tích vận hành: Lê Văn Chung lớp 10A4*"""
                st.markdown(final_answer)
                st.session_state.messages.append({"role": "assistant", "content": final_answer})
            except Exception as e:
                st.error("❌ Kết nối bị gián đoạn hoặc phản hồi quá hạn. Vui lòng thử lại!")

# Xử lý nếu bấm nút gợi ý nhanh
if st.session_state.pending_query:
    q = st.session_state.pending_query
    st.session_state.pending_query = None
    handle_message(q)

# Tiếp nhận dữ liệu gõ trực tiếp từ ô nhập liệu chat
if prompt := st.chat_input("Nhập mã lỗi hoặc linh kiện cần phân tích..."):
    st.session_state.greeted = True
    handle_message(prompt)
