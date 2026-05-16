import streamlit as st
import json
import re
import os

# CONFIG GIAO DIỆN CYBERPUNK CHUYÊN NGHIỆP
st.set_page_config(page_title="Vua PC Chatbot - Lê Văn Chung 10A4", page_icon="🖥️", layout="wide")

st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #020617, #0f172a, #1e1b4b); color: #f8fafc; }
.neon-title { text-align: center; font-size: 42px !important; font-weight: 900 !important; color: #ffffff; text-shadow: 0 0 10px #3b82f6, 0 0 30px #1d4ed8; }
.neon-subtitle { text-align: center; color: #38bdf8; font-size: 18px !important; font-weight: 500; }
[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) { background: linear-gradient(135deg, #1d4ed8, #1e40af); border-radius: 16px; border-left: 5px solid #60a5fa; }
[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-assistant"]) { background: rgba(15, 23, 42, 0.8); border-radius: 16px; border: 1px solid #334155; border-left: 5px solid #3b82f6; }
.stChatInput input { background-color: #0f172a !important; color: #ffffff !important; border: 2px solid #3b82f6 !important; }
section[data-testid="stSidebar"] { background-color: #020617; border-right: 1px solid #1e293b; }
</style>
""", unsafe_allow_html=True)

# LOAD DATABASE JSON
def load_database():
    if os.path.exists("database_pc.json"):
        with open("database_pc.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {"loi_he_thong": [], "linh_kien_pc": []}

data_pc = load_database()

# SIDEBAR CONTROL PANEL
with st.sidebar:
    st.markdown("<h2 style='color: #3b82f6; text-align: center;'>🖥️ Control Panel</h2>", unsafe_allow_html=True)
    st.success("⚡ HỆ THỐNG: MẠNG CHUYÊN GIA ĐA LUỒNG")
    st.markdown("---")
    st.write("📊 **Trạng thái Engine:**")
    st.info("✔️ Thuật toán Quét cụm từ (Substring Engine)")
    st.info("✔️ Tự động bắt bài từ viết tắt & Từ lóng")
    st.info("✔️ Tách biệt luồng Linh kiện / Mã lỗi hoàn toàn")
    st.markdown("---")
    st.warning("🤖 Phiên bản: Vua PC AI Engine v7.0")
    st.info("👨‍💻 Tác giả dự án STEM:\n\n**Lê Văn Chung - Lớp 10A4**")

st.markdown('<div class="neon-title">👑 VUA PC - CHATBOT HỆ CHUYÊN GIA NÂNG CAO</div>', unsafe_allow_html=True)
st.markdown('<div class="neon-subtitle">BỘ LÕI ĐA TẦNG PHÁT TRIỂN BỞI: LÊ VĂN CHUNG - LỚP 10A4</div>', unsafe_allow_html=True)
st.markdown("---")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

# ==========================================
# THUẬT TOÁN QUÉT TỪ KHÓA CHỨA (SUBSTRING MATCHING ENGINE)
# ==========================================
def engine_vua_pc(user_query):
    # 1. TIỀN XỬ LÝ CHUẨN HÓA CHUỖI VÀ CHỮ THƯỜNG
    q_clean = user_query.lower().strip()
    
    # Xử lý lời chào bách phát bách trúng
    if any(w in q_clean for w in ["hi", "hello", "chào", "xin chào", "alo"]):
        return ("👋 **Xin chào! Tôi là Vua PC - Hệ chuyên gia sửa chữa máy tính thế hệ v7.0 của Lê Văn Chung 10A4.**\n\n"
                "Tôi đã sửa toàn bộ lỗi nhận diện sai từ khóa. Bây giờ bạn cần tôi xử lý pan bệnh máy tính hay phân tích thông số thiết bị nào?")

    # 2. PHÂN LUỒNG Ý ĐỊNH BẰNG TỪ KHÓA ĐẶC TRƯNG
    hardware_signals = ["chạy", "được", "không", "ko", "so", "sánh", "mạnh", "hơn", "max", "hiệu", "năng", "tư", "vấn", "thông", "số", "cấu", "hình", "main", "chip", "cpu", "vga", "card", "ram", "buss", "bus"]
    
    # Kiểm tra xem câu hỏi có chứa tên linh kiện cụ thể (Dùng Regex để bắt các ký tự định danh phần cứng)
    has_hardware_name = any(re.search(r'(i3|i5|i7|i9|ryzen|gtx|rtx|rx|dimensity|snapdragon|h110|b660|h610)', q_clean) for w in q_clean.split())
    
    is_asking_hardware = has_hardware_name or any(sig in q_clean for sig in hardware_signals)

    # 3. TIỀN XỬ LÝ TỪ LÓNG CHO PHẦN BÁO LỖI (CHỈ CHẠY NẾU KHÔNG PHẢI LUỒNG LINH KIỆN)
    if not is_asking_hardware:
        if "xanh màn" in q_clean or "màn hình xanh" in q_clean or "màn xanh" in q_clean or "máy xanh" in q_clean:
            q_clean += " xanh bsod memory management"
        if "sập nguồn" in q_clean or "máy sập" in q_clean or "tắt nguồn" in q_clean or "chạy sập" in q_clean:
            q_clean += " sập nguồn quá nhiệt tắt"

    # 4. TIỀN HÀNH CHẤM ĐIỂM (ĐẾM SỐ TỪ TRÙNG KHỚP TRONG MẢNG KEYWORDS CỦA FILE JSON)
    best_match = None
    max_score = 0
    match_type = ""

    # Chọn kho dữ liệu ưu tiên dựa trên phân luồng ý định ban đầu
    if is_asking_hardware:
        # Ưu tiên quét kho linh kiện trước
        for item in data_pc.get("linh_kien_pc", []):
            score = sum(1 for kw in item["keywords"] if kw in q_clean)
            if score > max_score:
                max_score = score
                best_match = item
                match_type = "linh_kien"
    else:
        # Ưu tiên quét kho lỗi trước
        for item in data_pc.get("loi_he_thong", []):
            score = sum(1 for kw in item["keywords"] if kw in q_clean)
            if score > max_score:
                max_score = score
                best_match = item
                match_type = "loi"

    # 5. XỬ LÝ TRẢ LỜI VÀ PHÂN LUỒNG TỪ CHỐI THÔNG MINH
    if max_score >= 1 and best_match:
        if match_type == "loi":
            response = f"### 🎯 Phân tích phát hiện lỗi: {best_match['ten']}\n"
            response += f"⚠️ **Phân loại:** `{best_match['loai']}`\n\n"
            response += f"❌ **Nguyên nhân cốt lõi:** {best_match['nguyen_nhan']}\n\n"
            response += f"🛠️ **Phác đồ khắc phục chuyên sâu:**\n{best_match['giai_phap']}\n"
            response += f"*(Độ chính xác: {max_score} điểm từ khóa)*"
            return response
        elif match_type == "linh_kien":
            response = f"### 📦 Thông tin linh kiện: {best_match['ten']}\n"
            response += f"⚙️ **Thông số kỹ thuật:** {best_match['thong_so']}\n\n"
            response += f"💡 **Tư vấn cấu hình từ Chung 10A4:** *{best_match['chuyen_gia_tu_van']}*\n"
            response += f"*(Độ chính xác: {max_score} điểm từ khóa)*"
            return response

    # 6. TẦNG TỪ CHỐI TRÚNG ĐÍCH
    if is_asking_hardware:
        return (f"🤖 **Vua PC phản hồi:** Hệ thống nhận diện bạn đang hỏi về thông số phần cứng hoặc tư vấn linh kiện.\n\n"
                f"⚠️ Tuy nhiên, linh kiện này hiện **chưa được nạp** vào danh mục `linh_kien_pc` trong file `database_pc.json`.\n"
                f"💡 *Mẹo cho Chung: Hãy mở file JSON ra, tạo một khối mới và thêm tên linh kiện này vào mảng `keywords` nhé!*")
    else:
        return (f"🤖 **Vua PC phản hồi:** Hệ thống chưa tìm thấy pan bệnh nào khớp với mô tả lỗi của bạn trong cơ sở dữ liệu cục bộ.\n\n"
                f"💡 *Mẹo: Hãy bổ sung kịch bản xử lý hiện tượng này vào danh mục `loi_he_thong` trong file `database_pc.json`.*")

# THỰC THI NHẬP LIỆU CHAT
if prompt := st.chat_input("Mô tả lỗi máy tính hoặc linh kiện bạn cần chẩn đoán tại đây..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("💾 Bộ não ma trận đang phân tích tầng sâu dữ liệu..."):
            answer = engine_vua_pc(prompt)
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
