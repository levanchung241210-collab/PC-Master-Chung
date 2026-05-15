import streamlit as st
import google.generativeai as genai
import time

# 1. Cấu hình bảo mật qua st.secrets (Bắt buộc để không bị chặn Key)
try:
    # Tài liệu khuyến nghị dùng GEMINI_API_KEY lưu trong Secrets
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception:
    st.error("❌ Chưa cấu hình API Key trong Secrets! Chung hãy dán Key vào Settings -> Secrets.")
    st.stop()

# 2. Xác minh tên mô hình khả dụng (Dùng Gemini 2.0 theo tài liệu mới)
# Tài liệu khuyên dùng gemini-2.0-flash để ổn định và tránh lỗi 404 của bản 1.5 cũ
MODEL_NAME = "gemini-2.0-flash" 

try:
    model = genai.GenerativeModel(MODEL_NAME)
except Exception as e:
    st.error(f"❌ Không thể khởi tạo model {MODEL_NAME}. Lỗi: {str(e)}")
    st.stop()

# 3. Giao diện sản phẩm STEM - Lê Văn Chung 10A4
st.set_page_config(page_title="Chuyên Gia PC Chung 10A4", page_icon="🖥️")
st.title("🖥️ Chatbot Giải Lỗi PC - Chung 10A4")
st.markdown("---")

# Khởi tạo lịch sử chat trong st.session_state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Hiển thị hội thoại cũ
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Xử lý câu hỏi và chống lỗi 429 (Quota Exceeded)
if prompt := st.chat_input("Hỏi về mã lỗi Windows, CPU, Mainboard..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Tài liệu khuyên: Chèn tạm nghỉ và giới hạn token để tiết kiệm quota
            time.sleep(0.5) 
            
            # Cấu hình generation_config để tránh câu trả lời quá dài gây tốn token
            gen_config = {"max_output_tokens": 800, "temperature": 0.7}
            
            instruction = "Bạn là chuyên gia PC của Lê Văn Chung 10A4. Trả lời ngắn gọn, chia bước 1 2 3."
            response = model.generate_content(
                f"{instruction}\n\nCâu hỏi: {prompt}",
                generation_config=gen_config
            )
            
            answer = response.text
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
            
        except Exception as e:
            err = str(e)
            # Phân loại lỗi theo tài liệu hướng dẫn
            if "429" in err:
                st.warning("⚠️ Đã hết hạn mức (2 câu/phút). Chung chờ 30-60 giây rồi thử lại nhé!")
            elif "404" in err:
                st.error("❌ Lỗi 404: Tên model có thể đã thay đổi hoặc không tồn tại.")
            else:
                st.error(f"❌ Lỗi: {err}")
