import streamlit as st
import json
import re
import os
import random
from groq import Groq

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="PC Solving System — Lê Văn Chung 10A4",
    page_icon="⚡",
    layout="centered"
)

# =========================
# VALORANT UI
# =========================
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Barlow:wght@300;400;500;600&display=swap');

:root{
    --red:#ff4655;
    --bg:#0b0e13;
    --panel:#171c25;
    --text:#f3f4f6;
}

/* BASE */

html, body, .stApp{
    background:
        radial-gradient(circle at top right, rgba(255,70,85,0.08), transparent 25%),
        linear-gradient(180deg,#0a0c11 0%, #0f131a 100%);
    color:var(--text);
    font-family:'Barlow',sans-serif;
}

/* Background */

.stApp::before{
    content:"";
    position:fixed;
    inset:0;
    background:
    repeating-linear-gradient(
        -55deg,
        transparent,
        transparent 55px,
        rgba(255,70,85,0.015) 56px
    );
    pointer-events:none;
    z-index:0;
}

/* HEADER */

.valo-header{
    text-align:center;
    margin-top:10px;
}

.valo-title{
    font-family:'Rajdhani',sans-serif;
    font-size:60px;
    font-weight:700;
    color:white;
    line-height:0.95;

    text-shadow:
    0 0 18px rgba(255,70,85,0.18);
}

.valo-title span{
    color:var(--red);
}

.valo-sub{
    margin-top:8px;
    color:#cbd5e1;
    letter-spacing:3px;
    font-size:12px;
    text-transform:uppercase;
}

/* GREETING */

.valo-box{
    background:
    linear-gradient(
    145deg,
    rgba(23,28,37,0.96),
    rgba(16,20,28,0.98)
    );

    border:1px solid rgba(255,70,85,0.15);

    border-left:4px solid var(--red);

    border-radius:14px;

    padding:26px;

    margin-top:20px;

    box-shadow:
    0 0 24px rgba(255,70,85,0.05);
}

.valo-box h3{
    font-family:'Rajdhani',sans-serif;
    font-size:26px;
    margin-bottom:8px;
}

.valo-box p{
    color:#c7cfda;
    line-height:1.8;
}

/* BUTTON */

.stButton > button{

    background:
    linear-gradient(
    145deg,
    #1b2230,
    #151a23
    ) !important;

    color:#dce1ea !important;

    border:1px solid rgba(255,255,255,0.05) !important;

    border-left:3px solid transparent !important;

    border-radius:10px !important;

    padding:14px !important;

    transition:0.18s ease !important;

    min-height:58px !important;

    font-weight:500 !important;
}

.stButton > button:hover{

    border-left:3px solid var(--red) !important;

    transform:translateY(-2px);

    box-shadow:
    0 0 18px rgba(255,70,85,0.12) !important;
}

/* USER */

[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]){

    background:
    linear-gradient(
    145deg,
    rgba(255,70,85,0.08),
    rgba(255,70,85,0.03)
    );

    border:1px solid rgba(255,70,85,0.15);

    border-right:3px solid var(--red);

    border-radius:14px;

    padding:16px;

    margin:10px 0;
}

/* ASSISTANT */

[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-assistant"]){

    background:
    linear-gradient(
    145deg,
    rgba(25,31,42,0.96),
    rgba(18,22,30,0.98)
    );

    border:1px solid rgba(255,255,255,0.06);

    border-left:3px solid var(--red);

    border-radius:14px;

    padding:16px;

    margin:10px 0;

    box-shadow:
    0 0 20px rgba(255,70,85,0.04);
}

/* TEXT */

[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li{
    color:#eef2f7 !important;
    line-height:1.85 !important;
    font-size:15px !important;
}

/* INPUT */

.stChatInput textarea{

    background:#151b24 !important;

    color:white !important;

    border:1px solid rgba(255,255,255,0.08) !important;

    border-radius:12px !important;

    font-size:15px !important;
}

/* SIDEBAR */

section[data-testid="stSidebar"]{
    background:#0a0d12 !important;
    border-right:1px solid rgba(255,70,85,0.1);
}

section[data-testid="stSidebar"] *{
    color:#d0d6e0 !important;
}

/* HIDE */

#MainMenu,
footer,
header{
    visibility:hidden;
}

.block-container{
    max-width:850px !important;
    padding-top:1rem !important;
}

</style>
""", unsafe_allow_html=True)

# =========================
# GROQ CLIENT
# =========================
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("❌ Chưa thêm GROQ_API_KEY vào Secrets")
    st.stop()

# =========================
# DATABASE
# =========================
def load_database():
    if os.path.exists("database_pc.json"):
        with open("database_pc.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {"loi_he_thong": [], "linh_kien_pc": []}

data_pc = load_database()

# =========================
# SESSION
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================
# SIDEBAR
# =========================
with st.sidebar:

    st.markdown("## ⚡ PC SOLVING SYSTEM")
    st.markdown("---")
    st.markdown("Hệ thống hỗ trợ xử lý lỗi và tư vấn linh kiện PC.")

    if st.button("⟳ PHIÊN MỚI", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown("Lê Văn Chung — 10A4")

# =========================
# HEADER
# =========================
st.markdown("""
<div class="valo-header">
    <div class="valo-title">
        PC <span>SOLVING</span>
    </div>

    <div class="valo-sub">
        Diagnostic • Hardware • Performance
    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# GREETING
# =========================
if len(st.session_state.messages) == 0:

    st.markdown("""
    <div class="valo-box">

    <h3>💻 Hệ thống hỗ trợ kỹ thuật PC</h3>

    <p>
    Nhập mã lỗi Windows, mô tả hiện tượng hoặc linh kiện cần tư vấn.
    Hệ thống sẽ tự động phân tích và đưa ra giải pháp phù hợp.
    </p>

    </div>
    """, unsafe_allow_html=True)

# =========================
# SHOW CHAT
# =========================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# =========================
# ASK MODEL
# =========================
def ask_bot(prompt):

    system_prompt = """
Bạn là chuyên gia phần cứng máy tính của Lê Văn Chung lớp 10A4.

Nhiệm vụ:
- Chẩn đoán lỗi PC
- Giải thích lỗi Windows
- Tư vấn CPU GPU RAM Mainboard PSU
- Hướng dẫn sửa lỗi theo từng bước

QUY TẮC:
- Không nói mình là AI
- Trả lời chuyên nghiệp
- Chia bước rõ ràng
- Không lan man
"""

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role": "system",
                "content": system_prompt
            },

            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.4,
        max_tokens=700
    )

    return response.choices[0].message.content

# =========================
# CHAT INPUT
# =========================
if prompt := st.chat_input("Nhập lỗi PC hoặc linh kiện cần tư vấn..."):

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner("ĐANG PHÂN TÍCH HỆ THỐNG..."):

            try:

                answer = ask_bot(prompt)

                st.markdown(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as e:

                st.error(f"❌ Lỗi hệ thống: {str(e)}")
