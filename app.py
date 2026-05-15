import streamlit as st
import google.generativeai as genai

# 1. Cấu hình AI (Mã API của Chung)
API_KEY = "AIzaSyDRidtFgdsWXD7e7ybjah3ml-gqp0WweMo" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. Giao diện Chuyên gia
st.set_page_config(page_title="Chuyên Gia PC Chung 10A4", page_icon="🖥️")
st.title("🖥️ Chatbot Hướng Dẫn Giải Lỗi & Tư Vấn Linh Kiện")
st.subheader("Sản phẩm STEM: Lê Văn Chung - Lớp 10A4")
st.markdown("---")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Nhập mã lỗi Windows hoặc hỏi về linh kiện..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Chỉ thị siêu cấp cho AI
        instruction = (
            f"Bạn là chuyên gia máy tính của Lê Văn Chung 10A4. Nhiệm vụ của bạn:\n"
            f"1. Giải mã chính xác các mã lỗi Windows (ví dụ: 0x800..., 0xc00...) từ Win 10 trở lên.\n"
            f"2. Chẩn đoán lỗi linh kiện dựa trên mô tả (màn hình xanh, tiếng kêu tít tít, máy treo).\n"
            f"3. Tư vấn chuyên sâu về Intel (i3, i5, i7, i9 các đời), hậu tố K/F/Gen và mainboard tương thích.\n"
            f"Trả lời ngắn gọn, có danh sách các bước 1, 2, 3 rõ ràng. Câu hỏi: {prompt}"
        )
        response = model.generate_content(instruction)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
