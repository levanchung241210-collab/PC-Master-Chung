import streamlit as st
import requests

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="AI PC Assistant - Chung 10A4",
    page_icon="🤖",
    layout="wide"
)

# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>

/* ===== BACKGROUND ===== */
.stApp {
    background: linear-gradient(
        135deg,
        #0f172a,
        #111827,
        #1e293b
    );
    color: white;
}

/* ===== TITLE ===== */
h1 {
    color: #60a5fa !important;
    text-align: center;
    font-size: 45px !important;
}

/* ===== SUBTITLE ===== */
h3 {
    text-align: center;
    color: #cbd5e1;
}

/* ===== CHAT USER ===== */
[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) {
    background-color: #1d4ed8;
    border-radius: 15px;
    padding: 12px;
    margin-bottom: 12px;
}

/* ===== CHAT AI ===== */
[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-assistant"]) {
    background-color: #111827;
    border-radius: 15px;
    padding: 12px;
    margin-bottom: 12px;
    border: 1px solid #374151;
}

/* ===== INPUT ===== */
.stChatInput input {
    background-color: #111827 !important;
    color: white !important;
    border-radius: 12px !important;
}

/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"] {
    background-color: #0f172a;
}

/* ===== BUTTON ===== */
.stButton button {
    background-color: #2563eb;
    color: white;
    border-radius: 10px;
}

/* ===== SCROLLBAR ===== */
::-webkit-scrollbar {
    width: 10px;
}

::-webkit-scrollbar-thumb {
    background: #2563eb;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# API KEY
# =========================
try:

    API_KEY = st.secrets["OPENROUTER_API_KEY"]

except:

    st.error("❌ Chưa thêm OPENROUTER_API_KEY vào Secrets!")

    st.stop()

# =========================
# SIDEBAR
# =========================
with st.sidebar:

    st.title("⚙️ AI System")

    st.success("🟢 Online")

    st.markdown("---")

    st.markdown("## 🧠 Chức năng")

    st.write("✔️ Giải lỗi Windows")
    st.write("✔️ Giải mã BSOD")
    st.write("✔️ Tư vấn CPU")
    st.write("✔️ Tư vấn Mainboard")
    st.write("✔️ Chẩn đoán phần cứng")
    st.write("✔️ Tư vấn RAM/GPU")

    st.markdown("---")

    st.info("👨‍💻 STEM Project\n\nLê Văn Chung - 10A4")

# =========================
# MAIN TITLE
# =========================
st.title("🤖 AI PC Assistant")

st.markdown("### Chatbot Chuyên Gia Máy Tính")

st.markdown("---")

# =========================
# CHAT HISTORY
# =========================
if "messages" not in st.session_state:

    st.session_state.messages = []

# =========================
# DISPLAY OLD CHAT
# =========================
for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        st.markdown(msg["content"])

# =========================
# CHAT INPUT
# =========================
prompt = st.chat_input(
    "Nhập lỗi Windows hoặc tên linh kiện..."
)

# =========================
# HANDLE CHAT
# =========================
if prompt:

    # SAVE USER MESSAGE
    st.session_state.messages.append({

        "role": "user",

        "content": prompt

    })

    with st.chat_message("user"):

        st.markdown(prompt)

    with st.chat_message("assistant"):

        try:

            with st.spinner("🤖 AI đang phân tích lỗi..."):

                headers = {

                    "Authorization": f"Bearer {API_KEY}",

                    "Content-Type": "application/json"

                }

                payload = {

                    "model": "openai/gpt-oss-20b:free",

                    "messages": [

                        {
                            "role": "system",

                            "content":
                            """
Bạn là chuyên gia PC của Lê Văn Chung lớp 10A4.

Nhiệm vụ:
- giải lỗi Windows
- giải mã BSOD
- tư vấn CPU Intel AMD
- tư vấn Mainboard
- chẩn đoán phần cứng
- tư vấn GPU RAM SSD

Yêu cầu:
- trả lời tiếng Việt
- chuyên nghiệp
- dễ hiểu
- chia bước 1 2 3 rõ ràng
"""
                        },

                        {
                            "role": "user",

                            "content": prompt
                        }

                    ]

                }

                response = requests.post(

                    "https://openrouter.ai/api/v1/chat/completions",

                    headers=headers,

                    json=payload,

                    timeout=60

                )

                result = response.json()

                # =========================
                # SUCCESS
                # =========================
                if response.status_code == 200 and "choices" in result:

                    answer = result["choices"][0]["message"]["content"]

                    st.markdown(answer)

                    st.session_state.messages.append({

                        "role": "assistant",

                        "content": answer

                    })

                # =========================
                # ERROR
                # =========================
                else:

                    error_message = result.get(
                        "error",
                        {}
                    ).get(
                        "message",
                        "Lỗi không xác định"
                    )

                    st.error(f"❌ OpenRouter lỗi: {error_message}")

        except Exception as e:

            st.error(f"❌ Lỗi hệ thống: {str(e)}")
