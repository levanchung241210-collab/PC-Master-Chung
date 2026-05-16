import streamlit as st
import json
import re
import os
import random
import time
from groq import Groq

st.set_page_config(
    page_title="PC Solving System — Lê Văn Chung 10A4",
    page_icon="⚡",
    layout="centered"
)

# ══════════════════════════════════════
# VALORANT STYLE & CSS
# ══════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Barlow+Condensed:wght@400;600;700;800&family=Barlow:wght@300;400;500;600&display=swap');

:root {
    --valo-red:       #ff4655;
    --valo-red-dim:   #c0303d;
    --valo-teal:      #00d4bf;
    --bg0: #0b0e14;
    --bg2: #181c28;
    --cream:  #ece8e1;
    --white:  #ffffff;
    --dim:    #454851;
    --br-red:  rgba(255,70,85,0.22);
    --br-teal: rgba(0,212,191,0.3);
    --br-w:    rgba(255,255,255,0.06);
    --br-w2:   rgba(255,255,255,0.10);
}

html, body, .stApp {
    background: var(--bg0) !important;
    color: var(--cream) !important;
    font-family: 'Barlow', sans-serif !important;
}

.stApp::before {
    content: ''; position: fixed; inset: 0; pointer-events: none; z-index: 0;
    background:
        repeating-linear-gradient(-48deg, transparent 0px, transparent 60px, rgba(255,70,85,0.018) 60px, rgba(255,70,85,0.018) 61px),
        repeating-linear-gradient(42deg, transparent 0px, transparent 90px, rgba(0,212,191,0.010) 90px, rgba(0,212,191,0.010) 91px);
}

.stApp::after {
    content: ''; position: fixed; top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, var(--valo-red) 0%, var(--valo-red) 80px, transparent 260px, transparent calc(100% - 260px), var(--valo-teal) calc(100% - 80px), var(--valo-teal) 100%);
    z-index: 9999;
}

.valo-header { text-align: center; padding: 10px 0 2px; position: relative; }

/* FIX: Chữ Lê Văn Chung nổi bật có màu đỏ Valorant trên PC */
.valo-author {
    position: absolute; top: 8px; right: 0; font-family: 'Barlow Condensed', sans-serif;
    font-size: 12px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; 
    color: var(--valo-red) !important; text-shadow: 0 0 8px rgba(255, 70, 85, 0.6);
}

.valo-eyebrow {
    font-family: 'Barlow Condensed', sans-serif; font-size: clamp(9px, 2vw, 11px); font-weight: 700;
    letter-spacing: 6px; color: var(--valo-red); text-transform: uppercase; margin-bottom: 6px;
}
.valo-title {
    font-family: 'Rajdhani', sans-serif; font-size: clamp(30px, 7.5vw, 62px); font-weight: 700;
    letter-spacing: 3px; line-height: 1; color: var(--white); text-transform: uppercase;
}
.valo-title .red { color: var(--valo-red); }
.valo-title .slash { color: var(--valo-red); opacity: 0.6; margin: 0 2px; }

.valo-subtitle {
    font-family: 'Barlow Condensed', sans-serif; font-size: clamp(12px, 2.8vw, 14px); font-weight: 700;
    letter-spacing: 4px; text-transform: uppercase; margin-top: 8px; display: flex; align-items: center; justify-content: center; gap: 10px;
}
.valo-subtitle .sub-1 { color: var(--valo-red); }
.valo-subtitle .sub-2 { color: var(--white); }
.valo-subtitle .sub-3 { color: var(--valo-teal); }

.valo-greeting {
    position: relative; background: linear-gradient(135deg, rgba(24,28,40,0.8) 0%, rgba(18,22,31,0.9) 100%);
    border: 1px solid var(--br-red); border-top: 2px solid var(--valo-red); border-radius: 2px;
    padding: 20px; margin: 4px 0 16px; box-shadow: 0 8px 30px rgba(0,0,0,0.4);
}
.valo-status-row { display: flex; align-items: center; justify-content: center; gap: 6px; margin-bottom: 10px; }
.valo-status-dot { width: 6px; height: 6px; background: var(--valo-teal); border-radius: 50%; box-shadow: 0 0 6px var(--valo-teal); }
.valo-status-text { font-family: 'Barlow Condensed', sans-serif; font-size: 10px; font-weight: 700; letter-spacing: 3px; color: var(--valo-teal); }
.valo-greeting-title { font-family: 'Rajdhani', sans-serif; font-size: 20px; font-weight: 700; color: var(--white); text-align: center; text-transform: uppercase; }
.valo-greeting-sub { font-size: 13px; color: var(--cream); text-align: center; line-height: 1.6; }

.valo-stats { display: flex; justify-content: center; gap: 20px; margin-top: 14px; padding-top: 12px; border-top: 1px solid var(--br-w); }
.valo-stat { text-align: center; }
.valo-stat-num { font-family: 'Rajdhani', sans-serif; font-size: 20px; font-weight: 700; color: var(--valo-red); }
.valo-stat-label { font-family: 'Barlow Condensed', sans-serif; font-size: 9px; letter-spacing: 2px; color: var(--dim); text-transform: uppercase; }
.valo-stat-divider { width: 1px; background: var(--br-w2); align-self: stretch; }

.valo-suggest-label { display: flex; align-items: center; gap: 10px; margin: 8px 0 14px; }
.valo-suggest-label span { background: var(--valo-red); color: var(--white); font-family: 'Barlow Condensed', sans-serif; font-size: 12px; font-weight: 700; padding: 4px 16px; clip-path: polygon(8px 0, 100% 0, calc(100% - 8px) 100%, 0 100%); }

.stButton > button {
    background: linear-gradient(90deg, rgba(30,34,50,0.8), rgba(20,24,35,0.9)) !important; color: #ffffff !important;
    border: 1px solid rgba(0,212,191,0.2) !important; border-left: 3px solid var(--valo-teal) !important;
    font-family: 'Barlow Condensed', sans-serif !important; font-weight: 700 !important; width: 100% !important; text-align: left !important;
}
.stButton > button:hover {
    background: linear-gradient(90deg, rgba(0,212,191,0.2), rgba(255,70,85,0.1)) !important; border-color: var(--valo-teal) !important; border-left-color: var(--valo-red) !important; transform: translateX(4px) !important;
}

[data-testid="stChatMessage"] p, [data-testid="stChatMessage"] li { font-size: 15px !important; color: #ffffff !important; text-shadow: 1px 1px 3px rgba(0,0,0,0.9) !important; }
[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) { background: linear-gradient(135deg, rgba(60,15,20,0.85) 0%, rgba(20,10,12,0.95) 100%) !important; border: 1px solid rgba(255,70,85,0.4) !important; border-right: 4px solid var(--valo-red) !important; }
[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-assistant"]) { background: linear-gradient(135deg, rgba(10,40,45,0.85) 0%, rgba(10,15,20,0.95) 100%) !important; border: 1px solid rgba(0,212,191,0.3) !important; border-left: 4px solid var(--valo-teal) !important; }
[data-testid="stChatMessage"] h3 { font-family: 'Rajdhani', sans-serif !important; color: var(--white) !important; text-transform: uppercase; border-bottom: 1px solid var(--br-w) !important; }
[data-testid="stChatMessage"] strong { color: #ffb0b8 !important; }
[data-testid="stChatMessage"] code { background: rgba(0,212,191,0.15) !important; color: #55ffeb !important; }

.stChatInput textarea { background: var(--bg2) !important; color: var(--cream) !important; border-bottom: 2px solid rgba(255,70,85,0.2) !important; }
section[data-testid="stSidebar"] { background: #090c11 !important; border-right: 1px solid var(--br-red) !important; }
#MainMenu, footer, header { visibility: hidden !important; }
.block-container { padding-top: 1.2rem !important; max-width: 760px !important; }
</style>
""", unsafe_allow_html=True)

# ========================
# INITIALIZE GROQ
# ========================
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error("❌ Chưa cấu hình hoặc lỗi kết nối GROQ_API_KEY trong Secrets!")
    st.stop()

# ========================
# DATABASE CONTROLLER
# ========================
def load_database():
    if os.path.exists("database_pc.json"):
        try:
            with open("database_pc.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {"loi_he_thong": [], "linh_kien_pc": []}

data_pc = load_database()
db_loi   = len(data_pc.get("loi_he_thong", []))
db_lk    = len(data_pc.get("linh_kien_pc", []))

# ========================
# SESSION STATES
# ========================
if "messages" not in st.session_state:
    st.session_state.messages = []
if "suggestions" not in st.session_state:
    ALL_SUGGESTIONS = [
        ("⚠ Màn hình xanh chết BSOD", "Máy tính bị màn hình xanh chết, phải làm gì?"),
        ("▪ Màn hình đen không hiển thị", "Máy lên nguồn nhưng màn hình đen, không lên gì"),
        ("◈ PC bíp liên tục khi bật", "Máy tính bíp nhiều tiếng khi khởi động, lỗi gì?"),
        ("🌡 CPU overheat — quá nóng", "CPU bị overheat, nhiệt độ lên đến 95 độ C"),
        ("⚡ Cần bao nhiêu W nguồn điện", "Cấu hình PC của tôi cần bao nhiêu W nguồn là đủ?"),
        ("🎮 GTX 1650 chơi được game gì", "Card GTX 1650 chơi được những game nào mượt?")
    ]
    st.session_state.suggestions = random.sample(ALL_SUGGESTIONS, 4)

# ========================
# SIDEBAR
# ========================
with st.sidebar:
    st.markdown("## ⚡ PC Solving")
    st.markdown("---")
    if st.button("⟳  PHIÊN MỚI", use_container_width=True):
        st.session_state.messages = []
        st.session_state.suggestions = []
        st.rerun()
    st.markdown("---")
    st.markdown("<small>Lê Văn Chung · Lớp 10A4 🎓</small>", unsafe_allow_html=True)

# ========================
# HEADER RENDERING
# ========================
st.markdown("""
<div class="valo-header">
    <div class="valo-author">Lê Văn Chung · 10A4</div>
    <div class="valo-eyebrow">⚡ STEM PROJECT ⚡</div>
    <div class="valo-logo-wrap">
        <span class="valo-logo-icon">🖥</span>
        <div class="valo-title">PC<span class="slash">/</span><span class="red">SOLVING</span></div>
    </div>
    <div class="valo-subtitle"><span class="sub-1">CHẨN ĐOÁN</span> · <span class="sub-2">PHÂN TÍCH</span> · <span class="sub-3">XỬ LÝ</span></div>
</div>
""", unsafe_allow_html=True)

# ========================
# GREETING & STATS BOARD
# ========================
st.markdown(f"""
<div class="valo-greeting">
    <div class="valo-status-row"><div class="valo-status-dot"></div><div class="valo-status-text">Hệ thống sẵn sàng</div></div>
    <div class="valo-greeting-title">Hệ thống phân tích phần cứng máy tính</div>
    <div class="valo-greeting-sub">Nhập mã hiệu linh kiện hoặc mô tả hiện tượng lỗi hệ thống để nhận giải pháp xử lý tự động.</div>
    <div class="valo-stats">
        <div class="valo-stat"><span class="valo-stat-num">{db_loi}</span><br><span class="valo-stat-label">Lỗi hệ thống</span></div>
        <div class="valo-stat-divider"></div>
        <div class="valo-stat"><span class="valo-stat-num">{db_lk}</span><br><span class="valo-stat-label">Linh kiện PC</span></div>
    </div>
</div>
""", unsafe_allow_html=True)

# ========================
# CORE DETECT & ALGORITHM
# ========================
def search_database(user_query):
    q = user_query.lower()
    for item in data_pc.get("loi_he_thong", []):
        if any(kw.lower() in q for kw in item.get("keywords", [])):
            return f"### ✕ {item['ten']}\n\n**⚠ Nguyên nhân:** {item['nguyen_nhan']}\n\n**◈ Khắc phục:**\n{item['giai_phap']}"
    for item in data_pc.get("linh_kien_pc", []):
        if any(kw.lower() in q for kw in item.get("keywords", [])):
            return f"### ◆ {item['ten']}\n\n**⚙ Thông số:** {item.get('thong_so','')}\n\n**▶ Tư vấn:** {item.get('chuyen_gia_tu_van','')}"
    return None

def ask_llm(query, history):
    # FIX: Ép hệ thống kiểm tra chủ đề nghiêm ngặt, chặn câu hỏi lạc đề, giữ câu hỏi linh kiện điện tử/điện thoại
    system_prompt = (
        "Bạn là trợ lý chuyên sâu về phần cứng máy tính và linh kiện điện tử (bao gồm cả linh kiện điện thoại di động) "
        "của dự án PC Solving do Lê Văn Chung lớp 10A4 phát triển.\n\n"
        "QUY TẮC PHẠM VI CÂU HỎI:\n"
        "1. Chỉ trả lời các câu hỏi liên quan trực tiếp đến lỗi máy tính, linh kiện PC, thông số phần cứng, "
        "hoặc các linh kiện điện tử nói chung (bao gồm màn hình, pin, vi xử lý, chip điện thoại như Snapdragon, Apple A-series...).\n"
        "2. TUYỆT ĐỐI KHÔNG trả lời các câu hỏi ngoài lề như: bạn là ai, mô hình ngôn ngữ gì, thuộc công ty nào (Google, OpenAI, Meta, Groq...), "
        "hoặc các câu hỏi triết học, văn học, toán học không liên quan phần cứng.\n"
        "3. Nếu người dùng hỏi phạm vi ngoài ngành hoặc hỏi về danh tính/mô hình của bạn, bạn PHẢI trả lời chính xác và duy nhất dòng chữ sau, không giải thích thêm: "
        "\"[Hệ thống]: Câu hỏi chưa đúng lĩnh vực chuyên môn (Linh kiện điện tử & Phần cứng máy tính).\""
    )
    
    messages = [{"role": "system", "content": system_prompt}]
    for msg in history[-6:]:
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": query})
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.2, # Giảm nhiệt độ xuống để bot tuân thủ luật nghiêm ngặt hơn
        max_tokens=600
    )
    return response.choices[0].message.content

# ========================
# ENGINE PROCESSOR
# ========================
def process_user_input(prompt_text):
    st.session_state.messages.append({"role": "user", "content": prompt_text})
    st.rerun()

if not st.session_state.messages:
    st.markdown('<div class="valo-suggest-label"><span>CHỌN NHANH VẤN ĐỀ</span></div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2, gap="small")
    for i, (label, query) in enumerate(st.session_state.suggestions):
        with (col1 if i % 2 == 0 else col2):
            if st.button(label, key=f"sug_btn_{i}"):
                process_user_input(query)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if user_input := st.chat_input("Nhập mã lỗi hoặc linh kiện cần phân tích..."):
    process_user_input(user_input)

if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    latest_query = st.session_state.messages[-1]["content"]
    
    with st.chat_message("assistant"):
        msg_placeholder = st.empty()
        with st.spinner("ĐANG PHÂN TÍCH DỮ LIỆU..."):
            local_res = search_database(latest_query)
            final_ans = local_res if local_res else ask_llm(latest_query, st.session_state.messages[:-1])
            
            typed_text = ""
            for char in final_ans:
                typed_text += char
                msg_placeholder.markdown(typed_text + "▌")
                time.sleep(0.005)
            msg_placeholder.markdown(final_ans)
            
    st.session_state.messages.append({"role": "assistant", "content": final_ans})
