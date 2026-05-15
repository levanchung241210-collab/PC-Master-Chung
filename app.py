import streamlit as st
import google.generativeai as genai
import time

st.set_page_config(page_title="Chuyên Gia PC Chung 10A4", page_icon="🖥️")

try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception:
    st.error("❌ Chưa cấu hình API Key trong Secrets!")
    st.stop()

MODEL_NAME = "gemini-2.0-flash"

if "messages" not in st.session_state:
    st.session_state.messages = []

try:
    model = genai.GenerativeModel(MODEL_NAME)
except Exception as e:
    st.error(f"❌ Không khởi tạo được model {MODEL_NAME}.")
    st.exception(e)
    st.stop()

st.title("🖥️ Chatbot Giải Lỗi PC - Chung 10A4")
st.markdown("---")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Hỏi về mã lỗi Windows, CPU, Mainboard..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        instruction = (
            "Bạn là chuyên gia máy tính của Lê Văn Chung lớp 10A4. "
            "Trả lời ngắn gọn, chia bước 1, 2, 3."
        )

        try:
            response = model.generate_content(
                f"{instruction}\n\nCâu hỏi: {prompt}",
                generation_config={"max_output_tokens": 800, "temperature": 0.7}
            )
            answer = response.text
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

        except Exception as e:
            err = str(e)
            if "429" in err:
                st.warning("⚠️ Hết quota hoặc bị giới hạn tần suất. Thử lại sau ít giây.")
            elif "404" in err:
                st.error("❌ Model không tồn tại hoặc chưa được hỗ trợ trong project này.")
            else:
                st.error(f"❌ Lỗi AI: {err}")
