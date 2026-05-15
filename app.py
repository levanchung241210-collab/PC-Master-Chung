import streamlit as st
from google import genai

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Chatbot Giải Lỗi PC - Chung 10A4",
    page_icon="🖥️"
)

# =========================
# API KEY
# =========================
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]

    client = genai.Client(api_key=API_KEY)

except Exception as e:

    st.error("❌ Chưa cấu hình API KEY!")

    st.exception(e)

    st.stop()

# =========================
# UI
# =========================
st.title("🖥️ Chatbot Giải Lỗi PC - Chung 10A4")

st.markdown("### Sản phẩm STEM")

st.markdown("---")

# =========================
# SESSION STATE
# =========================
if "messages" not in st.session_state:

    st.session_state.messages = []

# =========================
# SHOW CHAT HISTORY
# =========================
for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# =========================
# CHAT INPUT
# =========================
prompt = st.chat_input(
    "Nhập mã lỗi hoặc câu hỏi về PC..."
)

# =========================
# USER MESSAGE
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

            response = client.models.generate_content(

                model="gemini-2.0-flash",

                contents=f"""
Bạn là chuyên gia PC của Lê Văn Chung lớp 10A4.

Trả lời:
- tiếng Việt
- ngắn gọn
- chia bước 1 2 3

Câu hỏi:
{prompt}
"""
            )

            answer = response.text

            st.markdown(answer)

            st.session_state.messages.append({

                "role": "assistant",

                "content": answer

            })

        except Exception as e:

            st.error(f"❌ Lỗi AI: {str(e)}")
