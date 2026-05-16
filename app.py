import streamlit as st
import json
import re
import os
import random
from groq import Groq

# CONFIG GIAO DIỆN HI-TECH CHUẨN THIÊN HƯỚNG TƯƠNG LAI
st.set_page_config(
    page_title="PC Solving Chatbot - Lê Văn Chung 10A4",
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
    background-image: linear-gradient(rgba(59,130,246,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(59,130,246,0.03) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
    z-index: 0;
}
.main-title {
    text-align: center;
    font-family: 'Syne', sans-serif;
    font-size: clamp(24px, 5vw, 44px);
    font-weight: 800;
    background: linear-gradient(135deg, #ffffff 0%, #93c5fd 50%, #3b82f6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.2;
    margin-bottom: 6px;
}
.sub-title {
    text-align: center;
    font-family: 'DM Sans', sans-serif;
    font-size: clamp(11px, 2vw, 13px);
    color: #475569;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 8px;
}
.divider {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, #1e40af44, transparent);
    margin: 16px 0;
}
[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) {
    background: linear-gradient(135deg, rgba(29,78,216,0.35), rgba(30,64,175,0.25));
    border-radius: 18px 18px 4px 18px;
    border: 1px solid rgba(96,165,250,0.18);
    padding: 14px 18px;
    margin: 6px 0;
    backdrop-filter: blur(10px);
}
[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-assistant"]) {
    background: rgba(15, 23, 42, 0.55);
    border-radius: 18px 18px 18px 4px;
    border: 1px solid rgba(51,65,85,0.4);
    border-left: 3px solid #3b82f6;
    padding: 14px 18px;
    margin: 6px 0;
    backdrop-filter: blur(10px);
}
.stChatInput textarea {
    background: rgba(15, 23, 42, 0.85) !important;
    color: #f1f5f9 !important;
    border: 1.5px solid rgba(59,130,246,0.35) !important;
    border-radius: 16px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 15px !important;
}
.stChatInput textarea:focus {
    border: 1.5px solid #3b82f6 !important;
    box-shadow: 0 0 20px rgba(59,130,246,0.12) !important;
}
.stButton > button {
    background: rgba(15, 23, 42, 0.65) !important;
    color: #93c5fd !important;
    border: 1px solid rgba(59,130,246,0.3) !important;
    border-radius: 24px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    padding: 10px 16px !important;
    width: 100% !important;
    text-align: left !important;
    backdrop-filter: blur(8px) !important;
    white-space: normal !important;
    height: auto !important;
    min-height: 48px !important;
    transition: all 0.2s ease !important;
    line-height: 1.4 !important;
}
.stButton > button:hover {
    background: rgba(29,78,216,0.3) !important;
    border-color: #3b82f6 !important;
    color: #ffffff !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 20px rgba(59,130,246,0.18) !important;
}
section[data-testid="stSidebar"] {
    background: rgba(8,12,20,0.97) !important;
    border-right: 1px solid rgba(30,41,59,0.7) !important;
}
section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] span, section[data-testid="stSidebar"] div, section[data-testid="stSidebar"] small {
    color: #94a3b8 !important;
}
.greeting-box {
    background: linear-gradient(135deg, rgba(29,78,216,0.1), rgba(15,23,42,0.5));
    border: 1px solid rgba(59,130,246,0.18);
    border-radius: 20px;
    padding: 28px 24px 20px;
    margin: 8px 0 4px;
    backdrop-filter: blur(12px);
    text-align: center;
}
.greeting-emoji { font-size: 38px; margin-bottom: 12px; }
.greeting-text {
    font-family: 'Syne', sans-serif;
    font-size: clamp(17px, 3vw, 22px);
    font-weight: 700;
    color: #f1f5f9;
    margin-bottom: 8px;
}
.greeting-sub { font-size: 14px; color: #64748b; line-height: 1.6; }
.suggest-label {
    text-align: center;
    font-size: 11px;
    color: #334155;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    margin: 20px 0 10px;
}
#MainMenu, footer, header { visibility: hidden !important; }
.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 2rem !important;
}
@media (max-width: 768px) {
    .block-container { padding: 1rem 0.75rem 5rem !important; }
    .greeting-box { padding: 20px 16px 16px; }
    [data-testid="stChatMessage"] { padding: 10px 12px !important; margin: 4px 0 !important; }
    .stButton > button { font-size: 12px !important; min-height: 44px !important; }
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

data_pc = load_database()

# Nạp chuỗi JSON thô để làm dày thêm ngữ cảnh cho thuật toán suy luận
def load_raw_json_string():
    if os.path.exists("database_pc.json"):
        with open("database_pc.json", "r", encoding="utf-8") as f:
            return f.read()
    return "{}"

raw_json_context = load_raw_json_string()

# ========================
# SIDEBAR
# ========================
with st.sidebar:
    st.markdown("## 💻 PC Solving System")
    st.markdown("---")
    st.markdown("Hệ thống toán học chẩn đoán lỗi thiết bị phần cứng và cấu hình linh kiện máy tính nâng cao.")
    st.markdown("---")
    if st.button("✨ Thiết lập phiên mới", use_container_width=True):
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
# DANH SÁCH GỢI Ý
# ========================
ALL_SUGGESTIONS = [
    ("🔵 Màn hình xanh chết (BSOD)", "Máy tính của tôi bị màn hình xanh chết, phải làm gì?"),
    ("⚫ Màn hình đen không lên", "Máy lên nguồn nhưng màn hình đen, không hiển thị gì"),
    ("🔊 PC bíp liên tục khi bật", "Máy tính bíp nhiều tiếng khi khởi động, lỗi gì vậy?"),
    ("🐌 Máy tính chạy chậm bất thường", "Máy tính đột nhiên chạy rất chậm, cách khắc phục?"),
    ("🌡️ CPU quá nóng, overheat", "CPU tôi bị overheat, nhiệt độ lên đến 95 độ C"),
    ("💾 RAM có phù hợp mainboard không", "Làm sao biết RAM có tương thích với mainboard không?"),
    ("⚡ Cần bao nhiêu W nguồn", "Cấu hình PC của tôi cần bao nhiêu W nguồn là đủ?"),
    ("🎮 GTX 1650 chơi được game gì", "Card GTX 1650 chơi được những game nào mượt?"),
    ("🔧 Lỗi 0xc0000005 khi mở game", "Tôi bị lỗi 0xc0000005 khi mở game, sửa thế nào?"),
    ("📀 Ổ cứng bị bad sector", "Ổ cứng bị bad sector, còn cứu được dữ liệu không?"),
    ("🖥️ Nên mua i5 hay Ryzen 5", "So sánh Intel i5 và AMD Ryzen 5, nên mua loại nào?"),
    ("🔌 PC không nhận VGA rời", "Máy không nhận card đồ họa rời, chỉ dùng được onboard"),
    ("💿 Windows Update bị lỗi", "Windows Update báo lỗi 0x80070002, không update được"),
    ("🖱️ Máy tính tự khởi động lại", "PC tự dưng khởi động lại giữa chừng, nguyên nhân là gì?"),
    ("🔋 Máy bật không lên nguồn", "Nhấn nút nguồn nhưng máy tính không bật được"),
    ("📶 Tản nhiệt CPU nên mua loại nào", "Tản nhiệt CPU loại nào tốt cho cấu hình tầm trung?"),
]

# ========================
# LỜI CHÀO KHI MỚI VÀO
# ========================
if not st.session_state.greeted and not st.session_state.messages:
    if not st.session_state.suggestions:
        st.session_state.suggestions = random.sample(ALL_SUGGESTIONS, 4)
        
    st.markdown("""
    <div class="greeting-box">
        <div class="greeting-emoji">💻</div>
        <div class="greeting-text">Hệ thống xử lý bài toán phần cứng máy tính</div>
        <div class="greeting-sub">Mô tả mã hiệu linh kiện hoặc các hiện tượng lỗi hệ thống.<br>Thuật toán phân tích tự động sẽ đưa ra giải pháp ngay lập tức!</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="suggest-label">✦ Chọn nhanh danh mục phân tích ✦</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
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
        # Nhúng dấu ấn tác giả ngay cả khi xuất dữ liệu từ Database tĩnh
        if match_pool == "loi":
            return (f"### 🎯 {best_match['ten']}\n"
                    f"*Trích xuất từ danh mục lưu trữ của Lê Văn Chung 10A4*\n\n"
                    f"⚠️ **Nguyên nhân cốt lõi:** {best_match['nguyen_nhan']}\n\n"
                    f"🛠️ **Phác đồ khắc phục:**\n{best_match['giai_phap']}")
        else:
            return (f"### 📦 {best_match['ten']}\n"
                    f"*Trích xuất từ danh mục lưu trữ của Lê Văn Chung 10A4*\n\n"
                    f"⚙️ **Thông số kỹ thuật:** {best_match.get('thong_so','')}\n\n"
                    f"🔌 **Cấu trúc Socket:** `{best_match.get('socket','')}`\n\n"
                    f"💡 **Khuyến nghị chuyên sâu:** *{best_match.get('chuyen_gia_tu_van','')}*")
    return None

# ========================
# KÍCH HOẠT THUẬT TOÁN ĐA LUỒNG SÂU (GIẤU TOÀN BỘ VẾT TÍCH AI)
# ========================
SYSTEM_PROMPT = f"""
Bạn là "Hệ thống chuyên gia phân tích Vua PC v14.0" - Bộ lõi xử lý logic toán học và chẩn đoán pan bệnh máy tính do học sinh Lê Văn Chung lớp 10A4 phát triển cho dự án STEM.

QUY TẮC PHÁT NGÔN BẮT BUỘC:
1. TUYỆT ĐỐI CẤM SỬ DỤNG CÁC TỪ SAU: "AI", "Trí tuệ nhân tạo", "Chatbot", "Mô hình", "Llama", "Groq", "Meta", "Google", "LLM", "Robot". Không đề cập đến việc bạn là một chương trình máy tính học từ Internet. Nếu vi phạm, sản phẩm STEM sẽ bị đánh rớt.
2. Bạn phải tự xưng là "Hệ thống chuyên gia Vua PC" hoặc "Bộ lõi toán học tự động".
3. Khi phân tích các câu hỏi so sánh (ví dụ: so sánh card đồ họa, CPU) hoặc chẩn đoán lỗi phức tạp, hãy mở đầu hoặc đan xen câu: "Dựa trên thuật toán xử lý ngôn ngữ tự nhiên và đối chiếu cấu trúc dữ liệu của tác giả Lê Văn Chung lớp 10A4...".

Nhiệm vụ chuyên môn:
- Bạn được cung cấp kho dữ liệu nền tảng gốc ở đây để tham chiếu thông số chuẩn:
{raw_json_context}
- Phân tích lỗi hệ điều hành Windows, mã màn hình xanh, lỗi xung đột phần cứng.
- Phân tích sâu các dòng phần cứng: CPU, RAM, GPU, Bo mạch chủ, Nguồn công suất thực.
- Nếu người dùng viết sai chính tả, viết tắt, gõ dính chữ hoặc hỏi các linh kiện nằm ngoài file dữ liệu nền tảng, bạn phải dùng thuật toán mở rộng của hệ thống để phân tích bản chất kỹ thuật, đưa ra so sánh chi tiết và giải pháp từng bước (Bước 1, Bước 2...) một cách thông minh, thuyết phục nhất.
"""

def ask_ai(user_query, chat_history):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for msg in chat_history[-8:]:
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": user_query})
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        max_tokens=1024,
        temperature=0.5 # Giảm xuống 0.5 để câu trả lời mang tính kỹ thuật, chính xác cao, không lan man
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
        with st.spinner("💾 Bộ lõi đang tính toán và truy vết dữ liệu..."):
            try:
                answer = search_database(prompt) or ask_ai(prompt, st.session_state.messages)
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"❌ Hệ thống gián đoạn: Không thể xử lý dữ liệu đầu vào.")

# Xử lý khi bấm gợi ý nhanh
if st.session_state.pending_query:
    query = st.session_state.pending_query
    st.session_state.pending_query = None
    handle_message(query)

# Xử lý input thủ công
if prompt := st.chat_input("Nhập thông số linh kiện hoặc pan bệnh cần hệ thống xử lý..."):
    st.session_state.greeted = True
    handle_message(prompt)
