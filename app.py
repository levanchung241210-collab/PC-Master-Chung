import streamlit as st
import anthropic

st.set_page_config(
    page_title="Chatbot Giải Lỗi PC - Chung 10A4",
    page_icon="🖥️"
)

try:
    API_KEY = st.secrets["ANTHROPIC_API_KEY"]
    client = anthropic.Anthropic(api_key=API_KEY)
except KeyError:
    st.error("❌ Chưa cấu hình ANTHROPIC_API_KEY trong Secrets!")
    st.stop()
except Exception as e:
    st.error(f"❌ Lỗi: {str(e)}")
    st.stop()

st.title("🖥️ Chatbot Giải Lỗi PC")
st.markdown("**Sản phẩm STEM - Lê Văn Chung 10A4**")
st.markdown("---")

SYSTEM_PROMPT = """Bạn là chuyên gia sửa chữa và tư vấn PC chuyên nghiệp.
Nhiệm vụ của bạn:
- Giải thích các mã lỗi Windows (BSOD, Error Code...)
- Chẩn đoán lỗi phần cứng (CPU, RAM, GPU, ổ cứng, nguồn...)
- Tư vấn linh kiện PC (thông số, so sánh, tương thích)
- Hướng dẫn sửa lỗi step-by-step

Quy tắc trả lời:
- Luôn dùng tiếng Việt
- Chia thành các bước đánh số rõ ràng (Bước 1, Bước 2...)
- Ngắn gọn, dễ hiểu cho học sinh
- Nếu là mã lỗi, giải thích nguyên nhân trước rồi mới đưa cách fix
- Kết thúc bằng lời khuyên phòng tránh nếu có thể"""

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if not st.session_state.messages:
    st.markdown("**💡 Bạn có thể hỏi ví dụ:**")
    cols = st.columns(2)
    with cols[0]:
        st.code("Lỗi 0x0000007B là gì?")
        st.code("RAM 8GB có đủ không?")
    with cols[1]:
        st.code("PC bị màn hình xanh chết")
        st.code("So sánh GTX 1650 vs RX 6500")

prompt = st.chat_input("Nhập mã lỗi hoặc câu hỏi về PC...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🔍 Đang phân tích..."):
            try:
                response = client.messages.create(
                    model="claude-haiku-4-5-20251001",
                    max_tokens=1024,
                    system=SYSTEM_PROMPT,
                    messages=st.session_state.messages
                )
                answer = response.content[0].text
                st.markdown(answer)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })
            except Exception as e:
                st.error(f"❌ Lỗi AI: {str(e)}")

with st.sidebar:
    st.markdown("### ℹ️ Hướng dẫn")
    st.markdown("""
- Nhập **mã lỗi** (VD: 0x00000050)
- Mô tả **triệu chứng** PC
- Hỏi về **linh kiện** bất kỳ
""")
    st.markdown("---")
    if st.button("🗑️ Xóa lịch sử chat"):
        st.session_state.messages = []
        st.rerun()
    st.markdown("---")
    st.caption("Made by Lê Văn Chung 10A4 🎓")
