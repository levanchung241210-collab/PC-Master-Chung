import streamlit as st
import streamlit.components.v1 as components
import json, re, os, random
import base64
from groq import Groq

st.set_page_config(page_title="PC Solving — LVC 10A4", page_icon="⚡", layout="centered")

# ══ INJECT DARK INPUT via components — bypasses Streamlit shadow DOM ══
components.html("""
<style>
  /* Target parent frames */
  body, html { background: #08090f !important; }
  
  :root {
    --r: #ff4655;
    --r2: #b72c37;
    --t: #00d4bf;
    --t2: #00ffe7;
    --g: #8f96a3;
    --w: #ece8e1;
    --s: #aa1221;
    --bg: #08090f;
    --card: #0b0e16;
  }
  
  /* Style cho File Uploader và Camera Input chuẩn màu Valorant Theme */
  .stFileUploader, .stCameraInput {
    background: #0b0e16 !important;
    border: 1px solid rgba(0, 212, 191, 0.2) !important;
    padding: 8px !important;
    border-radius: 0px !important;
  }
  .stFileUploader section {
    background-color: #08090f !important;
    border: 1px dashed rgba(255, 70, 85, 0.4) !important;
    color: #ece8e1 !important;
    border-radius: 0px !important;
  }
  .stCameraInput div button {
    background: linear-gradient(135deg, #ff4655, #b72c37) !important;
    color: white !important;
    border-radius: 0px !important;
    border: none !important;
  }

  /* CSS GỐC GIỮ NGUYÊN HOÀN TOÀN */
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

# ════ HIỂN THỊ LỊCH SỬ CHAT (KÈM ẢNH NẾU CÓ) ════
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "image" in msg and msg["image"]:
            st.image(f"data:image/jpeg;base64,{msg['image']}", caption="Hình ảnh đính kèm")

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

# ════ SMART AI ENGINE — Vision Model Integration ════
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
1. Đọc KỸ câu hỏi và xem KỸ hình ảnh đính kèm (nếu có) để chuẩn đoán chính xác linh kiện hoặc mã lỗi hiển thị trên màn hình.
2. Trả lời ĐÚNG nội dung được hỏi — không trả lời template.
3. Nếu hỏi về linh kiện cụ thể: nêu thông số thực tế, so sánh, ưu nhược, giá tham khảo.
4. Nếu hỏi lỗi: nguyên nhân chính (1 câu) + bước fix (≤4 bước ngắn) + 1 tip.
5. Nếu hỏi so sánh: phân tích khách quan từng mặt, kết luận rõ ràng.
6. Không mở đầu bằng "Xin chào", không lặp câu hỏi, không giải thích thừa.
7. Trả lời bằng tiếng Việt, súc tích, đúng trọng tâm.
8. TUYỆT ĐỐI KHÔNG nhắc "AI", "LLM", "Groq", "ngôn ngữ lớn".
9. Với câu hỏi về linh kiện mới (RTX 5090, Ryzen 9000, chip mobile 2024-2025): dùng kiến thức chuyên môn của bạn để trả lời, không nói "không biết".

Tự xưng là "hệ thống chuyên gia" khi cần, hoặc không tự xưng."""

def ask(uq, ch):
    # Sử dụng model đa phương tiện hỗ trợ phân tích hình ảnh của Groq
    model_name = "llama-3.2-11b-vision-preview"
    
    msgs = [{"role":"system","content":SYSTEM_PROMPT}]
    
    # Đóng gói lịch sử hội thoại (hỗ trợ cả text và image_url)
    for m in ch[-8:]:
        role = m["role"]
        content = m["content"]
        if "image" in m and m["image"]:
            msgs.append({
                "role": role,
                "content": [
                    {"type": "text", "text": content},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{m['image']}"
                        }
                    }
                ]
            })
        else:
            msgs.append({"role": role, "content": content})

    # Tính toán tokens linh hoạt
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
        model=model_name,
        messages=msgs,
        max_tokens=max_tok,
        temperature=0.45
    )
    return r.choices[0].message.content

def handle(p, img_file=None):
    base64_img = None
    if img_file is not None:
        bytes_data = img_file.getvalue()
        base64_img = base64.b64encode(bytes_data).decode("utf-8")

    st.session_state.messages.append({"role": "user", "content": p, "image": base64_img})
    with st.chat_message("user"):
        st.markdown(p)
        if img_file is not None:
            st.image(img_file, caption="Ảnh đính kèm", width=300)
            
    with st.chat_message("assistant"):
        with st.spinner("ĐANG PHÂN TÍCH DỮ LIỆU..."):
            try:
                # Nếu có ảnh đính kèm thì bắt buộc chạy qua AI Vision, không chạy Local DB
                a = None if img_file is not None else search_db(p)
                if not a:
                    a = ask(p, st.session_state.messages)
                st.markdown(a)
                st.session_state.messages.append({"role": "assistant", "content": a})
            except Exception as e:
                st.error(f"❌ {str(e)}")

# ════ TÍCH HỢP THANH ĐÍNH KÈM ẢNH/CAMERA CÂN ĐỐI (TRÊN THANH INPUT) ════
st.markdown('<div class="valo-suggest-label" style="margin-top:25px;"><span>📷 ĐÍNH KÈM HÌNH ẢNH / CAMERA (HỖ TRỢ CTRL+V PASTE)</span></div>', unsafe_allow_html=True)
img_col1, img_col2 = st.columns(2, gap="small")
with img_col1:
    uploaded_file = st.file_uploader("Upload hoặc Paste ảnh tại đây", type=["png", "jpg", "jpeg"], label_visibility="collapsed", key="file_paste_uploader")
with img_col2:
    camera_file = st.camera_input("Chụp ảnh trực tiếp", label_visibility="collapsed", key="camera_capture_input")

# Xác định ảnh nào đang được kích hoạt sử dụng
active_image = uploaded_file if uploaded_file is not None else camera_file

# ════ ĐIỀU HƯỚNG INPUT VÀO LUỒNG XỬ LÝ ════
if st.session_state.pending_query:
    q=st.session_state.pending_query; st.session_state.pending_query=None; handle(q, active_image)
if p:=st.chat_input("Nhập mã lỗi hoặc linh kiện cần phân tích..."):
    st.session_state.greeted=True; handle(p, active_image)
