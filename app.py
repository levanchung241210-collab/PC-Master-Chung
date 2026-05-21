import streamlit as st
import streamlit.components.v1 as components
import json, re, os, random, base64
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

  // PASTE HANDLER & UPLOADER UI FIX
  function initUploaderFix() {
    try {
      var w = window.parent || window;
      var doc = w.document;
      if (!doc) return;
      
      // Bắt sự kiện Paste (Ctrl+V)
      var chatTa = doc.querySelector('[data-testid="stChatInput"] textarea');
      if (chatTa && !chatTa.dataset.pasteAttached) {
        chatTa.dataset.pasteAttached = "true";
        chatTa.addEventListener('paste', function(e) {
          var items = (e.clipboardData || e.originalEvent.clipboardData).items;
          for (var i = 0; i < items.length; i++) {
            if (items[i].type.indexOf('image') !== -1) {
              var blob = items[i].getAsFile();
              var fileInput = doc.querySelector('[data-testid="stFileUploader"] input[type="file"]');
              if (fileInput) {
                var dataTransfer = new DataTransfer();
                dataTransfer.items.add(new File([blob], "pasted_image.png", {type: blob.type}));
                fileInput.files = dataTransfer.files;
                fileInput.dispatchEvent(new Event('change', {bubbles: true}));
              }
            }
          }
        });
      }
      
      // Di chuyển Uploader vào ngang hàng với Chat Input
      var uploader = doc.querySelector('div[data-testid="stFileUploader"]');
      var chatContainer = doc.querySelector('div[data-testid="stChatInput"] > div');
      
      if (uploader && chatContainer && uploader.parentNode !== chatContainer) {
         chatContainer.style.display = 'flex';
         chatContainer.style.alignItems = 'flex-end';
         chatContainer.style.gap = '8px';
         
         var chatInputBox = doc.querySelector('div[data-testid="stChatInput"]');
         if(chatInputBox) { chatInputBox.style.width = '100%'; }
         
         chatContainer.insertBefore(uploader, chatContainer.firstChild);
      }
    } catch(e) {}
  }
  setInterval(initUploaderFix, 150);

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

/* ══ BACKGROUND — V-shape + VISIBLE diagonal cuts ══ */
.stApp::before{
  content:'';position:fixed;inset:0;pointer-events:none;z-index:0;
  background:
    /* V-SHAPE red light from top-center */
    conic-gradient(from 180deg at 50% -18%,
      transparent 60deg, rgba(255,55,65,0.10) 76deg,
      rgba(255,70,85,0.18) 90deg,
      rgba(255,55,65,0.10) 104deg, transparent 120deg),
    /* Left red zone */
    radial-gradient(ellipse 50% 70% at -5% 20%, rgba(255,40,55,0.13) 0%,transparent 58%),
    /* Right teal zone */
    radial-gradient(ellipse 50% 70% at 105% 80%, rgba(0,212,191,0.10) 0%,transparent 58%),
    /* DIAGONAL RED SLASHES — bright enough to see */
    repeating-linear-gradient(-52deg,
      transparent 0, transparent 54px,
      rgba(255,70,85,0.13) 54px, rgba(255,70,85,0.13) 55.5px,
      rgba(255,70,85,0.05) 55.5px, rgba(255,70,85,0.05) 57px,
      transparent 57px),
    /* DIAGONAL TEAL SLASHES */
    repeating-linear-gradient(38deg,
      transparent 0, transparent 84px,
      rgba(0,212,191,0.10) 84px, rgba(0,212,191,0.10) 85.5px,
      rgba(0,212,191,0.04) 85.5px, rgba(0,212,191,0.04) 87px,
      transparent 87px),
    /* HUD GRID */
    linear-gradient(rgba(255,70,85,0.07) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,70,85,0.07) 1px, transparent 1px);
  background-size: auto,auto,auto,auto,auto,38px 38px,38px 38px;
}

/* ══ TOP BAR ══ */
.stApp::after{
  content:'';position:fixed;top:0;left:0;right:0;height:3px;z-index:9999;
  background:linear-gradient(90deg,var(--r2) 0%,var(--r) 80px,var(--g) 50%,var(--t) calc(100% - 80px),var(--t2) 100%);
  box-shadow:0 0 12px rgba(255,70,85,0.6),0 0 24px rgba(255,70,85,0.2);
}

/* ══ SMOKE ══ */
@keyframes sd1{0%{transform:translate(0,0)scale(1);opacity:.12;}50%{transform:translate(16px,-26px)scale(1.3);opacity:.16;}100%{transform:translate(-6px,-52px)scale(1.7);opacity:0;}}
@keyframes sd2{0%{transform:translate(0,0)scale(1);opacity:.10;}60%{transform:translate(-20px,-34px)scale(1.35);opacity:.13;}100%{transform:translate(10px,-65px)scale(1.8);opacity:0;}}
.smoke-1,.smoke-2{position:fixed;border-radius:50%;pointer-events:none;z-index:0;filter:blur(3px);}
.smoke-1{width:220px;height:220px;bottom:6%;left:1%;background:radial-gradient(circle,rgba(255,70,85,0.16) 0%,transparent 65%);animation:sd1 3.5s ease-in-out infinite;}
.smoke-2{width:200px;height:200px;bottom:10%;right:2%;background:radial-gradient(circle,rgba(0,212,191,0.14) 0%,transparent 65%);animation:sd2 4.5s ease-in-out infinite 1.2s;}

/* ══ SCAN LINE ══ */
@keyframes scan{0%{top:-35%;opacity:1}70%{opacity:.5}100%{top:130%;opacity:0}}
.scan-wrap{position:relative;overflow:hidden;}
.scan-wrap::after{content:'';position:absolute;top:-35%;left:0;right:0;height:28%;
  background:linear-gradient(180deg,transparent 0%,rgba(0,212,191,0.08) 40%,rgba(0,212,191,0.08) 60%,transparent 100%);
  animation:scan 2.2s linear infinite;pointer-events:none;z-index:2;}

/* ══ HEADER ══ */
.valo-header{text-align:center;padding:10px 0 2px;position:relative;}
.valo-author{font-family:'Barlow Condensed',sans-serif;font-size:11px;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:var(--t2);text-shadow:0 0 10px rgba(0,255,231,0.6);text-align:right;margin-bottom:4px;display:flex;align-items:center;justify-content:flex-end;gap:6px;}
.valo-author::before{content:'';width:22px;height:1px;background:linear-gradient(90deg,transparent,var(--t2));box-shadow:0 0 5px var(--t2);}
.valo-eyebrow{font-family:'Barlow Condensed',sans-serif;font-size:clamp(9px,2vw,11px);font-weight:800;letter-spacing:7px;color:var(--r);text-transform:uppercase;margin-bottom:6px;display:flex;align-items:center;justify-content:center;gap:12px;text-shadow:0 0 14px rgba(255,70,85,0.8);}
.valo-eyebrow::before{content:'';width:40px;height:1px;background:linear-gradient(90deg,transparent,var(--r));box-shadow:0 0 8px rgba(255,70,85,0.6);}
.valo-eyebrow::after {content:'';width:40px;height:1px;background:linear-gradient(90deg,var(--r),transparent);box-shadow:0 0 8px rgba(255,70,85,0.6);}
.valo-logo-wrap{display:flex;align-items:center;justify-content:center;gap:16px;margin-bottom:4px;}
.lvc-logo{width:clamp(40px,7vw,56px);height:clamp(40px,7vw,56px);flex-shrink:0;filter:drop-shadow(0 0 8px rgba(255,70,85,0.6)) drop-shadow(0 0 18px rgba(255,70,85,0.25));}
.lvc-logo svg{width:100%;height:100%;}
.valo-title{font-family:'Rajdhani',sans-serif;font-size:clamp(30px,8vw,68px);font-weight:700;letter-spacing:3px;line-height:1;text-transform:uppercase;margin:0;color:var(--w);text-shadow:0 0 24px rgba(255,255,255,0.1),0 2px 8px rgba(0,0,0,0.95);}
.valo-title .red{color:var(--r);text-shadow:0 0 18px rgba(255,70,85,0.9),0 0 36px rgba(255,70,85,0.35);}
.valo-title .slash{color:var(--r);opacity:.45;margin:0 3px;}
.valo-subtitle{font-family:'Barlow Condensed',sans-serif;font-size:clamp(11px,2.8vw,14px);font-weight:800;letter-spacing:5px;text-transform:uppercase;margin-top:8px;display:flex;align-items:center;justify-content:center;gap:8px;flex-wrap:wrap;}
.sub-r{color:var(--r);text-shadow:0 0 10px rgba(255,70,85,0.7);}
.sub-w{color:var(--w);text-shadow:0 0 6px rgba(255,255,255,0.2);}
.sub-t{color:var(--t);text-shadow:0 0 10px rgba(0,212,191,0.7);}
.sub-d{display:inline-block;width:5px;height:5px;transform:rotate(45deg);}
.sub-d.r{background:var(--r);box-shadow:0 0 6px var(--r);}
.sub-d.t{background:var(--t);box-shadow:0 0 6px var(--t);}
.valo-divider{display:flex;align-items:center;margin:12px 0 8px;}
.valo-divider::before,.valo-divider::after{content:'';flex:1;height:1px;background:rgba(255,255,255,0.07);}
.valo-divider-inner{display:flex;align-items:center;gap:6px;padding:0 14px;}
.vd{width:6px;height:6px;transform:rotate(45deg);}
.vd.r{background:var(--r);box-shadow:0 0 10px var(--r),0 0 20px rgba(255,70,85,0.4);}
.vd.t{background:var(--t);width:5px;height:5px;box-shadow:0 0 10px var(--t),0 0 20px rgba(0,212,191,0.4);}
.vdbar{width:60px;height:2px;background:linear-gradient(90deg,var(--r),var(--g),var(--t));clip-path:polygon(6px 0%,100% 0%,calc(100% - 6px) 100%,0% 100%);box-shadow:0 0 10px rgba(0,212,191,0.4),0 0 6px rgba(255,70,85,0.3);}

/* ══ CORNER BRACKETS ══ */
.valo-bracket{position:absolute;width:14px;height:14px;}
.valo-bracket.tl{top:6px;left:6px;border-top:2px solid var(--r);border-left:2px solid var(--r);box-shadow:-1px -1px 6px rgba(255,70,85,0.4);}
.valo-bracket.tr{top:6px;right:6px;border-top:2px solid var(--t);border-right:2px solid var(--t);box-shadow:1px -1px 6px rgba(0,212,191,0.4);}
.valo-bracket.bl{bottom:6px;left:6px;border-bottom:2px solid var(--t);border-left:2px solid var(--t);box-shadow:-1px 1px 6px rgba(0,212,191,0.4);}
.valo-bracket.br{bottom:6px;right:6px;border-bottom:2px solid var(--r);border-right:2px solid var(--r);box-shadow:1px 1px 6px rgba(255,70,85,0.4);}

/* ══ GREETING BOX ══ */
@keyframes greetBreathe{0%,100%{box-shadow:0 0 30px rgba(255,70,85,0.09),0 8px 40px rgba(0,0,0,0.85);}50%{box-shadow:0 0 48px rgba(255,70,85,0.14),0 0 70px rgba(0,212,191,0.05),0 8px 40px rgba(0,0,0,0.85);}}
.valo-greeting{position:relative;background:linear-gradient(160deg,rgba(40,12,18,0.97) 0%,rgba(16,19,32,0.98) 45%,rgba(8,26,28,0.97) 100%);clip-path:polygon(20px 0%,100% 0%,100% calc(100% - 14px),calc(100% - 14px) 100%,0% 100%,0% 20px);padding:clamp(18px,5vw,28px) clamp(16px,5vw,28px) clamp(14px,4vw,22px);margin:4px 0 14px;overflow:hidden;border:1px solid rgba(255,70,85,0.25);animation:greetBreathe 2s ease-in-out infinite;}
.vg-topline{position:absolute;top:0;left:20px;right:0;height:2px;background:linear-gradient(90deg,var(--r),rgba(255,70,85,0.2));box-shadow:0 0 12px rgba(255,70,85,0.7);}
.vg-leftline{position:absolute;left:0;top:20px;bottom:0;width:2px;background:linear-gradient(180deg,var(--r),rgba(0,212,191,0.2));box-shadow:0 0 10px rgba(255,70,85,0.5);}
.vg-cut-h{position:absolute;top:20px;left:20px;width:28px;height:1px;background:var(--t);opacity:.5;box-shadow:0 0 6px var(--t);}
.vg-cut-v{position:absolute;top:20px;left:20px;width:1px;height:20px;background:var(--t);opacity:.4;box-shadow:0 0 6px var(--t);}
.vg-smoke-r{position:absolute;top:-20px;right:10%;width:180px;height:120px;background:radial-gradient(ellipse,rgba(255,50,60,0.08) 0%,transparent 65%);pointer-events:none;animation:floatSmoke 4s ease-in-out infinite;}
.vg-smoke-t{position:absolute;bottom:-20px;left:5%;width:160px;height:100px;background:radial-gradient(ellipse,rgba(0,212,191,0.07) 0%,transparent 65%);pointer-events:none;animation:floatSmoke 5.5s ease-in-out infinite 1.5s;}
@keyframes floatSmoke{0%,100%{transform:translate(0,0)scale(1);opacity:1;}50%{transform:translate(12px,-10px)scale(1.12);opacity:.65;}}
.valo-vbar{position:absolute;left:2px;top:20px;bottom:0;width:3px;background:linear-gradient(180deg,var(--r) 0%,var(--g) 45%,var(--t) 80%,transparent 100%);box-shadow:0 0 10px rgba(255,70,85,0.4);opacity:.8;}
.valo-status-row{display:flex;align-items:center;justify-content:center;gap:7px;margin-bottom:12px;}
.valo-status-dot-wrap{position:relative;width:22px;height:22px;display:flex;align-items:center;justify-content:center;}
.valo-status-dot{width:8px;height:8px;background:var(--t);border-radius:50%;box-shadow:0 0 10px var(--t),0 0 4px var(--t2);z-index:1;position:relative;animation:dotBlink 1.2s ease-in-out infinite;}
@keyframes dotBlink{0%,100%{opacity:1;box-shadow:0 0 10px var(--t);}50%{opacity:.4;box-shadow:0 0 4px var(--t);}}
.valo-status-ring{position:absolute;border-radius:50%;border:1px solid rgba(0,212,191,0.45);animation:ringPulse 1.4s ease-out infinite;}
.valo-status-ring.r1{width:14px;height:14px;animation-delay:0s;}
.valo-status-ring.r2{width:21px;height:21px;animation-delay:.35s;border-color:rgba(0,212,191,0.2);}
@keyframes ringPulse{0%{transform:scale(.5);opacity:.9;}100%{transform:scale(1.9);opacity:0;}}
.valo-status-text{font-family:'Barlow Condensed',sans-serif;font-size:10px;font-weight:700;letter-spacing:3px;color:var(--t2);text-transform:uppercase;text-shadow:0 0 8px rgba(0,255,231,0.5);}
.valo-greeting-icon{font-size:clamp(28px,5vw,36px);display:block;text-align:center;margin-bottom:10px;filter:drop-shadow(0 0 12px rgba(255,70,85,0.7));animation:iconGlow 2s ease-in-out infinite;}
@keyframes iconGlow{0%,100%{filter:drop-shadow(0 0 12px rgba(255,70,85,0.7));}50%{filter:drop-shadow(0 0 20px rgba(255,140,50,0.9)) drop-shadow(0 0 6px rgba(255,200,100,0.4));}}
.valo-greeting-title{font-family:'Rajdhani',sans-serif;font-size:clamp(15px,4vw,22px);font-weight:700;color:var(--w);text-align:center;text-transform:uppercase;letter-spacing:2px;margin-bottom:8px;text-shadow:0 0 16px rgba(255,255,255,0.12),0 2px 8px rgba(0,0,0,0.9);}
.valo-greeting-sub{font-size:clamp(12px,3vw,13.5px);color:var(--s);text-align:center;line-height:1.7;text-shadow:0 1px 6px rgba(0,0,0,0.8);}
.valo-stats{display:flex;justify-content:center;gap:clamp(12px,3vw,28px);margin-top:14px;padding-top:12px;border-top:1px solid rgba(255,255,255,0.07);}
.valo-stat{text-align:center;line-height:1.2;}
.valo-stat-num{font-family:'Rajdhani',sans-serif;font-size:clamp(18px,4vw,24px);font-weight:700;color:var(--r);display:block;text-shadow:0 0 14px rgba(255,70,85,0.7);}
.valo-stat-label{font-family:'Barlow Condensed',sans-serif;font-size:9px;letter-spacing:2px;color:var(--d);text-transform:uppercase;}
.valo-stat-div{width:1px;background:rgba(255,255,255,0.09);align-self:stretch;}

/* ══ SUGGEST LABEL ══ */
.valo-suggest-label{display:flex;align-items:center;gap:10px;margin:10px 0 12px;}
.valo-suggest-label::before{content:'';flex:1;height:1px;background:linear-gradient(90deg,transparent,rgba(255,70,85,0.5));}
.valo-suggest-label::after {content:'';flex:1;height:1px;background:linear-gradient(90deg,rgba(0,212,191,0.5),transparent);}
.valo-suggest-label span{background:linear-gradient(90deg,var(--r2),var(--r));color:var(--w);font-family:'Barlow Condensed',sans-serif;font-size:12px;font-weight:800;letter-spacing:3px;text-transform:uppercase;padding:5px 20px;clip-path:polygon(10px 0,100% 0,calc(100% - 10px) 100%,0 100%);box-shadow:0 0 20px rgba(255,70,85,0.5),0 0 40px rgba(255,70,85,0.15);}

/* ══ SUGGESTION BUTTONS ══ */
@keyframes btnPulse{0%,100%{box-shadow:0 0 8px rgba(0,212,191,0.12),0 3px 12px rgba(0,0,0,0.75);}50%{box-shadow:0 0 16px rgba(0,212,191,0.22),0 3px 12px rgba(0,0,0,0.75);}}
.stButton>button{
  background:linear-gradient(110deg,rgba(0,58,52,0.92) 0%,rgba(0,32,28,0.88) 40%,rgba(5,10,20,0.95) 100%) !important;
  color:#d8f8f4 !important;
  border:1px solid rgba(0,212,191,0.28) !important;
  border-left:3px solid var(--t) !important;
  clip-path:polygon(0 0,100% 0,100% calc(100% - 10px),calc(100% - 10px) 100%,0 100%) !important;
  border-radius:0 !important;
  font-family:'Barlow Condensed',sans-serif !important;
  font-size:clamp(12px,3.2vw,14px) !important;font-weight:700 !important;letter-spacing:.8px !important;
  padding:13px 16px !important;width:100% !important;text-align:left !important;
  white-space:normal !important;min-height:52px !important;line-height:1.45 !important;
  transition:all .12s ease !important;
  text-shadow:0 1px 6px rgba(0,0,0,0.7),0 0 10px rgba(0,212,191,0.08) !important;
  animation:btnPulse 2.5s ease-in-out infinite !important;
}
.stButton>button:hover{
  background:linear-gradient(110deg,rgba(0,212,191,0.18) 0%,rgba(0,130,120,0.12) 40%,rgba(255,70,85,0.10) 100%) !important;
  border-left-color:var(--r) !important;border-color:rgba(0,212,191,0.48) !important;
  color:#ffffff !important;transform:translateX(6px) !important;
  box-shadow:0 0 26px rgba(0,212,191,0.45),0 0 52px rgba(0,212,191,0.15),0 4px 18px rgba(0,0,0,0.75) !important;
  text-shadow:0 0 12px rgba(0,255,231,0.3),0 1px 4px rgba(0,0,0,0.8) !important;
  animation:none !important;
}

/* ══ AVATARS ══ */
[data-testid="chatAvatarIcon-user"]{background:linear-gradient(135deg,#5c0e1a,#200508) !important;border:2px solid var(--r) !important;border-radius:0 !important;clip-path:polygon(0 0,100% 0,100% calc(100% - 9px),calc(100% - 9px) 100%,0 100%) !important;box-shadow:0 0 14px rgba(255,70,85,0.6),0 0 28px rgba(255,70,85,0.2) !important;overflow:hidden !important;}
[data-testid="chatAvatarIcon-user"]>*{display:none !important;}
[data-testid="chatAvatarIcon-user"]::before{content:'';display:block;width:100%;height:100%;background:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 36 36'%3E%3Crect width='36' height='36' fill='%235c0e1a'/%3E%3Cpolygon points='18,3 31,10.5 31,25.5 18,33 5,25.5 5,10.5' fill='none' stroke='%23ff4655' stroke-width='1.8'/%3E%3Cpolygon points='18,9 25,13 25,23 18,27 11,23 11,13' fill='rgba(255,70,85,0.15)'/%3E%3Ctext x='18' y='22' text-anchor='middle' font-family='Rajdhani,sans-serif' font-size='9' font-weight='700' fill='%23ff8090'%3EUSR%3C/text%3E%3Ccircle cx='18' cy='31' r='1.5' fill='%23ff4655'/%3E%3C/svg%3E") center/cover no-repeat !important;}
[data-testid="chatAvatarIcon-assistant"]{background:linear-gradient(135deg,#003c38,#000e0d) !important;border:2px solid var(--t) !important;border-radius:0 !important;clip-path:polygon(9px 0,100% 0,100% 100%,0 100%,0 9px) !important;box-shadow:0 0 14px rgba(0,212,191,0.6),0 0 28px rgba(0,212,191,0.2) !important;overflow:hidden !important;}
[data-testid="chatAvatarIcon-assistant"]>*{display:none !important;}
[data-testid="chatAvatarIcon-assistant"]::before{content:'';display:block;width:100%;height:100%;background:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 36 36'%3E%3Crect width='36' height='36' fill='%23003c38'/%3E%3Cpolygon points='18,2 32,10 32,26 18,34 4,26 4,10' fill='none' stroke='%2300d4bf' stroke-width='1.8'/%3E%3Ccircle cx='18' cy='18' r='6.5' fill='none' stroke='%2300d4bf' stroke-width='1.2' opacity='0.8'/%3E%3Ccircle cx='18' cy='18' r='2.8' fill='%2300ffe7'/%3E%3Cline x1='18' y1='2' x2='18' y2='10' stroke='%2300d4bf' stroke-width='1' opacity='0.6'/%3E%3Cline x1='18' y1='26' x2='18' y2='34' stroke='%2300d4bf' stroke-width='1' opacity='0.6'/%3E%3Cline x1='4' y1='18' x2='11' y2='18' stroke='%2300d4bf' stroke-width='1' opacity='0.5'/%3E%3Cline x1='25' y1='18' x2='32' y2='18' stroke='%2300d4bf' stroke-width='1' opacity='0.5'/%3E%3C/svg%3E") center/cover no-repeat !important;}

/* ══ CHAT BUBBLES ══ */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]){background:radial-gradient(ellipse 80% 80% at 100% 50%,rgba(255,50,60,0.06) 0%,transparent 60%),linear-gradient(135deg,rgba(80,14,22,0.95) 0%,rgba(48,8,14,0.97) 40%,rgba(16,8,12,0.98) 100%) !important;border:1px solid rgba(255,70,85,0.35) !important;clip-path:polygon(0 0,calc(100% - 14px) 0,100% 14px,100% 100%,14px 100%,0 calc(100% - 14px)) !important;border-radius:0 !important;padding:15px 20px !important;margin:8px 0 !important;box-shadow:3px 0 20px rgba(255,70,85,0.1),0 4px 20px rgba(0,0,0,0.75) !important;}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]){background:radial-gradient(ellipse 80% 80% at 0% 50%,rgba(0,212,191,0.05) 0%,transparent 60%),linear-gradient(135deg,rgba(5,52,50,0.95) 0%,rgba(4,30,30,0.97) 40%,rgba(5,10,16,0.98) 100%) !important;border:1px solid rgba(0,212,191,0.28) !important;clip-path:polygon(14px 0,100% 0,100% calc(100% - 14px),calc(100% - 14px) 100%,0 100%,0 14px) !important;border-radius:0 !important;padding:15px 20px !important;margin:8px 0 !important;box-shadow:-3px 0 20px rgba(0,212,191,0.08),0 4px 20px rgba(0,0,0,0.75) !important;}
[data-testid="stChatMessage"] p,[data-testid="stChatMessage"] li{font-size:clamp(13.5px,3.8vw,15px) !important;line-height:1.82 !important;color:#f5f0ea !important;text-shadow:0 1px 4px rgba(0,0,0,0.98),0 2px 10px rgba(0,0,0,0.8) !important;}
[data-testid="stChatMessage"] h3{font-family:'Rajdhani',sans-serif !important;font-size:clamp(14px,4vw,19px) !important;font-weight:700 !important;text-transform:uppercase !important;letter-spacing:2.5px !important;color:#ffffff !important;margin-bottom:8px !important;padding-bottom:6px !important;border-bottom:1px solid rgba(255,255,255,0.09) !important;text-shadow:0 0 14px rgba(255,255,255,0.15),0 2px 8px rgba(0,0,0,0.95) !important;}
[data-testid="stChatMessage"] strong{color:#ffc5cb !important;font-weight:700 !important;text-shadow:0 0 10px rgba(255,70,85,0.4),0 1px 6px rgba(0,0,0,0.9) !important;}
[data-testid="stChatMessage"] em{color:var(--t2) !important;font-style:normal !important;font-size:11px !important;text-shadow:0 0 8px rgba(0,255,231,0.5) !important;}
[data-testid="stChatMessage"] code{background:rgba(0,212,191,0.13) !important;color:#70ffee !important;border:1px solid rgba(0,212,191,0.38) !important;border-radius:2px !important;padding:2px 7px !important;font-size:12px !important;box-shadow:0 0 8px rgba(0,212,191,0.1) !important;}

/* ══ CHAT INPUT — VALORANT TERMINAL ══ */
@keyframes inputAura{0%,100%{box-shadow:0 -4px 24px rgba(255,70,85,0.08);}50%{box-shadow:0 -4px 36px rgba(255,70,85,0.13),0 -2px 50px rgba(0,212,191,0.04);}}
@keyframes submitGlow{0%,100%{box-shadow:0 0 10px rgba(255,70,85,0.25);}50%{box-shadow:0 0 20px rgba(255,70,85,0.45);}}

/* Kill white bottom bar */
.stBottom,.stBottom>*,.stBottom>*>*,.stBottom>*>*>*,
[data-testid="stBottom"],[data-testid="stBottom"]>*{
  background:#08090f !important;background-color:#08090f !important;
  border-top:2px solid rgba(255,70,85,0.5) !important;
  animation:inputAura 2.5s ease-in-out infinite !important;
}
.stChatInput,.stChatInput>div,[data-testid="stChatInput"],[data-testid="stChatInput"]>div,[data-testid="stChatInput"]>div>div{
  background:#08090f !important;background-color:#08090f !important;border:none !important;border-radius:0 !important;
}
.stChatInput textarea,[data-testid="stChatInput"] textarea,[data-testid="stChatInputTextArea"],div[class*="stChatInput"] textarea{
  background:#0b0e16 !important;background-color:#0b0e16 !important;
  color:#ece8e1 !important;-webkit-text-fill-color:#ece8e1 !important;
  border-top:2px solid rgba(255,70,85,0.65) !important;
  border-right:1px solid rgba(255,70,85,0.2) !important;
  border-bottom:1px solid rgba(0,212,191,0.3) !important;
  border-left:3px solid rgba(255,70,85,0.45) !important;
  clip-path:polygon(0 0,calc(100% - 16px) 0,100% 16px,100% 100%,0 100%) !important;
  border-radius:0 !important;font-family:'Barlow',sans-serif !important;
  font-size:clamp(13.5px,3.5vw,15px) !important;letter-spacing:0.4px !important;
  caret-color:#ff4655 !important;opacity:1 !important;padding:15px 18px !important;
  box-shadow:0 -3px 18px rgba(255,70,85,0.12),inset 0 2px 0 rgba(255,70,85,0.06),inset 0 0 30px rgba(8,9,15,0.5) !important;
  transition:all .18s ease !important;
}
.stChatInput textarea:focus,[data-testid="stChatInput"] textarea:focus{
  background:#0b0e16 !important;background-color:#0b0e16 !important;
  color:#f4f0e8 !important;-webkit-text-fill-color:#f4f0e8 !important;
  border-top-color:var(--r) !important;border-left-color:var(--r) !important;
  border-bottom-color:var(--t) !important;outline:none !important;
  box-shadow:0 -5px 28px rgba(255,70,85,0.18),inset 0 2px 0 rgba(255,70,85,0.1) !important;
}
.stChatInput textarea::placeholder,[data-testid="stChatInput"] textarea::placeholder{
  color:rgba(170,165,155,0.4) !important;-webkit-text-fill-color:rgba(170,165,155,0.4) !important;font-style:italic !important;
}
.stChatInput button,[data-testid="stChatInput"] button,[data-testid="stChatInputSubmitButton"]{
  background:linear-gradient(135deg,rgba(200,40,55,0.9),rgba(150,25,38,0.85)) !important;
  clip-path:polygon(6px 0,100% 0,100% calc(100% - 6px),calc(100% - 6px) 100%,0 100%,0 6px) !important;
  border-radius:0 !important;border:1px solid rgba(255,70,85,0.6) !important;
  border-top:2px solid rgba(255,100,110,0.8) !important;color:#fff !important;
  box-shadow:0 0 14px rgba(255,70,85,0.3) !important;
  animation:submitGlow 1.8s ease-in-out infinite !important;transition:all .12s ease !important;
}
.stChatInput button:hover,[data-testid="stChatInput"] button:hover{
  background:linear-gradient(135deg,rgba(255,70,85,0.95),rgba(200,40,55,0.9)) !important;
  box-shadow:0 0 24px rgba(255,70,85,0.55) !important;transform:scale(1.06) !important;animation:none !important;
}
textarea{background:#0b0e16 !important;background-color:#0b0e16 !important;color:#ece8e1 !important;-webkit-text-fill-color:#ece8e1 !important;caret-color:#ff4655 !important;}

/* ══ CUSTOM FILE UPLOADER AS CAMERA ICON ══ */
div[data-testid="stFileUploader"] {
    width: 48px !important;
    min-width: 48px !important;
    height: 48px !important;
    margin-bottom: 0 !important;
    padding: 0 !important;
    flex-shrink: 0 !important;
}
div[data-testid="stFileUploader"] section {
    padding: 0 !important;
    width: 100% !important;
    height: 100% !important;
}
div[data-testid="stFileUploaderDropzone"] {
    background: #0b0e16 !important;
    border: 1px solid rgba(255,70,85,0.4) !important;
    border-top: 2px solid rgba(255,70,85,0.7) !important;
    clip-path: polygon(0 0,calc(100% - 8px) 0,100% 8px,100% 100%,0 100%) !important;
    border-radius: 0 !important;
    width: 100% !important;
    height: 48px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    cursor: pointer !important;
}
div[data-testid="stFileUploaderDropzone"]:hover {
    background: rgba(255,70,85,0.1) !important;
}
div[data-testid="stFileUploaderDropzoneInstructions"] {
    display: none !important;
}
div[data-testid="stFileUploaderDropzone"] button {
    all: unset !important;
    position: absolute !important;
    inset: 0 !important;
    width: 100% !important;
    height: 100% !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    cursor: pointer !important;
    z-index: 10;
}
div[data-testid="stFileUploaderDropzone"] button::before {
    content: '📷' !important;
    font-size: 20px !important;
    color: #ff4655 !important;
}
div[data-testid="stFileUploader"] ~ div[data-testid="stVerticalBlock"],
[data-testid="stFileUploadDeleteBtn"] {
    display: none !important;
}

/* Make chat message render images correctly */
.upload-preview {
    margin-bottom: 10px;
    padding: 8px 12px;
    background: rgba(16,10,26,0.9);
    border-left: 3px solid #ff4655;
    font-size: 12px;
    color: #00d4bf;
    display: inline-block;
}


/* ══ SIDEBAR ══ */
section[data-testid="stSidebar"]{background:linear-gradient(180deg,#08090e,#0b0d16) !important;border-right:1px solid rgba(255,70,85,0.16) !important;}
section[data-testid="stSidebar"] p,section[data-testid="stSidebar"] span,section[data-testid="stSidebar"] div,section[data-testid="stSidebar"] small{color:#60625e !important;font-size:13px !important;}
section[data-testid="stSidebar"] h2{font-family:'Rajdhani',sans-serif !important;font-size:17px !important;color:var(--c) !important;text-transform:uppercase !important;letter-spacing:3px !important;}
section[data-testid="stSidebar"] .stButton>button{background:transparent !important;border:1px solid rgba(255,70,85,0.2) !important;border-left:2px solid var(--r) !important;color:#606060 !important;clip-path:polygon(0 0,100% 0,100% calc(100% - 6px),calc(100% - 6px) 100%,0 100%) !important;border-radius:0 !important;box-shadow:none !important;font-family:'Barlow Condensed',sans-serif !important;font-weight:700 !important;letter-spacing:1px !important;}
section[data-testid="stSidebar"] .stButton>button:hover{background:rgba(255,70,85,0.07) !important;color:var(--c) !important;transform:none !important;}
[data-testid="stSpinner"] p{color:var(--t) !important;font-family:'Barlow Condensed',sans-serif !important;letter-spacing:4px !important;font-size:11px !important;text-transform:uppercase !important;text-shadow:0 0 10px rgba(0,212,191,0.6) !important;}
::-webkit-scrollbar{width:4px;}::-webkit-scrollbar-track{background:var(--bg);}::-webkit-scrollbar-thumb{background:rgba(255,70,85,0.45);}::-webkit-scrollbar-thumb:hover{background:var(--r);}
#MainMenu,footer,header{visibility:hidden !important;}
.block-container{padding-top:1.2rem !important;padding-bottom:1.5rem !important;max-width:760px !important;}
@media(max-width:600px){.block-container{padding:.7rem .5rem 4.5rem !important;}[data-testid="stChatMessage"]{padding:10px 14px !important;margin:4px 0 !important;}.stButton>button{min-height:46px !important;padding:10px 11px !important;}.valo-greeting{padding:16px 12px !important;}.valo-author{position:relative !important;top:0 !important;justify-content:center !important;margin-bottom:8px !important;}.valo-author::before{display:none;}}
</style>
""", unsafe_allow_html=True)

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
    ("▪  Màn hình đen không có tín hiệu","Máy lên nguồn nhưng màn hình đen, không có tín hiệu"),
    ("◈  PC bíp dài khi khởi động","Máy bíp dài liên tục khi bật, không vào được Windows"),
    ("◉  Windows boot loop liên tục","Máy cứ khởi động lại liên tục không vào được Windows"),
    ("✕  Lỗi 0xc0000005 văng game","Game bị lỗi 0xc0000005 không mở được, cách fix?"),
    ("⚠  PC tự reboot khi chơi game","PC tự reboot đột ngột trong lúc chơi game nặng"),
    ("🌡  CPU 95°C overheat","CPU nhiệt độ lên đến 95 độ C khi chạy game, nguy hiểm không?"),
    ("◆  RAM 8GB đủ cho game 2024?","RAM 8GB có đủ dùng để chơi game hiện đại 2024 không?"),
    ("⚡  Nguồn bao nhiêu W cho RTX 4080?","RTX 4080 cần nguồn bao nhiêu W, dùng nguồn 750W được không?"),
    ("◆  Tản nhiệt nước hay khí?","Nên dùng tản nhiệt nước hay khí cho i5-13600K?"),
    ("◈  i3-12100F + RTX 3060 bottleneck?","i3-12100F dùng với RTX 3060 có bị cổ chai không?"),
    ("🎮  RTX 5090 mạnh cỡ nào?","RTX 5090 hiệu năng thế nào so với RTX 4090?"),
    ("▶  RTX 3060 vs RX 6600?","So sánh RTX 3060 và RX 6600, nên chọn card nào?"),
    ("◆  RTX 4060 Ti có đáng mua?","RTX 4060 Ti giá tiền có xứng đáng so với RTX 3070?"),
    ("▶  i5 vs Ryzen 5 tầm 3-4 triệu","Tầm 3-4 triệu nên chọn Intel i5 hay AMD Ryzen 5?"),
    ("◆  H610 hay B660?","Mainboard H610 và B660 khác nhau thế nào, nên mua loại nào?"),
    ("📱  Snapdragon 8 Gen 4 mạnh cỡ nào?","Chip Snapdragon 8 Elite (Gen 4) hiệu năng thế nào?"),
    ("📱  Dimensity 9300+ vs Snap 8 Gen 3","So sánh Dimensity 9300+ với Snapdragon 8 Gen 3?"),
    ("📱  iPhone 16 Pro chip A18 Pro?","Chip Apple A18 Pro trong iPhone 16 Pro mạnh đến đâu?"),
    ("⚡  Build PC gaming 15 triệu 2024","Gợi ý cấu hình PC gaming 15 triệu tốt nhất 2024"),
    ("◆  Ryzen 7 9800X3D có đáng mua?","Ryzen 7 9800X3D với 3D V-Cache có xứng đáng mua không?"),
    ("▶  SSD Gen 5 vs Gen 4 NVMe?","SSD PCIe Gen 5 có đáng nâng cấp từ Gen 4 không?"),
    ("◈  B550 dùng được Ryzen 5 5600X?","Mainboard B550 có tương thích Ryzen 5 5600X không?"),
    ("◉  iGPU Intel UHD đủ văn phòng?","Dùng Intel UHD Graphics cho văn phòng có đủ không?"),
    ("▪  Socket LGA1700 dùng CPU đời mấy?","Socket LGA1700 hỗ trợ CPU Intel đời mấy?"),
    ("⚠  Máy tự reboot khi render video","PC tự khởi động khi render video nặng, nguyên nhân gì?"),
    ("◆  RTX 4070 Super vs RX 7800 XT?","So sánh RTX 4070 Super và RX 7800 XT, mua cái nào?"),
    ("📱  Samsung Galaxy S25 Ultra chip?","Samsung S25 Ultra dùng chip gì, hiệu năng thế nào?"),
    ("◆  Core Ultra 200 vs Ryzen 9000?","Intel Core Ultra 200 series vs AMD Ryzen 9000 cái nào tốt hơn?"),
    ("▶  NVMe vs SATA SSD?","SSD NVMe và SATA khác nhau ở điểm gì, nên mua loại nào?"),
    ("◈  PC không nhận RAM sau nâng cấp","Nâng cấp RAM mới nhưng máy không nhận, xử lý thế nào?"),
    ("✕  Lỗi 0xc000021a không boot","Máy báo lỗi 0xc000021a không boot được vào Windows"),
]
if not st.session_state.suggestions:
    st.session_state.suggestions=random.sample(ALL_S,4)

st.markdown(f"""
<div class="valo-greeting scan-wrap">
  <div class="valo-bracket tl"></div><div class="valo-bracket tr"></div>
  <div class="valo-bracket bl"></div><div class="valo-bracket br"></div>
  <div class="vg-topline"></div><div class="vg-leftline"></div>
  <div class="vg-cut-h"></div><div class="vg-cut-v"></div>
  <div class="vg-smoke-r"></div><div class="vg-smoke-t"></div>
  <div class="valo-vbar"></div>
  <div class="valo-status-row">
    <div class="valo-status-dot-wrap"><div class="valo-status-ring r1"></div><div class="valo-status-ring r2"></div><div class="valo-status-dot"></div></div>
    <div class="valo-status-text">Hệ thống sẵn sàng</div>
  </div>
  <span class="valo-greeting-icon">⚡</span>
  <div class="valo-greeting-title">Hệ thống phân tích phần cứng máy tính</div>
  <div class="valo-greeting-sub">Nhập mã hiệu linh kiện hoặc mô tả hiện tượng lỗi.<br>Thuật toán phân tích tự động sẽ đưa ra giải pháp ngay lập tức.</div>
  <div class="valo-stats">
    <div class="valo-stat"><span class="valo-stat-num">{db_loi}</span><span class="valo-stat-label">Lỗi hệ thống</span></div>
    <div class="valo-stat-div"></div>
    <div class="valo-stat"><span class="valo-stat-num">{db_lk}</span><span class="valo-stat-label">Linh kiện PC</span></div>
    <div class="valo-stat-div"></div>
    <div class="valo-stat"><span class="valo-stat-num" style="color:var(--t);text-shadow:0 0 14px rgba(0,212,191,0.7)">24/7</span><span class="valo-stat-label">Hỗ trợ</span></div>
  </div>
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
    with st.chat_message(msg["role"]): 
        st.markdown(msg["content"])
        if msg.get("image"):
            st.image(base64.b64decode(msg["image"]), width=300)

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

# ════ SMART AI ENGINE — no template, full knowledge ════
SYSTEM_PROMPT = """Bạn là chuyên gia phần cứng máy tính và điện tử hàng đầu, với kiến thức cực kỳ sâu rộng và cập nhật đến 2025.

KIẾN THỨC BẮT BUỘC PHẢI BIẾT:
- CPU Intel: từ Core 2 đến Core Ultra 200, Arc GPU
- CPU AMD: từ FX đến Ryzen 9000 series, Threadripper, EPYC
- VGA NVIDIA: GTX 600 đến RTX 5090 (Blackwell), GeForce Now
- VGA AMD: từ RX 400 đến RX 9000 series (RDNA 4)
- VGA Intel Arc: A series, Battlemage
- Chip mobile: Snapdragon 8 Elite (Gen 4), Dimensity 9400, Apple A18 Pro/A17 Pro, Exynos 2500
- Điện thoại 2024-2025: iPhone 16 series, Samsung S25 series, Pixel 9 series
- SSD: PCIe Gen 3/4/5, NVMe M.2, SATA, các hãng Samsung/WD/SK Hynix
- RAM: DDR4, DDR5, LPDDR5X
- Mainboard: Intel 700/800 series, AMD X670/B650/B850
- Nguồn: 80+ Bronze/Gold/Platinum, ATX 3.0

QUY TẮC TRẢ LỜI — QUAN TRỌNG:
1. Đọc KỸ câu hỏi, trả lời ĐÚNG nội dung được hỏi — không trả lời template
2. Nếu hỏi về linh kiện cụ thể: nêu thông số thực tế, so sánh, ưu nhược, giá tham khảo
3. Nếu hỏi lỗi: nguyên nhân chính (1 câu) + bước fix (≤4 bước ngắn) + 1 tip
4. Nếu hỏi so sánh: phân tích khách quan từng mặt, kết luận rõ ràng
5. Không mở đầu bằng "Xin chào", không lặp câu hỏi, không giải thích thừa
6. Trả lời bằng tiếng Việt, súc tích, đúng trọng tâm
7. TUYỆT ĐỐI KHÔNG nhắc "AI", "LLM", "Groq", "ngôn ngữ lớn"
8. Với câu hỏi về linh kiện mới (RTX 5090, Ryzen 9000, chip mobile 2024-2025): dùng kiến thức chuyên môn của bạn để trả lời, không nói "không biết"

Tự xưng là "hệ thống chuyên gia" khi cần, hoặc không tự xưng."""

def ask(uq, ch, img_b64=None):
    msgs = [{"role":"system","content":SYSTEM_PROMPT}]
    for m in ch[-8:]:
        if "image" not in m: # Llama 3.3 70b text không nhận ảnh cũ
            msgs.append({"role":m["role"],"content":m["content"]})
            
    if img_b64:
        msgs.append({
            "role": "user",
            "content": [
                {"type": "text", "text": uq},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}}
            ]
        })
        r = client.chat.completions.create(
            model="llama-3.2-90b-vision-preview",
            messages=msgs,
            max_tokens=600,
            temperature=0.3
        )
        return r.choices[0].message.content
    else:
        msgs.append({"role":"user","content":uq})
        q = uq.lower()
        hw_words = ["so sánh","mua","build","cấu hình","rtx","gtx","rx","ryzen","core ultra","i5","i7","i9","snapdragon","dimensity","apple a","iphone","samsung"]
        err_words = ["lỗi","bsod","xanh","đen","bíp","crash","sập","không bật","0x","boot","restart"]
        
        if any(w in q for w in err_words):
            max_tok = 480
        elif any(w in q for w in hw_words):
            max_tok = 750
        else:
            max_tok = 580

        r = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=msgs,
            max_tokens=max_tok,
            temperature=0.45
        )
        return r.choices[0].message.content

def handle(p, img_b64=None):
    if img_b64:
        st.session_state.messages.append({"role":"user","content":p,"image":img_b64})
    else:
        st.session_state.messages.append({"role":"user","content":p})
        
    with st.chat_message("user"): 
        st.markdown(p)
        if img_b64:
            st.image(base64.b64decode(img_b64), width=300)
            
    with st.chat_message("assistant"):
        with st.spinner("ĐANG PHÂN TÍCH DỮ LIỆU..."):
            try:
                a = None
                if not img_b64:
                    a = search_db(p)
                if not a:
                    # Pass tin nhắn cũ (bỏ tin nhắn user hiện tại vì ask đã tự append)
                    a = ask(p, st.session_state.messages[:-1], img_b64)
                st.markdown(a)
                st.session_state.messages.append({"role":"assistant","content":a})
            except Exception as e:
                st.error(f"❌ {str(e)}")
                
    st.session_state.upload_key += 1
    st.rerun()

if "upload_key" not in st.session_state: 
    st.session_state.upload_key = 0

uploaded = st.file_uploader(
    "img", 
    type=["jpg", "jpeg", "png"], 
    key=f"uploader_{st.session_state.upload_key}", 
    label_visibility="collapsed"
)

img_b64 = None
if uploaded:
    img_b64 = base64.b64encode(uploaded.getvalue()).decode("utf-8")
    st.markdown('<div class="upload-preview">📸 Đã dán/tải ảnh thành công! Hãy nhập thêm yêu cầu bên dưới và Enter để gửi.</div>', unsafe_allow_html=True)

if st.session_state.pending_query:
    q=st.session_state.pending_query; st.session_state.pending_query=None; handle(q)
if p:=st.chat_input("Nhập mã lỗi, linh kiện hoặc dán ảnh (Ctrl+V)..."):
    st.session_state.greeted=True; handle(p, img_b64)
