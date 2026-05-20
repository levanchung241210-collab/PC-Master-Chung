import streamlit as st
import streamlit.components.v1 as components
import json, re, os, random, base64
from groq import Groq

# ══ CẤU HÌNH TRANG ══
st.set_page_config(page_title="PC Solving — LVC 10A4", page_icon="⚡", layout="centered")

# ══ INJECT DARK INPUT via components — bypasses Streamlit shadow DOM ══
components.html("""
<style>
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

# ══ GIAO DIỆN (GIỮ NGUYÊN CSS) ══
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Barlow+Condensed:wght@400;600;700;800&family=Barlow:wght@300;400;500&display=swap');
:root{ --r:#ff4655;--r2:#e0303f;--t:#00d4bf;--t2:#00ffe7;--g:#e8c97a; --bg:#08090f;--bg1:#0e1018;--bg2:#0b0e16;--c:#ece8e1;--s:#b0aca4;--w:#ffffff;--d:#363a46; }
html,body,.stApp{background:var(--bg)!important;color:var(--c)!important;font-family:'Barlow',sans-serif!important;}
.stApp::before{ content:'';position:fixed;inset:0;pointer-events:none;z-index:0; background: conic-gradient(from 180deg at 50% -18%, transparent 60deg, rgba(255,55,65,0.10) 76deg, rgba(255,70,85,0.18) 90deg, rgba(255,55,65,0.10) 104deg, transparent 120deg), radial-gradient(ellipse 50% 70% at -5% 20%, rgba(255,40,55,0.13) 0%,transparent 58%), radial-gradient(ellipse 50% 70% at 105% 80%, rgba(0,212,191,0.10) 0%,transparent 58%), repeating-linear-gradient(-52deg, transparent 0, transparent 54px, rgba(255,70,85,0.13) 54px, rgba(255,70,85,0.13) 55.5px, rgba(255,70,85,0.05) 55.5px, rgba(255,70,85,0.05) 57px, transparent 57px), repeating-linear-gradient(38deg, transparent 0, transparent 84px, rgba(0,212,191,0.10) 84px, rgba(0,212,191,0.10) 85.5px, rgba(0,212,191,0.04) 85.5px, rgba(0,212,191,0.04) 87px, transparent 87px), linear-gradient(rgba(255,70,85,0.07) 1px, transparent 1px), linear-gradient(90deg, rgba(255,70,85,0.07) 1px, transparent 1px); background-size: auto,auto,auto,auto,auto,38px 38px,38px 38px; }
.stApp::after{ content:'';position:fixed;top:0;left:0;right:0;height:3px;z-index:9999; background:linear-gradient(90deg,var(--r2) 0%,var(--r) 80px,var(--g) 50%,var(--t) calc(100% - 80px),var(--t2) 100%); box-shadow:0 0 12px rgba(255,70,85,0.6),0 0 24px rgba(255,70,85,0.2); }
.valo-header{text-align:center;padding:10px 0 2px;position:relative;}
.valo-author{font-family:'Barlow Condensed',sans-serif;font-size:11px;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:var(--t2);text-shadow:0 0 10px rgba(0,255,231,0.6);text-align:right;margin-bottom:4px;display:flex;align-items:center;justify-content:flex-end;gap:6px;}
.valo-eyebrow{font-family:'Barlow Condensed',sans-serif;font-size:clamp(9px,2vw,11px);font-weight:800;letter-spacing:7px;color:var(--r);text-transform:uppercase;margin-bottom:6px;display:flex;align-items:center;justify-content:center;gap:12px;text-shadow:0 0 14px rgba(255,70,85,0.8);}
.valo-logo-wrap{display:flex;align-items:center;justify-content:center;gap:16px;margin-bottom:4px;}
.lvc-logo{width:clamp(40px,7vw,56px);height:clamp(40px,7vw,56px);flex-shrink:0;filter:drop-shadow(0 0 8px rgba(255,70,85,0.6)) drop-shadow(0 0 18px rgba(255,70,85,0.25));}
.valo-title{font-family:'Rajdhani',sans-serif;font-size:clamp(30px,8vw,68px);font-weight:700;letter-spacing:3px;line-height:1;text-transform:uppercase;margin:0;color:var(--w);text-shadow:0 0 24px rgba(255,255,255,0.1),0 2px 8px rgba(0,0,0,0.95);}
.valo-title .red{color:var(--r);text-shadow:0 0 18px rgba(255,70,85,0.9),0 0 36px rgba(255,70,85,0.35);}
.valo-subtitle{font-family:'Barlow Condensed',sans-serif;font-size:clamp(11px,2.8vw,14px);font-weight:800;letter-spacing:5px;text-transform:uppercase;margin-top:8px;display:flex;align-items:center;justify-content:center;gap:8px;flex-wrap:wrap;}
.valo-divider{display:flex;align-items:center;margin:12px 0 8px;}
.valo-divider::before,.valo-divider::after{content:'';flex:1;height:1px;background:rgba(255,255,255,0.07);}
.vdbar{width:60px;height:2px;background:linear-gradient(90deg,var(--r),var(--g),var(--t));clip-path:polygon(6px 0%,100% 0%,calc(100% - 6px) 100%,0% 100%);}
.vd{width:6px;height:6px;transform:rotate(45deg);}
.vd.r{background:var(--r);}
.vd.t{background:var(--t);}
</style>
""", unsafe_allow_html=True)

# ══ GIAO DIỆN HEADER ══
LVC="""<svg viewBox="0 0 52 52" xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="rg" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:#ff2233"/><stop offset="100%" style="stop-color:#ff4655"/></linearGradient><linearGradient id="tg" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:#00d4bf"/><stop offset="100%" style="stop-color:#007a70"/></linearGradient><filter id="glow"><feGaussianBlur stdDeviation="1.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs><polygon points="26,2 48,14 48,38 26,50 4,38 4,14" fill="rgba(255,30,50,0.09)" stroke="url(#rg)" stroke-width="2" filter="url(#glow)"/><polygon points="26,8 42,17 42,35 26,44 10,35 10,17" fill="rgba(0,212,191,0.06)" stroke="url(#tg)" stroke-width="1.2" opacity="0.75"/><line x1="4" y1="14" x2="16" y2="26" stroke="#ff4655" stroke-width="1.5" opacity="0.45"/><line x1="48" y1="38" x2="36" y2="26" stroke="#00d4bf" stroke-width="1.5" opacity="0.45"/><text x="26" y="32" text-anchor="middle" font-family="Rajdhani,sans-serif" font-size="13" font-weight="700" fill="white" letter-spacing="0.5" filter="url(#glow)">LVC</text><circle cx="26" cy="40" r="2" fill="#ff4655" opacity="0.85"/><circle cx="26" cy="40" r="4" fill="none" stroke="#ff4655" stroke-width="0.5" opacity="0.35"/></svg>"""

st.markdown(f"""
<div class="valo-header">
  <div class="valo-author">Lê Văn Chung · 10A4</div>
  <div class="valo-eyebrow">⚡ STEM PROJECT ⚡</div>
  <div class="valo-logo-wrap"><div class="lvc-logo">{LVC}</div>
    <div class="valo-title">PC<span style="color:#ff4655;opacity:.45;margin:0 3px;">/</span><span class="red">SOLVING</span></div>
  </div>
</div>
<div class="valo-divider"><div style="display:flex;align-items:center;gap:6px;padding:0 14px;"><div class="vd r"></div><div class="vdbar"></div><div class="vd t"></div></div></div>
""", unsafe_allow_html=True)

# ══ KHỞI TẠO SESSION ══
if "messages" not in st.session_state: st.session_state.messages = []
if "uploader_key" not in st.session_state: st.session_state.uploader_key = 0

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("❌ Chưa cấu hình GROQ_API_KEY")
    st.stop()

# ══ HÀM GỌI AI ══
def get_ai_response(prompt, img_b64=None):
    if img_b64:
        return client.chat.completions.create(
            model="llama-3.2-90b-vision-preview",
            messages=[{"role": "user", "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}}
            ]}]
        ).choices[0].message.content
    else:
        return client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.45
        ).choices[0].message.content

# ══ SIDEBAR (CAMERA/UPLOAD) ══
with st.sidebar:
    st.markdown("## ⚡ CÔNG CỤ TÍCH HỢP")
    uploaded_file = st.file_uploader(
        "📷 Đính kèm ảnh lỗi", 
        type=["png", "jpg", "jpeg"], 
        key=f"uploader_{st.session_state.uploader_key}"
    )

# ══ LOGIC XỬ LÝ CHAT ══
def handle_submit(p, file):
    img_b64 = None
    if file:
        img_b64 = base64.b64encode(file.getvalue()).decode("utf-8")
        st.session_state.messages.append({"role": "user", "content": p, "img": img_b64})
    else:
        st.session_state.messages.append({"role": "user", "content": p})

    # Hiển thị UI
    with st.chat_message("user"):
        st.markdown(p)
        if img_b64: st.image(file, width=250)
    
    with st.chat_message("assistant"):
        with st.spinner("ĐANG PHÂN TÍCH..."):
            try:
                reply = get_ai_response(p, img_b64)
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"❌ {e}")
    
    # RESET UPLOADER
    st.session_state.uploader_key += 1
    st.rerun()

# ══ RENDER LỊCH SỬ ══
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "img" in msg:
            st.image(base64.b64decode(msg["img"]), width=250)

# ══ CHAT INPUT ══
if prompt := st.chat_input("Nhập mã lỗi hoặc linh kiện cần phân tích..."):
    handle_submit(prompt, uploaded_file)
