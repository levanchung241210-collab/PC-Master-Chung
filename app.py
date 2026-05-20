import streamlit as st
import streamlit.components.v1 as components
import json, re, os, random
from groq import Groq

st.set_page_config(page_title="PC Solving — LVC 10A4", page_icon="⚡", layout="centered")

# ══ INJECT DARK INPUT via components — bypasses Streamlit shadow DOM ══
components.html("""
<style>
  /* Target parent frames */
  body, html { background: #08090f !important; }
</style>
<script>
(function(){
  var DARK='#0b0e16', CREAM='#ece8e1', RED='#ff4655', TEAL='#00d4bf';
  var styleEl = document.createElement('style');
  styleEl.id = 'valo-fix';
  styleEl.textContent = `
    textarea { background:${DARK}!important; background-color:${DARK}!important; color:${CREAM}!important; -webkit-text-fill-color:${CREAM}!important; caret-color:${RED}!important; }
    [data-testid="stChatInput"] textarea { border-top:2px solid rgba(255,70,85,0.7)!important; }
  `;
  document.head.appendChild(styleEl);

  function fix(){
    // Walk up from current window to find parent Streamlit frame
    try {
      var topDoc = window.parent.document;
      if(topDoc && !topDoc.getElementById('valo-global-fix')){
        var s = topDoc.createElement('style');
        s.id = 'valo-global-fix';
        s.textContent = `
          div[data-testid="stAppViewContainer"] { background-color: #08090f !important; color: #ece8e1 !important; }
          div[data-testid="stHeader"] { background: transparent !important; }
          .stButton>button {
            background: #0b0e16 !important; border: 1px solid #333 !important; color: #ece8e1 !important;
            transition: all 0.2s ease-in-out;
          }
          .stButton>button:hover { border-color: #ff4655 !important; color: #ff4655 !important; box-shadow: 0 0 10px rgba(255,70,85,0.3); }
          div[data-testid="stChatMessage"] { background-color: #0b0e16 !important; border-left: 3px solid #333; margin-bottom: 10px; }
          div[data-testid="stChatMessage"]:has([data-testid="user-avatar"]) { border-left-color: #00d4bf !important; }
          div[data-testid="stChatMessage"]:has([data-testid="assistant-avatar"]) { border-left-color: #ff4655 !important; }
          div[data-testid="stChatInput"] { background: transparent !important; }
          
          /* Style cho khu vực Upload ảnh */
          div[data-testid="stExpander"] details { background-color: #0b0e16 !important; border: 1px solid #333 !important; border-radius: 0px !important; }
          div[data-testid="stExpander"] summary { color: #00d4bf !important; font-family: monospace; }
          div[data-testid="stFileUploader"] { background-color: #08090f !important; border: 1px dashed #ff4655 !important; padding: 10px !important; }
          div[data-testid="stFileUploader"] section { color: #ece8e1 !important; }
        `;
        topDoc.head.appendChild(s);
      }
    } catch(e){}
  }
  setInterval(fix, 1000); fix();
})();
</script>
""", height=0)

# Custom VALORANT CSS for UI
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Teko:wght@600&family=Playshare&display=swap');
    
    .valo-title {
        font-family: 'Teko', sans-serif;
        font-size: 55px;
        color: #ff4655;
        text-transform: uppercase;
        letter-spacing: 2px;
        line-height: 0.9;
        margin-bottom: 0px;
        text-shadow: 3px 3px 0px #00d4bf;
    }
    .valo-subtitle {
        font-family: monospace;
        font-size: 11px;
        color: #00d4bf;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-bottom: 30px;
        opacity: 0.8;
    }
    .suggestion-box {
        background: #0b0e16;
        border: 1px solid #1f2533;
        padding: 12px 15px;
        border-radius: 0px;
        cursor: pointer;
        transition: all 0.2s ease;
        margin-bottom: 10px;
        position: relative;
        overflow: hidden;
    }
    .suggestion-box:hover {
        border-color: #ff4655;
        background: #111622;
        transform: translateX(4px);
    }
    .suggestion-box::before {
        content: ''; position: absolute; left: 0; top: 0; height: 100%; width: 3px; background: #333;
    }
    .suggestion-box:hover::before { background: #ff4655; }
    .sug-title { color: #ff4655; font-weight: bold; font-size: 14px; text-transform: uppercase; font-family: monospace; }
    .sug-desc { color: #8f96a3; font-size: 12px; margin-top: 2px; }
</style>
""", unsafe_allowed_html=True)

# Initialize Groq Client
client = Groq(api_key=os.environ.get("GROQ_API_KEY", "gsk_xxxx"))

# Local Knowledge Database
DB = {
    "AOD": "Mã lỗi AOD thường xuất hiện trên các dòng bo mạch chủ ASUS (đặc biệt là dòng ROG/TUF) liên quan đến lỗi 'Driver không thể kích hoạt hoặc lỗi nhận diện thiết bị ngoại vi'. Khắc phục: 1. Cập nhật Chipset Driver mới nhất từ trang chủ ASUS. 2. Kiểm tra lại các thiết bị USB đang cắm, rút ra thử lại. 3. Nếu ép xung (OC) RAM/CPU, hãy đưa về mặc định (Clear CMOS).",
    "0x0000007B": "Mã lỗi màn hình xanh (BSOD) 'INACCESSIBLE_BOOT_DEVICE'. Nguyên nhân do Windows không thể đọc được phân vùng ổ cứng chứa hệ điều hành lúc khởi động. Khắc phục: Vào BIOS kiểm tra chế độ ổ cứng đang là AHCI hay RAID/SATA (chuyển đổi lại cho đúng lúc cài Win). Kiểm tra lại cáp kết nối SSD/HDD hoặc phân vùng boot bị lỗi, dùng USB cứu hộ nạp lại MBR/EFI.",
    "D6": "Mã lỗi Q-Code 'D6' trên Mainboard có nghĩa là 'No Console Output Devices are found' (Không tìm thấy thiết bị xuất hình ảnh). Khắc phục: 1. Kiểm tra lại card đồ họa (GPU) đã cắm chặt vào khe PCIe chưa, chân nguồn phụ đã cắm đủ chưa. 2. Lau sạch chân kim loại của card bằng gôm/tẩy. 3. Thử chuyển dây màn hình (HDMI/DP) sang cổng khác hoặc cắm trực tiếp vào Mainboard (nếu CPU có iGPU)."
}

# State Management
if "messages" not in st.session_state: st.session_state.messages = []
if "greeted" not in st.session_state: st.session_state.greeted = False
if "pending_query" not in st.session_state: st.session_state.pending_query = None

# Title UI
st.markdown('<h1 class="valo-title">PC SOLVING SYSTEMS</h1>', unsafe_allowed_html=True)
st.markdown('<div class="valo-subtitle">AGENT CONTROL // LVC UNIT — 10A4</div>', unsafe_allowed_html=True)

# Suggestions Grid (Ẩn đi nếu đã bắt đầu trò chuyện)
if not st.session_state.greeted and len(st.session_state.messages) == 0:
    st.markdown("<p style='font-family:monospace; color:#8f96a3; font-size:12px; letter-spacing:1px; margin-bottom:15px;'>CHỌN MÃ LỖI ĐỂ PHÂN TÍCH NHANH:</p>", unsafe_allowed_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔴 LỖI AOD (MAINBOARD ASUS)"): st.session_state.pending_query = "AOD"
        if st.button("🔵 MÀN HÌNH XANH 0x0000007B"): st.session_state.pending_query = "0x0000007B"
    with col2:
        if st.button("🟡 LỖI D6 (KHÔNG ĐÈN BÁO HÌNH)"): st.session_state.pending_query = "D6"
        if st.button("🔥 KIỂM TRA TỐI ƯU HÓA ATLASOS"): st.session_state.pending_query = "AtlasOS có an toàn và giúp tăng FPS khi chơi game không?"

# Render Chat History
for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

# 📸 KHU VỰC UPLOAD TÍCH HỢP NGAY TRÊN THANH CHAT (HỖ TRỢ PASTE TỪ PC)
with st.expander("📸 ĐÍNH KÈM HÌNH ẢNH (HỖ TRỢ DÁN/PASTE BẰNG CTRL+V)"):
    st.markdown("<p style='font-size:13px; color:#8f96a3;'>Click chuột vào ô viền đỏ bên dưới và nhấn <b>Ctrl + V</b> để dán ảnh lỗi/linh kiện.</p>", unsafe_allowed_html=True)
    img_file = st.file_uploader("", type=["png", "jpg", "jpeg"], label_visibility="collapsed")
    if img_file:
        st.success("⚡ Ảnh đã sẵn sàng! Gõ thêm mô tả vào thanh chat bên dưới và nhấn Gửi.")

def search_db(q):
    q_clean = q.strip().upper()
    for k in DB:
        if k in q_clean or q_clean in k: return DB[k]
    return None

def ask(p, history):
    max_tok = 1200
    sys_msg = (
        "Bạn là một chuyên gia sửa chữa máy tính, phần cứng và tối ưu hóa hệ điều hành chuyên sâu. "
        "Nhiệm vụ của bạn là phân tích mã lỗi phần cứng (Mainboard Q-Code, Beep Code), lỗi màn hình xanh (BSOD), "
        "lỗi hệ điều hành Windows, và tư vấn nâng cấp linh kiện (CPU, GPU, RAM) một cách chính xác, chi tiết, logic. "
        "Hãy trình bày câu trả lời rõ ràng, có phân mục (Nguyên nhân, Cách khắc phục từng bước). "
        "Ngôn ngữ: Tiếng Việt."
    )
    
    msgs = [{"role": "system", "content": sys_msg}]
    for m in history[-6:]:
        msgs.append({"role": m["role"], "content": m["content"]})
        
    r = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=msgs,
        max_tokens=max_tok,
        temperature=0.45 
    )
    return r.choices[0].message.content

def handle(p):
    st.session_state.messages.append({"role":"user","content":p})
    with st.chat_message("user"): st.markdown(p)
    with st.chat_message("assistant"):
        with st.spinner("ĐANG PHÂN TÍCH DỮ LIỆU..."):
            try:
                a = search_db(p) or ask(p, st.session_state.messages)
                st.markdown(a)
                st.session_state.messages.append({"role":"assistant","content":a})
            except Exception as e:
                st.error(f"❌ {str(e)}")

# Process logic input
if st.session_state.pending_query:
    q=st.session_state.pending_query; st.session_state.pending_query=None; handle(q)
if p:=st.chat_input("Nhập mã lỗi hoặc linh kiện cần phân tích..."):
    st.session_state.greeted=True; handle(p)
