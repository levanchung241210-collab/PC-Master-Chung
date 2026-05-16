import streamlit as st
import json
import re
import os
import random
from groq import Groq

st.set_page_config(
    page_title="PC Solving System - Lê Văn Chung 10A4",
    page_icon="💻",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, .stApp {
    background: #080c14 !important;
    color: #e2e8f0 !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(rgba(59,130,246,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(59,130,246,0.03) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
    z-index: 0;
}

/* ===== HEADER ===== */
.main-title {
    text-align: center;
    font-family: 'Syne', sans-serif;
    font-size: clamp(22px, 6vw, 46px);
    font-weight: 800;
    background: linear-gradient(135deg, #ffffff 0%, #93c5fd 50%, #3b82f6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.15;
    margin-bottom: 4px;
    padding: 0 8px;
}
.sub-title {
    text-align: center;
    font-size: clamp(10px, 2.5vw, 13px);
    color: #475569;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 6px;
}
.divider {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, #1e40af55, transparent);
    margin: 12px 0;
}

/* ===== CHAT BUBBLES ===== */
[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) {
    background: linear-gradient(135deg, rgba(29,78,216,0.3), rgba(30,64,175,0.2));
    border-radius: 16px 16px 4px 16px;
    border: 1px solid rgba(96,165,250,0.15);
    padding: 12px 16px;
    margin: 5px 0;
    backdrop-filter: blur(8px);
}
[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-assistant"]) {
    background: rgba(15, 23, 42, 0.6);
    border-radius: 16px 16px 16px 4px;
    border: 1px solid rgba(51,65,85,0.45);
    border-left: 3px solid #3b82f6;
    padding: 12px 16px;
    margin: 5px 0;
    backdrop-filter: blur(8px);
}

/* ===== TEXT TRONG CHAT ===== */
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] span {
    font-size: clamp(13px, 3.5vw, 15px) !important;
    line-height: 1.65 !important;
    color: #e2e8f0 !important;
}
[data-testid="stChatMessage"] h3 {
    font-size: clamp(14px, 4vw, 17px) !important;
    color: #93c5fd !important;
    margin-bottom: 6px !important;
}
[data-testid="stChatMessage"] strong {
    color: #bfdbfe !important;
}

/* ===== CHAT INPUT ===== */
.stChatInput textarea {
    background: rgba(15, 23, 42, 0.9) !important;
    color: #f1f5f9 !important;
    border: 1.5px solid rgba(59,130,246,0.3) !important;
    border-radius: 14px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: clamp(14px, 3.5vw, 15px) !important;
    padding: 12px 16px !important;
    caret-color: #3b82f6 !important;
}
.stChatInput textarea:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 16px rgba(59,130,246,0.1) !important;
}
.stChatInput textarea::placeholder {
    color: #334155 !important;
}

/* ===== BUTTONS GỢI Ý ===== */
.stButton > button {
    background: rgba(15, 23, 42, 0.7) !important;
    color: #93c5fd !important;
    border: 1px solid rgba(59,130,246,0.28) !important;
    border-radius: 22px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: clamp(11px, 3vw, 13px) !important;
    font-weight: 500 !important;
    padding: 10px 14px !important;
    width: 100% !important;
    text-align: left !important;
    backdrop-filter: blur(6px) !important;
    white-space: normal !important;
    height: auto !important;
    min-height: 46px !important;
    line-height: 1.4 !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover, .stButton > button:active {
    background: rgba(29,78,216,0.28) !important;
    border-color: #3b82f6 !important;
    color: #ffffff !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 18px rgba(59,130,246,0.15) !important;
}

/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"] {
    background: rgba(6, 10, 18, 0.98) !important;
    border-right: 1px solid rgba(30,41,59,0.6) !important;
}
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] div,
section[data-testid="stSidebar"] small,
section[data-testid="stSidebar"] li {
    color: #94a3b8 !important;
    font-size: 13px !important;
}
section[data-testid="stSidebar"] h2 {
    color: #e2e8f0 !important;
}

/* ===== GREETING BOX ===== */
.greeting-box {
    background: linear-gradient(135deg, rgba(29,78,216,0.09), rgba(15,23,42,0.55));
    border: 1px solid rgba(59,130,246,0.16);
    border-radius: 18px;
    padding: clamp(18px, 5vw, 28px) clamp(14px, 4vw, 24px) clamp(14px, 4vw, 20px);
    margin: 6px 0 2px;
    backdrop-filter: blur(10px);
    text-align: center;
}
.greeting-emoji {
    font-size: clamp(30px, 7vw, 40px);
    margin-bottom: 10px;
    display: block;
}
.greeting-text {
    font-family: 'Syne', sans-serif;
    font-size: clamp(15px, 4vw, 21px);
    font-weight: 700;
    color: #f1f5f9;
    margin-bottom: 7px;
    line-height: 1.3;
}
.greeting-sub {
    font-size: clamp(12px, 3vw, 14px);
    color: #64748b;
    line-height: 1.6;
}
.suggest-label {
    text-align: center;
    font-size: clamp(9px, 2.5vw, 11px);
    color: #2d3f55;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin: 16px 0 8px;
}

/* ===== ẨN UI STREAMLIT ===== */
#MainMenu, footer, header { visibility: hidden !important; }
.block-container {
    padding-top: 1.2rem !important;
    padding-bottom: 1.5rem !important;
    max-width: 780px !important;
}

/* ===== MOBILE ===== */
@media (max-width: 600px) {
    .block-container {
        padding: 0.8rem 0.6rem 4.5rem !important;
    }
    .greeting-box {
        margin: 4px 0 2px;
    }
    [data-testid="stChatMessage"] {
        padding: 10px 12px !important;
        margin: 3px 0 !important;
    }
    .stButton > button {
        min-height: 42px !important;
        padding: 8px 12px !important;
    }
    /* Fix avatar icon bị nhỏ trên mobile */
    [data-testid="chatAvatarIcon-user"],
    [data-testid="chatAvatarIcon-assistant"] {
        width: 28px !important;
        height: 28px !important;
        min-width: 28px !important;
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
    st.error(f"❌ Lỗi kết nối hệ thống: {str(e)}")
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
    st.markdown("## 💻 PC Solving System")
    st.markdown("---")
    st.markdown("Hệ thống chẩn đoán lỗi và tư vấn linh kiện máy tính chuyên sâu.")
    st.markdown("---")
    if st.button("✨ Phiên mới", use_container_width=True):
        st.session_state.messages = []
        st.session_state.greeted = False
        st.session_state.suggestions = []
        st.rerun()
    st.markdown("---")
    st.markdown("<small>Tác giả: Lê Văn Chung · Lớp 10A4 🎓</small>", unsafe_allow_html=True)

# ========================
# HEADER
# ========================
st.markdown('<div class="main-title">💻 PC Solving System</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Chẩn đoán logic · Phân tích linh kiện · Xử lý tự động</div>', unsafe_allow_html=True)
st.markdown('<hr class="divider">', unsafe_allow_html=True)

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
    ("🔵 Màn hình xanh chết (BSOD)", "Máy tính bị màn hình xanh chết, phải làm gì?"),
    ("⚫ Màn hình đen không lên", "Máy lên nguồn nhưng màn hình đen, không hiển thị gì"),
    ("🔊 PC bíp liên tục khi bật", "Máy tính bíp nhiều tiếng khi khởi động, lỗi gì?"),
    ("🐌 Máy tính chạy chậm bất thường", "Máy tính đột nhiên chạy rất chậm, cách khắc phục?"),
    ("🌡️ CPU quá nóng, overheat", "CPU bị overheat, nhiệt độ lên đến 95 độ C"),
    ("💾 RAM có phù hợp mainboard không", "Làm sao biết RAM có tương thích với mainboard không?"),
    ("⚡ Cần bao nhiêu W nguồn", "Cấu hình PC của tôi cần bao nhiêu W nguồn là đủ?"),
    ("🎮 GTX 1650 chơi được game gì", "Card GTX 1650 chơi được những game nào mượt?"),
    ("🔧 Lỗi 0xc0000005 khi mở game", "Bị lỗi 0xc0000005 khi mở game, sửa thế nào?"),
    ("📀 Ổ cứng bị bad sector", "Ổ cứng bị bad sector, còn cứu được dữ liệu không?"),
    ("🖥️ Nên mua i5 hay Ryzen 5", "So sánh Intel i5 và AMD Ryzen 5, nên mua loại nào?"),
    ("🔌 PC không nhận VGA rời", "Máy không nhận card đồ họa rời, chỉ dùng được onboard"),
    ("💿 Windows Update bị lỗi 0x80070002", "Windows Update báo lỗi 0x80070002, không update được"),
    ("🖱️ Máy tính tự khởi động lại", "PC tự dưng khởi động lại giữa chừng, nguyên nhân là gì?"),
    ("🔋 Bấm nguồn máy không bật", "Nhấn nút nguồn nhưng máy tính không bật được gì cả"),
    ("📶 Tản nhiệt CPU nên mua loại nào", "Tản nhiệt CPU loại nào tốt cho cấu hình tầm trung?"),
]

# ========================
# LỜI CHÀO
# ========================
if not st.session_state.greeted and not st.session_state.messages:
    if not st.session_state.suggestions:
        st.session_state.suggestions = random.sample(ALL_SUGGESTIONS, 4)

    st.markdown("""
    <div class="greeting-box">
        <span class="greeting-emoji">💻</span>
        <div class="greeting-text">Hệ thống xử lý bài toán phần cứng máy tính</div>
        <div class="greeting-sub">Mô tả mã hiệu linh kiện hoặc các hiện tượng lỗi hệ thống.<br>Thuật toán phân tích tự động sẽ đưa ra giải pháp ngay lập tức!</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="suggest-label">✦ Chọn nhanh danh mục phân tích ✦</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2, gap="small")
    for i, (label, query) in enumerate(st.session_state.suggestions):
        with (col1 if i % 2 == 0 else col2):
            if st.button(label, key=f"sug_{i}"):
                st.session_state.greeted = True
                st.session_state.pending_query = query
                st.rerun()

# ========================
# HIỂN THỊ LỊCH SỬ
# ========================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ========================
# THUẬT TOÁN DATABASE
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
            return (f"### 🎯 {best_match['ten']}\n"
                    f"*Trích xuất từ danh mục của Lê Văn Chung 10A4*\n\n"
                    f"⚠️ **Nguyên nhân:** {best_match['nguyen_nhan']}\n\n"
                    f"🛠️ **Khắc phục:**\n{best_match['giai_phap']}")
        else:
            return (f"### 📦 {best_match['ten']}\n"
                    f"*Trích xuất từ danh mục của Lê Văn Chung 10A4*\n\n"
                    f"⚙️ **Thông số:** {best_match.get('thong_so','')}\n\n"
                    f"🔌 **Socket:** `{best_match.get('socket','')}`\n\n"
                    f"💡 **Tư vấn:** *{best_match.get('chuyen_gia_tu_van','')}*")
    return None

# ========================
# PHÂN LOẠI CÂU HỎI
# ========================
def detect_question_type(query):
    q = query.lower()
    # Từ khóa linh kiện → cần tư vấn chi tiết
    hardware_words = ["i3","i5","i7","i9","ryzen","gtx","rtx","rx","vga","card","cpu","ram","ssd","hdd",
                      "mainboard","main","nguồn","psu","tản nhiệt","socket","ddr","mua","so sánh","tư vấn",
                      "nên chọn","upgrade","nâng cấp","ghép","combo","build","cấu hình"]
    # Từ khóa lỗi → cần trả lời nhanh gọn
    error_words = ["lỗi","bsod","xanh","đen","bíp","crash","sập","đơ","treo","chậm","lag","giật",
                   "không bật","không lên","restart","khởi động","update","0x","error","fix","sửa"]
    for w in hardware_words:
        if w in q:
            return "hardware"
    for w in error_words:
        if w in q:
            return "error"
    return "general"

# ========================
# SYSTEM PROMPT THÔNG MINH
# ========================
PROMPT_ERROR = f"""Bạn là hệ thống chẩn đoán lỗi máy tính chuyên nghiệp do Lê Văn Chung lớp 10A4 phát triển.

TUYỆT ĐỐI KHÔNG dùng các từ: "AI", "mô hình", "ngôn ngữ lớn", "LLM", "Groq", "Meta", "Llama".
Tự xưng là "Hệ thống chẩn đoán" hoặc không tự xưng.

Kho dữ liệu tham chiếu:
{raw_json_context}

QUY TẮC TRẢ LỜI LỖI (NGẮN GỌN):
- Tối đa 4 bước xử lý, mỗi bước 1 câu
- Nêu nguyên nhân chính (1 câu)
- Không giải thích dài dòng
- Không lặp lại câu hỏi của người dùng
- Kết thúc bằng 1 lưu ý ngắn nếu cần"""

PROMPT_HARDWARE = f"""Bạn là chuyên gia tư vấn linh kiện máy tính do Lê Văn Chung lớp 10A4 phát triển.

TUYỆT ĐỐI KHÔNG dùng các từ: "AI", "mô hình", "ngôn ngữ lớn", "LLM", "Groq", "Meta", "Llama".
Tự xưng là "Hệ thống chuyên gia" hoặc không tự xưng.
Khi so sánh hoặc phân tích chuyên sâu, có thể dùng: "Dựa trên cơ sở dữ liệu kỹ thuật của tác giả Lê Văn Chung 10A4..."

Kho dữ liệu tham chiếu:
{raw_json_context}

QUY TẮC TƯ VẤN LINH KIỆN (CHI TIẾT):
- Nêu thông số kỹ thuật quan trọng
- So sánh ưu/nhược nếu được hỏi
- Gợi ý combo phù hợp
- Nêu mức giá/phân khúc nếu biết
- Kết thúc bằng 1 khuyến nghị cụ thể"""

PROMPT_GENERAL = f"""Bạn là hệ thống hỗ trợ kỹ thuật máy tính do Lê Văn Chung lớp 10A4 phát triển.

TUYỆT ĐỐI KHÔNG dùng các từ: "AI", "mô hình", "ngôn ngữ lớn", "LLM", "Groq", "Meta", "Llama".

Kho dữ liệu tham chiếu:
{raw_json_context}

Trả lời bằng tiếng Việt, ngắn gọn, thực tế, chia bước rõ ràng nếu cần."""

def ask_engine(user_query, chat_history):
    qtype = detect_question_type(user_query)

    if qtype == "error":
        system = PROMPT_ERROR
        max_tok = 512
        temp = 0.3
    elif qtype == "hardware":
        system = PROMPT_HARDWARE
        max_tok = 800
        temp = 0.5
    else:
        system = PROMPT_GENERAL
        max_tok = 600
        temp = 0.4

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
        with st.spinner("💾 Đang phân tích..."):
            try:
                answer = search_database(prompt) or ask_engine(prompt, st.session_state.messages)
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error("❌ Hệ thống gián đoạn. Vui lòng thử lại.")

# Xử lý khi bấm gợi ý
if st.session_state.pending_query:
    query = st.session_state.pending_query
    st.session_state.pending_query = None
    handle_message(query)

# Xử lý input thủ công
if prompt := st.chat_input("Nhập mã lỗi hoặc linh kiện cần phân tích..."):
    st.session_state.greeted = True
    handle_message(prompt)
