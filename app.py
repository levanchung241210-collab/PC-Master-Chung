import streamlit as st
# DISPLAY MESSAGES
# =========================
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# =========================
# CHAT INPUT
# =========================
prompt = st.chat_input("Nhập mã lỗi hoặc mô tả tình trạng máy tính...")

if prompt:

    # Giới hạn độ dài prompt
    if len(prompt) > 1000:
        st.warning("⚠️ Câu hỏi quá dài!")
        st.stop()

    # Lưu user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant response
    with st.chat_message("assistant"):

        try:

            # Tạo lịch sử hội thoại
            history = []

            for msg in st.session_state.messages[:-1]:
                role = "model" if msg["role"] == "assistant" else "user"

                history.append({
                    "role": role,
                    "parts": [msg["content"]]
                })

            chat = model.start_chat(history=history)

            full_prompt = f"""
{SYSTEM_PROMPT}

Người dùng hỏi:
{prompt}
"""

            response = chat.send_message(
                full_prompt,
                generation_config={
                    "temperature": 0.7,
                    "max_output_tokens": 1024,
                }
            )

            answer = response.text

            st.markdown(answer)

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

        except Exception as e:

            st.error("❌ AI đang gặp lỗi!")
            st.exception(e)
