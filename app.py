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
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@600;700&family=Barlow+Condensed:wght@400;600;700;800&family=Barlow:wght@300;400;500&display=swap');

:root {
    --red:        #ff4655;
    --red-soft:   #ff465580;
    --red-dim:    #c0303d;
    --red-panel:  rgba(255,70,85,0.07);
    --dark:       #10131a;
    --dark2:      #161923;
    --dark3:      #1c2030;
    --cream:      #ece8e1;
    --white:      #ffffff;
    --muted:      #9a9891;
    --muted2:     #5c5e68;
    --border-r:   rgba(255,70,85,0.25);
    --border-w:   rgba(255,255,255,0.07);
}

/* =====================
   BASE RESET
===================== */
html, body, .stApp {
    background: var(--dark) !important;
    color: var(--cream) !important;
    font-family: 'Barlow', sans-serif !important;
}

/* =====================
   BACKGROUND — Valorant style
   Subtle dark panel lines + faint red slash
===================== */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        /* faint horizontal scanlines */
        repeating-linear-gradient(
            180deg,
            transparent 0px,
            transparent 3px,
            rgba(255,255,255,0.008) 3px,
            rgba(255,255,255,0.008) 4px
        ),
        /* diagonal slash accent */
        repeating-linear-gradient(
            -50deg,
            transparent 0px,
            transparent 80px,
            rgba(255,70,85,0.025) 80px,
            rgba(255,70,85,0.025) 81px
        );
    pointer-events: none;
    z-index: 0;
}

/* Top red bar — signature Valorant element */
.stApp::after {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--red) 0%, var(--red) 120px, transparent 400px);
    z-index: 9999;
}

/* =====================
   HEADER
===================== */
.valo-header {
    text-align: center;
    padding: 8px 0 4px;
}

.valo-eyebrow {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: clamp(9px, 2vw, 11px);
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

/* Big title — white + red highlight */
.valo-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: clamp(32px, 8vw, 64px);
    font-weight: 700;
    letter-spacing: 2px;
    line-height: 0.95;
    color: var(--white);
    text-transform: uppercase;
    margin: 0 0 6px;
    text-shadow: 0 2px 30px rgba(0,0,0,0.5);
}
.valo-title .highlight {
    color: var(--red);
    position: relative;
}

/* Subtitle — high contrast now */
.valo-subtitle {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: clamp(11px, 2.5vw, 13px);
    font-weight: 600;
    letter-spacing: 4px;
    color: #c4c0b9;           /* brighter than before */
    text-transform: uppercase;
    margin-top: 4px;
}

/* Divider */
.valo-divider {
    display: flex;
    align-items: center;
    margin: 12px 0 10px;
}
.valo-divider::before,
.valo-divider::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border-w);
}
.valo-divider-core {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 0 12px;
}
.valo-divider-bar {
    width: 40px; height: 2px;
    background: var(--red);
    clip-path: polygon(6px 0%, 100% 0%, calc(100%-6px) 100%, 0% 100%);
}
.valo-divider-dot {
    width: 4px; height: 4px;
    background: var(--red);
    transform: rotate(45deg);
}

/* =====================
   GREETING BOX
   Valorant card panel style
===================== */
.valo-greeting {
    position: relative;
    background: var(--dark2);
    border: 1px solid var(--border-r);
    border-top: 2px solid var(--red);
    border-radius: 2px;
    padding: clamp(18px, 5vw, 26px) clamp(16px, 5vw, 28px);
    margin: 4px 0 6px;
    overflow: hidden;
}

/* Top-left corner cut — Valorant signature */
.valo-greeting::before {
    content: '';
    position: absolute;
    top: -1px; left: -1px;
    width: 0; height: 0;
    border-style: solid;
    border-width: 20px 20px 0 0;
    border-color: var(--dark) transparent transparent transparent;
}

/* Bottom-right glow */
.valo-greeting::after {
    content: '';
    position: absolute;
    bottom: -40px; right: -40px;
    width: 120px; height: 120px;
    background: radial-gradient(circle, rgba(255,70,85,0.06) 0%, transparent 70%);
    pointer-events: none;
}

/* Red vertical accent bar inside */
.valo-greeting-accent {
    position: absolute;
    left: 0; top: 20%;
    width: 3px;
    height: 60%;
    background: linear-gradient(180deg, transparent, var(--red), transparent);
    opacity: 0.6;
}

.valo-greeting-icon {
    font-size: clamp(26px, 5vw, 34px);
    display: block;
    text-align: center;
    margin-bottom: 10px;
    filter: drop-shadow(0 0 8px rgba(255,70,85,0.4));
}

.valo-greeting-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: clamp(15px, 4vw, 20px);
    font-weight: 700;
    color: var(--white);          /* pure white — readable anywhere */
    text-align: center;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 8px;
    text-shadow: 0 1px 10px rgba(0,0,0,0.6);
}

.valo-greeting-sub {
    font-size: clamp(12px, 3vw, 13px);
    color: #b8b5af;               /* much brighter than before */
    text-align: center;
    line-height: 1.7;
    font-weight: 400;
}

/* =====================
   SUGGEST LABEL — visible outdoors
===================== */
.valo-suggest-label {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 16px 0 10px;
}
.valo-suggest-label::before,
.valo-suggest-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: rgba(255,255,255,0.08);
}
.valo-suggest-label span {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 3px;
    color: #6b6e7a;               /* slightly brighter */
    text-transform: uppercase;
    white-space: nowrap;
}

/* =====================
   BUTTONS — Valorant agent select style
===================== */
.stButton > button {
    background: var(--dark2) !important;
    color: #d4d0cb !important;    /* bright enough outdoors */
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-left: 2px solid rgba(255,70,85,0.3) !important;
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
    position: relative !important;
    overflow: hidden !important;
}
.stButton > button::after {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 0px;
    background: var(--red);
    transition: width 0.12s ease;
    opacity: 0.08;
}
.stButton > button:hover {
    background: rgba(255,70,85,0.1) !important;
    border-left-color: var(--red) !important;
    border-color: rgba(255,70,85,0.2) !important;
    color: var(--white) !important;
    transform: translateX(3px) !important;
}
.stButton > button:active {
    transform: translateX(1px) !important;
    background: rgba(255,70,85,0.18) !important;
}

/* =====================
   CHAT MESSAGES
===================== */
[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) {
    background: rgba(255,70,85,0.05);
    border: 1px solid rgba(255,70,85,0.15);
    border-right: 2px solid var(--red);
    border-radius: 2px;
    padding: 12px 16px;
    margin: 5px 0;
}
[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-assistant"]) {
    background: var(--dark2);
    border: 1px solid var(--border-w);
    border-left: 2px solid var(--red);
    border-radius: 2px;
    padding: 12px 16px;
    margin: 5px 0;
}

/* Chat text — bright enough to read outdoors on phone */
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li {
    font-size: clamp(13px, 3.5vw, 14.5px) !important;
    line-height: 1.75 !important;
    color: #ddd9d3 !important;    /* brighter */
}
[data-testid="stChatMessage"] h3 {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: clamp(15px, 4vw, 18px) !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 1.5px !important;
    color: var(--white) !important;
    margin-bottom: 8px !important;
    text-shadow: 0 1px 12px rgba(255,70,85,0.2) !important;
}
[data-testid="stChatMessage"] strong {
    color: #ff8a95 !important;    /* softer red, readable */
    font-weight: 600 !important;
}
[data-testid="stChatMessage"] em {
    color: #8a8885 !important;
    font-style: normal !important;
    font-size: 11px !important;
}
[data-testid="stChatMessage"] code {
    background: rgba(255,70,85,0.12) !important;
    color: #ffb3ba !important;
    border: 1px solid rgba(255,70,85,0.25) !important;
    border-radius: 2px !important;
    padding: 1px 6px !important;
    font-size: 12px !important;
    font-family: 'Barlow Condensed', monospace !important;
}

/* =====================
   CHAT INPUT
===================== */
.stChatInput textarea {
    background: var(--dark2) !important;
    color: var(--cream) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-bottom: 2px solid rgba(255,255,255,0.12) !important;
    border-radius: 2px !important;
    font-family: 'Barlow', sans-serif !important;
    font-size: clamp(13px, 3.5vw, 14px) !important;
    caret-color: var(--red) !important;
}
.stChatInput textarea:focus {
    border-color: rgba(255,255,255,0.12) !important;
    border-bottom-color: var(--red) !important;
    box-shadow: 0 4px 24px rgba(255,70,85,0.06) !important;
}
.stChatInput textarea::placeholder {
    color: #454852 !important;    /* slightly brighter placeholder */
    font-style: italic !important;
}

/* =====================
   SIDEBAR
===================== */
section[data-testid="stSidebar"] {
    background: #0c0f16 !important;
    border-right: 1px solid rgba(255,70,85,0.12) !important;
}
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] div,
section[data-testid="stSidebar"] small,
section[data-testid="stSidebar"] li {
    color: #6a6d78 !important;
    font-size: 13px !important;
}
section[data-testid="stSidebar"] h2 {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 18px !important;
    color: #c4c0b9 !important;
    text-transform: uppercase !important;
    letter-spacing: 3px !important;
}
section[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    border: 1px solid rgba(255,70,85,0.2) !important;
    border-left: 2px solid var(--red) !important;
    color: #8a8d98 !important;
    border-radius: 2px !important;
    font-family: 'Barlow Condensed', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: 1px !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(255,70,85,0.07) !important;
    color: var(--cream) !important;
    transform: none !important;
}

/* =====================
   SPINNER
===================== */
[data-testid="stSpinner"] p {
    color: #6a6d78 !important;
    font-family: 'Barlow Condensed', sans-serif !important;
    letter-spacing: 3px !important;
    font-size: 11px !important;
    text-transform: uppercase !important;
}

/* =====================
   HIDE STREAMLIT DEFAULT
===================== */
#MainMenu, footer, header { visibility: hidden !important; }
.block-container {
    padding-top: 1.2rem !important;
    padding-bottom: 1.5rem !important;
    max-width: 760px !important;
}

/* =====================
   MOBILE OPTIMIZATION
===================== */
@media (max-width: 600px) {
    .block-container {
        padding: 0.7rem 0.5rem 4.5rem !important;
    }
    .valo-title {
        letter-spacing: 0px;
        line-height: 1;
    }
    [data-testid="stChatMessage"] {
        padding: 10px 11px !important;
        margin: 3px 0 !important;
    }
    .stButton > button {
        min-height: 42px !important;
        padding: 8px 10px !important;
    }
    .valo-greeting {
        padding: 16px 14px !important;
    }
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
    st.markdown("## ⚡ PC Solving")
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
st.markdown("""
<div class="valo-header">
    <div class="valo-eyebrow">⚡ STEM PROJECT ⚡</div>
    <div class="valo-title">PC <span class="highlight">SOLVING</span> SYSTEM</div>
    <div class="valo-subtitle">Chẩn đoán &nbsp;·&nbsp; Phân tích &nbsp;·&nbsp; Xử lý tự động</div>
</div>
<div class="valo-divider">
    <div class="valo-divider-core">
        <div class="valo-divider-dot"></div>
        <div class="valo-divider-bar"></div>
        <div class="valo-divider-dot"></div>
    </div>
</div>
""", unsafe_allow_html=True)

# ========================
# SESSION STATE
# ========================
if "messages" not in st.session_state:
    st.session_state.messages = []
if "greeted" not in st.session_state:
    st.session_state.greeted = False
if "suggestions" not in st.session_state:
    st.session_state.suggestions = []
if "pending_query" not in st.session_state:
    st.session_state.pending_query = None

# ========================
# GỢI Ý NGẪU NHIÊN
# ========================
ALL_SUGGESTIONS = [
    ("⚠  Màn hình xanh chết BSOD",          "Máy tính bị màn hình xanh chết, phải làm gì?"),
    ("▪  Màn hình đen không hiển thị",        "Máy lên nguồn nhưng màn hình đen, không lên gì"),
    ("◈  PC bíp liên tục khi bật",            "Máy tính bíp nhiều tiếng khi khởi động, lỗi gì?"),
    ("◉  Máy chạy chậm bất thường",           "Máy tính đột nhiên chạy rất chậm, khắc phục thế nào?"),
    ("🌡  CPU overheat quá nóng",              "CPU bị overheat, nhiệt độ lên đến 95 độ C"),
    ("◆  RAM có tương thích mainboard không",  "Làm sao biết RAM có tương thích với mainboard không?"),
    ("⚡  Cần bao nhiêu W nguồn điện",         "Cấu hình PC của tôi cần bao nhiêu W nguồn là đủ?"),
    ("🎮  GTX 1650 chơi được game gì",         "Card GTX 1650 chơi được những game nào mượt?"),
    ("✕  Lỗi 0xc0000005 khi mở game",         "Bị lỗi 0xc0000005 khi mở game, sửa thế nào?"),
    ("◈  Ổ cứng bị bad sector",               "Ổ cứng bị bad sector, còn cứu được dữ liệu không?"),
    ("▶  So sánh Intel i5 vs Ryzen 5",        "So sánh Intel i5 và AMD Ryzen 5, nên mua loại nào?"),
    ("◉  PC không nhận VGA rời",              "Máy không nhận card đồ họa rời, chỉ dùng được onboard"),
    ("✕  Windows Update lỗi 0x80070002",      "Windows Update báo lỗi 0x80070002, không update được"),
    ("⚠  Máy tự khởi động lại đột ngột",      "PC tự dưng khởi động lại giữa chừng, nguyên nhân gì?"),
    ("▪  Bấm nguồn máy không bật",            "Nhấn nút nguồn nhưng máy tính không bật được gì cả"),
    ("◆  Tản nhiệt CPU nên mua loại nào",     "Tản nhiệt CPU loại nào tốt cho cấu hình tầm trung?"),
]

# ========================
# LỜI CHÀO
# ========================
if not st.session_state.greeted and not st.session_state.messages:
    if not st.session_state.suggestions:
        st.session_state.suggestions = random.sample(ALL_SUGGESTIONS, 4)

    st.markdown("""
    <div class="valo-greeting">
        <div class="valo-greeting-accent"></div>
        <span class="valo-greeting-icon">⚡</span>
        <div class="valo-greeting-title">Hệ thống phân tích phần cứng máy tính</div>
        <div class="valo-greeting-sub">
            Nhập mã hiệu linh kiện hoặc mô tả hiện tượng lỗi hệ thống.<br>
            Thuật toán phân tích tự động sẽ đưa ra giải pháp ngay lập tức.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="valo-suggest-label">
        <span>— CHỌN NHANH VẤN ĐỀ —</span>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="small")
    for i, (label, query) in enumerate(st.session_state.suggestions):
        with (col1 if i % 2 == 0 else col2):
            if st.button(label, key=f"sug_{i}"):
                st.session_state.greeted = True
                st.session_state.pending_query = query
                st.rerun()

# ========================
# LỊCH SỬ CHAT
# ========================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ========================
# DATABASE SEARCH
# ========================
def calculate_match_score(item, q_clean, user_numbers):
    score = 0
    item_kws = [str(kw).lower().strip() for kw in item.get("keywords", [])]
    user_words = q_clean.split()
    for kw in item_kws:
        if kw in user_words or (kw.isdigit() and kw in q_clean):
            score += 1
    if score == 0:
        return 0
    item_numbers = [re.sub(r'\D', '', kw) for kw in item_kws if re.search(r'\d{3,}', kw)]
    item_numbers = [n for n in item_numbers if n]
    if item_numbers and user_numbers:
        if not set(item_numbers).intersection(set(user_numbers)):
            return 0
    return score

def search_database(user_query):
    q_clean = re.sub(r'[-–_,.\?!\(\)]', ' ', user_query.lower().strip())
    user_numbers = [re.sub(r'\D', '', w) for w in q_clean.split() if re.search(r'\d{3,}', w)]
    user_numbers = [n for n in user_numbers if n]
    best_match, max_score, match_pool = None, 0, ""
    for item in data_pc.get("linh_kien_pc", []):
        s = calculate_match_score(item, q_clean, user_numbers)
        if s > max_score:
            max_score, best_match, match_pool = s, item, "linh_kien"
    for item in data_pc.get("loi_he_thong", []):
        s = calculate_match_score(item, q_clean, user_numbers)
        if s > max_score:
            max_score, best_match, match_pool = s, item, "loi"
    if max_score >= 2 and best_match:
        if match_pool == "loi":
            return (f"### ✕ {best_match['ten']}\n"
                    f"*— Dữ liệu: Lê Văn Chung 10A4*\n\n"
                    f"**⚠ Nguyên nhân:** {best_match['nguyen_nhan']}\n\n"
                    f"**◈ Khắc phục:**\n{best_match['giai_phap']}")
        else:
            return (f"### ◆ {best_match['ten']}\n"
                    f"*— Dữ liệu: Lê Văn Chung 10A4*\n\n"
                    f"**⚙ Thông số:** {best_match.get('thong_so','')}\n\n"
                    f"**◉ Socket:** `{best_match.get('socket','')}`\n\n"
                    f"**▶ Tư vấn:** {best_match.get('chuyen_gia_tu_van','')}")
    return None

# ========================
# PHÂN LOẠI CÂU HỎI
# ========================
def detect_type(query):
    q = query.lower()
    hw = ["i3","i5","i7","i9","ryzen","gtx","rtx","rx","vga","card","cpu","ram","ssd",
          "mainboard","main","nguồn","psu","tản nhiệt","socket","ddr","mua","so sánh",
          "nên chọn","upgrade","nâng cấp","combo","build","cấu hình"]
    err = ["lỗi","bsod","xanh","đen","bíp","crash","sập","đơ","treo","chậm","lag",
           "không bật","không lên","restart","khởi động","update","0x","error","fix","sửa"]
    for w in hw:
        if w in q: return "hardware"
    for w in err:
        if w in q: return "error"
    return "general"

# ========================
# SYSTEM PROMPTS
# ========================
BASE_RULE = """
TUYỆT ĐỐI KHÔNG dùng các từ: "AI", "mô hình ngôn ngữ", "LLM", "Groq", "Meta", "Llama", "trí tuệ nhân tạo".
Không nhắc đến việc bạn là phần mềm học từ dữ liệu internet.
"""

PROMPT_ERROR = f"""Bạn là hệ thống chẩn đoán lỗi máy tính của Lê Văn Chung 10A4.
{BASE_RULE}
Kho dữ liệu tham chiếu: {raw_json_context}

QUY TẮC — LỖI HỆ THỐNG (ngắn gọn, thẳng vào vấn đề):
- 1 câu nguyên nhân chính
- Tối đa 4 bước xử lý, mỗi bước 1 câu ngắn
- Không giải thích dài dòng, không lặp lại câu hỏi
- 1 dòng lưu ý cuối nếu thật sự cần"""

PROMPT_HARDWARE = f"""Bạn là chuyên gia tư vấn linh kiện PC của Lê Văn Chung 10A4.
{BASE_RULE}
Kho dữ liệu tham chiếu: {raw_json_context}

QUY TẮC — TƯ VẤN LINH KIỆN (chi tiết, có chiều sâu):
- Nêu thông số kỹ thuật quan trọng
- So sánh ưu/nhược điểm nếu được hỏi
- Gợi ý combo phù hợp ngân sách
- Kết thúc bằng 1 khuyến nghị cụ thể
- Khi phân tích chuyên sâu mở đầu bằng: "Dựa trên cơ sở dữ liệu kỹ thuật của tác giả Lê Văn Chung 10A4..." """

PROMPT_GENERAL = f"""Bạn là hệ thống hỗ trợ kỹ thuật máy tính của Lê Văn Chung 10A4.
{BASE_RULE}
Kho dữ liệu tham chiếu: {raw_json_context}
Trả lời tiếng Việt, súc tích, chia bước rõ ràng nếu cần."""

def ask_engine(user_query, chat_history):
    qtype = detect_type(user_query)
    if qtype == "error":
        system, max_tok, temp = PROMPT_ERROR, 480, 0.3
    elif qtype == "hardware":
        system, max_tok, temp = PROMPT_HARDWARE, 780, 0.5
    else:
        system, max_tok, temp = PROMPT_GENERAL, 560, 0.4

    messages = [{"role": "system", "content": system}]
    for msg in chat_history[-6:]:
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": user_query})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        max_tokens=max_tok,
        temperature=temp
    )
    return response.choices[0].message.content

# ========================
# XỬ LÝ TIN NHẮN
# ========================
def handle_message(prompt):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("ĐANG PHÂN TÍCH DỮ LIỆU..."):
            try:
                answer = search_database(prompt) or ask_engine(prompt, st.session_state.messages)
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error("❌ Hệ thống gián đoạn. Vui lòng thử lại.")

if st.session_state.pending_query:
    query = st.session_state.pending_query
    st.session_state.pending_query = None
    handle_message(query)

if prompt := st.chat_input("Nhập mã lỗi hoặc linh kiện cần phân tích..."):
    st.session_state.greeted = True
    handle_message(prompt)
