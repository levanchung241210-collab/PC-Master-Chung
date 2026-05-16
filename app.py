import streamlit as st
import json
import re
import os
import random
import base64
from groq import Groq

# CẤU HÌNH GIAO DIỆN CHUẨN ĐỂ KHÔNG BỊ TRÀN PC
st.set_page_config(
    page_title="PC Solving System — Lê Văn Chung 10A4",
    page_icon="⚡",
    layout="centered"
)

st.markdown("""
<style>
/* Nhúng font chữ có độ thon dài, góc cạnh sắc nét giống font Valorant gốc */
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Oswald:wght@500;700&family=Rajdhani:wght@600;700&family=Barlow+Condensed:wght@400;600;700;800&family=Barlow:wght@300;400;500;600&display=swap');

/* ══════════════════════════════════════
   VALORANT COLOR SYSTEM & TOKENS
══════════════════════════════════════ */
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

/* ══════════════════════════════════════
   BASE & NOISE
══════════════════════════════════════ */
html, body, .stApp {
    background: var(--bg0) !important;
    color: var(--cream) !important;
    font-family: 'Barlow', sans-serif !important;
}

.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 0;
    background:
        repeating-linear-gradient(
            -48deg,
            transparent 0px, transparent 60px,
            rgba(255, 70, 85, 0.018) 60px, rgba(255, 70, 85, 0.018) 61px
        ),
        repeating-linear-gradient(
            42deg,
            transparent 0px, transparent 90px,
            rgba(0, 212, 191, 0.010) 90px, rgba(0, 212, 191, 0.010) 91px
        ),
        repeating-linear-gradient(
            180deg,
            transparent 0px, transparent 4px,
            rgba(255, 255, 255, 0.004) 4px, rgba(255, 255, 255, 0.004) 5px
        );
}

.stApp::after {
    content: '';
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

/* ══════════════════════════════════════
   HEADER CHUẨN ĐỔI MÀU LVC NỔI BẬT
══════════════════════════════════════ */
.valo-header {
    text-align: center;
    padding: 5px 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

/* ĐÃ SỬA: Tên hiển thị rực rỡ, căn giữa tự nhiên, không bị đè chữ */
.valo-author {
    font-family: 'Barlow Condensed', sans-serif !important;
    font-size: clamp(13px, 4vw, 16px) !important;
    font-weight: 800 !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    color: var(--valo-teal) !important; /* Đổi sang màu xanh Neon rực rỡ */
    text-shadow: 0px 0px 8px rgba(0, 212, 191, 0.6) !important; /* Hiệu ứng sáng nổi bật */
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    line-height: 1.2;
}
.valo-author .dot { color: var(--white); }

.valo-eyebrow {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: clamp(9px, 2.5vw, 11px);
    font-weight: 700;
    letter-spacing: 4px;
    color: var(--valo-red);
    text-transform: uppercase;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
}
.valo-eyebrow::before,
.valo-eyebrow::after {
    content: '';
    display: inline-block;
    width: 20px; height: 1px;
    opacity: 0.5;
}
.valo-eyebrow::before { background: linear-gradient(90deg, transparent, var(--valo-red)); }
.valo-eyebrow::after { background: linear-gradient(90deg, var(--valo-red), transparent); }

.valo-logo-wrap {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    margin-bottom: 4px;
}
.valo-logo-icon {
    font-size: clamp(26px, 6vw, 36px);
    filter: drop-shadow(0 0 10px rgba(255, 70, 85, 0.5));
}
.valo-title {
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: clamp(32px, 8vw, 56px) !important;
    font-weight: 400 !important;
    letter-spacing: 2px !important;
    line-height: 1;
    color: var(--white);
    text-transform: uppercase;
    margin: 0;
}
.valo-title .red   { color: var(--valo-red); }
.valo-title .slash {
    color: var(--valo-red);
    opacity: 0.6;
    margin: 0 2px;
}

/* TIÊU ĐỀ KHUNG GREETING CHUẨN OSWALD SẮC CẠNH */
.valo-main-heading {
    font-family: 'Oswald', sans-serif !important;
    font-size: clamp(18px, 4.5vw, 28px) !important;
    font-weight: 700 !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    color: var(--white) !important;
    text-shadow: 2px 2px 0px rgba(0, 0, 0, 0.6) !important;
    margin: 12px 0 !important;
}

.valo-subtitle {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: clamp(11px, 2.8vw, 13px);
    font-weight: 600;
    letter-spacing: 4px;
    color: var(--silver);
    text-transform: uppercase;
    margin-top: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
}
.valo-subtitle .sub-1 { color: var(--valo-red); }
.valo-subtitle .sub-2 { color: var(--white); }
.valo-subtitle .sub-3 { color: var(--valo-teal); }
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
    margin: 10px 0 6px;
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
}

/* ══════════════════════════════════════
   GREETING BOX (CỐ ĐỊNH PHÍA TRÊN)
══════════════════════════════════════ */
.valo-greeting {
    position: relative;
    background: linear-gradient(135deg, rgba(24, 28, 40, 0.85) 0%, rgba(18, 22, 31, 0.95) 100%);
    border: 1px solid var(--br-red);
    border-top: 2px solid var(--valo-red);
    border-radius: 2px;
    padding: clamp(16px, 5vw, 26px) clamp(14px, 4vw, 24px);
    margin: 4px 0 16px;
    overflow: hidden;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.5);
}

.valo-greeting::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    border-style: solid;
    border-width: 20px 20px 0 0;
    border-color: var(--bg0) transparent transparent transparent;
}

.valo-vbar {
    position: absolute;
    left: 0; top: 15%; bottom: 15%;
    width: 3px;
    background: linear-gradient(180deg, transparent 0%, var(--valo-red) 30%, var(--valo-teal) 70%, transparent 100%);
}

.valo-status-row {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    margin-bottom: 8px;
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
    letter-spacing: 2px;
    color: var(--valo-teal);
    text-transform: uppercase;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.4; }
}

.valo-greeting-icon {
    font-size: clamp(28px, 6vw, 34px);
    display: block;
    text-align: center;
    margin-bottom: 6px;
    filter: drop-shadow(0 0 10px rgba(255, 70, 85, 0.5));
}
.valo-greeting-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: clamp(16px, 4vw, 21px);
    font-weight: 700;
    color: var(--white);
    text-align: center;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 8px;
}
.valo-greeting-sub {
    font-size: clamp(12px, 3.2vw, 14px);
    color: var(--cream);
    text-align: center;
    line-height: 1.6;
}

.valo-stats {
    display: flex;
    justify-content: center;
    gap: clamp(10px, 3vw, 20px);
    margin-top: 14px;
    padding-top: 12px;
    border-top: 1px solid var(--br-w);
}
.valo-stat {
    text-align: center;
}
.valo-stat-num {
    font-family: 'Rajdhani', sans-serif;
    font-size: clamp(16px, 4vw, 22px);
    font-weight: 700;
    color: var(--valo-red);
    display: block;
}
.valo-stat-label {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 9px;
    letter-spacing: 1.5px;
    color: var(--muted);
    text-transform: uppercase;
}
.valo-stat-divider {
    width: 1px;
    background: var(--br-w2);
    align-self: stretch;
}

/* ══════════════════════════════════════
   SUGGEST LABEL & BUTTONS
══════════════════════════════════════ */
.valo-suggest-label {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 8px 0 12px;
}
.valo-suggest-label span {
    background: var(--valo-red);
    color: var(--white);
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 3px 14px;
    clip-path: polygon(6px 0, 100% 0, calc(100% - 6px) 100%, 0 100%);
}

.stButton > button {
    background: linear-gradient(90deg, rgba(30, 34, 50, 0.85), rgba(20, 24, 35, 0.95)) !important;
    color: #ffffff !important;
    border: 1px solid rgba(0, 212, 191, 0.2) !important;
    border-left: 3px solid var(--valo-teal) !important;
    border-radius: 2px !important;
    font-family: 'Barlow Condensed', sans-serif !important;
    font-size: clamp(12px, 3.2vw, 14px) !important;
    font-weight: 700 !important;
    padding: 10px 12px !important;
    width: 100% !important;
    text-align: left !important;
    white-space: normal !important;
    min-height: 46px !important;
    transition: all 0.15s ease !important;
}
.stButton > button:hover {
    background: linear-gradient(90deg, rgba(0, 212, 191, 0.15), rgba(255, 70, 85, 0.08)) !important;
    border-color: var(--valo-teal) !important;
    border-left-color: var(--valo-red) !important;
    transform: translateX(3px) !important;
    box-shadow: 0 4px 12px rgba(0, 212, 191, 0.2) !important;
}

/* ══════════════════════════════════════
   CHAT MESSAGES (CHỮ SIÊU RÕ)
══════════════════════════════════════ */
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li {
    font-size: clamp(14px, 3.8vw, 15px) !important;
    line-height: 1.7 !important;
    color: #ffffff !important; 
    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.9) !important;
}

/* Khung User (Omen Red) */
[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) {
    background: linear-gradient(135deg, rgba(55, 15, 20, 0.9) 0%, rgba(18, 10, 12, 0.98) 100%) !important;
    border: 1px solid rgba(255, 70, 85, 0.35) !important;
    border-right: 4px solid var(--valo-red) !important;
    border-radius: 4px !important;
    margin: 6px 0 !important;
}

/* Khung Bot (Cypher Teal) */
[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-assistant"]) {
    background: linear-gradient(135deg, rgba(10, 38, 42, 0.9) 0%, rgba(10, 14, 18, 0.98) 100%) !important;
    border: 1px solid rgba(0, 212, 191, 0.25) !important;
    border-left: 4px solid var(--valo-teal) !important;
    border-radius: 4px !important;
    margin: 6px 0 !important;
}

[data-testid="stChatMessage"] h3 {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: clamp(15px, 4vw, 18px) !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    color: var(--white) !important;
    border-bottom: 1px solid var(--br-w) !important;
}

/* ══════════════════════════════════════
   CHAT INPUT & INTERFACES FIXES
══════════════════════════════════════ */
.stChatInput textarea {
    background: var(--bg2) !important; color: var(--cream) !important;
    border: 1px solid var(--br-w2) !important; border-bottom: 2px solid rgba(255, 70, 85, 0.2) !important;
}
.stChatInput textarea:focus {
    border-bottom-color: var(--valo-red) !important;
}

section[data-testid="stSidebar"] {
    background: #090c11 !important;
    border-right: 1px solid var(--br-red) !important;
}

#MainMenu, footer, header { visibility: hidden !important; }
.block-container {
    padding-top: 1rem !important;
    padding-bottom: 1.5rem !important;
    max-width: 740px !important;
}

/* ══════════════════════════════════════
   MOBILE BUGS FIX
══════════════════════════════════════ */
@media (max-width: 600px) {
    .block-container { padding: 0.6rem 0.4rem 4.5rem !important; }
    /* ĐÃ SỬA: KHÔNG ẩn phần tên trên điện thoại nữa */
    .valo-author { display: flex !important; margin-bottom: 4px; } 
    [data-testid="stChatMessage"] { padding: 10px 12px !important; }
    .valo-greeting { padding: 14px 12px !important; }
}
</style>
""", unsafe_allow_html=True)

# ========================
# KẾT NỐI API GROQ
# ========================
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except KeyError:
    st.error("❌ Hệ thống thiếu GROQ_API_KEY trong tệp cấu hình Secrets!")
    st.stop()

# ========================
# TẢI CƠ SỞ DỮ LIỆU CỤC BỘ
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
# THANH ĐIỀU HƯỚNG BÊN TRÁI (SIDEBAR)
# ========================
with st.sidebar:
    st.markdown("### ⚡ PC SOLVING SYSTEM")
    st.markdown("---")
    if st.button("⟳ KÍCH HOẠT LẠI", use_container_width=True):
        st.session_state.messages = []
        st.session_state.greeted = False
        st.session_state.pending_query = None
        st.rerun()
    st.markdown("---")
    st.markdown("<span style='color:#00d4bf; font-weight:bold;'>Tác giả: Lê Văn Chung - 10A4</span>", unsafe_allow_html=True)

# ========================
# GIAO DIỆN TRỰC QUAN ĐẦU TRANG (HEADER)
# ========================
st.markdown(f"""
<div class="valo-header">
    <div class="valo-author">LÊ VĂN CHUNG <span class="dot">·</span> 10A4 <span class="dot">🖥️</span><span class="dot">🖥️</span><span class="dot">🖥️</span></div>
    <div class="valo-eyebrow">⚡ STEM PROJECT CONCEPT DỰ ÁN ỨNG DỤNG HOÀN CHỈNH</div>
    <div class="valo-logo-wrap">
        <span class="valo-logo-icon">🖥️</span>
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

# ========================
# GREETING PANEL CỐ ĐỊNH PHÍA TRÊN
# ========================
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

# Chỉ hiển thị nút gợi ý khi chưa chat
if not st.session_state.messages:
    st.markdown('<div class="valo-suggest-label"><span>CHỌN NHANH VẤN ĐỀ</span></div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2, gap="small")
    for i, (label, query) in enumerate(st.session_state.suggestions):
        with (col1 if i % 2 == 0 else col2):
            if st.button(label, key=f"sug_{i}"):
                st.session_state.pending_query = query
                st.rerun()

# LỊCH SỬ CHAT
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# THUẬT TOÁN QUÉT TÌM KIẾM DATA JSON CỤC BỘ
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
                    f"*Phân tích: Tra cứu Dữ liệu Kỹ thuật — Lê Văn Chung 10A4*\n\n"
                    f"**⚠ Nguyên nhân:** {best_match['nguyen_nhan']}\n\n"
                    f"**◈ Phác đồ sửa chữa:**\n{best_match['giai_phap']}")
        else:
            return (f"### ◆ {best_match['ten']}\n"
                    f"*Phân tích: Tra cứu Dữ liệu Linh kiện — Lê Văn Chung 10A4*\n\n"
                    f"**⚙ Thông số phần cứng:** {best_match.get('thong_so','')}\n\n"
                    f"**◉ Chuẩn Socket:** `{best_match.get('socket','')}`\n\n"
                    f"**▶ Tư vấn khuyến nghị:** {best_match.get('chuyen_gia_tu_van','')}")
    return None

def ask_engine(user_query, chat_history):
    system_prompt = f"""Bạn là mô hình trí tuệ nhân tạo chuyên sâu về chẩn đoán phần cứng máy tính và linh kiện PC của tác giả học sinh Lê Văn Chung lớp 10A4.
TUYỆT ĐỐI KHÔNG tự xưng là mô hình ngôn ngữ lớn, không nhắc đến Meta, Llama hay Groq.
Khi giải đáp các câu hỏi kỹ thuật, hãy tận dụng tối đa kho tri thức gốc sau đây nếu có dữ liệu phù hợp: {raw_json_context}.
Trình bày mạch lạc bằng tiếng Việt, ngắn gọn rành mạch theo dạng gạch đầu dòng kỹ thuật."""
    
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

# ĐIỀU PHỐI ĐẦU VÀO
def handle_message(prompt):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        
    with st.chat_message("assistant"):
        with st.spinner("ĐANG QUÉT PIXEL & PHÂN TÍCH LOGIC..."):
            try:
                answer = search_database(prompt) or ask_engine(prompt, st.session_state.messages)
                final_answer = f"""{answer}\n\n---\n*— Hệ thống chẩn đoán tự động: Lê Văn Chung lớp 10A4*"""
                st.markdown(final_answer)
                st.session_state.messages.append({"role": "assistant", "content": final_answer})
            except Exception as e:
                st.error("❌ Kết nối trục trặc hoặc API quá hạn. Hãy thử lại!")

if st.session_state.pending_query:
    q = st.session_state.pending_query
    st.session_state.pending_query = None
    handle_message(q)

if prompt := st.chat_input("Nhập mã lỗi hoặc linh kiện cần phân tích..."):
    handle_message(prompt)
