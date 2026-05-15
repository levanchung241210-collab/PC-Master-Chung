import streamlit as st
import google.generativeai as genai

# 1. Cấu hình AI (Dùng mã API bạn đã lấy)
API_KEY = "AIzaSyDRidtFgdsWXD7e7ybjah3ml-gqp0WweMo" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. Giao diện trang web
st.set_page_config(page_title="Chatbot Giải Lỗi PC", page_icon="🖥️")
st.title("🖥️ Chatbot Hướng Dẫn Giải Lỗi Máy Tính")
st.subheader("Sản phẩm STEM: Lê Văn Chung - Lớp 10A4")
st.markdown("---")

# 3. Xử lý tin nhắn
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Máy tính bạn đang bị lỗi gì?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        instruction = f"Bạn là 'Chatbot Hướng Dẫn Giải Lỗi Máy Tính' của Lê Văn Chung 10A4. Hãy tư vấn cách sửa lỗi máy tính chuyên sâu, ngắn gọn cho câu hỏi: {prompt}"
        response = model.generate_content(instruction)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})