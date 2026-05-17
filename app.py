import streamlit as st
import json
import re
import os
import random
from groq import Groq

st.set_page_config(
    page_title="PC Solving System — Lê Văn Chung 10A4",
    page_icon="⚡",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Barlow+Condensed:wght@400;600;700;800&family=Barlow:wght@300;400;500;600&display=swap');

/* ══════════════════════════════════════
   VALORANT COLOR SYSTEM
══════════════════════════════════════ */
:root {
    --valo-red:       #ff4655;
    --valo-red-dim:   #c0303d;
    --valo-red-glow:  rgba(255,70,85,0.18);
    --valo-red-faint: rgba(255,70,85,0.06);

    --valo-teal:      #00d4bf;
    --valo-teal-dim:  rgba(0,212,191,0.12);
    --valo-teal-glow: rgba(0,212,191,0.08);

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

    --br-red:  rgba(255,70,85,0.22);
    --br-teal: rgba(0,212,191,0.3);
    --br-w:    rgba(255,255,255,0.06);
    --br-w2:   rgba(255,255,255,0.10);
}

/* ══════════════════════════════════════
   BASE
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
            rgba(255,70,85,0.018) 60px, rgba(255,70,85,0.018) 61px
        ),
        repeating-linear-gradient(
            42deg,
            transparent 0px, transparent 90px,
            rgba(0,212,191,0.010) 90px, rgba(0,212,191,0.010) 91px
        ),
        repeating-linear-gradient(
            180deg,
            transparent 0px, transparent 4px,
            rgba(255,255,255,0.004) 4px, rgba(255,255,255,0.004) 5px
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
   HEADER
══════════════════════════════════════ */
.valo-header {
    text-align: center;
    padding: 10px 0 2px;
    position: relative;
}

.valo-author {
    position: absolute;
    top: 8px; right: 0;
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #00f0ff !important;
    filter: drop-shadow(0 0 5px rgba(0, 240, 255, 0.6));
    text-shadow: 0 0 8px rgba(0, 240, 255, 0.4);
    display: flex;
    align-items: center;
    gap: 5px;
    line-height: 1;
}
.valo-author::before {
    content: '';
    display: block;
    width: 12px; height: 1px;
    background: #00f0ff !important;
    opacity: 0.7;
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
.valo-eyebrow::before, .valo-eyebrow::after {
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
    filter: drop-shadow(0 0 12px rgba(255,70,85,0.6));
}
.valo-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: clamp(30px, 7.5vw, 62px);
    font-weight: 700;
    letter-spacing: 3px;
    line-height: 1;
    color: var(--white);
    text-transform: uppercase;
    margin: 0;
    text-shadow: 0 0 40px rgba(255,70,85,0.15);
}
.valo-title .red   { color: var(--valo-red); }
.valo-title .teal  { color: var(--valo-teal); }
.valo-title .slash { color: var(--valo-red); font-weight: 500; opacity: 0.6; margin: 0 2px; }

/* TÔ MÀU PHỤ ĐỀ */
.valo-subtitle {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: clamp(12px, 2.8vw, 14px);
    font-weight: 700;
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-top: 8px;
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
    width: 4px; height: 4px;
    background: var(--dim);
    transform: rotate(45deg);
}

.valo-divider {
    display: flex;
    align-items: center;
    gap: 8px;
    margin: 12px 0 8px;
}
.valo-divider::before, .valo-divider::after { content: ''; flex: 1; height: 1px; background: var(--br-w); }
.valo-divider-inner { display: flex; align-items: center; gap: 5px; }
.valo-diam { width: 5px; height: 5px; transform: rotate(45deg); }
.valo-diam.r { background: var(--valo-red); }
.valo-diam.t { background: var(--valo-teal); width: 4px; height: 4px; opacity: 0.7; }
.valo-dbar {
    width: 50px; height: 2px;
    background: linear-gradient(90deg, var(--valo-red), var(--valo-teal));
    clip-path: polygon(5px 0%, 100% 0%, calc(100% - 5px) 100%, 0% 100%);
}

/* ══════════════════════════════════════
   GREETING BOX (CỐ ĐỊNH)
══════════════════════════════════════ */
.valo-greeting {
    position: relative;
    background: linear-gradient(135deg, rgba(24,28,40,0.8) 0%, rgba(18,22,31,0.9) 100%);
    border: 1px solid var(--br-red);
    border-top: 2px solid var(--valo-red);
    border-radius: 2px;
    padding: clamp(18px,5vw,28px) clamp(16px,5vw,28px) clamp(14px,4vw,22px);
    margin: 4px 0 16px;
    overflow: hidden;
    box-shadow: 0 8px 30px rgba(0,0,0,0.4);
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
    background: radial-gradient(circle, rgba(0,212,191,0.06) 0%, transparent 65%);
    pointer-events: none;
}
.valo-vbar {
    position: absolute;
    left: 0; top: 18%; bottom: 18%;
    width: 3px;
    background: linear-gradient(180deg, transparent 0%, var(--valo-red) 30%, var(--valo-teal) 70%, transparent 100%);
    opacity: 0.8;
}
.valo-status-row {
    display: flex; align-items: center; justify-content: center; gap: 6px; margin-bottom: 10px;
}
.valo-status-dot {
    width: 6px; height: 6px; background: var(--valo-teal); border-radius: 50%;
    box-shadow: 0 0 6px var(--valo-teal); animation: pulse 2s infinite;
}
.valo-status-text {
    font-family: 'Barlow Condensed', sans-serif; font-size: 10px; font-weight: 700;
    letter-spacing: 3px; color: var(--valo-teal); text-transform: uppercase;
}
@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.4; } }
.valo-greeting-icon {
    font-size: clamp(30px, 6vw, 38px); display: block; text-align: center; margin-bottom: 8px;
    filter: drop-shadow(0 0 10px rgba(255,70,85,0.5));
}
.valo-greeting-title {
    font-family: 'Rajdhani', sans-serif; font-size: clamp(16px, 4vw, 22px); font-weight: 700;
    color: var(--white); text-align: center; text-transform: uppercase; letter-spacing: 2px;
    margin-bottom: 8px; text-shadow: 0 2px 10px rgba(0,0,0,0.5);
}
.valo-greeting-sub {
    font-size: clamp(12px, 3vw, 14px); color: var(--cream); text-align: center; line-height: 1.7; font-weight: 400;
}
.valo-stats {
    display: flex; justify-content: center; gap: clamp(12px, 3vw, 24px);
    margin-top: 14px; padding-top: 12px; border-top: 1px solid var(--br-w);
}
.valo-stat { text-align: center; line-height: 1.2; }
.valo-stat-num { font-family: 'Rajdhani', sans-serif; font-size: clamp(16px, 4vw, 22px); font-weight: 700; color: var(--valo-red); display: block; }
.valo-stat-label { font-family: 'Barlow Condensed', sans-serif; font-size: 9px; letter-spacing: 2px; color: var(--dim); text-transform: uppercase; }
.valo-stat-divider { width: 1px; background: var(--br-w2); align-self: stretch; }

/* ══════════════════════════════════════
   SUGGEST LABEL (MÀU MỚI VALORANT)
══════════════════════════════════════ */
.valo-suggest-label {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 8px 0 14px;
}
.valo-suggest-label::before, .valo-suggest-label::after {
    content: ''; flex: 1; height: 1px; background: rgba(255,255,255,0.1);
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
    box-shadow: 0 4px 15px rgba(255,70,85,0.3);
}

/* ══════════════════════════════════════
   BUTTONS GỢI Ý (ĐỔ MÀU KHUNG)
══════════════════════════════════════ */
.stButton > button {
    background: linear-gradient(90deg, rgba(30,34,50,0.8), rgba(20,24,35,0.9)) !important;
    color: #ffffff !important;
    border: 1px solid rgba(0,212,191,0.2) !important;
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
    box-shadow: 0 2px 10px rgba(0,0,0,0.3) !important;
}
.stButton > button:hover {
    background: linear-gradient(90deg, rgba(0,212,191,0.2), rgba(255,70,85,0.1)) !important;
    border-color: var(--valo-teal) !important;
    border-left-color: var(--valo-red) !important;
    color: var(--white) !important;
    transform: translateX(4px) !important;
    box-shadow: 0 4px 15px rgba(0,212,191,0.3) !important;
}

/* ══════════════════════════════════════
   CHAT MESSAGES (SỬA LỖI NERF CHỮ)
══════════════════════════════════════ */
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li {
    font-size: clamp(14px, 3.8vw, 15px) !important;
    line-height: 1.75 !important;
    color: #ffffff !important; 
    font-weight: 400 !important;
    text-shadow: 1px 1px 3px rgba(0,0,0,0.9) !important;
}

/* KHUNG NGƯỜI DÙNG (MÀU ĐỎ OMEN) */
[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) {
    background: linear-gradient(135deg, rgba(60,15,20,0.85) 0%, rgba(20,10,12,0.95) 100%) !important;
    border: 1px solid rgba(255,70,85,0.4) !important;
    border-right: 4px solid var(--valo-red) !important;
    border-radius: 4px !important;
    padding: 14px 18px !important;
    margin: 8px 0 !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.5) !important;
}

/* KHUNG BOT TRẢ LỜI (MÀU XANH CYPHER) */
[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-assistant"]) {
    background: linear-gradient(135deg, rgba(10,40,45,0.85) 0%, rgba(10,15,20,0.95) 100%) !important;
    border: 1px solid rgba(0,212,191,0.3) !important;
    border-left: 4px solid var(--valo-teal) !important;
    border-radius: 4px !important;
    padding: 14px 18px !important;
    margin: 8px 0 !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.5) !important;
}

/* Các format đặc biệt trong chat */
[data-testid="stChatMessage"] h3 {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: clamp(15px, 4vw, 19px) !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 2px !important;
    color: var(--white) !important;
    margin-bottom: 8px !important;
    padding-bottom: 5px !important;
    border-bottom: 1px solid var(--br-w) !important;
    text-shadow: 0 2px 5px rgba(0,0,0,0.8) !important;
}
[data-testid="stChatMessage"] strong {
    color: #ffb0b8 !important;
    font-weight: 700 !important;
}
[data-testid="stChatMessage"] code {
    background: rgba(0,212,191,0.15) !important;
    color: #55ffeb !important;
    border: 1px solid rgba(0,212,191,0.4) !important;
    border-radius: 3px !important;
    padding: 2px 6px !important;
    font-size: 13px !important;
    text-shadow: none !important;
}

/* ══════════════════════════════════════
   CHAT INPUT
══════════════════════════════════════ */
.stChatInput textarea {
    background: var(--bg2) !important; color: var(--cream) !important;
    border: 1px solid var(--br-w2) !important; border-bottom: 2px solid rgba(255,70,85,0.2) !important;
    border-radius: 2px !important; font-family: 'Barlow', sans-serif !important;
    font-size: clamp(14px, 3.5vw, 15px) !important; caret-color: var(--valo-red) !important;
}
.stChatInput textarea:focus {
    border-color: var(--br-w2) !important; border-bottom-color: var(--valo-red) !important;
    box-shadow: 0 4px 24px rgba(255,70,85,0.1) !important;
}

/* ══════════════════════════════════════
   SIDEBAR & SPINNER
══════════════════════════════════════ */
section[data-testid="stSidebar"] { background: #090c11 !important; border-right: 1px solid var(--br-red) !important; }
section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] span, section[data-testid="stSidebar"] div, section[data-testid="stSidebar"] small { color: var(--muted) !important; font-size: 13px !important; }
section[data-testid="stSidebar"] h2 { font-family: 'Rajdhani', sans-serif !important; font-size: 17px !important; color: var(--cream) !important; text-transform: uppercase !important; letter-spacing: 3px !important; }
section[data-testid="stSidebar"] .stButton > button { background: transparent !important; border: 1px solid var(--br-red) !important; border-left: 2px solid var(--valo-red) !important; color: var(--cream) !important; font-family: 'Barlow Condensed', sans-serif !important; font-weight: 700 !important; letter-spacing: 1px !important; box-shadow: none !important; }

[data-testid="stSpinner"] p { color: var(--valo-teal) !important; font-family: 'Barlow Condensed', sans-serif !important; letter-spacing: 4px !important; font-size: 12px !important; text-transform: uppercase !important; }

#MainMenu, footer, header { visibility: hidden !important; }
.block-container { padding-top: 1.2rem !important; padding-bottom: 1.5rem !important; max-width: 760px !important; }

/* ══════════════════════════════════════
   MOBILE BUGS FIX
══════════════════════════════════════ */
@media (max-width: 600px) {
    .block-container { padding: 0.7rem 0.5rem 4.5rem !important; }
    
    .valo-author { 
        position: relative !important; 
        top: 0 !important; 
        justify-content: center !important; 
        margin-bottom: 12px !important; 
        font-size: 12px !important;
        color: var(--valo-teal) !important;
        filter: drop-shadow(0 0 5px rgba(0,212,191,0.5)) !important;
        text-shadow: none !important;
    }
    .valo-author::before { display: none; }
    
    [data-testid="stChatMessage"] { padding: 12px 14px !important; margin: 5px 0 !important; }
    .stButton > button { min-height: 44px !important; padding: 10px 12px !important; font-size: 13px !important; }
    .valo-greeting { padding: 18px 14px !important; margin-bottom: 10px !important; }
    .valo-stats { gap: 10px; }
}
</style>
""", unsafe_allow_html=True)

# ========================
# GROQ CLIENT
# ========================
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except KeyError:
    st.error("❌ Chưa cấu hình GROQ_API_KEY trong Secrets!")
    st.stop()
except Exception as e:
    st.error(f"❌ Lỗi kết nối: {str(e)}")
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

data_pc   = load_database()
raw_json_context = load_raw_json()
db_loi    = len(data_pc.get("loi_he_thong", []))
db_lk     = len(data_pc.get("linh_kien_pc", []))

# ========================
# SIDEBAR
# ========================
with st.sidebar:
    st.markdown("## ⚡ PC Solving")
    st.markdown("---")
    st.markdown("Hệ thống chẩn đoán lỗi và tư vấn linh kiện máy tính chuyên sâu.")
    st.markdown("---")
    if st.button("⟳  PHIÊN MỚI", use_container_width=True):
        st.session_state.messages = []
        st.session_state.greeted  = False
        st.session_state.suggestions = []
        st.rerun()
    st.markdown("---")
    st.markdown("<small>Lê Văn Chung · Lớp 10A4 🎓</small>", unsafe_allow_html=True)

# ========================
# HEADER
# ========================
st.markdown(f"""
<div class="valo-header">
    <div class="
