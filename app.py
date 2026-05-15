import streamlit as st
import google.generativeai as genai

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Siêu Chuyên Gia PC - Chung 10A4",
    page_icon="🖥️",
    layout="centered"
)

# =========================
# LOAD API KEY
# =========================
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]

    genai.configure(api_key=API_KEY)

except Exception as e:
    st.error("❌ Chưa cấu hình API Key trong Streamlit Secrets!")
    st.exception(e)
    st.stop()

# =========================
# LOAD MODEL
# =========================
try:
    model = genai.GenerativeModel("gemini-2.0-flash")
except:
    model = genai.GenerativeModel("gemini-1.5-flash-latest")

# =========================
# SYSTEM PROMPT
# =========================
SYSTEM_PROMPT = """
Bạn là chuyên gia máy tính của Lê Văn Chung lớp 10A4.

Nhiệm vụ:
1. Giải mã lỗi Windows.
2. Hướng dẫn sửa lỗi Win 10/11.
3. Giải thích CPU Intel.
4. Tư vấn Mainboard tương thích.
5. Chẩn đoán lỗi phần cứng.
6. Giải thích lỗi màn hình xanh (BSOD).
7. Giải thích tiếng beep BIOS.

Yêu cầu:
- Trả lời bằng tiếng Việt.
- Có bước 1, 2, 3 rõ ràng.
- Dễ hiểu.
- Không lan man.
"""

# =========================
# UI
# =========================
st.title("🖥️ Chatbot Giải Lỗi Windows & Linh Kiện")

st.markdown("### Sản phẩm STEM: Lê Văn Chung - Lớp 10A4")

with st.expander("ℹ️ Giới thiệu"):
    st.write(
        "AI hỗ trợ giải mã lỗi Windows, BSOD, CPU Intel, Mainboard, RAM và phần cứng máy tính."
    )

# =========================
# FIX SESSION STATE
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================
# HIỂN THỊ LỊCH SỬ CHAT
# =========================
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# =========================
# INPUT
# =========================
prompt = st.chat_input("Nhập mã lỗi hoặc mô tả tình trạng máy tính...")

# =========================
# USER SEND MESSAGE
# =========================
if prompt:

    # Chống spam prompt quá dài
    if len(prompt) > 1000:
        st.warning("⚠️ Câu hỏi quá dài!")
        st.stop()

    # Lưu tin nhắn user
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # Hiển thị user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant trả lời
    with st.chat_message("assistant"):

        try:

            # Tạo history cho AI nhớ hội thoại
            history = []

            for msg in st.session_state.messages[:-1]:

                role = "model" if msg["role"] == "assistant" else "user"

                history.append({
                    "role": role,
                    "parts": [msg["content"]]
                })

            chat = model.start_chat(history=history)

            full_prompt = f"""
{SYSTEM_PROMPT}

Người dùng hỏi:
{prompt}
"""

            response = chat.send_message(
                full_prompt,
                generation_config={
                    "temperature": 0.7,
                    "max_output_tokens": 1024,
                }
            )

            answer = response.text

            # Hiển thị câu trả lời
            st.markdown(answer)

            # Lưu assistant message
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

        except Exception as e:

            st.error("❌ AI đang gặp lỗi!")
            st.exception(e)
