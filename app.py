import streamlit as st
import streamlit.components.v1 as components
import json, re, os, random
from groq import Groq
import base64
from PIL import Image
import io

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
    try {
      var w = window.parent || window;
      var frames = w.document ? [w] : [];
      frames.forEach(function(fw){
        fw.document.querySelectorAll('textarea').forEach(function(el){
          el.style.setProperty('background',DARK,'important');
          el.style.setProperty('background-color',DARK,'important');
          el.style.setProperty('color',CREAM,'important');
          el.style.setProperty('-webkit-text-fill-color',CREAM,'important');
          el.style.setProperty('caret-color',RED,'important');
        });
        fw.document.querySelectorAll('.stBottom,.stBottom>*,[data-testid="stBottom"]').forEach(function(el){
          el.style.setProperty('background',DARK,'important');
          el.style.setProperty('background-color',DARK,'important');
          el.style.setProperty('border-top','2px solid rgba(255,70,85,0.5)','important');
        });
      });
    } catch(e){}
  }
  fix();
  setInterval(fix, 100);
  new MutationObserver(fix).observe(document.documentElement,{subtree:true,childList:true});
})();
</script>
""", height=0)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Barlow+Condensed:wght@400;600;700;800&family=Barlow:wght@300;400;500&display=swap');

:root{
  --r:#ff4655;--r2:#e0303f;--t:#00d4bf;--t2:#00ffe7;--g:#e8c97a;
  --bg:#08090f;--bg1:#0e1018;--bg2:#0b0e16;--c:#ece8e1;--s:#b0aca4;--w:#ffffff;--d:#363a46;
}
html,body,.stApp{background:var(--bg)!important;color:var(--c)!important;font-family:'Barlow',sans-serif!important;}

/* === CSS MỚI CHO UPLOAD ẢNH === */
.valo-cam-btn {
  display:flex;align-items:center;justify-content:center;
  width:48px;height:48px;flex-shrink:0;cursor:pointer;
  background:linear-gradient(135deg,rgba(16,20,32,0.98),rgba(10,14,24,0.98));
  border:1px solid rgba(189,147,249,0.4);
  border-top:2px solid rgba(189,147,249,0.65);
  clip-path:polygon(0 0,calc(100% - 8px) 0,100% 8px,100% 100%,0 100%);
  transition:all .15s ease;
  box-shadow:0 0 12px rgba(189,147,249,0.15);
}
.valo-cam-btn:hover {
  background:rgba(189,147,249,0.12);
  border-color:rgba(189,147,249,0.7);
}
.valo-cam-icon { font-size:24px; color:#bd93f9; }

.valo-img-preview {
  background:linear-gradient(135deg,rgba(16,10,26,0.97),rgba(10,14,24,0.98));
  border:1px solid rgba(189,147,249,0.3);
  border-left:3px solid rgba(189,147,249,0.55);
  clip-path:polygon(0 0,calc(100% - 10px) 0,100% 10px,100% 100%,0 100%);
  padding:8px 12px;
  margin-bottom:8px;
  display:flex;align-items:center;gap:10px;
}
.valo-img-preview img {
  height:58px;width:auto;object-fit:cover;
  border:1px solid rgba(189,147,249,0.35);
}
.valo-del-btn {
  background:rgba(255,70,85,0.12);border:1px solid rgba(255,70,85,0.3);
  color:#ff4655;cursor:pointer;
  width:32px;height:32px;
  display:flex;align-items:center;justify-content:center;
  font-size:16px;font-weight:700;
}
</style>
""", unsafe_allow_html=True)

# === PHẦN CSS DÀI CỦA BẠN (GIỮ NGUYÊN) ===
# (Bạn copy nguyên phần CSS từ file cũ vào đây, từ .stApp::before đến hết style)

# ════ GROQ ════
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except KeyError:
    st.error("❌ Chưa cấu hình GROQ_API_KEY!"); st.stop()
except Exception as e:
    st.error(f"❌ {e}"); st.stop()

def load_db():
    if os.path.exists("database_pc.json"):
        with open("database_pc.json","r",encoding="utf-8") as f: return json.load(f)
    return {"loi_he_thong":[],"linh_kien_pc":[]}

data_pc=load_db()
db_loi=len(data_pc.get("loi_he_thong",[])); db_lk=len(data_pc.get("linh_kien_pc",[]))

with st.sidebar:
    st.markdown("## ⚡ PC Solving")
    st.markdown("---")
    st.markdown("Hệ thống chẩn đoán lỗi và tư vấn linh kiện máy tính chuyên sâu.")
    st.markdown("---")
    if st.button("⟳  PHIÊN MỚI", use_container_width=True):
        st.session_state.messages=[]; st.session_state.greeted=False
        st.session_state.suggestions=[]; st.rerun()
    st.markdown("---")
    st.markdown("<small>Lê Văn Chung · Lớp 10A4 🎓</small>", unsafe_allow_html=True)

LVC="""<svg viewBox="0 0 52 52" xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="rg" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:#ff2233"/><stop offset="100%" style="stop-color:#ff4655"/></linearGradient><linearGradient id="tg" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:#00d4bf"/><stop offset="100%" style="stop-color:#007a70"/></linearGradient><filter id="glow"><feGaussianBlur stdDeviation="1.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs><polygon points="26,2 48,14 48,38 26,50 4,38 4,14" fill="rgba(255,30,50,0.09)" stroke="url(#rg)" stroke-width="2" filter="url(#glow)"/><polygon points="26,8 42,17 42,35 26,44 10,35 10,17" fill="rgba(0,212,191,0.06)" stroke="url(#tg)" stroke-width="1.2" opacity="0.75"/><line x1="4" y1="14" x2="16" y2="26" stroke="#ff4655" stroke-width="1.5" opacity="0.45"/><line x1="48" y1="38" x2="36" y2="26" stroke="#00d4bf" stroke-width="1.5" opacity="0.45"/><text x="26" y="32" text-anchor="middle" font-family="Rajdhani,sans-serif" font-size="13" font-weight="700" fill="white" letter-spacing="0.5" filter="url(#glow)">LVC</text><circle cx="26" cy="40" r="2" fill="#ff4655" opacity="0.85"/><circle cx="26" cy="40" r="4" fill="none" stroke="#ff4655" stroke-width="0.5" opacity="0.35"/></svg>"""

st.markdown(f"""
<div class="valo-header">
  <div class="valo-author">Lê Văn Chung · 10A4</div>
  <div class="valo-eyebrow">⚡ STEM PROJECT ⚡</div>
  <div class="valo-logo-wrap"><div class="lvc-logo">{LVC}</div>
    <div class="valo-title">PC<span class="slash">/</span><span class="red">SOLVING</span></div>
  </div>
  <div class="valo-subtitle"><span class="sub-d r"></span><span class="sub-r">CHẨN ĐOÁN</span><span class="sub-d r"></span><span class="sub-w">PHÂN TÍCH</span><span class="sub-d t"></span><span class="sub-t">XỬ LÝ TỰ ĐỘNG</span><span class="sub-d t"></span></div>
</div>
<div class="valo-divider"><div class="valo-divider-inner"><div class="vd r"></div><div class="vdbar"></div><div class="vd t"></div></div></div>
""", unsafe_allow_html=True)

if "messages"      not in st.session_state: st.session_state.messages=[]
if "greeted"       not in st.session_state: st.session_state.greeted=False
if "suggestions"   not in st.session_state: st.session_state.suggestions=[]
if "pending_query" not in st.session_state: st.session_state.pending_query=None

ALL_S=[
    ("⚠  Màn hình xanh BSOD đột ngột","Máy tính bị màn hình xanh chết đột ngột, phải làm gì?"),
    # ... (bạn giữ nguyên toàn bộ list ALL_S dài)
]

if not st.session_state.suggestions:
    st.session_state.suggestions=random.sample(ALL_S,4)

st.markdown(f"""
<div class="valo-greeting scan-wrap">
  <!-- Giữ nguyên toàn bộ greeting box -->
</div>
""", unsafe_allow_html=True)

st.markdown("""<div class="smoke-1"></div><div class="smoke-2"></div>""", unsafe_allow_html=True)
st.markdown('<div class="valo-suggest-label"><span>CHỌN NHANH VẤN ĐỀ</span></div>', unsafe_allow_html=True)
col1,col2=st.columns(2,gap="small")
for i,(lb,qr) in enumerate(st.session_state.suggestions):
    with (col1 if i%2==0 else col2):
        if st.button(lb,key=f"s{i}"):
            st.session_state.greeted=True; st.session_state.pending_query=qr; st.rerun()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

# ════ DATABASE SEARCH ════
def calc_score(item,qc,un):
    sc=0; kws=[str(k).lower().strip() for k in item.get("keywords",[])]; uw=qc.split()
    for k in kws:
        if k in uw or (k.isdigit() and k in qc): sc+=1
    if sc==0: return 0
    ins=[re.sub(r'\D','',k) for k in kws if re.search(r'\d{3,}',k)]; ins=[n for n in ins if n]
    if ins and un:
        if not set(ins).intersection(set(un)): return 0
    return sc

def search_db(uq):
    qc=re.sub(r'[-–_,.\?!\(\)]',' ',uq.lower().strip())
    un=[re.sub(r'\D','',w) for w in qc.split() if re.search(r'\d{3,}',w)]; un=[n for n in un if n]
    bm,ms,mp=None,0,""
    for it in data_pc.get("linh_kien_pc",[]):
        s=calc_score(it,qc,un)
        if s>ms: ms,bm,mp=s,it,"lk"
    for it in data_pc.get("loi_he_thong",[]):
        s=calc_score(it,qc,un)
        if s>ms: ms,bm,mp=s,it,"loi"
    if ms>=2 and bm:
        if mp=="loi": return f"### ✕  {bm['ten']}\n*— Lê Văn Chung 10A4*\n\n**⚠ Nguyên nhân:** {bm['nguyen_nhan']}\n\n**◈ Khắc phục:**\n{bm['giai_phap']}"
        else: return f"### ◆  {bm['ten']}\n*— Lê Văn Chung 10A4*\n\n**⚙ Thông số:** {bm.get('thong_so','')}\n\n**◉ Socket:** `{bm.get('socket','')}`\n\n**▶ Tư vấn:** {bm.get('chuyen_gia_tu_van','')}"
    return None

# ════ SMART AI ENGINE ════
SYSTEM_PROMPT = """..."""  # giữ nguyên

def ask(uq, ch):
    # giữ nguyên hàm ask của bạn
    ...

# ════ VISION FUNCTION ════
def ask_vision(img_b64, caption, chat_history):
    user_text = caption.strip() if caption.strip() else "Hãy phân tích ảnh này. Đây là lỗi PC gì và cách khắc phục?"
    msgs = [
        {"role": "system", "content": "Bạn là chuyên gia phần cứng. Phân tích ảnh và trả lời bằng tiếng Việt ngắn gọn."},
        {"role": "user", "content": [
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}},
            {"type": "text", "text": user_text}
        ]}
    ]
    r = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=msgs,
        max_tokens=600,
        temperature=0.3
    )
    return r.choices[0].message.content

# ════ IMAGE UPLOAD + INPUT (ĐÃ FIX THEO YÊU CẦU) ════
if "img_data" not in st.session_state: st.session_state.img_data = None
if "img_name" not in st.session_state: st.session_state.img_name = ""
if "img_b64" not in st.session_state: st.session_state.img_b64 = ""
if "img_caption" not in st.session_state: st.session_state.img_caption = ""

components.html("""
<script>
document.addEventListener('paste', function(e) {
    if (e.clipboardData.files.length > 0) {
        const file = e.clipboardData.files[0];
        if (file.type.startsWith('image/')) {
            const dt = new DataTransfer();
            dt.items.add(file);
            document.querySelectorAll('input[type="file"]').forEach(inp => {
                if (!inp.files || inp.files.length === 0) {
                    inp.files = dt.files;
                    inp.dispatchEvent(new Event('change', {bubbles: true}));
                }
            });
        }
    }
});
</script>
""", height=0)

uploaded = st.file_uploader(" ", type=["jpg","jpeg","png","webp"], label_visibility="collapsed", key="img_uploader")

if uploaded is not None and st.session_state.img_data is None:
    try:
        img_obj = Image.open(uploaded).convert("RGB")
        buf = io.BytesIO()
        img_obj.save(buf, format="JPEG", quality=85)
        st.session_state.img_data = buf.getvalue()
        st.session_state.img_b64 = base64.b64encode(st.session_state.img_data).decode("utf-8")
        st.session_state.img_name = uploaded.name
        st.rerun()
    except:
        st.error("Không đọc được ảnh")

if st.session_state.img_data:
    preview_src = f"data:image/jpeg;base64,{st.session_state.img_b64}"
    st.markdown(f"""
    <div class="valo-img-preview">
      <img src="{preview_src}" alt="preview"/>
      <div style="flex:1">
        <strong>📷 Ảnh đã chọn</strong><br>{st.session_state.img_name}
      </div>
      <div onclick="document.getElementById('del_img_btn').click()" class="valo-del-btn">✕</div>
    </div>
    """, unsafe_allow_html=True)

    col_cap, col_del = st.columns([4,1])
    with col_cap:
        st.session_state.img_caption = st.text_input("Ghi chú", value=st.session_state.img_caption, placeholder="Mô tả lỗi hoặc câu hỏi...", label_visibility="collapsed", key="caption_input")
    with col_del:
        if st.button("✕ XÓA ẢNH", key="del_img_btn"):
            st.session_state.img_data = st.session_state.img_b64 = st.session_state.img_name = st.session_state.img_caption = None
            st.rerun()

c1, c2 = st.columns([1, 11], gap="small")
with c1:
    st.markdown('<div class="valo-cam-btn"><span class="valo-cam-icon">+</span></div>', unsafe_allow_html=True)
    st.file_uploader("", type=["jpg","jpeg","png","webp"], label_visibility="collapsed", key="plus_uploader")

with c2:
    prompt = st.chat_input("Nhập lỗi, linh kiện hoặc dán ảnh...")

if st.session_state.img_data and st.button("⚡ PHÂN TÍCH ẢNH", type="primary", use_container_width=True):
    cap = st.session_state.img_caption.strip()
    user_text = f"📷 **Ảnh lỗi PC** — {cap}" if cap else "📷 **Ảnh lỗi PC** — Phân tích giúp tôi"
    st.session_state.messages.append({"role":"user","content":user_text})
    with st.chat_message("user"):
        st.markdown(user_text)
        st.image(st.session_state.img_data, use_column_width=True)
    with st.chat_message("assistant"):
        with st.spinner("🔍 Đang phân tích ảnh..."):
            try:
                ans = ask_vision(st.session_state.img_b64, cap, st.session_state.messages)
                st.markdown(ans)
                st.session_state.messages.append({"role":"assistant","content":ans})
            except Exception as e:
                st.error(f"❌ {e}")
    st.session_state.img_data = st.session_state.img_b64 = st.session_state.img_name = st.session_state.img_caption = None
    st.rerun()

# ════ TEXT HANDLER ════
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

if st.session_state.pending_query:
    q=st.session_state.pending_query; st.session_state.pending_query=None; handle(q)
if prompt:
    st.session_state.greeted=True; handle(prompt)
