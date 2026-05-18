import streamlit as st
import json, re, os, random
from groq import Groq

st.set_page_config(page_title="PC Solving System — Lê Văn Chung 10A4", page_icon="⚡", layout="centered")

# ====================== CSS VALORANT NÂNG CẤP MẠNH ======================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Barlow+Condensed:wght@400;600;700;800&family=Barlow:wght@300;400;500;600&display=swap');

:root {
    --R: #ff4655; --R2: #ff7080; --R3: rgba(255,70,85,0.25);
    --T: #00d4bf; --T2: #00ffe7; --T3: rgba(0,212,191,0.22);
    --G: #e8c97a;
    --bg: #090b11; --p1: #0f1320; --p2: #151929; --p3: #1c2236;
    --W: #ffffff; --C: #ece8e1; --S: #b8b4ac;
}

html, body, .stApp { background:var(--bg) !important; color:var(--C) !important; font-family:'Barlow',sans-serif !important; }

/* Background Tactical đậm & thu hút hơn */
.stApp::before {
    content:''; position:fixed; inset:0; pointer-events:none; z-index:0;
    background:
        linear-gradient(135deg, rgba(255,70,85,0.16) 0%, transparent 45%),
        linear-gradient(315deg, rgba(0,212,191,0.13) 0%, transparent 45%),
        radial-gradient(ellipse 40% 30% at 100% 0%, rgba(189,147,249,0.08) 0%, transparent 60%),
        repeating-linear-gradient(-55deg, transparent 0, transparent 48px, rgba(255,70,85,0.032) 48px, rgba(255,70,85,0.038) 49px),
        repeating-linear-gradient(35deg, transparent 0, transparent 72px, rgba(0,212,191,0.028) 72px, rgba(0,212,191,0.033) 73px);
}

/* Top Glow Bar mạnh */
.stApp::after {
    content:''; position:fixed; top:0; left:0; right:0; height:3px; z-index:9999;
    background:linear-gradient(90deg,transparent 0%,#ff4655 15%,#ff7080 30%,transparent 45%,transparent 55%,#00d4bf 70%,#00ffe7 85%,transparent 100%);
    filter:drop-shadow(0 0 12px #ff4655) drop-shadow(0 0 28px #00d4bf);
}

/* Greeting Panel Glow mạnh */
.valo-greeting {
    box-shadow: 0 0 85px rgba(255,70,85,0.4), 0 0 160px rgba(0,212,191,0.28),
                0 10px 50px rgba(0,0,0,0.9), inset 0 0 95px rgba(255,70,85,0.1) !important;
    animation:greetGlow 4.2s ease-in-out infinite;
}

@keyframes greetGlow {
    0%,100% { box-shadow:0 0 60px rgba(255,70,85,0.32),0 0 130px rgba(255,70,85,0.1),0 10px 50px rgba(0,0,0,0.9); }
    50% { box-shadow:0 0 100px rgba(255,70,85,0.52),0 0 180px rgba(0,212,191,0.35),0 10px 50px rgba(0,0,0,0.9); }
}

/* Chat Bubbles */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    border-right:5px solid var(--R) !important;
    box-shadow:7px 0 40px rgba(255,70,85,0.38) !important;
}

[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    border-left:5px solid var(--T) !important;
    box-shadow:-7px 0 40px rgba(0,212,191,0.38) !important;
}

/* Button hover */
.stButton > button:hover {
    transform:translateX(10px) !important;
    box-shadow:0 0 40px rgba(0,212,191,0.6) !important;
}

/* Scrollbar */
::-webkit-scrollbar{width:4px;}
::-webkit-scrollbar-thumb{background:linear-gradient(#ff4655, #00d4bf); border-radius:2px;}
::-webkit-scrollbar-thumb:hover{background:var(--R);}
</style>
""", unsafe_allow_html=True)

# ====================== PHẦN CODE GỐC CỦA BẠN (GIỮ NGUYÊN HOÀN TOÀN) ======================
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("❌ Chưa cấu hình GROQ_API_KEY!"); st.stop()

def load_db():
    if os.path.exists("database_pc.json"):
        with open("database_pc.json","r",encoding="utf-8") as f: return json.load(f)
    return {"loi_he_thong":[],"linh_kien_pc":[]}

def load_raw():
    if os.path.exists("database_pc.json"):
        with open("database_pc.json","r",encoding="utf-8") as f: return f.read()
    return "{}"

data_pc=load_db(); raw=load_raw()
db_loi=len(data_pc.get("loi_he_thong",[])); db_lk=len(data_pc.get("linh_kien_pc",[]))

with st.sidebar:
    st.markdown("## ⚡ PC Solving")
    st.markdown("---")
    st.markdown("Hệ thống chẩn đoán lỗi và tư vấn linh kiện máy tính chuyên sâu.")
    st.markdown("---")
    if st.button("⟳ PHIÊN MỚI", use_container_width=True):
        st.session_state.messages=[]; st.session_state.greeted=False; st.session_state.suggestions=[]; st.rerun()
    st.markdown("---")
    st.markdown("<small>Lê Văn Chung · Lớp 10A4 🎓</small>", unsafe_allow_html=True)

LVC = """<svg viewBox="0 0 52 52" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="rg" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:#ff2233"/><stop offset="100%" style="stop-color:#ff4655"/></linearGradient>
    <linearGradient id="tg" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:#00d4bf"/><stop offset="100%" style="stop-color:#007a70"/></linearGradient>
    <filter id="glow"><feGaussianBlur stdDeviation="1.8" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  </defs>
  <polygon points="26,2 48,14 48,38 26,50 4,38 4,14" fill="rgba(255,30,50,0.1)" stroke="url(#rg)" stroke-width="2.2" filter="url(#glow)"/>
  <polygon points="26,9 41,17.5 41,34.5 26,43 11,34.5 11,17.5" fill="rgba(0,212,191,0.05)" stroke="url(#tg)" stroke-width="1" opacity="0.7"/>
  <line x1="4" y1="14" x2="16" y2="26" stroke="#ff4655" stroke-width="1.5" opacity="0.45"/>
  <line x1="48" y1="38" x2="36" y2="26" stroke="#00d4bf" stroke-width="1.5" opacity="0.45"/>
  <text x="26" y="31" text-anchor="middle" font-family="Rajdhani,sans-serif" font-size="13" font-weight="700" fill="white" letter-spacing="1" filter="url(#glow)">LVC</text>
  <circle cx="26" cy="39" r="2" fill="#ff4655" opacity="0.9" filter="url(#glow)"/>
</svg>"""

st.markdown(f"""
<div class="valo-header">
    <div class="valo-author">Lê Văn Chung · 10A4</div>
    <div class="valo-eyebrow">⚡ STEM PROJECT ⚡</div>
    <div class="valo-logo-wrap">
        <div class="lvc-logo">{LVC}</div>
        <div class="valo-title">PC<span class="slash">/</span><span class="red">SOLVING</span></div>
    </div>
    <div class="valo-subtitle">
        <span class="sub-d r"></span><span class="sub-r">CHẨN ĐOÁN</span>
        <span class="sub-d r"></span><span class="sub-w">PHÂN TÍCH</span>
        <span class="sub-d t"></span><span class="sub-t">XỬ LÝ TỰ ĐỘNG</span>
        <span class="sub-d t"></span>
    </div>
</div>
<div class="valo-divider"><div class="valo-divider-inner"><div class="vd r"></div><div class="vdbar"></div><div class="vd t"></div></div></div>
""", unsafe_allow_html=True)

for k,v in [("messages",[]),("greeted",False),("suggestions",[]),("pending_query",None)]:
    if k not in st.session_state: st.session_state[k]=v

SUGG = [
    ("⚠ Màn hình xanh BSOD đột ngột", "Máy tính bị màn hình xanh chết đột ngột, phải làm gì?"),
    ("▪ Màn hình đen không có tín hiệu", "Máy lên nguồn nhưng màn hình đen, không có tín hiệu"),
    ("◈ PC bíp dài khi khởi động", "Máy bíp dài liên tục khi bật, không vào được Windows"),
    ("◉ Windows boot loop liên tục", "Máy cứ khởi động lại liên tục không vào được Windows"),
    ("✕ Lỗi 0xc0000005 văng game", "Game bị lỗi 0xc0000005 không mở được cách fix?"),
    ("⚠ PC tự reboot khi chơi game nặng", "PC tự reboot đột ngột trong lúc chơi game nặng"),
    ("◈ SSD NVMe không nhận trong BIOS", "BIOS không nhận ổ SSD NVMe sau khi lắp vào mainboard"),
    ("🌡 CPU 95°C — overheat nghiêm trọng", "CPU nhiệt độ lên đến 95 độ C khi chạy game nguy hiểm không?"),
    ("◆ RAM 8GB có đủ cho game 2024?", "RAM 8GB có đủ dùng để chơi game hiện đại năm 2024 không?"),
    ("⚡ Nguồn bao nhiêu W cho RTX 3060?", "RTX 3060 cần nguồn bao nhiêu W dùng nguồn 500W được không?"),
    ("◆ i5-12400F chơi game 2024 đủ không?", "i5-12400F hiệu năng thế nào chơi game 2024 có đủ không?"),
    ("▶ i5 vs Ryzen 5 tầm 3-4 triệu", "Tầm giá 3-4 triệu nên chọn Intel i5 hay AMD Ryzen 5?"),
    ("🎮 GTX 1650 chơi game gì mượt ở FHD?", "GTX 1650 chơi mượt những game nào ở độ phân giải 1080p?"),
    ("▶ RTX 3060 vs RX 6600 nên mua cái nào?","So sánh RTX 3060 và RX 6600 nên chọn card nào?"),
    ("◆ H610 hay B660 nên chọn mainboard nào?","Mainboard H610 và B660 khác nhau thế nào nên mua loại nào?"),
    ("📱 Snapdragon 888 nóng máy bình thường?","Chip Snapdragon 888 bị nóng máy nhiều có phải lỗi không?"),
    ("📱 Dimensity 9200 vs Snapdragon 8 Gen2", "So sánh Dimensity 9200 với Snapdragon 8 Gen 2 loại nào mạnh?"),
    ("⚡ Build PC 10 triệu chơi game FHD", "Gợi ý cấu hình PC build 10 triệu đồng chơi game Full HD mượt"),
    ("◆ Combo i5-12400F + RTX 3060 tốt không?","Combo i5-12400F với RTX 3060 12GB chơi game có bottleneck không?"),
    ("◉ RAM 2x8GB vs 1x16GB cái nào nhanh?", "Lắp 2 thanh RAM 8GB hay 1 thanh 16GB thì nhanh hơn?"),
    ("▶ SSD NVMe vs SSD SATA khác gì?", "SSD NVMe và SSD SATA khác nhau ở điểm gì nên mua loại nào?"),
    ("◈ i3-12100F + RTX 3060 có bottleneck?", "i3-12100F dùng với RTX 3060 có bị cổ chai hiệu năng không?"),
]

if not st.session_state.suggestions: st.session_state.suggestions=random.sample(SUGG,4)

st.markdown(f"""
<div class="valo-greeting">
    <div class="vg-top"></div><div class="vg-lbar"></div><div class="vg-bot"></div>
    <div class="vg-cb-tl"></div><div class="vg-cb-tr"></div>
    <div class="vg-glow"></div><div class="vg-glow2"></div>
    <div class="valo-status-row"><div class="valo-status-dot"></div><div class="valo-status-text">Hệ thống sẵn sàng</div></div>
    <span class="valo-greeting-icon">⚡</span>
    <div class="valo-greeting-title">Hệ thống phân tích phần cứng máy tính</div>
    <div class="valo-greeting-sub">Nhập mã hiệu linh kiện hoặc mô tả hiện tượng lỗi hệ thống.<br>Thuật toán phân tích tự động sẽ đưa ra giải pháp ngay lập tức.</div>
    <div class="valo-stats">
        <div class="valo-stat"><span class="valo-stat-n">{db_loi}</span><span class="valo-stat-l">Lỗi hệ thống</span></div>
        <div class="valo-stat-d"></div>
        <div class="valo-stat"><span class="valo-stat-n">{db_lk}</span><span class="valo-stat-l">Linh kiện PC</span></div>
        <div class="valo-stat-d"></div>
        <div class="valo-stat"><span class="valo-stat-n" style="color:var(--T);text-shadow:0 0 16px rgba(0,212,191,0.8)">24/7</span><span class="valo-stat-l">Hỗ trợ</span></div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="valo-suggest-label"><span>CHỌN NHANH VẤN ĐỀ</span></div>', unsafe_allow_html=True)

c1,c2=st.columns(2,gap="small")
for i,(lb,qr) in enumerate(st.session_state.suggestions):
    with (c1 if i%2==0 else c2):
        if st.button(lb,key=f"s{i}"): st.session_state.greeted=True; st.session_state.pending_query=qr; st.rerun()

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

def score(item,q,nums):
    s=0; kws=[str(k).lower().strip() for k in item.get("keywords",[])]; ws=q.split()
    for k in kws:
        if k in ws or (k.isdigit() and k in q): s+=1
    if s==0: return 0
    ins=[re.sub(r'\D','',k) for k in kws if re.search(r'\d{3,}',k)]; ins=[n for n in ins if n]
    if ins and nums:
        if not set(ins)&set(nums): return 0
    return s

def search(uq):
    q=re.sub(r'[-–_,.\?!\(\)]',' ',uq.lower().strip())
    ns=[re.sub(r'\D','',w) for w in q.split() if re.search(r'\d{3,}',w)]; ns=[n for n in ns if n]
    bm,ms,mp=None,0,""
    for it in data_pc.get("linh_kien_pc",[]):
        s=score(it,q,ns)
        if s>ms: ms,bm,mp=s,it,"lk"
    for it in data_pc.get("loi_he_thong",[]):
        s=score(it,q,ns)
        if s>ms: ms,bm,mp=s,it,"loi"
    if ms>=2 and bm:
        if mp=="loi": return f"### ✕ {bm['ten']}\n*— Lê Văn Chung 10A4*\n\n**⚠ Nguyên nhân:** {bm['nguyen_nhan']}\n\n**◈ Khắc phục:**\n{bm['giai_phap']}"
        else: return f"### ◆ {bm['ten']}\n*— Lê Văn Chung 10A4*\n\n**⚙ Thông số:** {bm.get('thong_so','')}\n\n**◉ Socket:** `{bm.get('socket','')}`\n\n**▶ Tư vấn:** {bm.get('chuyen_gia_tu_van','')}"
    return None

def dtype(q):
    ql=q.lower()
    for w in ["i3","i5","i7","i9","ryzen","gtx","rtx","rx","vga","card","cpu","ram","ssd","mainboard","main","nguồn","psu","tản nhiệt","socket","ddr","mua","so sánh","nên chọn","combo","build","cấu hình","snapdragon","dimensity","chip","điện thoại","apple","iphone","samsung"]:
        if w in ql: return "hw"
    for w in ["lỗi","bsod","xanh","đen","bíp","crash","sập","đơ","treo","chậm","lag","không bật","không lên","restart","khởi động","update","0x","error","fix","sửa","boot","không nhận"]:
        if w in ql: return "err"
    return "gen"

B="TUYỆT ĐỐI KHÔNG dùng: 'AI','LLM','Groq','Meta','Llama','trí tuệ nhân tạo'. Đọc KỸ câu hỏi. Trả lời ĐÚNG ĐỦ."
PE=f"Bạn là hệ thống chẩn đoán lỗi của Lê Văn Chung 10A4.\n{B}\nKho:{raw}\nQUY TẮC: 1 câu nguyên nhân + tối đa 4 bước ngắn + 1 tip. Không dài dòng."
PH=f"Bạn là chuyên gia tư vấn linh kiện PC của Lê Văn Chung 10A4.\n{B}\nKho:{raw}\nQUY TẮC: Thông số quan trọng, so sánh nếu cần, gợi ý combo, kết bằng 1 khuyến nghị. Mở đầu: 'Dựa trên cơ sở dữ liệu kỹ thuật của tác giả Lê Văn Chung 10A4...'"
PG=f"Bạn là hệ thống hỗ trợ kỹ thuật của Lê Văn Chung 10A4.\n{B}\nKho:{raw}\nTrả lời tiếng Việt, súc tích."

def ask(uq,hist):
    t=dtype(uq)
    if t=="err": sy,mx,tp=PE,500,0.3
    elif t=="hw": sy,mx,tp=PH,800,0.5
    else: sy,mx,tp=PG,600,0.4
    ms=[{"role":"system","content":sy}]
    for m in hist[-6:]: ms.append({"role":m["role"],"content":m["content"]})
    ms.append({"role":"user","content":uq})
    r=client.chat.completions.create(model="llama-3.3-70b-versatile",messages=ms,max_tokens=mx,temperature=tp)
    return r.choices[0].message.content

def handle(p):
    st.session_state.messages.append({"role":"user","content":p})
    with st.chat_message("user"): st.markdown(p)
    with st.chat_message("assistant"):
        with st.spinner("ĐANG PHÂN TÍCH DỮ LIỆU..."):
            try:
                a=search(p) or ask(p,st.session_state.messages)
                st.markdown(a); st.session_state.messages.append({"role":"assistant","content":a})
            except: st.error("❌ Hệ thống gián đoạn. Thử lại.")

if st.session_state.pending_query:
    q=st.session_state.pending_query; st.session_state.pending_query=None; handle(q)

if p:=st.chat_input("Nhập mã lỗi hoặc linh kiện cần phân tích..."):
    st.session_state.greeted=True; handle(p)
