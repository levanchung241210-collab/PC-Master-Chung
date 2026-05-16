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
   HEADER & VALORANT FONTS
══════════════════════════════════════ */
.valo-header {
    text-align: center;
    padding: 10px 0 2px;
    position: relative;
}

/* TÁC GIẢ LÊ VĂN CHUNG 10A4 — STYLE VALORANT */
.valo-author {
    position: absolute;
    top: 8px; right: 0;
    font-family: 'Barlow Condensed', sans-serif !important;
    font-size: 13px !important;
    font-weight: 800 !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    color: var(--dim) !important;
    display: flex;
    align-items: center;
    gap: 5px;
    line-height: 1;
}
.valo-author .dot { color: var(--valo-teal); font-size: 15px; }

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
    opacity: 0.6;
}
.valo-eyebrow::before { background: linear-gradient(90deg, transparent, var(--valo-red)); }
.valo-eyebrow::after { background: linear-gradient(90deg, var(--valo-red), transparent); }

.valo-logo-wrap {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 14px;
    margin-bottom: 4px;
}
.valo-logo-icon {
    font-size: clamp(28px, 6vw, 40px);
    filter: drop-shadow(0 0 12px rgba(255, 70, 85, 0.6));
}
.valo-title {
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: clamp(30px, 7.5vw, 62px) !important;
    font-weight: 400 !important;
    letter-spacing: 3px !important;
    line-height: 1;
    color: var(--white);
    text-transform: uppercase;
    margin: 0;
    text-shadow: 0 0 40px rgba(255, 70, 85, 0.15);
}
.valo-title .red   { color: var(--valo-red); }
.valo-title . teal  { color: var(--valo-teal); }
.valo-title . slash {
    color: var(--valo-red);
    font-weight: 500;
    opacity: 0.6;
    margin: 0 2px;
}

/* SỬA LỖI LOẠN FONT TIÊU ĐỀ — ÁP DỤNG Oswald SẮC CẠNH */
.valo-main-heading {
    font-family: 'Oswald', sans-serif !important;
    font-size: clamp(20px, 4.5vw, 32px) !important;
    font-weight: 700 !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    color: var(--white) !important;
    text-shadow: 2px 2px 0px rgba(0, 0, 0, 0.5) !important;
    margin: 15px 0 !important;
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

/* ══════════════════════════════════════
   GREETING BOX (CỐ ĐỊNH PHÍA TRÊN, KHÔNG ẨN KHI CHAT)
══════════════════════════════════════ */
.valo-greeting {
    position: relative;
    background: linear-gradient(135deg, rgba(24, 28, 40, 0.8) 0%, rgba(18, 22, 31, 0.9) 100%);
    border: 1px solid var(--br-red);
    border-top: 2px solid var(--valo-red);
    border-radius: 2px;
    padding: clamp(18px, 5vw, 28px) clamp(16px, 5vw, 28px) clamp(14px, 4vw, 22px);
    margin: 4px 0 16px;
    overflow: hidden;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4);
}

.valo-greeting::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    border-style: solid;
    border-width: 22px 22px 0 0;
    border-color: var(--bg0) transparent transparent transparent;
}

.valo-greeting::after {
    content: '';
    position: absolute;
    bottom: -30px; right: -30px;
    width: 160px; height: 160px;
    background: radial-gradient(circle, rgba(0, 212, 191, 0.06) 0%, transparent 65%);
    pointer-events: none;
}

.valo-vbar {
    position: absolute;
    left: 0; top: 18%; bottom: 18%;
    width: 3px;
    background: linear-gradient(180deg,
        transparent 0%,
        var(--valo-red) 30%,
        var(--valo-teal) 70%,
        transparent 100%
    );
    opacity: 0.8;
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
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.4; }
}

.valo-greeting-icon {
    font-size: clamp(30px, 6vw, 38px);
    display: block;
    text-align: center;
    margin-bottom: 8px;
    filter: drop-shadow(0 0 10px rgba(255, 70, 85, 0.5));
}
.valo-greeting-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: clamp(16px, 4vw, 22px);
    font-weight: 700;
    color: var(--white);
    text-align: center;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 8px;
    text-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
}
.valo-greeting-sub {
    font-size: clamp(12px, 3vw, 14px);
    color: var(--cream);
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
    font-family: 'Rajdhani', sans-serif;
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

/* ══════════════════════════════════════
   SUGGEST LABEL (PHỐI MÀU VALORANT CHỌN NHANH VẤN ĐỀ)
══════════════════════════════════════ */
.valo-suggest-label {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 8px 0 14px;
}
.valo-suggest-label::before,
.valo-suggest-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: rgba(255, 255, 255, 0.1);
}
.valo-suggest-label span {
    background: var(--valo-red);
    color: var(--white);
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 4px 16px;
    clip-path: polygon(8px 0, 100% 0, calc(100% - 8px) 100%, 0 100%);
    box-shadow: 0 4px 15px rgba(255, 70, 85, 0.3);
}

/* ══════════════════════════════════════
   BUTTONS GỢI Ý (ĐỔ MÀU KHUNG CHUYÊN NGHIỆP)
══════════════════════════════════════ */
.stButton > button {
    background: linear-gradient(90deg, rgba(30, 34, 50, 0.8), rgba(20, 24, 35, 0.9)) !important;
    color: #ffffff !important;
    border: 1px solid rgba(0, 212, 191, 0.2) !important;
    border-left: 3px solid var(--valo-teal) !important;
    border-radius: 2px !important;
    font-family: 'Barlow Condensed', sans-serif !important;
    font-size: clamp(12px, 3vw, 14px) !important;
    font-weight: 700 !important;
    letter-spacing: 0.5px !important;
    padding: 12px 14px !important;
    width: 100% !important;
    text-align: left !important;
    white-space: normal !important;
    height: auto !important;
    min-height: 48px !important;
    line-height: 1.4 !important;
    transition: all 0.15s ease !important;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3) !important;
}
.stButton > button:hover {
    background: linear-gradient(90deg, rgba(0, 212, 191, 0.2), rgba(255, 70, 85, 0.1)) !important;
    border-color: var(--valo-teal) !important;
    border-left-color: var(--valo-red) !important;
    color: var(--white) !important;
    transform: translateX(4px) !important;
    box-shadow: 0 4px 15px rgba(0, 212, 191, 0.3) !important;
}

/* ══════════════════════════════════════
   CHAT MESSAGES (SỬA LỖI CHỮ BỊ CHÌM)
══════════════════════════════════════ */
/* Ép toàn bộ chữ trong khung chat thành màu TRẮNG SÁNG hiển thị rõ trên mọi thiết bị */
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li {
    font-size: clamp(14px, 3.8vw, 15px) !important;
    line-height: 1.75 !important;
    color: #ffffff !important; 
    font-weight: 400 !important;
    text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.9) !important; /* Đổ bóng đen siêu đậm để nổi chữ */
}

/* KHUNG NGƯỜI DÙNG ( Phe Tiến Công - Đỏ Omen) */
[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) {
    background: linear-gradient(135deg, rgba(60, 15, 20, 0.85) 0%, rgba(20, 10, 12, 0.95) 100%) !important;
    border: 1px solid rgba(255, 70, 85, 0.4) !important;
    border-right: 4px solid var(--valo-red) !important;
    border-radius: 4px !important;
    padding: 14px 18px !important;
    margin: 8px 0 !important;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5) !important;
}

/* KHUNG BOT TRẢ LỜI (Phe Phòng Thủ - Xanh Teal Cypher) */
[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-assistant"]) {
    background: linear-gradient(135deg, rgba(10, 40, 45, 0.85) 0%, rgba(10, 15, 20, 0.95) 100%) !important;
    border: 1px solid rgba(0, 212, 191, 0.3) !important;
    border-left: 4px solid var(--valo-teal) !important;
    border-radius: 4px !important;
    padding: 14px 18px !important;
    margin: 8px 0 !important;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5) !important;
}

/* Các format đặc biệt trong chat (Giữ font chuẩn Cypher) */
[data-testid="stChatMessage"] h3 {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: clamp(15px, 4.2vw, 18px) !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 2px !important;
    color: var(--white) !important;
    margin-bottom: 8px !important;
    padding-bottom: 5px !important;
    border-bottom: 1px solid var(--br-w) !important;
    text-shadow: 0 2px 5px rgba(0, 0, 0, 0.8) !important;
}
[data-testid="stChatMessage"] strong {
    color: #ffb0b8 !important; /* Đỏ nhạt để nổi trên nền tối Omen */
    font-weight: 700 !important;
}
[data-testid="stChatMessage"] code {
    background: rgba(0, 212, 191, 0.08) !important;
    color: var(--valo-teal) !important;
    border: 1px solid rgba(0, 212, 191, 0.2) !important;
    border-radius: 2px !important;
    padding: 2px 6px !important;
    font-size: 13px !important;
}

/* ══════════════════════════════════════
   CHAT INPUT
══════════════════════════════════════ */
.stChatInput textarea {
    background: var(--bg2) !important; color: var(--cream) !important;
    border: 1px solid var(--br-w2) !important; border-bottom: 2px solid rgba(255, 70, 85, 0.2) !important;
    border-radius: 2px !important; font-family: 'Barlow', sans-serif !important;
    font-size: clamp(13px, 3.5vw, 14px) !important; caret-color: var(--valo-red) !important;
}
.stChatInput textarea:focus {
    border-color: var(--br-w2) !important; border-bottom-color: var(--valo-red) !important;
    box-shadow: 0 4px 24px rgba(255, 70, 85, 0.06) !important;
}
.stChatInput textarea::placeholder {
    color: var(--dim) !important;
}

/* ══════════════════════════════════════
   SIDEBAR
══════════════════════════════════════ */
section[data-testid="stSidebar"] {
    background: #090c11 !important;
    border-right: 1px solid var(--br-red) !important;
}
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] div,
section[data-testid="stSidebar"] small {
    color: var(--muted) !important;
    font-size: 13px !important;
}
section[data-testid="stSidebar"] h2 {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 17px !important;
    color: var(--cream) !important;
    text-transform: uppercase !important;
    letter-spacing: 3px !important;
}
section[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    border: 1px solid var(--br-red) !important;
    border-left: 2px solid var(--valo-red) !important;
    color: var(--muted) !important;
    font-family: 'Barlow Condensed', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: 1px !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background: var(--valo-red-faint) !important;
    color: var(--cream) !important;
}

/* ══════════════════════════════════════
   SPINNER
══════════════════════════════════════ */
[data-testid="stSpinner"] p {
    color: var(--valo-teal) !important;
    font-family: 'Barlow Condensed', sans-serif !important;
    letter-spacing: 4px !important;
    font-size: 12px !important;
    text-transform: uppercase !important;
}

/* ══════════════════════════════════════
   HIDE STREAMLIT
══════════════════════════════════════ */
#MainMenu, footer, header { visibility: hidden !important; }
.block-container {
    padding-top: 1.2rem !important;
    padding-bottom: 1.5rem !important;
    max-width: 760px !important;
}

/* ══════════════════════════════════════
   MOBILE BUGS FIX
══════════════════════════════════════ */
@media (max-width: 600px) {
    .block-container { padding: 0.7rem 0.5rem 4.5rem !important; }
    .valo-author { display: none; }
    [data-testid="stChatMessage"] { padding: 10px 11px !important; margin: 3px 0 !important; }
    .stButton > button { min-height: 42px !important; padding: 8px 10px !important; }
    .valo-greeting { padding: 16px 14px !important; }
    .valo-stats { gap: 10px; }
}
</style>
""", unsafe_allow_html=True)

# ========================
# KẾT NỐI API GROQ ĐIỀU KHIỂN
# ========================
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except KeyError:
    st.error("❌ Hệ thống thiếu GROQ_API_KEY trong tệp cấu hình Secrets!")
    st.stop()
except Exception as e:
    st.error(f"❌ Lỗi thiết lập kết nối: {str(e)}")
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
    st.markdown("Hệ thống nhúng thuật toán phân tích lỗi phần cứng và linh kiện PC.")
    st.markdown("---")
    if st.button("⟳ KÍCH HOẠT LẠI", use_container_width=True):
        st.session_state.messages = []
        st.session_state.greeted = False
        st.session_state.suggestions = []
        st.rerun()
    st.markdown("---")
    st.markdown("<span style='color:#00d4bf; font-weight:bold;'>Tác giả: Lê Văn Chung - 10A4</span>", unsafe_allow_html=True)

# ========================
# GIAO DIỆN TRỰC QUAN ĐẦU TRANG (HEADER)
# ========================
st.markdown(f"""
<div class="valo-header">
    <div class="valo-author">LÊ VĂN CHUNG <span class="dot">·</span> 10A4 <span class="dot">🖥</span><span class="dot">🖥</span><span class="dot">🖥</span></div>
    <div class="valo-eyebrow">⚡ STEM PROJECT CONCEPT DỰ ÁN ỨNG DỤNG HOÀN CHỈNH</div>
    <div class="valo-logo-wrap">
        <span class="valo-logo-icon">🖥</span>
        <div class="valo-title">PC<span class="slash">/</span><span class="red">SOLVING</span></div>
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

# ========================
# KHỞI TẠO BỘ NHỚ LƯU TRỮ TRẠNG THÁI CHAT
# ========================
if "messages" not in st.session_state: st.session_state.messages = []
if "greeted" not in st.session_state: st.session_state.greeted = False
if "suggestions" not in st.session_state: st.session_state.suggestions = []
if "pending_query" not in st.session_state: st.session_state.pending_query = None

# Danh sách 4 câu hỏi gợi ý nhanh ban đầu
ALL_SUGGESTIONS = [
    ("⚠ Màn hình xanh chết BSOD", "Máy tính bị màn hình xanh chết, phải làm gì?"),
    ("▪ Màn hình đen không hiển thị", "Máy lên nguồn nhưng màn hình đen, không lên gì"),
    ("◈ PC bíp liên tục khi bật", "Máy tính bíp nhiều tiếng khi khởi động, lỗi gì?"),
    ("◉ Máy chạy chậm bất thường", "Máy tính đột nhiên chạy rất chậm, khắc phục thế nào?"),
    ("🌡 CPU overheat — quá nóng", "CPU bị overheat, nhiệt độ lên đến 95 độ C"),
    ("◆ RAM có tương thích mainboard không", "Làm sao biết RAM có tương thích với mainboard không?"),
    ("⚡ Cần bao nhiêu W nguồn điện", "Cấu hình PC của tôi cần bao nhiêu W nguồn là đủ?"),
    ("🎮開 GTX 1650 chơi được game gì", "Card GTX 1650 chơi được những game nào mượt?"),
]

if not st.session_state.suggestions:
    st.session_state.suggestions = random.sample(ALL_SUGGESTIONS, 4)

# ========================
# KHỐI GREETING PANEL CỐ ĐỊNH PHÍA TRÊN
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

# Chỉ hiển thị 4 nút bấm gợi ý khi người dùng chưa bắt đầu thực hiện chat
if not st.session_state.messages:
    st.markdown('<div class="valo-suggest-label"><span>CHỌN NHANH VẤN ĐỀ</span></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="small")
    for i, (label, query) in enumerate(st.session_state.suggestions):
        with (col1 if i % 2 == 0 else col2):
            if st.button(label, key=f"sug_{i}"):
                st.session_state.greeted = True
                st.session_state.pending_query = query
                st.rerun()

# ========================
# LỊCH SỬ TIN NHẮN CHAT TƯƠNG TÁC
# ========================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ========================
# THUẬT TOÁN QUÉT TÌM KIẾM DATA TRONG JSON CỤC BỘ
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

# ========================
# XỬ LÝ TRUY VẤN QUA LLM TRÍ TUỆ NHÂN TẠO
# ========================
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

# ========================
# LUỒNG TIẾP NHẬN & ĐIỀU PHỐI DỮ LIỆU CHAT
# ========================
def handle_message(prompt):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        
    with st.chat_message("assistant"):
        with st.spinner("ĐANG QUÉT pixel & PHÂN TÍCH LOGIC..."):
            try:
                # Nếu chỉ là text, ưu tiên quét DB cục bộ trước, nếu không tìm thấy mới gọi AI
                answer = search_database(prompt) or ask_engine(prompt, st.session_state.messages)
                final_answer = f"""{answer}\n\n---\n*— Hệ thống chẩn đoán tự động: Lê Văn Chung lớp 10A4*"""
                st.markdown(final_answer)
                st.session_state.messages.append({"role": "assistant", "content": final_answer})
            except Exception as e:
                st.error("❌ Kết nối trục trặc hoặc API quá hạn. Hãy thử lại!")

# Xử lý nếu bấm nút gợi ý nhanh
if st.session_state.pending_query:
    q = st.session_state.pending_query
    st.session_state.pending_query = None
    handle_message(q)

# Tiếp nhận dữ liệu gõ trực tiếp từ ô nhập liệu chat
if prompt := st.chat_input("Nhập mã lỗi hoặc linh kiện cần phân tích..."):
    st.session_state.greeted = True
    handle_message(prompt)
