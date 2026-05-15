import streamlit as st
import google.generativeai as genai
import time

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Chatbot Giải Lỗi PC - Chung 10A4",
    page_icon="🖥️",
    layout="centered"
)

# =========================
# LOAD API KEY
# =========================
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]

    genai.configure(api_key=API_KEY)

except Exception:
    st.error(
        "❌ Chưa cấu hình GEMINI_API_KEY trong Streamlit Secrets!"
    )
    st.stop()

# =========================
# MODEL
# =========================
MODEL_NAME = "models/gemini-1.5-flash-latest"

try:
    model = genai.GenerativeModel(MODEL_NAME)

except Exception as e:
    st.error(f"❌ Không thể khởi tạo model: {MODEL_NAME}")
    st.exception(e)
    st.stop()

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
6. Giải thích màn hình xanh (BSOD).
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
st.title("🖥️ Chatbot Giải Lỗi PC - Chung 10A4")

st.markdown("### Sản phẩm STEM")

st.markdown("---")

with st.expander("ℹ️ Giới thiệu"):
    st.write(
        "AI hỗ trợ giải mã lỗi Windows, BSOD, CPU Intel, Mainboard, RAM và phần cứng máy tính."
    )

# =========================
# SESSION STATE
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================
# HIỂN THỊ CHAT CŨ
# =========================
for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# =========================
# INPUT
# =========================
prompt = st.chat_input(
    "Nhập mã lỗi Windows hoặc câu hỏi về PC..."
)

# =========================
# USER SEND MESSAGE
# =========================
if prompt:

    # Chống spam prompt quá dài
    if len(prompt) > 1000:

        st.warning("⚠️ Câu hỏi quá dài!")

        st.stop()

    # Lưu user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # Hiển thị user message
    with st.chat_message("user"):

        st.markdown(prompt)

    # Assistant message
    with st.chat_message("assistant"):

        try:

            # Chống spam request
            time.sleep(1)

            # Gửi prompt cho Gemini
            response = model.generate_content(

                f"""
{SYSTEM_PROMPT}

Người dùng hỏi:
{prompt}
""",

                generation_config={

                    "temperature": 0.7,

                    "max_output_tokens": 512

                }

            )

            # Lấy text
            answer = response.text

            # Hiển thị
            st.markdown(answer)

            # Lưu history
            st.session_state.messages.append({

                "role": "assistant",

                "content": answer

            })

        except Exception as e:

            err = str(e)

            # 429 = quota exceeded
            if "429" in err:

                st.warning(
                    "⚠️ Gemini đang giới hạn request hoặc hết quota free.\n\n"
                    "Đợi khoảng 15-30 giây rồi thử lại."
                )

            # 404 = model not found
            elif "404" in err:

                st.error(
                    "❌ Model không tồn tại hoặc chưa được hỗ trợ."
                )

            else:

                st.error(f"❌ Lỗi AI: {err}")
