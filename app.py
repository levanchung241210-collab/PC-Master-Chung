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
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@600;700&family=Barlow+Condensed:wght@400;600;700&family=Barlow:wght@300;400;500&display=swap');

/* ==============================
   VALORANT CORE PALETTE
============================== */
:root {
    --red:     #ff4655;
    --red-dim: #c0303d;
    --red-glow:#ff465540;
    --dark:    #0f1116;
    --dark2:   #14171e;
    --dark3:   #1a1d27;
    --panel:   #0d1117cc;
    --border:  #ff465520;
    --border2: #ffffff0d;
    --text:    #ece8e1;
    --muted:   #7b7a78;
    --accent:  #fffbf5;
}

/* ==============================
   BASE
============================== */
html, body, .stApp {
    background: var(--dark) !important;
    color: var(--text) !important;
    font-family: 'Barlow', sans-serif !important;
}

/* Diagonal slash texture background */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        repeating-linear-gradient(
            -55deg,
            transparent,
            transparent 40px,
            rgba(255,70,85,0.012) 40px,
            rgba(255,70,85,0.012) 41px
        );
    pointer-events: none;
    z-index: 0;
}

/* Red corner accent top-left */
.stApp::after {
    content: '';
    position: fixed;
    top: 0; left: 0;
    width: 220px; height: 3px;
    background: linear-gradient(90deg, var(--red), transparent);
    z-index: 999;
}

/* ==============================
   HEADER
============================== */
.valo-header {
    position: relative;
    text-align: center;
    padding: 6px 0 2px;
    margin-bottom: 2px;
}

.valo-eyebrow {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: clamp(9px, 2vw, 11px);
    font-weight: 600;
    letter-spacing: 5px;
    color: var(--red);
    text-transform: uppercase;
    margin-bottom: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
}
.valo-eyebrow::before,
.valo-eyebrow::after {
    content: '';
    display: inline-block;
    width: 24px; height: 1px;
    background: var(--red);
    opacity: 0.6;
}

.valo-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: clamp(28px, 7vw, 58px);
    font-weight: 700;
    letter-spacing: -1px;
    line-height: 1;
    color: var(--accent);
    text-transform: uppercase;
    margin: 0;
}
.valo-title span {
    color: var(--red);
}

.valo-subtitle {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: clamp(10px, 2.5vw, 12px);
    font-weight: 400;
    letter-spacing: 4px;
    color: var(--muted);
    text-transform: uppercase;
    margin-top: 5px;
}

/* Red slash divider */
.valo-divider {
    display: flex;
    align-items: center;
    gap: 0;
    margin: 10px 0 8px;
    height: 2px;
}
.valo-divider::before {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border2);
}
.valo-divider-bar {
    width: 60px; height: 2px;
    background: var(--red);
    clip-path: polygon(4px 0%, 100% 0%, calc(100% - 4px) 100%, 0% 100%);
}
.valo-divider::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border2);
}

/* ==============================
   GREETING BOX
============================== */
.valo-greeting {
    position: relative;
    background: var(--dark3);
    border: 1px solid var(--border);
    border-left: 3px solid var(--red);
    border-radius: 4px;
    padding: clamp(16px, 4vw, 24px) clamp(14px, 4vw, 22px);
    margin: 6px 0 4px;
    overflow: hidden;
}
/* Corner triangle decoration */
.valo-greeting::before {
    content: '';
    position: absolute;
    top: 0; right: 0;
    border-style: solid;
    border-width: 0 28px 28px 0;
    border-color: transparent var(--red-dim) transparent transparent;
    opacity: 0.5;
}
.valo-greeting::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0;
    border-style: solid;
    border-width: 0 0 20px 20px;
    border-color: transparent transparent var(--red-dim) transparent;
    opacity: 0.2;
}

.valo-agent-icon {
    font-size: clamp(28px, 6vw, 36px);
    margin-bottom: 8px;
    display: block;
    text-align: center;
}
.valo-greeting-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: clamp(16px, 4vw, 22px);
    font-weight: 700;
    color: var(--accent);
    text-align: center;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 5px;
}
.valo-greeting-sub {
    font-size: clamp(12px, 3vw, 13px);
    color: var(--muted);
    text-align: center;
    line-height: 1.6;
}

/* ==============================
   SUGGEST LABEL
============================== */
.valo-suggest-label {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 14px 0 8px;
}
.valo-suggest-label::before,
.valo-suggest-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border2);
}
.valo-suggest-label span {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 10px;
    letter-spacing: 3px;
    color: #3a3d46;
    text-transform: uppercase;
    white-space: nowrap;
}

/* ==============================
   BUTTONS
============================== */
.stButton > button {
    background: var(--dark3) !important;
    color: #ccc8c3 !important;
    border: 1px solid #ffffff12 !important;
    border-radius: 3px !important;
    font-family: 'Barlow Condensed', sans-serif !important;
    font-size: clamp(11px, 3vw, 13px) !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px !important;
    padding: 10px 14px !important;
    width: 100% !important;
    text-align: left !important;
    white-space: normal !important;
    height: auto !important;
    min-height: 46px !important;
    line-height: 1.4 !important;
    transition: all 0.15s ease !important;
    position: relative !important;
    border-left: 2px solid #ffffff08 !important;
}
.stButton > button:hover {
    background: rgba(255,70,85,0.08) !important;
    border-color: #ffffff1a !important;
    border-left-color: var(--red) !important;
    color: var(--accent) !important;
    transform: translateX(2px) !important;
}
.stButton > button:active {
    background: rgba(255,70,85,0.15) !important;
    transform: translateX(1px) !important;
}

/* ==============================
   CHAT MESSAGES
============================== */
[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) {
    background: rgba(255,70,85,0.06);
    border: 1px solid rgba(255,70,85,0.12);
    border-right: 2px solid var(--red);
    border-radius: 3px 3px 3px 3px;
    padding: 12px 16px;
    margin: 5px 0;
}
[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-assistant"]) {
    background: var(--dark3);
    border: 1px solid var(--border2);
    border-left: 2px solid var(--red);
    border-radius: 3px;
    padding: 12px 16px;
    margin: 5px 0;
}

/* Chat text */
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li {
    font-size: clamp(13px, 3.5vw, 14px) !important;
    line-height: 1.7 !important;
    color: #d4d0cb !important;
}
[data-testid="stChatMessage"] h3 {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: clamp(14px, 4vw, 17px) !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
    color: var(--accent) !important;
    margin-bottom: 6px !important;
}
[data-testid="stChatMessage"] strong {
    color: #ff8590 !important;
    font-weight: 600 !important;
}
[data-testid="stChatMessage"] code {
    background: rgba(255,70,85,0.1) !important;
    color: #ff8590 !important;
    border: 1px solid rgba(255,70,85,0.2) !important;
    border-radius: 2px !important;
    padding: 1px 5px !important;
    font-size: 12px !important;
}

/* ==============================
   CHAT INPUT
============================== */
.stChatInput textarea {
    background: var(--dark3) !important;
    color: var(--text) !important;
    border: 1px solid #ffffff14 !important;
    border-bottom: 2px solid #ffffff1a !important;
    border-radius: 3px !important;
    font-family: 'Barlow', sans-serif !important;
    font-size: clamp(13px, 3.5vw, 14px) !important;
    caret-color: var(--red) !important;
}
.stChatInput textarea:focus {
    border-color: #ffffff1a !important;
    border-bottom-color: var(--red) !important;
    box-shadow: 0 4px 20px rgba(255,70,85,0.08) !important;
    outline: none !important;
}
.stChatInput textarea::placeholder {
    color: #3a3d46 !important;
}

/* ==============================
   SIDEBAR
============================== */
section[data-testid="stSidebar"] {
    background: #0a0c11 !important;
    border-right: 1px solid #ff465515 !important;
}
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] div,
section[data-testid="stSidebar"] small {
    color: #5a5d66 !important;
    font-size: 13px !important;
    font-family: 'Barlow', sans-serif !important;
}
section[data-testid="stSidebar"] h2 {
    font-family: 'Rajdhani', sans-serif !important;
    color: var(--text) !important;
    text-transform: uppercase !important;
    letter-spacing: 2px !important;
}

/* Sidebar new session button */
section[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    border: 1px solid #ff465525 !important;
    border-left: 2px solid var(--red) !important;
    color: #7a7d86 !important;
    border-radius: 2px !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(255,70,85,0.06) !important;
    color: var(--text) !important;
}

/* ==============================
   SPINNER
============================== */
[data-testid="stSpinner"] p {
    color: var(--muted) !important;
    font-family: 'Barlow Condensed', sans-serif !important;
    letter-spacing: 2px !important;
    font-size: 12px !important;
}

/* ==============================
   HIDE STREAMLIT UI
============================== */
#MainMenu, footer, header { visibility: hidden !important; }
.block-container {
    padding-top: 1.2rem !important;
    padding-bottom: 1.5rem !important;
    max-width: 760px !important;
}

/* ==============================
   MOBILE
============================== */
@media (max-width: 600px) {
    .block-container { padding: 0.8rem 0.5rem 4.5rem !important; }
    [data-testid="stChatMessage"] { padding: 10px 11px !important; margin: 3px 0 !important; }
    .stButton > button { min-height: 42px !important; padding: 8px 11px !important; }
    .valo-greeting { padding: 14px 12px; }
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
st.markdown("""
<div class="valo-header">
    <div class="valo-eyebrow">⚡ STEM PROJECT ⚡</div>
    <div class="valo-title">PC <span>SOLVING</span> SYSTEM</div>
    <div class="valo-subtitle">Chẩn đoán · Phân tích · Xử lý tự động</div>
</div>
<div class="valo-divider"><div class="valo-divider-bar"></div></div>
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
    ("⚠  Màn hình xanh chết BSOD",         "Máy tính bị màn hình xanh chết, phải làm gì?"),
    ("▪  Màn hình đen không hiển thị",       "Máy lên nguồn nhưng màn hình đen, không lên gì"),
    ("◈  PC bíp liên tục khi bật",           "Máy tính bíp nhiều tiếng khi khởi động, lỗi gì?"),
    ("◉  Máy chạy chậm bất thường",          "Máy tính đột nhiên chạy rất chậm, khắc phục thế nào?"),
    ("🌡  CPU overheat quá nóng",             "CPU bị overheat, nhiệt độ lên đến 95 độ C"),
    ("◆  RAM có tương thích mainboard không", "Làm sao biết RAM có tương thích với mainboard không?"),
    ("⚡  Cần bao nhiêu W nguồn điện",        "Cấu hình PC của tôi cần bao nhiêu W nguồn là đủ?"),
    ("🎮  GTX 1650 chơi được game gì",        "Card GTX 1650 chơi được những game nào mượt?"),
    ("✕  Lỗi 0xc0000005 khi mở game",        "Bị lỗi 0xc0000005 khi mở game, sửa thế nào?"),
    ("◈  Ổ cứng bị bad sector",              "Ổ cứng bị bad sector, còn cứu được dữ liệu không?"),
    ("▶  So sánh Intel i5 vs Ryzen 5",       "So sánh Intel i5 và AMD Ryzen 5, nên mua loại nào?"),
    ("◉  PC không nhận VGA rời",             "Máy không nhận card đồ họa rời, chỉ dùng được onboard"),
    ("✕  Windows Update lỗi 0x80070002",     "Windows Update báo lỗi 0x80070002, không update được"),
    ("⚠  Máy tự khởi động lại đột ngột",     "PC tự dưng khởi động lại giữa chừng, nguyên nhân là gì?"),
    ("▪  Bấm nguồn máy không bật",           "Nhấn nút nguồn nhưng máy tính không bật được gì cả"),
    ("◆  Tản nhiệt CPU nên mua loại nào",    "Tản nhiệt CPU loại nào tốt cho cấu hình tầm trung?"),
]

# ========================
# LỜI CHÀO
# ========================
if not st.session_state.greeted and not st.session_state.messages:
    if not st.session_state.suggestions:
        st.session_state.suggestions = random.sample(ALL_SUGGESTIONS, 4)

    st.markdown("""
    <div class="valo-greeting">
        <span class="valo-agent-icon">💻</span>
        <div class="valo-greeting-title">Hệ thống phân tích phần cứng máy tính</div>
        <div class="valo-greeting-sub">
            Nhập mã hiệu linh kiện hoặc mô tả hiện tượng lỗi.<br>
            Thuật toán phân tích tự động sẽ đưa ra giải pháp ngay lập tức.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="valo-suggest-label"><span>CHỌN NHANH VẤN ĐỀ</span></div>
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
TUYỆT ĐỐI KHÔNG dùng: "AI", "mô hình ngôn ngữ", "LLM", "Groq", "Meta", "Llama", "trí tuệ nhân tạo".
Không nhắc đến việc bạn là phần mềm học từ internet.
"""

PROMPT_ERROR = f"""Bạn là hệ thống chẩn đoán lỗi máy tính của Lê Văn Chung 10A4.
{BASE_RULE}
Kho dữ liệu: {raw_json_context}

QUY TẮC — LỖI HỆ THỐNG (ngắn gọn, đúng việc):
- 1 câu nguyên nhân chính
- Tối đa 4 bước xử lý, mỗi bước ngắn gọn
- Không giải thích thừa, không lặp lại câu hỏi
- Nếu có lưu ý thì 1 dòng cuối là đủ"""

PROMPT_HARDWARE = f"""Bạn là chuyên gia tư vấn linh kiện PC của Lê Văn Chung 10A4.
{BASE_RULE}
Kho dữ liệu: {raw_json_context}

QUY TẮC — TƯ VẤN LINH KIỆN (chi tiết, có chiều sâu):
- Nêu thông số kỹ thuật quan trọng
- So sánh ưu/nhược nếu được hỏi
- Gợi ý combo phù hợp ngân sách
- Kết thúc bằng 1 khuyến nghị cụ thể
- Khi phân tích chuyên sâu, dùng câu mở đầu: "Dựa trên cơ sở dữ liệu kỹ thuật của tác giả Lê Văn Chung 10A4..." """

PROMPT_GENERAL = f"""Bạn là hệ thống hỗ trợ kỹ thuật máy tính của Lê Văn Chung 10A4.
{BASE_RULE}
Kho dữ liệu: {raw_json_context}
Trả lời tiếng Việt, súc tích, chia bước nếu cần."""

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