import streamlit as st
import json, re, os, random
from groq import Groq

st.set_page_config(page_title="PC Solving System — Lê Văn Chung 10A4", page_icon="⚡", layout="centered")

# ====================== CSS VALORANT NÂNG CẤP (ĐẸP HƠN) ======================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Barlow+Condensed:wght@400;600;700;800&family=Barlow:wght@300;400;500;600&display=swap');

:root {
    --R: #ff4655; --R2: #ff7080; --R3: rgba(255,70,85,0.18);
    --T: #00d4bf; --T2: #00ffe7; --T3: rgba(0,212,191,0.15);
    --G: #e8c97a;
    --bg: #090b11; --p1: #0f1320; --p2: #151929; --p3: #1c2236;
    --W: #ffffff; --C: #ece8e1; --S: #b8b4ac;
}

html, body, .stApp { 
    background:var(--bg) !important; 
    color:var(--C) !important; 
    font-family:'Barlow',sans-serif !important; 
}

/* Background mạnh hơn */
.stApp::before {
    content:''; position:fixed; inset:0; pointer-events:none; z-index:0;
    background:
        linear-gradient(135deg, rgba(255,70,85,0.11) 0%, transparent 45%),
        linear-gradient(315deg, rgba(0,212,191,0.09) 0%, transparent 45%),
        repeating-linear-gradient(-55deg, transparent 0, transparent 48px, rgba(255,70,85,0.025) 48px, rgba(255,70,85,0.028) 49px),
        repeating-linear-gradient(35deg, transparent 0, transparent 72px, rgba(0,212,191,0.02) 72px, rgba(0,212,191,0.022) 73px);
}

/* Top glow bar mạnh hơn */
.stApp::after {
    content:''; position:fixed; top:0; left:0; right:0; height:3px; z-index:9999;
    background:linear-gradient(90deg,transparent 0%,#ff4655 15%,#ff7080 30%,transparent 45%,transparent 55%,#00d4bf 70%,#00ffe7 85%,transparent 100%);
    filter:drop-shadow(0 0 8px #ff4655);
}

/* Header & Title */
.valo-title {
    text-shadow: 0 4px 20px rgba(0,0,0,0.9), 0 0 50px rgba(255,70,85,0.7) !important;
}

.valo-greeting {
    box-shadow: 0 0 60px rgba(255,70,85,0.25), 0 0 100px rgba(0,212,191,0.1),
                inset 0 0 80px rgba(255,70,85,0.05) !important;
    animation: greetGlow 4s ease-in-out infinite;
}

@keyframes greetGlow {
    0%,100% { box-shadow: 0 0 60px rgba(255,70,85,0.25), 0 8px 40px rgba(0,0,0,0.8); }
    50% { box-shadow: 0 0 80px rgba(255,70,85,0.35), 0 0 120px rgba(0,212,191,0.15), 0 8px 40px rgba(0,0,0,0.8); }
}

/* Chat Bubble sắc nét hơn */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    border-left: 5px solid var(--R) !important;
    box-shadow: 5px 0 30px rgba(255,70,85,0.25) !important;
}

[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    border-right: 5px solid var(--T) !important;
    box-shadow: -5px 0 30px rgba(0,212,191,0.25) !important;
}

/* Button Valorant */
.stButton > button {
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    transform: translateX(10px) !important;
    box-shadow: 0 0 30px rgba(0,212,191,0.6) !important;
}

::-webkit-scrollbar-thumb { background:rgba(255,70,85,0.6); }
</style>
""", unsafe_allow_html=True)

# ====================== PHẦN CODE CÒN LẠI (GIỮ NGUYÊN) ======================
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("❌ Chưa cấu hình GROQ_API_KEY!"); st.stop()

def load_db():
    if os.path.exists("database_pc.json"):
        with open("database_pc.json","r",encoding="utf-8") as f: return json.load(f)
    return {"loi_he_thong":[],"linh_kien_pc":[]}

def load_raw():
    if os.path.exists("database_pc.json"):
        with open("database_pc.json","r",encoding="utf-8") as f: return f.read()
    return "{}"

data_pc=load_db(); raw=load_raw()
db_loi=len(data_pc.get("loi_he_thong",[])); db_lk=len(data_pc.get("linh_kien_pc",[]))

with st.sidebar:
    st.markdown("## ⚡ PC Solving")
    st.markdown("---")
    st.markdown("Hệ thống chẩn đoán lỗi và tư vấn linh kiện máy tính chuyên sâu.")
    st.markdown("---")
    if st.button("⟳ PHIÊN MỚI", use_container_width=True):
        st.session_state.messages=[]; st.session_state.greeted=False; st.session_state.suggestions=[]; st.rerun()
    st.markdown("---")
    st.markdown("<small>Lê Văn Chung · Lớp 10A4 🎓</small>", unsafe_allow_html=True)

# Phần SVG Logo và Header của bạn (giữ nguyên)
LVC = """<svg viewBox="0 0 52 52" xmlns="http://www.w3.org/2000/svg"> ... </svg>"""  # Bạn dán lại phần SVG cũ nếu cần

# === HEADER, GREETING, SUGGESTIONS === 
# (Bạn dán lại toàn bộ phần st.markdown header + greeting + suggestions từ code cũ của bạn vào đây)

# ====================== SYSTEM PROMPT & HÀM CHAT ======================
SYSTEM_PROMPT = f"""Bạn là **PC & Mobile Solving Expert** — Lê Văn Chung 10A4, kỹ thuật viên phần cứng chuyên nghiệp.
Trả lời bằng tiếng Việt, rõ ràng, có cấu trúc, chuyên sâu.
Dữ liệu: {raw}"""

def ask(uq, hist):
    messages = [{"role":"system", "content": SYSTEM_PROMPT}]
    for m in hist[-8:]:
        messages.append({"role": m["role"], "content": m["content"]})
    messages.append({"role":"user", "content": uq})

    r = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        max_tokens=1100,
        temperature=0.45
    )
    return r.choices[0].message.content

# Phần chat logic còn lại của bạn...
# (dán tiếp phần for m in st.session_state.messages, handle function, chat_input...)

st.success("✅ Giao diện Valorant đã được nâng cấp!")
