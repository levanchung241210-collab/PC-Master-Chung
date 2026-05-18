import streamlit as st
import json, re, os, random
from groq import Groq

st.set_page_config(page_title="PC Solving System — Lê Văn Chung 10A4", page_icon="⚡", layout="centered")

# ====================== CSS NÂNG CẤP VALORANT ======================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Barlow+Condensed:wght@400;600;700;800&family=Barlow:wght@300;400;500;600&display=swap');

:root {
    --R: #ff4655;
    --R2: #ff7080;
    --T: #00d4bf;
    --T2: #00ffe7;
    --G: #e8c97a;
    --bg: #0a0b11;
    --panel: #11141f;
}

html, body, .stApp {
    background: var(--bg) !important;
    color: #ece8e1 !important;
    font-family: 'Barlow', sans-serif;
}

/* Background Tactical Valorant */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 0;
    background:
        linear-gradient(135deg, rgba(255,70,85,0.13) 0%, transparent 50%),
        linear-gradient(225deg, rgba(0,212,191,0.09) 0%, transparent 50%),
        repeating-linear-gradient(45deg, transparent, transparent 40px, rgba(255,70,85,0.03) 40px, rgba(255,70,85,0.03) 41px),
        repeating-linear-gradient(-45deg, transparent, transparent 60px, rgba(0,212,191,0.02) 60px, rgba(0,212,191,0.02) 61px);
}

/* Top Red-Teal Bar */
.stApp::after {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, transparent, var(--R), #ff7080, var(--T), var(--T2), transparent);
    box-shadow: 0 0 12px var(--R), 0 0 25px var(--T);
    z-index: 9999;
}

/* Header Valorant */
.valo-header {
    text-align: center;
    padding: 15px 0 8px;
    position: relative;
}

.valo-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: clamp(38px, 9vw, 72px);
    font-weight: 700;
    letter-spacing: 6px;
    text-transform: uppercase;
    color: white;
    text-shadow: 0 0 40px rgba(255,70,85,0.9),
                 0 0 80px rgba(255,70,85,0.4);
}

.valo-title .red {
    color: var(--R);
    text-shadow: 0 0 30px var(--R), 0 0 60px var(--R);
}

/* Greeting Panel - Nâng cấp mạnh */
.valo-greeting {
    position: relative;
    background: linear-gradient(140deg, #1a0f12, #0f1621, #0a1a1a);
    margin: 10px 0 20px;
    padding: 28px 24px;
    border: 1px solid rgba(255,70,85,0.3);
    clip-path: polygon(0 0, 100% 0, 100% 92%, 93% 100%, 0 100%);
    box-shadow: 0 0 60px rgba(255,70,85,0.25),
                inset 0 0 80px rgba(0,212,191,0.08);
    overflow: hidden;
}

.valo-greeting::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, var(--R), var(--T));
}

/* Chat Bubbles Valorant Style */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background: linear-gradient(135deg, #2a1217, #1a0a0e) !important;
    border: 1px solid rgba(255,70,85,0.6) !important;
    border-left: 5px solid var(--R) !important;
    clip-path: polygon(0 0, 100% 0, 100% 100%, 12px 100%, 0 85%);
}

[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    background: linear-gradient(135deg, #0a1f1d, #0f161f) !important;
    border: 1px solid rgba(0,212,191,0.6) !important;
    border-right: 5px solid var(--T) !important;
    clip-path: polygon(12px 0, 100% 0, 100% 85%, 100% 100%, 0 100%);
}

/* Button Style Valorant */
.stButton > button {
    background: rgba(15, 20, 35, 0.95) !important;
    border: 1px solid rgba(0,212,191,0.4) !important;
    border-left: 4px solid var(--T) !important;
    color: #e0f8f5 !important;
    font-weight: 700;
    letter-spacing: 1px;
    transition: all 0.2s ease;
    clip-path: polygon(4% 0, 100% 0, 96% 100%, 0 100%);
}

.stButton > button:hover {
    background: linear-gradient(90deg, rgba(255,70,85,0.15), rgba(0,212,191,0.15)) !important;
    border-color: var(--R) !important;
    color: white !important;
    transform: translateX(8px);
    box-shadow: 0 0 25px rgba(0,212,191,0.5);
}

/* Other improvements */
[data-testid="stChatInput"] textarea {
    border: 2px solid rgba(255,70,85,0.3) !important;
}

[data-testid="stChatInput"] textarea:focus {
    border-color: var(--R) !important;
    box-shadow: 0 0 15px rgba(255,70,85,0.4);
}
</style>
""", unsafe_allow_html=True)

# ====================== PHẦN CODE LOGIC (GIỮ NGUYÊN) ======================
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("❌ Chưa cấu hình GROQ_API_KEY!")
    st.stop()

# Load database...
def load_db():
    if os.path.exists("database_pc.json"):
        with open("database_pc.json","r",encoding="utf-8") as f: 
            return json.load(f)
    return {"loi_he_thong":[],"linh_kien_pc":[]}

data_pc = load_db()
raw = open("database_pc.json","r",encoding="utf-8").read() if os.path.exists("database_pc.json") else "{}"

# System Prompt (đã tối ưu trước đó)
SYSTEM_PROMPT = f"""Bạn là PC & Mobile Solving Expert — Lê Văn Chung 10A4..."""  # (dùng prompt mình đưa trước)

# Tiếp tục code logic chat như trước...
# (Bạn có thể dán phần code logic từ file cũ vào đây)

st.success("✅ Giao diện Valorant đã được nâng cấp!")
