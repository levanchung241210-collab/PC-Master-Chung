import streamlit as st
import google.generativeai as genai

# 1. Cấu hình bảo mật qua st.secrets
# Đảm bảo bạn đã dán GEMINI_API_KEY vào mục Settings -> Secrets trên Streamlit Cloud
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception:
    st.error("❌ Chưa cấu hình API Key trong Secrets!")
    st.stop()

# 2. Khởi tạo Model
# Dùng "gemini-1.5-flash-latest" để có hạn mức (quota) tốt nhất cho bản miễn phí
try:
    model = genai.GenerativeModel("gemini-1.5-flash-latest")
except Exception as e:
    st.error(f"❌ Lỗi khởi tạo Model: {str(e)}")
    st.stop()

# 3. Giao diện sản phẩm STEM - Lê Văn Chung 10A4
st.set_page_config(page_title="Chatbot PC Chung 10A4", page_icon="🖥️")
st.title("🖥️ Chatbot Giải Lỗi PC - Chung 10A4")
st.markdown("### Sản phẩm STEM")
st.markdown("---")

# Khởi tạo lịch sử chat (session_state)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Hiển thị các tin nhắn đã có trong lịch sử
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Xử lý câu hỏi từ người dùng
if prompt := st.chat_input("Nhập câu hỏi (ví dụ: i5-6500 thông số thế nào?)..."):
    # Lưu và hiển thị câu hỏi của người dùng
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Phản hồi từ AI
    with st.chat_message("assistant"):
        # System instruction: Giúp AI trả lời đúng vai chuyên gia của Chung
        instruction = "Bạn là chuyên gia máy tính của Lê Văn Chung lớp 10A4. Trả lời ngắn gọn, có bước 1, 2, 3."
        
        try:
            # Gọi API với cấu hình tối ưu
            response = model.generate_content(
                f"{instruction}\n\nCâu hỏi: {prompt}",
                generation_config={"temperature": 0.7, "max_output_tokens": 1000}
            )
            
            answer = response.text
            st.markdown(answer)
            
            # Lưu câu trả lời vào lịch sử
            st.session_state.messages.append({"role": "assistant", "content": answer})
            
        except Exception as e:
            # Xử lý các lỗi phổ biến dựa trên tài liệu bạn gửi
            err_msg = str(e)
            if "429" in err_msg:
                st.warning("⚠️ AI đang bận (hết lượt dùng tạm thời). Chung chờ 10 giây rồi nhấn gửi lại nhé!")
            elif "404" in err_msg:
                st.error("❌ Lỗi cấu hình Model (404). Hãy kiểm tra lại tên model trong code.")
            else:
                st.error(f"❌ Lỗi kết nối AI: {err_msg}")
