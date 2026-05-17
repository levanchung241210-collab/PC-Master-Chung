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

:root {
    --red:   #ff4655;
    --teal:  #00d4bf;
    --gold:  #e8c97a;
    --purple:#9b59b6;
    --bg0:   #0b0e14;
    --bg1:   #12161f;
    --bg2:   #181c28;
    --cream: #ece8e1;
    --white: #ffffff;
    --silver:#c4c0b8;
    --muted: #7a7875;
    --dim:   #454851;
    --br-r:  rgba(255,70,85,0.25);
    --br-t:  rgba(0,212,191,0.22);
    --br-w:  rgba(255,255,255,0.07);
    --br-w2: rgba(255,255,255,0.11);
}

html, body, .stApp {
    background: var(--bg0) !important;
    color: var(--cream) !important;
    font-family: 'Barlow', sans-serif !important;
}

/* ══ BACKGROUND — Valorant map panels ══ */
.stApp::before {
    content: '';
    position: fixed; inset: 0;
    pointer-events: none; z-index: 0;
    background:
        /* Top-left red panel */
        radial-gradient(ellipse 40% 30% at 0% 0%,
            rgba(255,70,85,0.08) 0%, transparent 70%),
        /* Bottom-right teal panel */
        radial-gradient(ellipse 40% 30% at 100% 100%,
            rgba(0,212,191,0.06) 0%, transparent 70%),
        /* Center gold glow */
        radial-gradient(ellipse 60% 40% at 50% 50%,
            rgba(232,201,122,0.03) 0%, transparent 70%),
        /* Slash lines red */
        repeating-linear-gradient(-50deg,
            transparent 0px, transparent 55px,
            rgba(255,70,85,0.022) 55px,
            rgba(255,70,85,0.022) 56px),
        /* Slash lines teal */
        repeating-linear-gradient(40deg,
            transparent 0px, transparent 85px,
            rgba(0,212,191,0.012) 85px,
            rgba(0,212,191,0.012) 86px);
}

/* Top bar */
.stApp::after {
    content: '';
    position: fixed; top:0; left:0; right:0; height:3px;
    background: linear-gradient(90deg,
        var(--red) 0%, var(--red) 80px,
        transparent 240px, transparent calc(100% - 240px),
        var(--teal) calc(100% - 80px), var(--teal) 100%);
    z-index: 9999;
}

/* ══ HEADER ══ */
.valo-header { text-align:center; padding:10px 0 2px; position:relative; }

.valo-author {
    font-family:'Barlow Condensed',sans-serif;
    font-size:10px; font-weight:700; letter-spacing:2.5px;
    text-transform:uppercase; color:#00f0ff;
    text-shadow:0 0 8px rgba(0,240,255,0.5);
    text-align:right; margin-bottom:2px;
    display:flex; align-items:center; justify-content:flex-end; gap:5px;
}
.valo-author::before { content:''; width:14px; height:1px; background:#00f0ff; opacity:.6; }

.valo-eyebrow {
    font-family:'Barlow Condensed',sans-serif;
    font-size:clamp(9px,2vw,11px); font-weight:700;
    letter-spacing:6px; color:var(--red); text-transform:uppercase;
    margin-bottom:6px;
    display:flex; align-items:center; justify-content:center; gap:12px;
}
.valo-eyebrow::before { content:''; width:32px; height:1px; background:linear-gradient(90deg,transparent,var(--red)); opacity:.6; }
.valo-eyebrow::after  { content:''; width:32px; height:1px; background:linear-gradient(90deg,var(--red),transparent); opacity:.6; }

.valo-logo-wrap {
    display:flex; align-items:center; justify-content:center; gap:14px; margin-bottom:4px;
}

/* LVC LOGO — Valorant style */
.lvc-logo {
    width:clamp(38px,7vw,52px); height:clamp(38px,7vw,52px);
    position:relative; flex-shrink:0;
}
.lvc-logo svg { width:100%; height:100%; }

.valo-title {
    font-family:'Rajdhani',sans-serif;
    font-size:clamp(30px,7.5vw,62px); font-weight:700;
    letter-spacing:3px; line-height:1; color:var(--white);
    text-transform:uppercase; margin:0;
    text-shadow:0 0 40px rgba(255,70,85,0.15);
}
.valo-title .red   { color:var(--red); }
.valo-title .slash { color:var(--red); opacity:.55; margin:0 2px; }

.valo-subtitle {
    font-family:'Barlow Condensed',sans-serif;
    font-size:clamp(11px,2.8vw,14px); font-weight:700;
    letter-spacing:4px; text-transform:uppercase;
    margin-top:8px;
    display:flex; align-items:center; justify-content:center;
    gap:8px; flex-wrap:wrap;
}
.sub-r { color:var(--red); }
.sub-w { color:var(--white); }
.sub-t { color:var(--teal); }
.sub-d {
    display:inline-block; width:4px; height:4px;
    transform:rotate(45deg); opacity:.6;
}
.sub-d.r { background:var(--red); }
.sub-d.t { background:var(--teal); }

/* Divider */
.valo-divider { display:flex; align-items:center; margin:12px 0 8px; }
.valo-divider::before, .valo-divider::after { content:''; flex:1; height:1px; background:var(--br-w); }
.valo-divider-inner { display:flex; align-items:center; gap:5px; padding:0 12px; }
.vd { width:5px; height:5px; transform:rotate(45deg); }
.vd.r { background:var(--red); }
.vd.t { background:var(--teal); width:4px; height:4px; opacity:.7; }
.vdbar {
    width:50px; height:2px;
    background:linear-gradient(90deg,var(--red),var(--teal));
    clip-path:polygon(5px 0%,100% 0%,calc(100% - 5px) 100%,0% 100%);
}

/* ══ GREETING BOX ══ */
.valo-greeting {
    position:relative;
    background:linear-gradient(135deg,
        rgba(28,32,46,0.92) 0%,
        rgba(16,20,30,0.95) 100%);
    border:1px solid var(--br-r);
    border-top:2px solid var(--red);
    border-radius:2px;
    padding:clamp(18px,5vw,28px) clamp(16px,5vw,28px) clamp(14px,4vw,22px);
    margin:4px 0 14px;
    overflow:hidden;
    box-shadow:0 8px 32px rgba(0,0,0,0.5),
               inset 0 1px 0 rgba(255,255,255,0.04);
}
/* Corner cut top-left */
.valo-greeting::before {
    content:''; position:absolute; top:0; left:0;
    border-style:solid; border-width:22px 22px 0 0;
    border-color:var(--bg0) transparent transparent transparent;
}
/* Teal glow bottom-right */
.valo-greeting::after {
    content:''; position:absolute; bottom:-40px; right:-40px;
    width:180px; height:180px;
    background:radial-gradient(circle,rgba(0,212,191,0.07) 0%,transparent 65%);
    pointer-events:none;
}
/* Red corner bottom-left */
.vg-corner-bl {
    position:absolute; bottom:0; left:0;
    border-style:solid; border-width:0 0 16px 16px;
    border-color:transparent transparent rgba(255,70,85,0.3) transparent;
}
.valo-vbar {
    position:absolute; left:0; top:15%; bottom:15%;
    width:3px;
    background:linear-gradient(180deg,transparent 0%,var(--red) 35%,var(--teal) 65%,transparent 100%);
    opacity:.7;
}
.valo-status-row { display:flex; align-items:center; justify-content:center; gap:6px; margin-bottom:10px; }
.valo-status-dot {
    width:6px; height:6px; background:var(--teal); border-radius:50%;
    box-shadow:0 0 8px var(--teal); animation:pulse 2s infinite;
}
@keyframes pulse { 0%,100%{opacity:1;box-shadow:0 0 8px var(--teal);} 50%{opacity:.4;box-shadow:0 0 2px var(--teal);} }
.valo-status-text {
    font-family:'Barlow Condensed',sans-serif; font-size:10px; font-weight:700;
    letter-spacing:3px; color:var(--teal); text-transform:uppercase;
}
.valo-greeting-icon {
    font-size:clamp(28px,5vw,36px); display:block; text-align:center; margin-bottom:8px;
    filter:drop-shadow(0 0 12px rgba(255,70,85,0.6));
}
.valo-greeting-title {
    font-family:'Rajdhani',sans-serif;
    font-size:clamp(15px,4vw,21px); font-weight:700;
    color:var(--white); text-align:center; text-transform:uppercase;
    letter-spacing:2px; margin-bottom:8px;
}
.valo-greeting-sub {
    font-size:clamp(12px,3vw,13.5px); color:var(--silver);
    text-align:center; line-height:1.7;
}
.valo-stats {
    display:flex; justify-content:center; gap:clamp(12px,3vw,24px);
    margin-top:14px; padding-top:12px; border-top:1px solid var(--br-w);
}
.valo-stat { text-align:center; line-height:1.2; }
.valo-stat-num {
    font-family:'Rajdhani',sans-serif;
    font-size:clamp(16px,4vw,22px); font-weight:700; color:var(--red); display:block;
}
.valo-stat-label {
    font-family:'Barlow Condensed',sans-serif;
    font-size:9px; letter-spacing:2px; color:var(--dim); text-transform:uppercase;
}
.valo-stat-div { width:1px; background:var(--br-w2); align-self:stretch; }

/* ══ SUGGEST LABEL ══ */
.valo-suggest-label {
    display:flex; align-items:center; gap:10px; margin:8px 0 12px;
}
.valo-suggest-label::before,
.valo-suggest-label::after { content:''; flex:1; height:1px; background:rgba(255,255,255,.08); }
.valo-suggest-label span {
    background:var(--red); color:var(--white);
    font-family:'Barlow Condensed',sans-serif;
    font-size:12px; font-weight:800; letter-spacing:2px; text-transform:uppercase;
    padding:4px 16px;
    clip-path:polygon(8px 0,100% 0,calc(100% - 8px) 100%,0 100%);
    box-shadow:0 4px 16px rgba(255,70,85,0.35);
}

/* ══ BUTTONS ══ */
.stButton > button {
    background:linear-gradient(90deg,rgba(28,32,46,0.9),rgba(18,22,32,0.95)) !important;
    color:var(--white) !important;
    border:1px solid rgba(0,212,191,0.18) !important;
    border-left:3px solid var(--teal) !important;
    border-radius:2px !important;
    font-family:'Barlow Condensed',sans-serif !important;
    font-size:clamp(12px,3vw,14px) !important;
    font-weight:700 !important;
    letter-spacing:.5px !important;
    padding:11px 14px !important;
    width:100% !important;
    text-align:left !important;
    white-space:normal !important;
    min-height:48px !important;
    line-height:1.4 !important;
    transition:all .12s ease !important;
    box-shadow:0 2px 8px rgba(0,0,0,.35) !important;
}
.stButton > button:hover {
    background:linear-gradient(90deg,rgba(0,212,191,0.15),rgba(255,70,85,0.08)) !important;
    border-left-color:var(--red) !important;
    border-color:rgba(0,212,191,.3) !important;
    transform:translateX(4px) !important;
    box-shadow:0 4px 16px rgba(0,212,191,.25) !important;
}

/* ══ CHAT AVATARS — custom Valorant icons ══ */
/* USER avatar — red Omen style */
[data-testid="chatAvatarIcon-user"] {
    background:linear-gradient(135deg,#c0303d,#7a1a22) !important;
    border:2px solid var(--red) !important;
    border-radius:3px !important;
    font-size:14px !important;
    box-shadow:0 0 10px rgba(255,70,85,.4) !important;
    display:flex; align-items:center; justify-content:center;
    overflow:hidden;
}
[data-testid="chatAvatarIcon-user"]::before {
    content:'⚡';
    font-size:14px; line-height:1;
}
[data-testid="chatAvatarIcon-user"] img,
[data-testid="chatAvatarIcon-user"] svg { display:none !important; }

/* BOT avatar — teal Cypher style */
[data-testid="chatAvatarIcon-assistant"] {
    background:linear-gradient(135deg,#005a52,#001f1c) !important;
    border:2px solid var(--teal) !important;
    border-radius:3px !important;
    font-size:14px !important;
    box-shadow:0 0 10px rgba(0,212,191,.35) !important;
    display:flex; align-items:center; justify-content:center;
    overflow:hidden;
}
[data-testid="chatAvatarIcon-assistant"]::before {
    content:'🖥';
    font-size:13px; line-height:1;
}
[data-testid="chatAvatarIcon-assistant"] img,
[data-testid="chatAvatarIcon-assistant"] svg { display:none !important; }

/* ══ CHAT MESSAGES ══ */
[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) {
    background:linear-gradient(135deg,
        rgba(55,12,18,0.88) 0%,
        rgba(22,10,14,0.96) 100%) !important;
    border:1px solid rgba(255,70,85,.35) !important;
    border-right:4px solid var(--red) !important;
    border-radius:4px !important;
    padding:13px 16px !important;
    margin:6px 0 !important;
    box-shadow:0 4px 16px rgba(0,0,0,.5),
               inset 0 1px 0 rgba(255,70,85,.08) !important;
}
[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-assistant"]) {
    background:linear-gradient(135deg,
        rgba(8,38,42,0.88) 0%,
        rgba(10,16,22,0.96) 100%) !important;
    border:1px solid rgba(0,212,191,.28) !important;
    border-left:4px solid var(--teal) !important;
    border-radius:4px !important;
    padding:13px 16px !important;
    margin:6px 0 !important;
    box-shadow:0 4px 16px rgba(0,0,0,.5),
               inset 0 1px 0 rgba(0,212,191,.06) !important;
}

[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li {
    font-size:clamp(13.5px,3.8vw,15px) !important;
    line-height:1.8 !important;
    color:#f0ece6 !important;
    text-shadow:0 1px 3px rgba(0,0,0,.8) !important;
}
[data-testid="stChatMessage"] h3 {
    font-family:'Rajdhani',sans-serif !important;
    font-size:clamp(14px,4vw,18px) !important;
    font-weight:700 !important; text-transform:uppercase !important;
    letter-spacing:2px !important; color:var(--white) !important;
    margin-bottom:8px !important; padding-bottom:5px !important;
    border-bottom:1px solid rgba(255,255,255,.08) !important;
}
[data-testid="stChatMessage"] strong { color:#ffb3ba !important; font-weight:700 !important; }
[data-testid="stChatMessage"] em {
    color:var(--teal) !important; font-style:normal !important;
    font-size:11px !important; opacity:.8 !important;
}
[data-testid="stChatMessage"] code {
    background:rgba(0,212,191,.12) !important; color:#55ffeb !important;
    border:1px solid rgba(0,212,191,.3) !important;
    border-radius:2px !important; padding:1px 6px !important; font-size:12px !important;
}

/* ══ CHAT INPUT ══ */
.stChatInput textarea {
    background:var(--bg2) !important; color:var(--cream) !important;
    border:1px solid var(--br-w2) !important;
    border-bottom:2px solid rgba(255,70,85,.22) !important;
    border-radius:2px !important;
    font-family:'Barlow',sans-serif !important;
    font-size:clamp(13px,3.5vw,14px) !important;
    caret-color:var(--red) !important;
}
.stChatInput textarea:focus {
    border-bottom-color:var(--red) !important;
    box-shadow:0 4px 20px rgba(255,70,85,.07) !important;
}
.stChatInput textarea::placeholder { color:var(--dim) !important; }

/* ══ SIDEBAR ══ */
section[data-testid="stSidebar"] {
    background:#090c11 !important;
    border-right:1px solid var(--br-r) !important;
}
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] div,
section[data-testid="stSidebar"] small { color:var(--muted) !important; font-size:13px !important; }
section[data-testid="stSidebar"] h2 {
    font-family:'Rajdhani',sans-serif !important; font-size:17px !important;
    color:var(--cream) !important; text-transform:uppercase !important; letter-spacing:3px !important;
}
section[data-testid="stSidebar"] .stButton > button {
    background:transparent !important;
    border:1px solid var(--br-r) !important; border-left:2px solid var(--red) !important;
    color:var(--muted) !important;
    font-family:'Barlow Condensed',sans-serif !important;
    font-weight:700 !important; letter-spacing:1px !important; box-shadow:none !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background:rgba(255,70,85,.07) !important; color:var(--cream) !important;
    transform:none !important;
}

[data-testid="stSpinner"] p {
    color:var(--teal) !important;
    font-family:'Barlow Condensed',sans-serif !important;
    letter-spacing:4px !important; font-size:11px !important; text-transform:uppercase !important;
}

#MainMenu, footer, header { visibility:hidden !important; }
.block-container {
    padding-top:1.2rem !important; padding-bottom:1.5rem !important; max-width:760px !important;
}

@media (max-width:600px) {
    .block-container { padding:.7rem .5rem 4.5rem !important; }
    .valo-author { position:relative !important; top:0 !important; justify-content:center !important; margin-bottom:10px !important; }
    .valo-author::before { display:none; }
    [data-testid="stChatMessage"] { padding:10px 12px !important; margin:4px 0 !important; }
    .stButton > button { min-height:44px !important; padding:9px 11px !important; }
    .valo-greeting { padding:16px 12px !important; }
    .valo-stats { gap:10px; }
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

data_pc          = load_database()
raw_json_context = load_raw_json()
db_loi           = len(data_pc.get("loi_he_thong", []))
db_lk            = len(data_pc.get("linh_kien_pc",  []))

# ========================
# SIDEBAR
# ========================
with st.sidebar:
    st.markdown("## ⚡ PC Solving")
    st.markdown("---")
    st.markdown("Hệ thống chẩn đoán lỗi và tư vấn linh kiện máy tính chuyên sâu.")
    st.markdown("---")
    if st.button("⟳  PHIÊN MỚI", use_container_width=True):
        st.session_state.messages     = []
        st.session_state.greeted      = False
        st.session_state.suggestions  = []
        st.rerun()
    st.markdown("---")
    st.markdown("<small>Lê Văn Chung · Lớp 10A4 🎓</small>", unsafe_allow_html=True)

# ========================
# LVC LOGO SVG
# ========================
LVC_SVG = """
<svg viewBox="0 0 52 52" xmlns="http://www.w3.org/2000/svg">
  <!-- Outer hexagon-like shape -->
  <polygon points="26,2 48,14 48,38 26,50 4,38 4,14"
    fill="none" stroke="#ff4655" stroke-width="2" opacity="0.9"/>
  <!-- Inner accent -->
  <polygon points="26,8 42,17 42,35 26,44 10,35 10,17"
    fill="rgba(255,70,85,0.07)" stroke="rgba(0,212,191,0.4)" stroke-width="1"/>
  <!-- LVC text -->
  <text x="26" y="32" text-anchor="middle"
    font-family="Rajdhani,sans-serif" font-size="14" font-weight="700"
    fill="#ffffff" letter-spacing="1">LVC</text>
  <!-- Red corner slash -->
  <line x1="4" y1="14" x2="12" y2="22" stroke="#ff4655" stroke-width="1.5" opacity="0.5"/>
</svg>
"""

# ========================
# HEADER
# ========================
st.markdown(f"""
<div class="valo-header">
    <div class="valo-author">Lê Văn Chung · 10A4</div>
    <div class="valo-eyebrow">⚡ STEM PROJECT ⚡</div>
    <div class="valo-logo-wrap">
        <div class="lvc-logo">{LVC_SVG}</div>
        <div class="valo-title">PC<span class="slash">/</span><span class="red">SOLVING</span></div>
    </div>
    <div class="valo-subtitle">
        <span class="sub-d r"></span>
        <span class="sub-r">CHẨN ĐOÁN</span>
        <span class="sub-d r"></span>
        <span class="sub-w">PHÂN TÍCH</span>
        <span class="sub-d t"></span>
        <span class="sub-t">XỬ LÝ TỰ ĐỘNG</span>
        <span class="sub-d t"></span>
    </div>
</div>
<div class="valo-divider">
    <div class="valo-divider-inner">
        <div class="vd r"></div>
        <div class="vdbar"></div>
        <div class="vd t"></div>
    </div>
</div>
""", unsafe_allow_html=True)

# ========================
# SESSION STATE
# ========================
if "messages"      not in st.session_state: st.session_state.messages      = []
if "greeted"       not in st.session_state: st.session_state.greeted       = False
if "suggestions"   not in st.session_state: st.session_state.suggestions   = []
if "pending_query" not in st.session_state: st.session_state.pending_query = None

# ========================
# GỢI Ý — 32 CÂU ĐA DẠNG
# ========================
ALL_SUGGESTIONS = [
    # Lỗi hệ thống
    ("⚠  Màn hình xanh BSOD đột ngột",       "Máy tính bị màn hình xanh chết đột ngột, phải làm gì?"),
    ("▪  Màn hình đen không hiển thị",         "Máy lên nguồn nhưng màn hình đen, không có tín hiệu"),
    ("◈  PC bíp dài khi khởi động",            "Máy bíp dài liên tục khi bật, không vào được Windows"),
    ("◉  Windows boot loop — khởi động lại",   "Máy cứ khởi động lại liên tục, không vào được Windows"),
    ("✕  Lỗi 0xc0000005 văng game",            "Game bị lỗi 0xc0000005, không mở được, cách fix?"),
    ("✕  Lỗi 0xc000021a không vào Windows",    "Máy báo lỗi 0xc000021a, không boot được vào Windows"),
    ("⚠  PC tự khởi động lại khi chơi game",   "PC tự reboot đột ngột trong lúc chơi game nặng"),
    ("▪  Máy không nhận bàn phím, chuột USB",  "Cắm USB chuột bàn phím vào máy không nhận, lỗi gì?"),
    ("◈  Ổ cứng SSD không nhận trong BIOS",    "BIOS không nhận ổ SSD NVMe sau khi lắp vào mainboard"),
    ("◉  Lỗi No Boot Device khi bật máy",      "Máy báo No Boot Device Found, không vào được hệ điều hành"),
    # Phần cứng
    ("🌡  CPU 95°C — overheat nghiêm trọng",   "CPU nhiệt độ lên đến 95 độ C khi chạy game, nguy hiểm không?"),
    ("◆  RAM 8GB có đủ cho game 2024?",         "RAM 8GB có đủ dùng để chơi game hiện đại năm 2024 không?"),
    ("⚡  Nguồn bao nhiêu W cho RTX 3060?",     "RTX 3060 cần nguồn bao nhiêu W, dùng nguồn 500W được không?"),
    ("◆  Tản nhiệt nước hay tản nhiệt khí?",    "Nên dùng tản nhiệt nước hay tản nhiệt khí cho i5-12400F?"),
    ("▶  SSD NVMe vs SSD SATA khác gì?",        "SSD NVMe và SSD SATA khác nhau ở điểm gì, nên mua loại nào?"),
    ("◉  RAM 2 thanh 8GB vs 1 thanh 16GB",      "Lắp 2 thanh RAM 8GB hay 1 thanh 16GB thì nhanh hơn?"),
    # CPU
    ("◆  i5-12400F có chơi game mượt không?",   "i5-12400F hiệu năng thế nào, chơi game 2024 có đủ không?"),
    ("▶  i5 vs Ryzen 5 tầm 3-4 triệu",         "Tầm giá 3-4 triệu nên chọn Intel i5 hay AMD Ryzen 5?"),
    ("◈  i3-12100F có bị bottleneck RTX 3060?", "i3-12100F dùng với RTX 3060 có bị cổ chai hiệu năng không?"),
    ("⚡  CPU Ryzen 5 5600X có cần tản rời?",   "Ryzen 5 5600X có kèm tản nhiệt box dùng được không?"),
    # VGA / Card đồ họa
    ("🎮  GTX 1650 chơi được game gì ở FHD?",   "GTX 1650 chơi mượt những game nào ở độ phân giải 1080p?"),
    ("▶  RTX 3060 vs RX 6600 cái nào tốt hơn?", "So sánh RTX 3060 và RX 6600, nên chọn card nào?"),
    ("◆  RTX 4060 có đáng mua hơn RTX 3060?",   "RTX 4060 mới có đáng mua hơn RTX 3060 về giá tiền không?"),
    ("◉  VGA onboard đủ dùng cho văn phòng?",   "Dùng Intel UHD Graphics (iGPU) cho văn phòng có đủ không?"),
    # Mainboard
    ("◆  H610 hay B660 nên chọn cái nào?",      "Mainboard H610 và B660 khác nhau thế nào, nên mua loại nào?"),
    ("▪  Socket LGA1700 dùng CPU đời mấy?",     "Socket LGA1700 hỗ trợ những CPU Intel đời mấy?"),
    ("◈  Mainboard B550 có dùng được Ryzen 5?", "Mainboard B550 có tương thích với Ryzen 5 5600X không?"),
    # Điện thoại / Mobile chip
    ("📱  Snapdragon 888 nóng máy có bình thường?","Chip Snapdragon 888 bị nóng máy nhiều có phải lỗi không?"),
    ("📱  Dimensity 9200 mạnh hơn Snap 8 Gen2?", "So sánh Dimensity 9200 với Snapdragon 8 Gen 2 loại nào mạnh?"),
    ("📱  iPhone A17 Pro mạnh cỡ nào so Android?","Chip Apple A17 Pro mạnh đến đâu so với chip Android cao cấp?"),
    # Build PC
    ("⚡  Build PC 10 triệu chơi game FHD",      "Gợi ý cấu hình PC build 10 triệu đồng chơi game Full HD mượt"),
    ("◆  Combo i5-12400F + RTX 3060 có tốt?",   "Combo i5-12400F với RTX 3060 12GB chơi game có bottleneck không?"),
]

# Đảm bảo gợi ý thật sự ngẫu nhiên mỗi lần
if not st.session_state.suggestions:
    st.session_state.suggestions = random.sample(ALL_SUGGESTIONS, 4)

# ========================
# GREETING BOX — luôn hiển thị
# ========================
st.markdown(f"""
<div class="valo-greeting">
    <div class="valo-vbar"></div>
    <div class="vg-corner-bl"></div>
    <div class="valo-status-row">
        <div class="valo-status-dot"></div>
        <div class="valo-status-text">Hệ thống sẵn sàng</div>
    </div>
    <span class="valo-greeting-icon">⚡</span>
    <div class="valo-greeting-title">Hệ thống phân tích phần cứng máy tính</div>
    <div class="valo-greeting-sub">
        Nhập mã hiệu linh kiện hoặc mô tả hiện tượng lỗi hệ thống.<br>
        Thuật toán phân tích tự động sẽ đưa ra giải pháp ngay lập tức.
    </div>
    <div class="valo-stats">
        <div class="valo-stat">
            <span class="valo-stat-num">{db_loi}</span>
            <span class="valo-stat-label">Lỗi hệ thống</span>
        </div>
        <div class="valo-stat-div"></div>
        <div class="valo-stat">
            <span class="valo-stat-num">{db_lk}</span>
            <span class="valo-stat-label">Linh kiện PC</span>
        </div>
        <div class="valo-stat-div"></div>
        <div class="valo-stat">
            <span class="valo-stat-num" style="color:var(--teal)">24/7</span>
            <span class="valo-stat-label">Hỗ trợ</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="valo-suggest-label"><span>CHỌN NHANH VẤN ĐỀ</span></div>',
            unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="small")
for i, (label, query) in enumerate(st.session_state.suggestions):
    with (col1 if i % 2 == 0 else col2):
        if st.button(label, key=f"sug_{i}"):
            st.session_state.greeted      = True
            st.session_state.pending_query = query
            st.rerun()

# ========================
# CHAT HISTORY
# ========================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ========================
# DATABASE SEARCH
# ========================
def calculate_match_score(item, q_clean, user_numbers):
    score      = 0
    item_kws   = [str(kw).lower().strip() for kw in item.get("keywords", [])]
    user_words = q_clean.split()
    for kw in item_kws:
        if kw in user_words or (kw.isdigit() and kw in q_clean):
            score += 1
    if score == 0: return 0
    item_nums = [re.sub(r'\D','',kw) for kw in item_kws if re.search(r'\d{3,}',kw)]
    item_nums = [n for n in item_nums if n]
    if item_nums and user_numbers:
        if not set(item_nums).intersection(set(user_numbers)): return 0
    return score

def search_database(user_query):
    q_clean      = re.sub(r'[-–_,.\?!\(\)]',' ', user_query.lower().strip())
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
            return (f"### ✕  {best_match['ten']}\n"
                    f"*— Lê Văn Chung 10A4*\n\n"
                    f"**⚠ Nguyên nhân:** {best_match['nguyen_nhan']}\n\n"
                    f"**◈ Khắc phục:**\n{best_match['giai_phap']}")
        else:
            return (f"### ◆  {best_match['ten']}\n"
                    f"*— Lê Văn Chung 10A4*\n\n"
                    f"**⚙ Thông số:** {best_match.get('thong_so','')}\n\n"
                    f"**◉ Socket:** `{best_match.get('socket','')}`\n\n"
                    f"**▶ Tư vấn:** {best_match.get('chuyen_gia_tu_van','')}")
    return None

# ========================
# PHÂN LOẠI CÂU HỎI
# ========================
def detect_type(query):
    q   = query.lower()
    hw  = ["i3","i5","i7","i9","ryzen","gtx","rtx","rx","vga","card","cpu","ram","ssd",
           "mainboard","main","nguồn","psu","tản nhiệt","socket","ddr","mua","so sánh",
           "nên chọn","upgrade","nâng cấp","combo","build","cấu hình","snapdragon",
           "dimensity","exynos","helio","chip","điện thoại","iphone","samsung"]
    err = ["lỗi","bsod","xanh","đen","bíp","crash","sập","đơ","treo","chậm","lag",
           "không bật","không lên","restart","khởi động","update","0x","error","fix","sửa",
           "boot","không nhận","không vào"]
    for w in hw:
        if w in q: return "hardware"
    for w in err:
        if w in q: return "error"
    return "general"

# ========================
# SYSTEM PROMPTS — SMARTER
# ========================
BASE_RULE = """
TUYỆT ĐỐI KHÔNG dùng: "AI","mô hình ngôn ngữ","LLM","Groq","Meta","Llama","trí tuệ nhân tạo".
Không nhắc đến việc bạn là phần mềm học từ internet.
QUAN TRỌNG: Đọc KỸ toàn bộ câu hỏi của người dùng trước khi trả lời.
Không được trả lời theo khuôn mẫu cứng nhắc — phân tích ĐÚNG những gì người dùng đang hỏi.
Nếu câu hỏi có nhiều thành phần (ví dụ: hỏi về hiệu năng + nhiệt độ + combo), hãy trả lời ĐỦ tất cả các phần đó.
"""

PROMPT_ERROR = f"""Bạn là hệ thống chẩn đoán lỗi máy tính của Lê Văn Chung 10A4.
{BASE_RULE}
Kho dữ liệu tham chiếu: {raw_json_context}

QUY TẮC TRẢ LỜI LỖI — NGẮN GỌN, ĐÚNG VẤN ĐỀ:
- Đọc kỹ câu hỏi, trả lời ĐÚNG lỗi được hỏi
- 1 câu nguyên nhân chính
- Tối đa 4 bước xử lý, mỗi bước ngắn gọn súc tích
- Không lặp lại câu hỏi, không giải thích thừa
- Cuối thêm 1 tip phòng tránh ngắn nếu có ích"""

PROMPT_HARDWARE = f"""Bạn là chuyên gia tư vấn linh kiện PC và điện tử của Lê Văn Chung 10A4.
{BASE_RULE}
Kho dữ liệu tham chiếu: {raw_json_context}

QUY TẮC TƯ VẤN LINH KIỆN — CHI TIẾT, ĐÚNG TRỌNG TÂM:
- Đọc kỹ câu hỏi: người dùng hỏi gì thì trả lời ĐÚNG cái đó
- Nêu thông số kỹ thuật QUAN TRỌNG, không liệt kê tất cả
- So sánh ưu/nhược điểm nếu câu hỏi yêu cầu so sánh
- Gợi ý combo hoặc lựa chọn thay thế nếu phù hợp
- Kết thúc bằng 1 khuyến nghị cụ thể rõ ràng
- Khi phân tích chuyên sâu mở đầu: "Dựa trên cơ sở dữ liệu kỹ thuật của tác giả Lê Văn Chung 10A4..." """

PROMPT_GENERAL = f"""Bạn là hệ thống hỗ trợ kỹ thuật máy tính và điện tử của Lê Văn Chung 10A4.
{BASE_RULE}
Kho dữ liệu tham chiếu: {raw_json_context}
Trả lời tiếng Việt, súc tích, đúng trọng tâm câu hỏi, chia bước nếu cần."""

def ask_engine(user_query, chat_history):
    qtype = detect_type(user_query)
    if   qtype == "error":    system, max_tok, temp = PROMPT_ERROR,    500, 0.3
    elif qtype == "hardware": system, max_tok, temp = PROMPT_HARDWARE, 800, 0.5
    else:                     system, max_tok, temp = PROMPT_GENERAL,  600, 0.4

    messages = [{"role":"system","content":system}]
    for msg in chat_history[-6:]:
        messages.append({"role":msg["role"],"content":msg["content"]})
    messages.append({"role":"user","content":user_query})
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages, max_tokens=max_tok, temperature=temp
    )
    return response.choices[0].message.content

# ========================
# XỬ LÝ TIN NHẮN
# ========================
def handle_message(prompt):
    st.session_state.messages.append({"role":"user","content":prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("ĐANG PHÂN TÍCH DỮ LIỆU..."):
            try:
                answer = search_database(prompt) or ask_engine(prompt, st.session_state.messages)
                st.markdown(answer)
                st.session_state.messages.append({"role":"assistant","content":answer})
            except:
                st.error("❌ Hệ thống gián đoạn. Vui lòng thử lại.")

if st.session_state.pending_query:
    q = st.session_state.pending_query
    st.session_state.pending_query = None
    handle_message(q)

if prompt := st.chat_input("Nhập mã lỗi hoặc linh kiện cần phân tích..."):
    st.session_state.greeted = True
    handle_message(prompt)
