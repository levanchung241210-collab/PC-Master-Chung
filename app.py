import streamlit as st
import json
import re
import os
from groq import Groq

st.set_page_config(
    page_title="Vua PC Chatbot - Lê Văn Chung 10A4",
    page_icon="🖥️",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Share+Tech+Mono&display=swap');
.stApp { background: linear-gradient(135deg, #020617, #0b1329, #1c1a27); color: #f8fafc; }
.neon-title { text-align:center; font-family:'Orbitron',monospace; font-size:36px!important; font-weight:900!important; color:#fff; text-shadow:0 0 10px #3b82f6,0 0 30px #1d4ed8,0 0 60px #1e40af; margin-bottom:4px; }
.neon-subtitle { text-align:center; font-family:'Share Tech Mono',monospace; color:#38bdf8; font-size:13px!important; letter-spacing:2px; margin-bottom:10px; }
.badge-db { display:inline-block; padding:2px 10px; border-radius:20px; font-size:11px; font-weight:bold; background:#1e3a5f; color:#60a5fa; border:1px solid #3b82f6; }
.badge-ai { display:inline-block; padding:2px 10px; border-radius:20px; font-size:11px; font-weight:bold; background:#1a2e1a; color:#4ade80; border:1px solid #22c55e; }
[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) { background:linear-gradient(135deg,#1d4ed8,#1e40af); border-radius:16px; border-left:5px solid #60a5fa; padding:12px; }
[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-assistant"]) { background:rgba(15,23,42,0.85); border-radius:16px; border:1px solid #334155; border-left:5px solid #3b82f6; padding:12px; }
.stChatInput textarea { background-color:#0f172a!important; color:#fff!important; border:2px solid #3b82f6!important; }
section[data-testid="stSidebar"] { background-color:#020617; border-right:1px solid #1e293b; }
</style>
""", unsafe_allow_html=True)

# GROQ CLIENT
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except KeyError:
    st.error("❌ Chưa cấu hình GROQ_API_KEY trong Secrets!")
    st.info("Vào Settings → Secrets → thêm: GROQ_API_KEY = 'gsk_...'")
    st.stop()
except Exception as e:
    st.error(f"❌ Lỗi kết nối AI: {str(e)}")
    st.stop()

# LOAD DATABASE
def load_database():
    if os.path.exists("database_pc.json"):
        with open("database_pc.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {"loi_he_thong": [], "linh_kien_pc": []}

data_pc = load_database()

# SIDEBAR
with st.sidebar:
    st.markdown("<h2 style='color:#3b82f6;text-align:center;font-family:Orbitron,monospace;'>🖥️ VUA PC LAB</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#64748b;font-size:12px;'>v12.0 · GROQ POWERED</p>", unsafe_allow_html=True)
    st.markdown("---")
    db_loi = len(data_pc.get("loi_he_thong", []))
    db_lk = len(data_pc.get("linh_kien_pc", []))
    st.markdown("**📊 Database:**")
    st.success(f"✅ {db_loi} lỗi hệ thống")
    st.success(f"✅ {db_lk} linh kiện PC")
    st.markdown("---")
    st.markdown("**⚡ Chế độ:**")
    st.info("1️⃣ Tìm trong Database JSON\n\n2️⃣ Không có → Groq AI trả lời")
    st.markdown("---")
    if st.button("🗑️ Xóa lịch sử chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.markdown("---")
    st.markdown("<p style='text-align:center;color:#475569;font-size:11px;'>Made by Lê Văn Chung 10A4 🎓</p>", unsafe_allow_html=True)

# HEADER
st.markdown('<div class="neon-title">👑 VUA PC CHATBOT</div>', unsafe_allow_html=True)
st.markdown('<div class="neon-subtitle">CHẨN ĐOÁN LỖI & TƯ VẤN LINH KIỆN · LÊ VĂN CHUNG 10A4</div>', unsafe_allow_html=True)
st.markdown("---")

if "messages" not in st.session_state:
    st.session_state.messages = []

# THUẬT TOÁN TÌM DATABASE
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
            return (f'<span class="badge-db">📁 TỪ DATABASE</span>\n\n'
                    f"### 🎯 {best_match['ten']}\n"
                    f"⚠️ **Phân loại:** `{best_match.get('loai','')}`\n\n"
                    f"❌ **Nguyên nhân:** {best_match['nguyen_nhan']}\n\n"
                    f"🛠️ **Cách khắc phục:**\n{best_match['giai_phap']}")
        else:
            return (f'<span class="badge-db">📁 TỪ DATABASE</span>\n\n'
                    f"### 📦 {best_match['ten']}\n"
                    f"⚙️ **Thông số:** {best_match.get('thong_so','')}\n\n"
                    f"🔌 **Socket:** `{best_match.get('socket','')}`\n\n"
                    f"⚡ **Nguồn:** {best_match.get('nguon_khuyen_nghi','')}\n\n"
                    f"💡 **Tư vấn:** *{best_match.get('chuyen_gia_tu_van','')}*")
    return None

# GROQ AI
SYSTEM_PROMPT = """Bạn là chuyên gia PC của Lê Văn Chung lớp 10A4 - kỹ sư phần cứng chuyên nghiệp.

Nhiệm vụ:
- Chẩn đoán lỗi Windows, BSOD, mã lỗi số hiệu
- Phân tích lỗi phần cứng: CPU, RAM, GPU, ổ cứng, nguồn, mainboard
- Tư vấn linh kiện PC, thông số kỹ thuật, độ tương thích
- Hướng dẫn sửa chữa từng bước

Quy tắc:
- Luôn dùng tiếng Việt
- Chia bước rõ ràng: Bước 1, Bước 2...
- Giải thích nguyên nhân TRƯỚC khi đưa cách fix
- Ngắn gọn, dễ hiểu cho học sinh THPT
- Kết thúc bằng 1 lời khuyên phòng tránh"""

def ask_groq(user_query, chat_history):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for msg in chat_history[-6:]:
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": user_query})
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        max_tokens=1024,
        temperature=0.7
    )
    return f'<span class="badge-ai">🤖 GROQ AI</span>\n\n{response.choices[0].message.content}'

# HIỂN THỊ LỊCH SỬ
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"], unsafe_allow_html=True)

if not st.session_state.messages:
    st.markdown("**💡 Thử hỏi:**")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.code("Lỗi màn hình xanh BSOD")
        st.code("i5-12400F mạnh không?")
    with c2:
        st.code("Mã lỗi 0x0000007E")
        st.code("RAM 8GB có đủ chơi game?")
    with c3:
        st.code("PC bíp 3 tiếng khi bật")
        st.code("GTX 1660 Super vs RX 6600")

# XỬ LÝ INPUT
if prompt := st.chat_input("Nhập mã lỗi, tên linh kiện hoặc mô tả triệu chứng..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("⚡ Đang phân tích..."):
            try:
                answer = search_database(prompt) or ask_groq(prompt, st.session_state.messages)
                st.markdown(answer, unsafe_allow_html=True)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"❌ Lỗi: {str(e)}")