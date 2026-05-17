# ========================
# IMPORT
# ========================
import streamlit as st
import json
import re
import os
import random
from groq import Groq

# ========================
# PAGE CONFIG
# ========================
st.set_page_config(
    page_title="PC Solving System — Lê Văn Chung 10A4",
    page_icon="⚡",
    layout="centered"
)

# ========================
# CSS
# ========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Barlow+Condensed:wght@400;600;700;800&family=Barlow:wght@300;400;500;600&display=swap');

html, body, .stApp {
    background: #0b0e14 !important;
    color: #ece8e1 !important;
    font-family: 'Barlow', sans-serif !important;
}

.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    pointer-events: none;
    background:
        repeating-linear-gradient(
            -48deg,
            transparent 0px,
            transparent 60px,
            rgba(255,70,85,0.018) 60px,
            rgba(255,70,85,0.018) 61px
        );
}

.valo-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: clamp(30px, 7vw, 62px);
    font-weight: 700;
    letter-spacing: 3px;
    text-align: center;
    margin-bottom: 6px;
    text-transform: uppercase;
    color: white;
}

.valo-title .red {
    color: #ff4655;
}

.valo-subtitle {
    text-align: center;
    color: #00d4bf;
    font-size: 13px;
    letter-spacing: 4px;
    margin-bottom: 20px;
    font-weight: 700;
}

.valo-greeting {
    background: linear-gradient(135deg, rgba(24,28,40,0.8), rgba(18,22,31,0.95));
    border: 1px solid rgba(255,70,85,0.25);
    border-left: 4px solid #ff4655;
    border-radius: 6px;
    padding: 22px;
    margin-bottom: 18px;
}

.valo-greeting-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: 22px;
    font-weight: 700;
    color: white;
    margin-bottom: 8px;
    text-transform: uppercase;
}

.valo-greeting-sub {
    color: #ece8e1;
    line-height: 1.7;
}

.valo-suggest-label {
    text-align: center;
    margin: 18px 0 10px;
}

.valo-suggest-label span {
    background: #ff4655;
    padding: 6px 16px;
    font-size: 12px;
    font-weight: 700;
    border-radius: 4px;
    letter-spacing: 2px;
    color: white;
}

.stButton > button {
    background: rgba(20,24,35,0.95) !important;
    color: white !important;
    border: 1px solid rgba(0,212,191,0.2) !important;
    border-left: 4px solid #00d4bf !important;
    border-radius: 4px !important;
    font-weight: 700 !important;
    min-height: 48px !important;
    transition: 0.15s ease !important;
}

.stButton > button:hover {
    transform: translateX(3px);
    border-left-color: #ff4655 !important;
    background: rgba(0,212,191,0.08) !important;
}

[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) {
    background: rgba(255,70,85,0.08);
    border: 1px solid rgba(255,70,85,0.2);
    border-right: 4px solid #ff4655;
    border-radius: 6px;
    padding: 14px;
}

[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-assistant"]) {
    background: rgba(0,212,191,0.06);
    border: 1px solid rgba(0,212,191,0.18);
    border-left: 4px solid #00d4bf;
    border-radius: 6px;
    padding: 14px;
}

[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li {
    color: white !important;
    font-size: 15px !important;
    line-height: 1.8 !important;
}

[data-testid="stChatMessage"] strong {
    color: #ff9ea7 !important;
}

[data-testid="stChatMessage"] h3 {
    color: white !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 20px !important;
    text-transform: uppercase !important;
}

.stChatInput textarea {
    background: #181c28 !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-bottom: 2px solid #ff4655 !important;
}

section[data-testid="stSidebar"] {
    background: #090c11 !important;
    border-right: 1px solid rgba(255,70,85,0.2);
}

#MainMenu, footer, header {
    visibility: hidden;
}

.block-container {
    max-width: 760px !important;
    padding-top: 1rem !important;
}
</style>
""", unsafe_allow_html=True)

# ========================
# GROQ CLIENT
# ========================
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("❌ Thiếu GROQ_API_KEY trong Secrets")
    st.stop()

# ========================
# LOAD DATABASE
# ========================
def load_database():
    if os.path.exists("database_pc.json"):
        with open("database_pc.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "loi_he_thong": [],
        "linh_kien_pc": []
    }

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
    st.markdown("Hệ thống chẩn đoán lỗi & tư vấn linh kiện PC.")
    st.markdown("---")

    if st.button("⟳ PHIÊN MỚI", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown("**Lê Văn Chung · 10A4 🎓**")

# ========================
# HEADER
# ========================
st.markdown("""
<div class="valo-title">
PC <span class="red">SOLVING</span>
</div>

<div class="valo-subtitle">
CHẨN ĐOÁN • PHÂN TÍCH • XỬ LÝ
</div>
""", unsafe_allow_html=True)

# ========================
# SESSION
# ========================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_query" not in st.session_state:
    st.session_state.pending_query = None

# ========================
# GREETING
# ========================
st.markdown("""
<div class="valo-greeting">
    <div class="valo-greeting-title">
        ⚡ Hệ thống phân tích phần cứng máy tính
    </div>

    <div class="valo-greeting-sub">
        Nhập lỗi hệ thống, tên linh kiện hoặc mô tả vấn đề.<br>
        Hệ thống sẽ tự động phân tích và đưa ra giải pháp.
    </div>
</div>
""", unsafe_allow_html=True)

# ========================
# SUGGESTIONS
# ========================
ALL_SUGGESTIONS = [
    ("⚠ Màn hình xanh BSOD", "Máy tính bị màn hình xanh"),
    ("🌡 CPU quá nóng", "CPU nhiệt độ 95 độ"),
    ("🎮 GTX 1650 chơi game gì", "GTX 1650 chơi game gì"),
    ("⚡ Máy không lên nguồn", "Bấm nút nguồn máy không lên"),
]

st.markdown("""
<div class="valo-suggest-label">
    <span>CHỌN NHANH</span>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

for i, (label, query) in enumerate(ALL_SUGGESTIONS):
    with (col1 if i % 2 == 0 else col2):
        if st.button(label, key=f"sug_{i}"):
            st.session_state.pending_query = query
            st.rerun()

# ========================
# CHAT HISTORY
# ========================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ========================
# SEARCH DATABASE
# ========================
def calculate_match_score(item, q_clean):
    score = 0

    item_kws = [
        str(kw).lower().strip()
        for kw in item.get("keywords", [])
    ]

    for kw in item_kws:
        if kw in q_clean:
            score += 1

    return score

def search_database(user_query):
    q_clean = user_query.lower().strip()

    best_match = None
    max_score = 0
    match_pool = ""

    for item in data_pc.get("linh_kien_pc", []):
        s = calculate_match_score(item, q_clean)

        if s > max_score:
            max_score = s
            best_match = item
            match_pool = "linh_kien"

    for item in data_pc.get("loi_he_thong", []):
        s = calculate_match_score(item, q_clean)

        if s > max_score:
            max_score = s
            best_match = item
            match_pool = "loi"

    if max_score >= 1 and best_match:

        if match_pool == "loi":
            return f"""
### ⚠ {best_match['ten']}

**Nguyên nhân:**  
{best_match['nguyen_nhan']}

**Khắc phục:**  
{best_match['giai_phap']}
"""

        else:
            return f"""
### ⚙ {best_match['ten']}

**Thông số:**  
{best_match.get('thong_so', '')}

**Socket:**  
`{best_match.get('socket', '')}`

**Tư vấn:**  
{best_match.get('chuyen_gia_tu_van', '')}
"""

    return None

# ========================
# DETECT TYPE
# ========================
def detect_type(query):
    q = query.lower()

    hardware_keywords = [
        "cpu","gpu","vga","ram","ssd","hdd",
        "main","mainboard","ryzen","intel",
        "rtx","gtx","nguồn","psu","socket"
    ]

    error_keywords = [
        "lỗi","bsod","đen","xanh","lag",
        "crash","treo","đơ","restart",
        "không lên","không bật"
    ]

    for w in hardware_keywords:
        if w in q:
            return "hardware"

    for w in error_keywords:
        if w in q:
            return "error"

    return "general"

# ========================
# PROMPTS
# ========================
BASE_RULE = """
Không được nhắc tới AI, mô hình ngôn ngữ, Groq, Meta hoặc Llama.
"""

PROMPT_ERROR = f"""
Bạn là chuyên gia sửa lỗi máy tính.
{BASE_RULE}

Kho dữ liệu:
{raw_json_context}

Trả lời ngắn gọn, dễ hiểu.
"""

PROMPT_HARDWARE = f"""
Bạn là chuyên gia tư vấn linh kiện PC.
{BASE_RULE}

Kho dữ liệu:
{raw_json_context}

Trả lời chuyên sâu, có thông số kỹ thuật.
"""

PROMPT_GENERAL = f"""
Bạn là hệ thống hỗ trợ máy tính.
{BASE_RULE}

Kho dữ liệu:
{raw_json_context}

Trả lời tự nhiên bằng tiếng Việt.
"""

# ========================
# AI ENGINE
# ========================
def ask_engine(user_query, chat_history):

    qtype = detect_type(user_query)

    if qtype == "error":
        system = PROMPT_ERROR
        max_tok = 480
        temp = 0.3

    elif qtype == "hardware":
        system = PROMPT_HARDWARE
        max_tok = 780
        temp = 0.5

    else:
        system = PROMPT_GENERAL
        max_tok = 560
        temp = 0.4

    messages = [
        {
            "role": "system",
            "content": system
        }
    ]

    for msg in chat_history[-6:]:
        messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })

    messages.append({
        "role": "user",
        "content": user_query
    })

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        max_tokens=max_tok,
        temperature=temp
    )

    return response.choices[0].message.content

# ========================
# HANDLE MESSAGE
# ========================
def handle_message(prompt):

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner("ĐANG PHÂN TÍCH DỮ LIỆU..."):

            try:
                answer = (
                    search_database(prompt)
                    or ask_engine(prompt, st.session_state.messages)
                )

                st.markdown(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as e:
                st.error("❌ Hệ thống gián đoạn")

# ========================
# AUTO QUERY
# ========================
if st.session_state.pending_query:
    q = st.session_state.pending_query
    st.session_state.pending_query = None
    handle_message(q)

# ========================
# CHAT INPUT
# ========================
if prompt := st.chat_input("Nhập lỗi hoặc linh kiện cần phân tích..."):
    handle_message(prompt)