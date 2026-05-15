import streamlit as st
import google.generativeai as genai

# 1. Bảo mật API Key
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception:
    st.error("❌ Chung chưa dán Key vào Settings -> Secrets rồi!")
    st.stop()

# 2. Cơ chế CHỐNG LỖI 404 (Thử lần lượt các model)
@st.cache_resource
def load_model():
    # Thử danh sách các model từ mới đến cũ
    for model_name in ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro"]:
        try:
            m = genai.GenerativeModel(model_name)
            # Chạy thử một câu lệnh nhỏ để kiểm tra model có sống không
            m.generate_content("test") 
            return m
        except:
            continue
    return None

model = load_model()

if model is None:
    st.error("❌ Google đang chặn API này hoặc Key của bạn bị sai. Hãy tạo Key mới tại Google AI Studio!")
    st.stop()

# 3. Giao diện
st.title("🖥️ Chatbot PC Chung 10A4")
st.markdown("---")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Hỏi Chung về máy tính..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Gửi kèm hướng dẫn để AI đóng vai chuyên gia
            full_prompt = f"Bạn là chuyên gia máy tính của Lê Văn Chung 10A4. Hãy trả lời câu này: {prompt}"
            response = model.generate_content(full_prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"⚠️ Lỗi kết nối: {str(e)}. Chung hãy thử Reboot App nhé!")
