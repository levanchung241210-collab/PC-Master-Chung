import streamlit as st
import requests

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Chuyên Gia PC - Chung 10A4",
    page_icon="🖥️"
)

# =========================
# API KEY
# =========================
try:
    API_KEY = st.secrets["OPENROUTER_API_KEY"]

except Exception:

    st.error("❌ Chưa thêm OPENROUTER_API_KEY vào Secrets!")

    st.stop()

# =========================
# UI
# =========================
st.title("🖥️ Chatbot Giải Lỗi PC - Chung 10A4")

st.markdown("### Sản phẩm STEM")

st.markdown("---")

# =========================
# CHAT HISTORY
# =========================
if "messages" not in st.session_state:

    st.session_state.messages = []

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

            headers = {

                "Authorization": f"Bearer {API_KEY}",

                "Content-Type": "application/json"

            }

            data = {

                "model": "deepseek/deepseek-chat-v3-0324:free",

                "messages": [

                    {
                        "role": "system",
                        "content":
                        """
Bạn là chuyên gia PC của Lê Văn Chung lớp 10A4.

Nhiệm vụ:
- giải lỗi Windows
- tư vấn CPU
- tư vấn mainboard
- chẩn đoán phần cứng

Trả lời:
- tiếng Việt
- ngắn gọn
- chia bước 1 2 3
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

                json=data

            )

            result = response.json()

            answer = result["choices"][0]["message"]["content"]

            st.markdown(answer)

            st.session_state.messages.append({

                "role": "assistant",

                "content": answer

            })

        except Exception as e:

            st.error(f"❌ Lỗi AI: {str(e)}")
