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
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@600;700&family=Barlow+Condensed:wght@400;500;600;700&family=Barlow:wght@300;400;500;600&display=swap');

/* ==============================
   VALORANT CORE PALETTE & TOKENS
============================== */
:root {
    --red:     #ff4655;
    --red-dim: #b7323f;
    --red-glow: rgba(255, 70, 85, 0.25);
    --dark:    #0f1115;
    --dark2:   #161920;
    --dark3:   #1f232e;
    --panel:   rgba(15, 17, 21, 0.85);
    --border:  rgba(255, 70, 85, 0.3);
    --border2: rgba(236, 232, 225, 0.08);
    --text:    #ece8e1;
    --muted:   #76787c;
    --accent:  #fffbf5;
}

/* ==============================
   BASE SYSTEM
============================== */
html, body, .stApp {
    background: var(--dark) !important;
    color: var(--text) !important;
    font-family: 'Barlow', sans-serif !important;
}

/* VALORANT Grid & Diagonal Texture Line */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image: 
        linear-gradient(rgba(236, 232, 225, 0.005) 1px, transparent 1px),
        linear-gradient(90deg, rgba(236, 232, 225, 0.005) 1px, transparent 1px),
        repeating-linear-gradient(-45deg, transparent, transparent 30px, rgba(255, 70, 85, 0.008) 30px, rgba(255, 70, 85, 0.008) 31px);
    background-size: 40px 40px, 40px 40px, auto;
    pointer-events: none;
    z-index: 0;
}

/* Top indicator border */
.stApp::after {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0;
    height: 4px;
    background: linear-gradient(90deg, var(--red) 0%, var(--red) 30%, transparent 70%);
    z-index: 999;
}

/* ==============================
   HEADER (VALORANT UI BRANDING)
============================== */
.valo-header {
    position: relative;
    text-align: center;
    padding: 15px 0 5px;
    margin-bottom: 5px;
}

.valo-eyebrow {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: clamp(10px, 2.5vw, 12px);
    font-weight: 700;
    letter-spacing: 6px;
    color: var(--red);
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
    width: 30px; height: 1px;
    background: var(--red);
    opacity: 0.5;
}

.valo-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: clamp(32px, 8vw, 62px);
    font-weight: 700;
    letter-spacing: -0.5px;
    line-height: 0.95;
    color: var(--accent);
    text-transform: uppercase;
    margin: 0;
}
.valo-title span {
    color: var(--red);
    position: relative;
}

.valo-subtitle {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: clamp(11px, 2.8vw, 13px);
    font-weight: 500;
    letter-spacing: 5px;
    color: var(--muted);
    text-transform: uppercase;
    margin-top: 8px;
}

/* Custom Slash Divider */
.valo-divider {
    display: flex;
    align-items: center;
    margin: 15px 0 12px;
    height: 3px;
}
.valo-divider::before, .valo-divider::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border2);
}
.valo-divider-bar {
    width: 80px; height: 3px;
    background: var(--red);
    clip-path: polygon(6px 0%, 100% 0%, calc(100% - 6px) 100%, 0% 100%);
    margin: 0 10px;
}

/* ==============================
   AGENT GREETING INTERFACE
============================== */
.valo-greeting {
    position: relative;
    background: var(--dark2);
    border: 1px solid rgba(236, 232, 225, 0.05);
    border-left: 4px solid var(--red);
    border-radius: 0px; /* Valorant prefers sharp edges */
    padding: clamp(20px, 5vw, 28px) clamp(16px, 4vw, 24px);
    margin: 10px 0 8px;
    box-shadow: inset 0 0 15px rgba(0,0,0,0.2);
}
/* Angular sub-decorations */
.valo-greeting::before {
    content: '// LVC_SYS';
    position: absolute;
    top: 4px; right: 8px;
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 9px;
    color: var(--muted);
    letter-spacing: 1px;
}

.valo-agent-icon {
    font-size: clamp(32px, 7vw, 42px);
    margin-bottom: 10px;
    display: block;
    text-align: center;
    filter: drop-shadow(0 0 10px var(--red-glow));
}
.valo-greeting-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: clamp(18px, 4.5vw, 24px);
    font-weight: 700;
    color: var(--accent);
    text-align: center;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 6px;
}
.valo-greeting-sub {
    font-size: clamp(12.5px, 3.2vw, 14px);
    color: #b5b3ae;
    text-align: center;
    line-height: 1.6;
}

/* ==============================
   SELECTION LABELS
============================== */
.valo-suggest-label {
    display: flex;
    align-items: center;
    margin: 20px 0 12px;
}
.valo-suggest-label::before, .valo-suggest-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border2);
}
.valo-suggest-label span {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 4px;
    color: #4b4f58;
    text-transform: uppercase;
    white-space: nowrap;
    padding: 0 12px;
}

/* ==============================
   VALORANT BUTTONS (TACTICAL CUTS)
============================== */
.stButton > button {
    background: #1e222b !important;
    color: #c9c5be !important;
    border: 1px solid rgba(236, 232, 225, 0.08) !important;
    border-radius: 0px !important; /* Sharp corners like Valorant cards */
    font-family: 'Barlow Condensed', sans-serif !important;
    font-size: clamp(12px, 3.2vw, 14px) !important;
    font-weight: 600 !important;
    letter-spacing: 0.8px !important;
    text-transform: uppercase !important;
    padding: 12px 16px !important;
    width: 100% !important;
    text-align: left !important;
    white-space: normal !important;
    height: auto !important;
    min-height: 50px !important;
    line-height: 1.3 !important;
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
    position: relative !important;
    border-left: 3px solid rgba(236, 232, 225, 0.1) !important;
    /* Angle cut on bottom right corner */
    clip-path: polygon(0 0, 100% 0, 100% calc(100% - 8px), calc(100% - 8px) 100%, 0 100%) !important;
}
.stButton > button:hover {
    background: var(--red) !important;
    border-color: var(--red) !important;
    border-left-color: var(--accent) !important;
    color: var(--dark) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 15px var(--red-glow) !important;
}
.stButton > button:active {
    background: var(--red-dim) !important;
    transform: translateY(0px) !important;
}

/* ==============================
   MILITARY CHAT BOX PATTERNS
============================== */
[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) {
    background: rgba(255, 70, 85, 0.04) !important;
    border: 1px solid rgba(255, 70, 85, 0.15) !important;
    border-right: 4px solid var(--red) !important;
    border-radius: 0px !important;
    padding: 14px 18px !important;
    margin: 8px 0 !important;
}
[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-assistant"]) {
    background: var(--dark2) !important;
    border: 1px solid rgba(236, 232, 225, 0.04) !important;
    border-left: 4px solid var(--red) !important;
    border-radius: 0px !important;
    padding: 14px 18px !important;
    margin: 8px 0 !important;
}

/* Tactical Text Formatting */
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li {
    font-size: clamp(13.5px, 3.6vw, 14.5px) !important;
    line-height: 1.75 !important;
    color: #dbd7d1 !important;
}
[data-testid="stChatMessage"] h3 {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: clamp(15px, 4.2vw, 18px) !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 1.2px !important;
    color: var(--accent) !important;
    margin-top: 4px !important;
    margin-bottom: 8px !important;
    border-bottom: 1px dashed rgba(236, 232, 225, 0.1) !important;
    padding-bottom: 4px !important;
}
[data-testid="stChatMessage"] strong {
    color: var(--red) !important;
    font-weight: 600 !important;
}
[data-testid="stChatMessage"] code {
    background: rgba(255, 70, 85, 0.08) !important;
    color: var(--red) !important;
    border: 1px solid rgba(255, 70, 85, 0.18) !important;
    border-radius: 0px !important;
    padding: 2px 6px !important;
    font-size: 12.5px !important;
    font-family: monospace !important;
}

/* ==============================
   TACTICAL INPUT CONSOLE
============================== */
.stChatInput textarea {
    background: var(--dark2) !important;
    color: var(--text) !important;
    border: 1px solid rgba(236, 232, 225, 0.1) !important;
    border-bottom: 3px solid rgba(236, 232, 225, 0.15) !important;
    border-radius: 0px !important;
    font-family: 'Barlow', sans-serif !important;
    font-size: 14px !important;
    caret-color: var(--red) !important;
    padding-top: 10px !important;
}
.stChatInput textarea:focus {
    border-color: rgba(236, 232, 225, 0.15) !important;
    border-bottom-color: var(--red) !important;
    box-shadow: 0 4px 25px rgba(255, 70, 85, 0.06) !important;
    outline: none !important;
}

/* ==============================
   SIDEBAR NAVY
============================== */
section[data-testid="stSidebar"] {
    background: #0b0d12 !important;
    border-right: 1px solid rgba(255, 70, 85, 0.08) !important;
}
section[data-testid="stSidebar"] h2 {
    font-family: 'Rajdhani', sans-serif !important;
    color: var(--accent) !important;
    text-transform: uppercase !important;
    letter-spacing: 2.5px !important;
    font-weight: 700 !important;
}
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] div,
section[data-testid="stSidebar"] small {
    color: #676a72 !important;
    font-family: 'Barlow', sans-serif !important;
}

/* Sidebar tactical reset button */
section[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    border: 1px solid rgba(255, 70, 85, 0.2) !important;
    border-left: 3px solid var(--red) !important;
    color: #8c909c !important;
    clip-path: none !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(255, 70, 85, 0.1) !important;
    color: var(--accent) !important;
}

/* ==============================
   LOADING STATUS
============================== */
[data-testid="stSpinner"] p {
    color: var(--red) !important;
    font-family: 'Barlow Condensed', sans-serif !important;
    letter-spacing: 3px !important;
    font-weight: 600 !important;
    font-size: 12px !important;
}

/* ==============================
   STREAMLIT UI WIPEOUT
============================== */
#MainMenu, footer, header { visibility: hidden !important; }
.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 2rem !important;
    max-width: 740px !important;
}

/* MOBILE FIXES */
@media (max-width: 600px) {
    .block-container { padding: 1rem 0.6rem 5rem !important; }
    [data-testid="stChatMessage"] { padding: 12px 14px !important; }
    .stButton > button { min-height: 44px !important; padding: 10px 12px !important; }
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

data_pc = load_database()
raw_json_context = load_raw_json()

# ========================
# SIDEBAR
# ========================
with st.sidebar:
    st.markdown("## ⚡ PC Solving System")
    st.markdown("---")
    st.markdown("Hệ thống chẩn đoán lỗi và tư vấn linh kiện máy tính chuyên sâu.")
    st.markdown("---")
    if st.button("⟳  PHIÊN MỚI", use_container_width=True):
        st.session_state.messages = []
        st.session_state.greeted = False
        st.session_state.suggestions = []
        st.rerun()
    st.markdown("---")
    st.markdown("<small>Lê Văn Chung · Lớp 10A4 🎓</small>", unsafe_allow_html=True)

# ========================
# HEADER
# ========================
