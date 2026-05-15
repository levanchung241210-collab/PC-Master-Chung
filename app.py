import streamlit as st
import google.generativeai as genai

# 1. Cấu hình AI (Mã API của Chung)
API_KEY = "AIzaSyDRidtFgdsWXD7e7ybjah3ml-gqp0WweMo" 
genai.configure(api_key=API_KEY)

# Sử dụng tên model chuẩn để tránh lỗi NotFound
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. Giao diện Chuyên gia PC
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
        # Chỉ thị giúp AI trở thành siêu chuyên gia
        instruction = (
            f"Bạn là chuyên gia máy tính của Lê Văn Chung 10A4. Nhiệm vụ của bạn:\n"
            f"1. Giải mã các mã lỗi Windows (ví dụ: 0x800..., BSOD) cho Win 10 trở lên.\n"
            f"2. Chẩn đoán lỗi linh kiện dựa trên mô tả người dùng.\n"
            f"3. Tư vấn chuyên sâu về linh kiện (CPU Intel i3/i5/i7, Mainboard, RAM).\n"
            f"Ví dụ: i5-6500 là đời 6 Skylake, socket LGA 1151, đi với main H110/B150.\n"
            f"Trả lời bằng tiếng Việt, chia các bước 1, 2, 3 rõ ràng. Câu hỏi: {prompt}"
        )
        try:
            response = model.generate_content(instruction)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Lỗi kết nối AI: {e}. Chung hãy kiểm tra lại API Key nhé!")
