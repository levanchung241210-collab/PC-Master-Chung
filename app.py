import streamlit as st
import json
import re
import os
import random
from groq import Groq

# CẤU HÌNH GIAO DIỆN CHUẨN ĐỂ KHÔNG BỊ TRÀN PC
st.set_page_config(
    page_title="PC Solving System — Lê Văn Chung 10A4",
    page_icon="⚡",
    layout="centered"
)

st.markdown("""
<style>
/* Nhúng font chữ Cyberpunk/Valorant: Barlow Condensed cho tên tác giả, Oswald cho tiêu đề góc cạnh */
@import url('https://fonts.googleapis.com/css2?family=Oswald:wght@700&family=Barlow+Condensed:wght@400;600;700;800&family=Barlow:wght@300;400;500;600&display=swap');

/* ==============================
   VALORANT CORE PALETTE
============================== */
:root {
    --valo-red:       #ff4655;
    --valo-red-dim:   #2a1618;
    --valo-red-glow:  rgba(255, 70, 85, 0.18);
    --valo-red-faint: rgba(255, 70, 85, 0.06);

    --valo-teal:      #00d4bf;
    --valo-teal-dim:  #0b1e1d;
    --valo-teal-glow: rgba(0, 212, 191, 0.08);

    --valo-gold:      #c8aa6e;

    --bg0: #0b0e14;
    --bg1: #12161f;
    --bg2: #181c28;
    --bg3: #1e2232;

    --cream:  #ece8e1;
    --white:  #ffffff;
    --silver: #b5b2ad;
    --muted:  #7a7875;
    --dim:    #454851;

    --br-red:  rgba(255, 70, 85, 0.22);
    --br-teal: rgba(0, 212, 191, 0.3);
    --br-w:    rgba(255, 255, 255, 0.06);
    --br-w2:   rgba(255, 255, 255, 0.10);
}

/* ==============================
   BASE - FIX BACKGROUND LVC STYLE VALORANT (PC & ĐIỆN THOẠI)
============================== */
html, body, .stApp {
    background: var(--bg0) !important;
    color: var(--cream) !important;
    font-family: 'Barlow', sans-serif !important;
}

/* Ép chữ LVC góc cạnh chìm hẳn dưới nền bằng SVG Vector, bao mượt cả Mobile + PC */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 0; 
    opacity: 0.06;
    background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%"><text x="50%" y="55%" font-family="Oswald, Impact, sans-serif" font-size="28vw" font-weight="900" fill="none" stroke="%23ff4655" stroke-width="4" stroke-dasharray="15 10" text-anchor="middle" dominant-baseline="middle">LVC</text></svg>');
    background-position: center center;
    background-repeat: no-repeat;
    background-size: cover;
}

/* Thêm lớp vân sọc chéo phụ của Valorant để tăng độ gai góc */
.stApp::after {
    content: '';
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 0;
    opacity: 0.08;
    background: 
        repeating-linear-gradient(
            -52deg,
            transparent 0px, transparent 60px,
            var(--valo-red) 60px, var(--valo-red) 61px
        );
}

/* Top bar accent đỏ phe tấn công (Khóa trên cùng) */
.valo-top-line {
    position: fixed;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg,
        var(--valo-red) 0%,
        var(--valo-red) 80px,
        transparent 260px,
        transparent calc(100% - 260px),
        var(--valo-teal) calc(100% - 80px),
        var(--valo-teal) 100%
    );
    z-index: 9999;
}

/* ==============================
   HEADER BỐ CỤC CHUẨN
============================== */
.valo-header {
    text-align: center;
    padding: 10px 0 2px;
    position: relative;
    z-index: 10;
}

.valo-author {
    position: absolute;
    top: 8px; right: 0;
    font-family: 'Barlow Condensed', sans-serif !important;
    font-size: 13px !important;
    font-weight: 800 !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    color: var(--valo-teal) !important;
    display: flex;
    align-items: center;
    gap: 5px;
    line-height: 1;
}

.valo-eyebrow {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: clamp(9px, 2vw, 11px);
    font-weight: 700;
    letter-spacing: 6px;
    color: var(--valo-red);
    text-transform: uppercase;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
}
.valo-eyebrow::before,
.valo-eyebrow::after {
    content: '';
    display: inline-block;
    width: 32px; height: 1px;
    background: var(--valo-red);
    opacity: 0.6;
}

.valo-logo-wrap {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 14px;
    margin-bottom: 4px;
}
.valo-logo-icon {
    font-size: clamp(28px, 6vw, 40px);
    filter: drop-shadow(0 0 12px rgba(255,70,85,0.6));
}
.valo-title {
    font-family: 'Oswald', sans-serif !important;
    font-size: clamp(30px, 7.5vw, 62px) !important;
    font-weight: 700 !important;
    letter-spacing: 1px !important;
    line-height: 1;
    color: var(--white);
    text-transform: uppercase;
    margin: 0;
    text-shadow: 0 0 40px rgba(255,70,85,0.15);
}
.valo-title .red   { color: var(--valo-red); }
.valo-title .slash {
    color: var(--valo-red);
    font-weight: 500;
    opacity: 0.6;
    margin: 0 2px;
}

.valo-subtitle {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: clamp(11px, 2.5vw, 13px);
    font-weight: 600;
    letter-spacing: 5px;
    color: var(--silver);
    text-transform: uppercase;
    margin-top: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
}
.valo-subtitle .dot {
    display: inline-block;
    width: 3px; height: 3px;
    background: var(--valo-teal);
    transform: rotate(45deg);
}

.valo-divider {
    display: flex;
    align-items: center;
    gap: 8px;
    margin: 12px 0 8px;
}
.valo-divider::before,
.valo-divider::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--br-w);
}
.valo-divider-inner {
    display: flex;
    align-items: center;
    gap: 5px;
}
.valo-diam {
    width: 5px; height: 5px;
    transform: rotate(45deg);
}
.valo-diam.r { background: var(--valo-red); }
.valo-diam.t { background: var(--valo-teal); width: 4px; height: 4px; opacity: 0.7; }
.valo-dbar {
    width: 50px; height: 2px;
    background: linear-gradient(90deg, var(--valo-red), var(--valo-teal));
    clip-path: polygon(5px 0%, 100% 0%, calc(100% - 5px) 100%, 0% 100%);
}

/* ==============================
   KHUNG LỚN HỆ THỐNG (CỐ ĐỊNH)
============================== */
.valo-greeting {
    position: relative;
    background: linear-gradient(135deg, var(--bg2) 0%, var(--bg1) 100%);
    border: 1px solid var(--br-red);
    border-top: 2px solid var(--valo-red);
    border-radius: 2px;
    padding: clamp(18px,5vw,28px) clamp(16px,5vw,28px) clamp(14px,4vw,22px);
    margin: 4px 0 6px;
    overflow: hidden;
    z-index: 10;
}

.valo-greeting::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    border-style: solid;
    border-width: 22px 22px 0 0;
    border-color: var(--bg0) transparent transparent transparent;
}

.valo-vbar {
    position: absolute;
    left: 0; top: 18%; bottom: 18%;
    width: 3px;
    background: linear-gradient(180deg, transparent 0%, var(--valo-red) 30%, var(--valo-teal) 70%, transparent 100%);
    opacity: 0.55;
}

.valo-status-row {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    margin-bottom: 10px;
}
.valo-status-dot {
    width: 6px; height: 6px;
    background: var(--valo-teal);
    border-radius: 50%;
    box-shadow: 0 0 6px var(--valo-teal);
    animation: pulse 2s infinite;
}
.valo-status-text {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 3px;
    color: var(--valo-teal);
    text-transform: uppercase;
}

@keyframes pulse {
    0%, 100% { opacity: 1; box-shadow: 0 0 6px var(--valo-teal); }
    50%       { opacity: 0.5; box-shadow: 0 0 2px var(--valo-teal); }
}

.valo-greeting-icon {
    font-size: clamp(30px, 6vw, 38px);
    display: block;
    text-align: center;
    margin-bottom: 8px;
    filter: drop-shadow(0 0 10px rgba(255,70,85,0.5));
}
.valo-greeting-title {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: clamp(15px, 4vw, 21px);
    font-weight: 700;
    color: var(--white);
    text-align: center;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 8px;
}
.valo-greeting-sub {
    font-size: clamp(12px, 3vw, 13.5px);
    color: var(--silver);
    text-align: center;
    line-height: 1.7;
}

.valo-stats {
    display: flex;
    justify-content: center;
    gap: clamp(12px, 3vw, 24px);
    margin-top: 14px;
    padding-top: 12px;
    border-top: 1px solid var(--br-w);
}
.valo-stat {
    text-align: center;
    line-height: 1.2;
}
.valo-stat-num {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: clamp(16px, 4vw, 22px);
    font-weight: 700;
    color: var(--valo-red);
    display: block;
}
.valo-stat-label {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 9px;
    letter-spacing: 2px;
    color: var(--dim);
    text-transform: uppercase;
}
.valo-stat-divider {
    width: 1px;
    background: var(--br-w2);
    align-self: stretch;
}

/* ==============================
   CHỮ "CHỌN VẤN ĐỀ" CÂN ĐỐI 100%
============================== */
.valo-suggest-label {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 15px;
    margin: 20px 0 12px;
    width: 100%;
    z-index: 10;
}
.valo-suggest-label::before,
.valo-suggest-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: rgba(255, 255, 255, 0.15);
}
.valo-suggest-label span {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 3px;
    color: var(--silver);
    text-transform: uppercase;
    white-space: nowrap;
}

/* ==============================
   BUTTONS GỢI Ý CỐ ĐỊNH
============================== */
.stButton > button {
    background: var(--bg2) !important;
    color: #c8c4be !important;
    border: 1px solid var(--br-w2) !important;
    border-left: 2px solid rgba(255,70,85,0.25) !important;
    border-radius: 2px !important;
    font-family: 'Barlow Condensed', sans-serif !important;
    font-size: clamp(11px, 3vw, 13px) !important;
    font-weight: 700 !important;
    letter-spacing: 0.5px !important;
    padding: 10px 14px !important;
    width: 100% !important;
    text-align: left !important;
    white-space: normal !important;
    height: auto !important;
    min-height: 46px !important;
    line-height: 1.4 !important;
    transition: all 0.12s ease !important;
    z-index: 10;
}
.stButton > button:hover {
    background: linear-gradient(90deg, rgba(255,70,85,0.10), rgba(0,212,191,0.04)) !important;
    border-left-color: var(--valo-red) !important;
    border-color: var(--br-red) !important;
    color: var(--white) !important;
    transform: translateX(3px) !important;
}

/* ==============================
   CHAT MESSAGES
============================== */
[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) {
    background: linear-gradient(90deg, rgba(255,70,85,0.06), transparent);
    border: 1px solid rgba(255,70,85,0.14);
    border-right: 2px solid var(--valo-red);
    border-radius: 2px;
    padding: 12px 16px;
    margin: 5px 0;
    z-index: 10;
}
[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-assistant"]) {
    background: var(--bg1);
    border: 1px solid var(--br-w);
    border-left: 2px solid var(--valo-teal);
    border-radius: 2px;
    padding: 12px 16px;
    margin: 5px 0;
    z-index: 10;
}

[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li {
    font-size: clamp(13px, 3.5vw, 14.5px) !important;
    line-height: 1.75 !important;
    color: #ddd9d3 !important;
}

/* ==============================
   CHAT INPUT
============================== */
.stChatInput textarea {
    background: var(--bg2) !important;
    color: var(--cream) !important;
    border: 1px solid var(--br-w2) !important;
    border-bottom: 2px solid rgba(255,70,85,0.2) !important;
    border-radius: 2px !important;
}

/* HIDE STREAMLIT BRANDING */
#MainMenu, footer, header { visibility: hidden !important; }
.block-container {
    padding-top: 1.2rem !important;
    padding-bottom: 1.5rem !important;
    max-width: 760px !important;
}

@media (max-width: 600px) {
    .block-container { padding: 0.7rem 0.5rem 4.5rem !important; }
    .valo-author { display: none; }
}
</style>
<div class="valo-top-line"></div>
""", unsafe_allow_html=True)

# ========================
# GROQ CLIENT
# ========================
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except KeyError:
    st.error("❌ Chưa cấu hình GROQ_API_KEY trong Secrets!")
    st.stop()

# ========================
# LOAD DATABASE
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

# SIDEBAR
with st.sidebar:
    st.markdown("## ⚡ PC SOLVING SYSTEM")
    st.markdown("---")
    if st.button("⟳ KÍCH HOẠT LẠI", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending_query = None
        st.rerun()
    st.markdown("---")
    st.markdown("<span style='color:#00d4bf; font-weight:bold;'>Tác giả: Lê Văn Chung - 10A4🎓</span>", unsafe_allow_html=True)

# HEADER CỐ ĐỊNH
st.markdown(f"""
<div class="valo-header">
    <div class="valo-author">LÊ VĂN CHUNG · 10A4 🖥️🖥️🖥️</div>
    <div class="valo-eyebrow">⚡ STEM PROJECT CONCEPT DỰ ÁN ỨNG DỤNG HOÀN CHỈNH</div>
    <div class="valo-logo-wrap">
        <span class="valo-logo-icon">🖥</span>
        <div class="valo-title"><span class="white">PC</span><span class="slash">/</span><span class="red">SOLVING</span></div>
    </div>
    <div class="valo-subtitle">
        <span class="dot"></span>
        <span class="sub-1">CHẨN ĐOÁN</span>
        <span class="dot"></span>
        <span class="sub-2">PHÂN TÍCH</span>
        <span class="dot"></span>
        <span class="sub-3">XỬ LÝ TỰ ĐỘNG</span>
        <span class="dot"></span>
    </div>
</div>
<div class="valo-divider">
    <div class="valo-divider-inner">
        <div class="valo-diam r"></div>
        <div class="valo-dbar"></div>
        <div class="valo-diam t"></div>
    </div>
</div>
""", unsafe_allow_html=True)

# TRẠNG THÁI CHAT
if "messages" not in st.session_state: st.session_state.messages = []
if "suggestions" not in st.session_state: st.session_state.suggestions = []
if "pending_query" not in st.session_state: st.session_state.pending_query = None

# Danh sách gợi ý cố định
ALL_SUGGESTIONS = [
    ("⚠ Màn hình xanh chết BSOD", "Máy tính bị màn hình xanh chết, phải làm gì?"),
    ("▪ Màn hình đen không hiển thị", "Máy lên nguồn nhưng màn hình đen, không lên gì"),
    ("◈ PC bíp liên tục khi bật", "Máy tính bíp nhiều tiếng khi khởi động, lỗi gì?"),
    ("◉ Máy chạy chậm bất thường", "Máy tính đột nhiên chạy rất chậm, khắc phục thế nào?"),
    ("🌡️ CPU overheat — quá nóng", "CPU bị overheat, nhiệt độ lên đến 95 độ C"),
    ("◆ RAM có tương thích không", "Làm sao biết RAM có tương thích với mainboard không?"),
    ("⚡ Cần bao nhiêu W nguồn điện", "Cấu hình PC của tôi cần bao nhiêu W nguồn là đủ?"),
    ("🎮 GTX 1650 chơi được game gì", "Card GTX 1650 chơi được những game nào mượt?"),
]

if not st.session_state.suggestions:
    st.session_state.suggestions = random.sample(ALL_SUGGESTIONS, 4)

# ==============================================================
# KHUNG LỚN HỆ THỐNG & NÚT GỢI Ý KHÓA CỐ ĐỊNH Ở TRÊN (KHÔNG MẤT ĐI)
# ==============================================================
st.markdown(f"""
<div class="valo-greeting">
    <div class="valo-vbar"></div>
    <div class="valo-status-row">
        <div class="valo-status-dot"></div>
        <div class="valo-status-text">Hệ thống sẵn sàng</div>
    </div>
    <span class="valo-greeting-icon">⚡</span>
    <div class="valo-greeting-title">Hệ thống phân tích phần cứng máy tính</div>
    <div class="valo-greeting-sub">
        Nhập các chuỗi ký tự mã lỗi hệ thống hoặc điền tên thiết bị phần cứng linh kiện cần tra cứu.<br>
        Hệ thống nhúng thuật toán chẩn đoán tự động sẽ đưa ra giải pháp ngay lập tức.
    </div>
    <div class="valo-stats">
        <div class="valo-stat">
            <span class="valo-stat-num">{db_loi}</span>
            <span class="valo-stat-label">Lỗi hệ thống</span>
        </div>
        <div class="valo-stat-divider"></div>
        <div class="valo-stat">
            <span class="valo-stat-num">{db_lk}</span>
            <span class="valo-stat-label">Linh kiện PC</span>
        </div>
        <div class="valo-stat-divider"></div>
        <div class="valo-stat">
            <span class="valo-stat-num" style="color:var(--valo-teal)">24/7</span>
            <span class="valo-stat-label">Hỗ trợ</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Hiển thị khu vực chọn nhanh vấn đề (Cân đối hoàn hảo, khóa vị trí)
st.markdown('<div class="valo-suggest-label"><span>CHỌN NHANH VẤN ĐỀ</span></div>', unsafe_allow_html=True)
col1, col2 = st.columns(2, gap="small")
for i, (label, query) in enumerate(st.session_state.suggestions):
    with (col1 if i % 2 == 0 else col2):
        if st.button(label, key=f"sug_{i}"):
            st.session_state.pending_query = query

# KHU VỰC LỊCH SỬ CHAT (NẰM DƯỚI)
st.write("---")
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ==============================================================
# THUẬT TOÁN TRA CỨU LOGIC CỤC BỘ (FIX LỖI THỤT DÒNG - INDENTATION)
# ==============================================================
def calculate_match_score(item, q_clean, user_numbers):
    score = 0
    item_kws = [str(kw).lower().strip() for kw in item.get("keywords", [])]
    user_words = q_clean.split()
    for kw in item_kws:
        if kw in user_words or (kw.isdigit() and kw in q_clean):
            score += 1
    if score == 0: 
        return 0
    item_nums = [re.sub(r'\D','',kw) for kw in item_kws if re.search(r'\d{3,}',kw)]
    item_nums = [n for n in item_nums if n]
    if item_nums
