import streamlit as st
import requests

# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Chatbot Giải Lỗi PC - Chung 10A4",
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
# GIAO DIỆN
# =========================
st.title("🖥️ Chatbot Giải Lỗi PC - Chung 10A4")

st.markdown("### Sản phẩm STEM")

with st.expander("ℹ️ Giới thiệu"):

    st.write(
        "AI hỗ trợ giải mã lỗi Windows, BSOD, CPU Intel, Mainboard, RAM và phần cứng máy tính."
    )

st.markdown("---")

# =========================
# LỊCH SỬ CHAT
# =========================
if "messages" not in st.session_state:

    st.session_state.messages = []

# HIỂN THỊ CHAT CŨ
for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        st.markdown(msg["content"])

# =========================
# Ô NHẬP CHAT
# =========================
prompt = st.chat_input(
    "Nhập mã lỗi hoặc tên linh kiện..."
)

# =========================
# XỬ LÝ CHAT
# =========================
if prompt:

    # LƯU USER MESSAGE
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

                # MODEL FREE ỔN ĐỊNH
                "deepseek/deepseek-r1-0528:free"

                "messages": [

                    {
                        "role": "system",

                        "content":
                        """
Bạn là chuyên gia PC của Lê Văn Chung lớp 10A4.

Nhiệm vụ:
- giải mã lỗi Windows
- giải lỗi màn hình xanh
- tư vấn CPU Intel AMD
- tư vấn mainboard
- tư vấn RAM
- chẩn đoán phần cứng

Yêu cầu:
- trả lời tiếng Việt
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

            # =========================
            # KIỂM TRA LỖI
            # =========================
            if "choices" in result:

                answer = result["choices"][0]["message"]["content"]

            else:

                answer = f"❌ OpenRouter lỗi:\n\n{result}"

            st.markdown(answer)

            # LƯU CHATBOT MESSAGE
            st.session_state.messages.append({

                "role": "assistant",

                "content": answer

            })

        except Exception as e:

            st.error(f"❌ Lỗi AI: {str(e)}")
