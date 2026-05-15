import streamlit as st
import google.generativeai as genai

# Cấu hình bảo mật
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception:
    st.error("Chưa cấu hình Key trong Secrets!")
    st.stop()

# FIX LỖI 404: Dùng bản -latest và viết thường hoàn toàn
model = genai.GenerativeModel("gemini-1.5-flash-latest")

st.title("🖥️ Chatbot Giải Lỗi PC - Chung 10A4")
st.markdown("### Sản phẩm STEM")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Nhập câu hỏi..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Chỉ thị hệ thống để AI đóng vai chuyên gia
        instruction = "Bạn là chuyên gia máy tính của Lê Văn Chung lớp 10A4. Trả lời ngắn gọn, có bước 1, 2, 3."
        try:
            # FIX LỖI 404: Gửi kèm prompt của người dùng
            response = model.generate_content(f"{instruction}\n\nCâu hỏi: {prompt}")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Lỗi AI: {str(e)}")
