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
/* Nhúng font chữ có độ thon dài, góc cạnh sắc nét giống font Valorant */
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Oswald:wght@500;700&family=Rowdies:wght@700&family=Barlow+Condensed:wght@600;700;800&family=Barlow:wght@400;500;600&display=swap');

/* ══════════════════════════════════════
   VALORANT SYSTEM VARIABLES
══════════════════════════════════════ */
:root {
    --valo-red:       #ff4655;
    --valo-red-dim:   #8b222b;
    --valo-teal:      #00d4bf;
    --valo-teal-dim:  #0a3c36;
    --valo-dark-bg:   #0f141c;
    --valo-panel-bg:  #161d28;
    --valo-panel-br:  #242e3d;
    --white:          #ffffff;
    --cream:          #ece8e1;
    --muted:          #7e8591;
}

/* ══════════════════════════════════════
   BASE STYLES & BACKGROUND
══════════════════════════════════════ */
html, body, .stApp {
    background: var(--valo-dark-bg) !important;
    color: var(--cream) !important;
    font-family: 'Barlow', sans-serif !important;
}

/* Tạo các đường lưới mờ ảo góc gaming phía sau nền app */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 0;
    background:
        linear-gradient(rgba(15, 20, 28, 0.94), rgba(15, 20, 28, 0.94)),
        repeating-linear-gradient(0deg, transparent, transparent 39px, rgba(255, 70, 85, 0.015) 39px, rgba(255, 70, 85, 0.015) 40px),
        repeating-linear-gradient(90deg, transparent, transparent 39px, rgba(0, 212, 191, 0.012) 39px, rgba(0, 212, 191, 0.012) 40px);
}

/* Thanh nẹp năng lượng chạy ngang đỉnh màn hình */
.stApp::after {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0;
    height: 4px;
    background: linear-gradient(90deg, var(--valo-red) 0%, #ff7680 40%, var(--valo-teal) 70%, #66ffef 100%);
    z-index: 9999;
}

/* Ép khung chứa nội dung rộng ra đồng nhất trên cả PC và Mobile */
.block-container {
    max-width: 820px !important;
    padding-top: 1.5rem !important;
    padding-bottom: 6rem !important;
}

/* ══════════════════════════════════════
   HEADER & VALORANT FONTS SỬA ĐỔI
══════════════════════════════════════ */
.valo-header {
    text-align: center;
    padding: 15px 0 5px;
    position: relative;
}

/* Fix dứt điểm chữ tên tác giả - Luôn có màu Teal rực rỡ và font đậm chất gaming */
.valo-author {
    font-family: 'Barlow Condensed', sans-serif !important;
    font-size: 14px !important;
    font-weight: 800 !important;
    letter-spacing: 3px !important;
    text-transform: uppercase !important;
    color: var(--valo-teal) !important;
    text-shadow: 0 0 10px rgba(0, 212, 191, 0.6), 2px 2px 0px #000000 !important;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
}

.valo-eyebrow {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 13px;
    letter-spacing: 5px;
    color: var(--muted);
}

.valo-logo-wrap {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    margin: 5px 0;
}

.valo-title {
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: clamp(38px, 8vw, 68px) !important;
    font-weight: 400 !important;
    letter-spacing: 4px !important;
    line-height: 0.95;
    color: var(--white);
}
.valo-title .red { color: var(--valo-red); }
.valo-title .slash { color: var(--muted); padding: 0 4px; }

/* Áp dụng font Valorant sắc cạnh vào dòng tiêu đề hệ thống phần cứng máy tính */
.valo-main-heading {
    font-family: 'Oswald', sans-serif !important;
    font-size: clamp(18px, 4.2vw, 30px) !important;
    font-weight: 700 !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    color: var(--white) !important;
    text-shadow: 2px 2px 0px rgba(0, 0, 0, 0.5) !important;
    margin: 15px 0;
}

.valo-subtitle {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 4px;
    color: var(--muted);
    margin-top: 5px;
}
.valo-subtitle span { color: var(--white); }

.valo-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--valo-panel-br), transparent);
    margin: 15px 0;
}

/* ══════════════════════════════════════
   GREETING PANEL (CỐ ĐỊNH PHÍA TRÊN)
══════════════════════════════════════ */
.valo-greeting {
    background: var(--valo-panel-bg);
    border: 1px solid var(--valo-panel-br);
    border-left: 4px solid var(--valo-red);
    padding: 24px;
    border-radius: 4px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.4);
    text-align: center;
    margin-bottom: 20px;
}

.valo-status-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(0, 212, 191, 0.08);
    border: 1px solid rgba(0, 212, 191, 0.2);
    padding: 4px 12px;
    border-radius: 2px;
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 11px;
    font-weight: 700;
    color: var(--valo-teal);
    letter-spacing: 2px;
    text-transform: uppercase;
}

.valo-greeting-desc {
    color: var(--muted);
    font-size: 14px;
    line-height: 1.6;
    margin: 12px auto;
    max-width: 580px;
}

.valo-stats-grid {
    display: flex;
    justify-content: center;
    gap: 30px;
    margin-top: 15px;
    padding-top: 15px;
    border-top: 1px dashed var(--valo-panel-br);
}
.valo-stat-box { text-align: center; }
.valo-stat-val { font-family: 'Bebas Neue', sans-serif; font-size: 24px; color: var(--valo-red); }
.valo-stat-lbl { font-family: 'Barlow Condensed', sans-serif; font-size: 10px; color: var(--muted); letter-spacing: 1.5px; text-transform: uppercase; }

/* Khung tiêu đề mục chọn nhanh vấn đề gân guốc góc cạnh */
.valo-tag-container {
    background: var(--valo-red);
    color: var(--white);
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 2px;
    padding: 6px 20px;
    display: inline-block;
    clip-path: polygon(8px 0%, 100% 0%, calc(100% - 8px) 100%, 0% 100%);
    margin: 10px 0 15px;
}

/* ══════════════════════════════════════
   VALORANT BUTTONS INTERFACE
══════════════════════════════════════ */
.stButton > button {
    background: #1a222d !important;
    color: var(--white) !important;
    border: 1px solid var(--valo-panel-br) !important;
    border-left: 3px solid var(--valo-teal) !important;
    font-family: 'Barlow Condensed', sans-serif !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    letter-spacing: 0.5px !important;
    text-align: left !important;
    padding: 12px 16px !important;
    border-radius: 0px !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
}
.stButton > button:hover {
    background: var(--valo-panel-br) !important;
    border-color: var(--valo-teal) !important;
    box-shadow: 0 0 15px rgba(0, 212, 191, 0.25) !important;
    transform: scale(1.01);
}

/* ══════════════════════════════════════
   SỬA CÂN ĐỐI KHUNG CHAT (FIX LỆCH PC)
══════════════════════════════════════ */
/* Ép toàn bộ khối bọc của khung chat rộng chuẩn 100% khớp với container chính */
[data-testid="stChatMessageContainer"] {
    max-width: 820px !important;
    margin: 0 auto !important;
    padding: 0 !important;
}

[data-testid="stChatMessage"] {
    border-radius: 0px !important;
    padding: 16px 20px !important;
    margin: 12px 0 !important;
}

/* Text bên trong khung chat bắt buộc rõ nét, không lỗi mờ */
[data-testid="stChatMessage"] p, [data-testid="stChatMessage"] li {
    font-size: 15px !important;
    line-height: 1.7 !important;
    color: var(--white) !important;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.8) !important;
}

/* KHUNG CHAT CỦA USER — Phe Attack (Đỏ) */
[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) {
    background: linear-gradient(90deg, #251619 0%, #171012 100%) !important;
    border: 1px solid var(--valo-red-dim) !important;
    border-right: 4px solid var(--valo-red) !important;
}

/* KHUNG CHAT CỦA BOT — Phe Defense (Teal) */
[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-assistant"]) {
    background: linear-gradient(90deg, #102221 0%, #0e151b 100%) !important;
    border: 1px solid var(--valo-teal-dim) !important;
    border-left: 4px solid var(--valo-teal) !important;
}

/* Cấu trúc tiêu đề nhỏ bên trong lời giải của Bot */
[data-testid="stChatMessage"] h3 {
    font-family: 'Oswald', sans-serif !important;
    font-size: 18px !important;
    color: var(--valo-teal) !important;
    text-transform: uppercase !important;
    margin-top: 5px !important;
    letter-spacing: 1px !important;
}

/* ══════════════════════════════════════
   SỬA KHUNG INPUT ĐỒNG BỘ VỚI PC KHÔNG BỊ TRÀN
══════════════════════════════════════ */
/* Ép form chat input thu nhỏ lại nằm giữa màn hình PC giống hệt khung greeting */
[data-testid="stChatInput"] {
    max-width: 820px !important;
    margin-left: auto !important;
    margin-right: auto !important;
    left: 0 !important;
    right: 0 !important;
    background: transparent !important;
}

[data-testid="stChatInput"] > div {
    background: #18202c !important;
    border: 1px solid var(--valo-panel-br) !important;
    border-bottom: 2px solid var(--valo-red) !important;
    border-radius: 2px !important;
}

[data-testid="stChatInput"] textarea {
    color: var(--white) !important;
    font-size: 15px !important;
}

/* Ẩn các thành phần thừa hệ thống */
#MainMenu, footer, header { visibility: hidden !important; }
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
    <div class="valo-author">⚡ LÊ VĂN CHUNG · LỚP 10A4 ⚡</div>
    <div class="valo-eyebrow">VALORANT DESIGN CONCEPT DỰ ÁN STEM</div>
    <div class="valo-logo-wrap">
        <div class="valo-title">PC<span class="slash">/</span><span class="red">SOLVING</span></div>
    </div>
    <div class="valo-subtitle">ANALYZE SYSTEM — <span>CHẨN ĐOÁN</span> • <span>PHÂN TÍCH</span> • <span>XỬ LÝ TỰ ĐỘNG</span></div>
</div>
<div class="valo-divider"></div>
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
    <div class="valo-status-badge">● HỆ THỐNG SẴN SÀNG</div>
    <div class="valo-main-heading">HỆ THỐNG PHÂN TÍCH PHẦN CỨNG MÁY TÍNH</div>
    <div class="valo-greeting-desc">
        Nhập các chuỗi ký tự mã lỗi hệ thống hoặc điền tên thiết bị phần cứng linh kiện cần tra cứu.<br>
        Mô hình AI sẽ liên kết với kho tri thức của hệ thống để phân tích phản hồi nhanh.
    </div>
    <div class="valo-stats-grid">
        <div class="valo-stat-box">
            <div class="valo-stat-val">{db_loi}</div>
            <div class="valo-stat-lbl">LỖI HỆ THỐNG</div>
        </div>
        <div class="valo-stat-box" style="border-left: 1px dashed var(--valo-panel-br); padding-left: 20px;">
            <div class="valo-stat-val">{db_lk}</div>
            <div class="valo-stat-lbl">LINH KIỆN PC</div>
        </div>
        <div class="valo-stat-box" style="border-left: 1px dashed var(--valo-panel-br); padding-left: 20px;">
            <div class="valo-stat-val" style="color:var(--valo-teal)">24/7</div>
            <div class="valo-stat-lbl">HỖ TRỢ TRỰC TUYẾN</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Chỉ hiển thị 4 nút bấm gợi ý khi người dùng chưa bắt đầu thực hiện chat
if not st.session_state.messages:
    st.markdown('<div class="valo-tag-container">CHỌN NHANH VẤN ĐỀ</div>', unsafe_allow_html=True)
    
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
                    f"*Chuyên mục: Lỗi Hệ Thống — Cơ sở kỹ thuật Lê Văn Chung 10A4*\n\n"
                    f"**⚠ Nguyên nhân chính:** {best_match['nguyen_nhan']}\n\n"
                    f"**◈ Các bước xử lý chuẩn:**\n{best_match['giai_phap']}")
        else:
            return (f"### ◆ {best_match['ten']}\n"
                    f"*Chuyên mục: Thiết Bị Linh Kiện — Cơ sở kỹ thuật Lê Văn Chung 10A4*\n\n"
                    f"**⚙ Thông số phần cứng:** {best_match.get('thong_so','')}\n\n"
                    f"**◉ Chuẩn Socket:** `{best_match.get('socket','')}`\n\n"
                    f"**▶ Khuyến nghị từ hệ thống:** {best_match.get('chuyen_gia_tu_van','')}")
    return None

# ========================
# XỬ LÝ TRUY VẤN QUA LLM TRÍ TUỆ NHÂN TẠO
# ========================
def ask_engine(user_query, chat_history):
    system_prompt = f"""Bạn là hệ thống trí tuệ nhân tạo chuyên sâu về chẩn đoán phần cứng máy tính, được phát triển bởi học sinh Lê Văn Chung lớp 10A4.
TUYỆT ĐỐI KHÔNG tự xưng là mô hình ngôn ngữ lớn, không nhắc đến Meta, Llama hay Groq. 
Mọi thông tin phản hồi phải dựa vào dữ liệu kiến thức gốc: {raw_json_context}.
Trình bày rõ ràng bằng tiếng Việt, ngắn gọn theo dạng gạch đầu dòng kỹ thuật."""
    
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
        with st.spinner("ĐANG PHÂN TÍCH DỮ LIỆU HỆ THỐNG..."):
            try:
                answer = search_database(prompt) or ask_engine(prompt, st.session_state.messages)
                final_answer = f"""{answer}\n\n---\n*— Phân tích tự động phát triển bởi: Lê Văn Chung lớp 10A4*"""
                st.markdown(final_answer)
                st.session_state.messages.append({"role": "assistant", "content": final_answer})
            except Exception as e:
                st.error("❌ Kết nối trục trặc hoặc token quá hạn. Hãy thử lại!")

if st.session_state.pending_query:
    q = st.session_state.pending_query
    st.session_state.pending_query = None
    handle_message(q)

if prompt := st.chat_input("Nhập mã lỗi hoặc linh kiện cần phân tích..."):
    st.session_state.greeted = True
    handle_message(prompt)
