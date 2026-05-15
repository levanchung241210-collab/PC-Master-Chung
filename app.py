import streamlit as st
import google.generativeai as genai

# 1. Cấu hình bảo mật qua st.secrets (Không dán key trực tiếp vào đây)
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception:
    st.error("❌ Chưa cấu hình API Key trong Streamlit Secrets! Chung hãy vào Settings -> Secrets để dán key nhé.")
    st.stop()

# 2. Khởi tạo Model (Dùng bản -latest để có hạn mức cao nhất và tránh lỗi 404)
# Theo tài liệu: gemini-1.5-flash-latest là bản ổn định nhất cho Free tier
model = genai.GenerativeModel("gemini-1.5-flash-latest")

# 3. Giao diện sản phẩm STEM của Lê Văn Chung 10A4
st.set_page_config(page_title="Chuyên Gia PC Chung 10A4", page_icon="🖥️")
st.title("🖥️ Chatbot Giải Lỗi PC - Chung 10A4")
st.markdown("---")

# Khởi tạo lịch sử chat trong st.session_state (Bắt buộc theo tài liệu Streamlit)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Hiển thị các tin nhắn cũ
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Xử lý câu hỏi từ người dùng
if prompt := st.chat_input("Nhập mã lỗi hoặc hỏi về linh kiện..."):
    # Lưu tin nhắn của người dùng
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Chỉ thị hệ thống (System Prompt) để AI đóng vai chuyên gia
        instruction = (
            "Bạn là chuyên gia máy tính của Lê Văn Chung lớp 10A4.\n"
            "Nhiệm vụ: Giải mã lỗi Windows (màn hình xanh, mã lỗi), tư vấn chọn CPU/Mainboard.\n"
            "Yêu cầu: Trả lời ngắn gọn, rành mạch, chia các bước 1, 2, 3."
        )
        
        try:
            # Gửi yêu cầu tới AI với giới hạn output để tiết kiệm token
            response = model.generate_content(
                f"{instruction}\n\nCâu hỏi: {prompt}",
                generation_config={"temperature": 0.7, "max_output_tokens": 800}
            )
            
            answer = response.text
            st.markdown(answer)
            # Lưu câu trả lời của AI vào lịch sử
            st.session_state.messages.append({"role": "assistant", "content": answer})
            
        except Exception as e:
            # Xử lý các lỗi phổ biến (429 - Hết quota, 404 - Sai model)
            error_msg = str(e)
            if "429" in error_msg:
                st.warning("⚠️ Hệ thống đang bận do quá nhiều yêu cầu. Chung chờ khoảng 10 giây rồi thử lại nhé!")
            elif "404" in error_msg:
                st.error("❌ Lỗi cấu hình Model (404). Hãy đảm bảo tên model là 'gemini-1.5-flash-latest'.")
            else:
                st.error(f"❌ Lỗi AI: {error_msg}")
