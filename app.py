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

# ========================
# CSS
# ========================
st.markdown("""
<style>
html, body, .stApp {
    background: #0b0e14;
    color: white;
}

.stChatInput textarea {
    background: #181c28 !important;
    color: white !important;
}

.stButton > button {
    width: 100%;
    border-radius: 10px;
    border: 1px solid #ff4655;
    background: #181c28;
    color: white;
    transition: 0.2s;
}

.stButton > button:hover {
    background: #ff4655;
    transform: translateY(-2px);
}

[data-testid="stChatMessage"] {
    border-radius: 10px;
    padding: 10px;
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

data_pc = load_database()

# ========================
# SIDEBAR
# ========================
with st.sidebar:
    st.title("⚡ PC Solving")

    if st.button("🔄 Phiên mới"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown("### 📊 Database")

    st.write("Lỗi hệ thống:", len(data_pc["loi_he_thong"]))
    st.write("Linh kiện:", len(data_pc["linh_kien_pc"]))

# ========================
# HEADER
# ========================
st.markdown("""
# ⚡ PC SOLVING

### Hệ thống phân tích lỗi & linh kiện PC
""")

# ========================
# SESSION
# ========================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ========================
# GỢI Ý
# ========================
suggestions = [
    ("⚠ BSOD", "Máy tính bị màn hình xanh BSOD"),
    ("🎮 GTX 1650", "GTX 1650 chơi được game gì"),
    ("🌡 CPU nóng", "CPU bị nóng 95 độ"),
    ("💾 SSD lỗi", "SSD bị bad sector"),
]

st.markdown("### ⚡ Chọn nhanh")

col1, col2 = st.columns(2)

for i, (label, query) in enumerate(suggestions):
    with (col1 if i % 2 == 0 else col2):
        if st.button(label):
            st.session_state["quick_prompt"] = query

# ========================
# CHAT HISTORY
# ========================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ========================
# SEARCH DATABASE
# ========================
def search_database(user_query):
    q = user_query.lower()

    for item in data_pc.get("loi_he_thong", []):
        keywords = [k.lower() for k in item.get("keywords", [])]

        if any(k in q for k in keywords):
            return f"""
### ⚠ {item['ten']}

**Nguyên nhân:**  
{item['nguyen_nhan']}

**Khắc phục:**  
{item['giai_phap']}
"""

    for item in data_pc.get("linh_kien_pc", []):
        keywords = [k.lower() for k in item.get("keywords", [])]

        if any(k in q for k in keywords):
            return f"""
### 🔧 {item['ten']}

**Thông số:**  
{item.get('thong_so', '')}

**Socket:**  
`{item.get('socket', '')}`

**Tư vấn:**  
{item.get('chuyen_gia_tu_van', '')}
"""

    return None

# ========================
# AI RESPONSE
# ========================
SYSTEM_PROMPT = """
Bạn là hệ thống hỗ trợ kỹ thuật PC của Lê Văn Chung 10A4.

KHÔNG được nhắc:
- AI
- Groq
- Meta
- LLM

Trả lời như chuyên gia kỹ thuật máy tính.
"""

def ask_ai(prompt, history):
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    for msg in history[-6:]:
        messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })

    messages.append({
        "role": "user",
        "content": prompt
    })

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        max_tokens=700,
        temperature=0.5
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
        with st.spinner("Đang phân tích..."):

            try:
                answer = search_database(prompt)

                if not answer:
                    answer = ask_ai(prompt, st.session_state.messages)

                st.markdown(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as e:
                st.error(f"❌ Lỗi: {str(e)}")

# ========================
# QUICK BUTTON
# ========================
if "quick_prompt" in st.session_state:
    prompt = st.session_state["quick_prompt"]
    del st.session_state["quick_prompt"]
    handle_message(prompt)

# ========================
# CHAT INPUT
# ========================
prompt = st.chat_input("Nhập lỗi hoặc linh kiện cần phân tích...")

if prompt:
    handle_message(prompt)