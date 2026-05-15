import streamlit as st
import requests

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="PC Assistant - Chung 10A4",
    page_icon="🖥️",
    layout="wide"
)

# =========================
# CSS
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
    color: #93c5fd !important;
    text-align: center;
    font-size: 42px !important;
    font-weight: 700 !important;
}

/* ===== SUBTITLE ===== */
h3 {
    text-align: center;
    color: #cbd5e1;
}

/* ===== CHAT USER ===== */
[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) {
    background-color: #1d4ed8;
    border-radius: 16px;
    padding: 12px;
    margin-bottom: 12px;
}

/* ===== CHAT BOT ===== */
[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-assistant"]) {
    background-color: #111827;
    border-radius: 16px;
    padding: 12px;
    margin-bottom: 12px;
    border: 1px solid #334155;
}

/* ===== INPUT ===== */
.stChatInput input {
    background-color: #111827 !important;
    color: white !important;
    border-radius: 14px !important;
}

/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"] {
    background-color: #0f172a;
}

/* ===== SCROLLBAR ===== */
::-webkit-scrollbar {
    width: 10px;
}

::-webkit-scrollbar-thumb {
    background: #3b82f6;
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

    st.title("🖥️ PC Assistant")

    st.success("🟢 Online")

    st.markdown("---")

    st.markdown("### 🔧 Hỗ trợ")

    st.write("✔️ Lỗi Windows")
    st.write("✔️ Màn hình xanh")
    st.write("✔️ CPU & Mainboard")
    st.write("✔️ RAM & GPU")
    st.write("✔️ Chẩn đoán phần cứng")

    st.markdown("---")

    st.info(
        "👨‍💻 Sản phẩm STEM\n\nLê Văn Chung - 10A4"
    )

# =========================
# TITLE
# =========================
st.title("🖥️ Chatbot PC Assistant")

st.markdown(
    "### Hỗ trợ giải lỗi và tư vấn linh kiện máy tính"
)

st.markdown("---")

# =========================
# CHAT HISTORY
# =========================
if "messages" not in st.session_state:

    st.session_state.messages = []

# =========================
# SHOW OLD CHAT
# =========================
for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        st.markdown(msg["content"])

# =========================
# INPUT
# =========================
prompt = st.chat_input(
    "Nhập lỗi Windows hoặc tên linh kiện..."
)

# =========================
# HANDLE CHAT
# =========================
if prompt:

    st.session_state.messages.append({

        "role": "user",

        "content": prompt

    })

    with st.chat_message("user"):

        st.markdown(prompt)

    with st.chat_message("assistant"):

        try:

            with st.spinner("🔍 Đang phân tích..."):

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
- giải mã màn hình xanh
- tư vấn CPU Intel AMD
- tư vấn Mainboard
- chẩn đoán phần cứng
- tư vấn GPU RAM SSD

Yêu cầu:
- trả lời tiếng Việt
- cực kỳ ngắn gọn
- không giải thích lan man
- tối đa 5 dòng
- chia bước 1 2 3
- ưu tiên giải pháp nhanh
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

                # SUCCESS
                if response.status_code == 200 and "choices" in result:

                    answer = result["choices"][0]["message"]["content"]

                    st.markdown(answer)

                    st.session_state.messages.append({

                        "role": "assistant",

                        "content": answer

                    })

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
