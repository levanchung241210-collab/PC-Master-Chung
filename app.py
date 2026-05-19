import streamlit as st
import json, re, os, random
from groq import Groq

st.set_page_config(page_title="PC Solving — LVC 10A4", page_icon="⚡", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Barlow+Condensed:wght@400;600;700;800&family=Barlow:wght@300;400;500&display=swap');

:root {
  --r:#ff4655; --r2:#e03040; --rg:rgba(255,70,85,0.12);
  --t:#00d4bf; --t2:#00ffe7; --tg:rgba(0,212,191,0.10);
  --g:#e8c97a; --p:#bd93f9;
  --bg:#09090f; --bg1:#0e1018; --bg2:#131722; --bg3:#192030;
  --w:#ffffff; --c:#ece8e1; --s:#b0aca4; --d:#363a46;
}
html,body,.stApp{background:var(--bg) !important;color:var(--c) !important;font-family:'Barlow',sans-serif !important;}

/* ══════════════════════════════════════
   BACKGROUND — Valorant V-shape + smoke
══════════════════════════════════════ */
.stApp::before {
  content:''; position:fixed; inset:0; pointer-events:none; z-index:0;
  background:
    /* V-shape light — main Valorant signature */
    conic-gradient(from 180deg at 50% -20%,
      transparent 60deg,
      rgba(255,50,60,0.09) 80deg,
      rgba(255,70,85,0.15) 90deg,
      rgba(255,50,60,0.09) 100deg,
      transparent 120deg),
    /* Red smoke left */
    radial-gradient(ellipse 50% 60% at -8% 30%, rgba(255,40,55,0.13) 0%, transparent 60%),
    /* Teal smoke right */
    radial-gradient(ellipse 50% 60% at 108% 70%, rgba(0,212,191,0.10) 0%, transparent 60%),
    /* Purple top-right */
    radial-gradient(ellipse 35% 25% at 100% 0%, rgba(189,147,249,0.06) 0%, transparent 55%),
    /* Warm floor glow */
    radial-gradient(ellipse 80% 20% at 50% 110%, rgba(255,70,85,0.07) 0%, transparent 55%),
    /* HUD grid subtle */
    linear-gradient(rgba(255,70,85,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,70,85,0.03) 1px, transparent 1px),
    /* Cross diagonal slashes */
    repeating-linear-gradient(-52deg, transparent 0, transparent 80px, rgba(255,70,85,0.018) 80px, rgba(255,70,85,0.018) 81px),
    repeating-linear-gradient( 38deg, transparent 0, transparent 110px, rgba(0,212,191,0.012) 110px, rgba(0,212,191,0.012) 111px);
  background-size: auto,auto,auto,auto,auto, 44px 44px, 44px 44px, auto, auto;
}

/* ══ TOP NEON LINE — softer ══ */
.stApp::after {
  content:''; position:fixed; top:0; left:0; right:0; height:3px; z-index:9999;
  background:linear-gradient(90deg, var(--r2) 0%, var(--r) 80px, var(--g) 50%, var(--t) calc(100% - 80px), var(--t2) 100%);
  box-shadow:0 0 10px rgba(255,70,85,0.5), 0 0 20px rgba(255,70,85,0.15), 0 2px 6px rgba(0,212,191,0.15);
}

/* ══ SMOKE PARTICLES drifting ══ */
@keyframes smokeDrift1 { 0%{transform:translate(0,0) scale(1);opacity:.06;} 50%{transform:translate(20px,-30px) scale(1.3);opacity:.1;} 100%{transform:translate(-10px,-60px) scale(1.6);opacity:0;} }
@keyframes smokeDrift2 { 0%{transform:translate(0,0) scale(1);opacity:.05;} 60%{transform:translate(-25px,-40px) scale(1.4);opacity:.08;} 100%{transform:translate(15px,-80px) scale(1.8);opacity:0;} }
@keyframes smokeDrift3 { 0%{transform:translate(0,0) scale(1);opacity:.04;} 70%{transform:translate(30px,-50px) scale(1.5);opacity:.07;} 100%{transform:translate(-5px,-90px) scale(2);opacity:0;} }
.smoke-1,.smoke-2,.smoke-3 { position:absolute; border-radius:50%; pointer-events:none; }
.smoke-1 { width:120px; height:120px; bottom:10%; left:5%; background:radial-gradient(circle,rgba(255,70,85,0.08) 0%,transparent 70%); animation:smokeDrift1 8s ease-in-out infinite; }
.smoke-2 { width:100px; height:100px; bottom:15%; right:8%; background:radial-gradient(circle,rgba(0,212,191,0.07) 0%,transparent 70%); animation:smokeDrift2 10s ease-in-out infinite 2s; }
.smoke-3 { width:80px; height:80px; bottom:5%; left:40%; background:radial-gradient(circle,rgba(232,201,122,0.05) 0%,transparent 70%); animation:smokeDrift3 12s ease-in-out infinite 4s; }

/* ══ SCAN LINE ══ */
@keyframes scanDown { 0%{top:-40%;opacity:.6} 80%{opacity:.3} 100%{top:130%;opacity:0} }
.scan-wrap { position:relative; overflow:hidden; }
.scan-wrap::after { content:''; position:absolute; top:-40%; left:0; right:0; height:35%;
  background:linear-gradient(180deg,transparent 0%,rgba(0,212,191,0.035) 50%,transparent 100%);
  animation:scanDown 6s linear infinite; pointer-events:none; z-index:2; }

/* ══ HEADER ══ */
.valo-header { text-align:center; padding:10px 0 2px; position:relative; }

/* author */
.valo-author {
  font-family:'Barlow Condensed',sans-serif; font-size:11px; font-weight:700;
  letter-spacing:3px; text-transform:uppercase; color:var(--t2);
  text-shadow:0 0 10px rgba(0,255,231,0.6);
  text-align:right; margin-bottom:4px;
  display:flex; align-items:center; justify-content:flex-end; gap:6px;
}
.valo-author::before { content:''; width:22px; height:1px; background:linear-gradient(90deg,transparent,var(--t2)); box-shadow:0 0 5px var(--t2); }

/* eyebrow */
.valo-eyebrow {
  font-family:'Barlow Condensed',sans-serif; font-size:clamp(9px,2vw,11px);
  font-weight:800; letter-spacing:7px; color:var(--r); text-transform:uppercase; margin-bottom:6px;
  display:flex; align-items:center; justify-content:center; gap:12px;
  text-shadow:0 0 12px rgba(255,70,85,0.7);
}
.valo-eyebrow::before { content:''; width:40px; height:1px; background:linear-gradient(90deg,transparent,var(--r)); box-shadow:0 0 6px rgba(255,70,85,0.5); }
.valo-eyebrow::after  { content:''; width:40px; height:1px; background:linear-gradient(90deg,var(--r),transparent); box-shadow:0 0 6px rgba(255,70,85,0.5); }

/* logo + title */
.valo-logo-wrap { display:flex; align-items:center; justify-content:center; gap:16px; margin-bottom:4px; }
.lvc-logo { width:clamp(40px,7vw,56px); height:clamp(40px,7vw,56px); flex-shrink:0;
  filter:drop-shadow(0 0 8px rgba(255,70,85,0.55)) drop-shadow(0 0 16px rgba(255,70,85,0.2)); }
.lvc-logo svg { width:100%; height:100%; }
.valo-title {
  font-family:'Rajdhani',sans-serif; font-size:clamp(30px,8vw,68px); font-weight:700;
  letter-spacing:3px; line-height:1; text-transform:uppercase; margin:0;
  color:var(--w); text-shadow:0 0 24px rgba(255,255,255,0.1),0 2px 8px rgba(0,0,0,0.95);
}
.valo-title .red { color:var(--r); text-shadow:0 0 16px rgba(255,70,85,0.8),0 0 32px rgba(255,70,85,0.3); }
.valo-title .slash { color:var(--r); opacity:.45; margin:0 3px; }

/* subtitle */
.valo-subtitle {
  font-family:'Barlow Condensed',sans-serif; font-size:clamp(11px,2.8vw,14px);
  font-weight:800; letter-spacing:5px; text-transform:uppercase; margin-top:8px;
  display:flex; align-items:center; justify-content:center; gap:8px; flex-wrap:wrap;
}
.sub-r { color:var(--r); text-shadow:0 0 10px rgba(255,70,85,0.7); }
.sub-w { color:var(--w); text-shadow:0 0 6px rgba(255,255,255,0.2); }
.sub-t { color:var(--t); text-shadow:0 0 10px rgba(0,212,191,0.7); }
.sub-d { display:inline-block; width:5px; height:5px; transform:rotate(45deg); }
.sub-d.r { background:var(--r); box-shadow:0 0 6px var(--r); }
.sub-d.t { background:var(--t); box-shadow:0 0 6px var(--t); }

/* divider */
.valo-divider { display:flex; align-items:center; margin:12px 0 8px; }
.valo-divider::before,.valo-divider::after { content:''; flex:1; height:1px; background:rgba(255,255,255,0.07); }
.valo-divider-inner { display:flex; align-items:center; gap:6px; padding:0 14px; }
.vd { width:6px; height:6px; transform:rotate(45deg); }
.vd.r { background:var(--r); box-shadow:0 0 8px var(--r),0 0 16px rgba(255,70,85,0.4); }
.vd.t { background:var(--t); width:5px; height:5px; box-shadow:0 0 8px var(--t),0 0 16px rgba(0,212,191,0.4); }
.vdbar {
  width:60px; height:2px;
  background:linear-gradient(90deg,var(--r),var(--g),var(--t));
  clip-path:polygon(6px 0%,100% 0%,calc(100% - 6px) 100%,0% 100%);
  box-shadow:0 0 8px rgba(0,212,191,0.4),0 0 5px rgba(255,70,85,0.3);
}

/* ═══════════════════════════
   CORNER BRACKETS
═══════════════════════════ */
.valo-bracket { position:absolute; width:14px; height:14px; }
.valo-bracket.tl { top:6px; left:6px; border-top:2px solid var(--r); border-left:2px solid var(--r); box-shadow:-1px -1px 6px rgba(255,70,85,0.35); }
.valo-bracket.tr { top:6px; right:6px; border-top:2px solid var(--t); border-right:2px solid var(--t); box-shadow:1px -1px 6px rgba(0,212,191,0.35); }
.valo-bracket.bl { bottom:6px; left:6px; border-bottom:2px solid var(--t); border-left:2px solid var(--t); box-shadow:-1px 1px 6px rgba(0,212,191,0.35); }
.valo-bracket.br { bottom:6px; right:6px; border-bottom:2px solid var(--r); border-right:2px solid var(--r); box-shadow:1px 1px 6px rgba(255,70,85,0.35); }

/* ═══════════════════════════
   GREETING BOX — Valorant panel
   Smoky dark, not pure black
═══════════════════════════ */
.valo-greeting {
  position:relative;
  background:
    radial-gradient(ellipse 80% 50% at 50% 0%, rgba(255,50,60,0.07) 0%, transparent 55%),
    radial-gradient(ellipse 60% 60% at 100% 100%, rgba(0,212,191,0.06) 0%, transparent 55%),
    linear-gradient(160deg, rgba(38,12,18,0.97) 0%, rgba(16,19,32,0.98) 45%, rgba(8,26,28,0.97) 100%);
  clip-path:polygon(20px 0%,100% 0%,100% calc(100% - 14px),calc(100% - 14px) 100%,0% 100%,0% 20px);
  padding:clamp(18px,5vw,28px) clamp(16px,5vw,28px) clamp(14px,4vw,22px);
  margin:4px 0 14px; overflow:hidden;
  border:1px solid rgba(255,70,85,0.22);
  box-shadow:
    0 0 40px rgba(255,70,85,0.09),
    0 0 80px rgba(0,212,191,0.04),
    0 8px 40px rgba(0,0,0,0.8);
  animation:greetBreathe 5s ease-in-out infinite;
}
@keyframes greetBreathe {
  0%,100%{ box-shadow:0 0 40px rgba(255,70,85,0.09),0 8px 40px rgba(0,0,0,0.8); }
  50%    { box-shadow:0 0 55px rgba(255,70,85,0.14),0 0 80px rgba(0,212,191,0.05),0 8px 40px rgba(0,0,0,0.8); }
}

/* Structural lines inside box */
.vg-topline { position:absolute; top:0; left:20px; right:0; height:2px;
  background:linear-gradient(90deg,var(--r),rgba(255,70,85,0.2));
  box-shadow:0 0 10px rgba(255,70,85,0.6); }
.vg-leftline { position:absolute; left:0; top:20px; bottom:0; width:2px;
  background:linear-gradient(180deg,var(--r),rgba(0,212,191,0.2));
  box-shadow:0 0 8px rgba(255,70,85,0.4); }
/* Inner accent lines at cut corner */
.vg-cut-h { position:absolute; top:20px; left:20px; width:24px; height:1px;
  background:var(--t); opacity:.45; box-shadow:0 0 5px var(--t); }
.vg-cut-v { position:absolute; top:20px; left:20px; width:1px; height:18px;
  background:var(--t); opacity:.38; box-shadow:0 0 5px var(--t); }
/* Bottom BR cut line */
.vg-br-line { position:absolute; bottom:14px; right:0; width:40px; height:1px;
  background:linear-gradient(90deg,transparent,rgba(255,70,85,0.3)); }
/* Floating smoke blobs inside box */
.vg-smoke-r { position:absolute; top:-20px; right:10%; width:180px; height:120px;
  background:radial-gradient(ellipse,rgba(255,50,60,0.06) 0%,transparent 70%);
  pointer-events:none; animation:floatSmoke 7s ease-in-out infinite; }
.vg-smoke-t { position:absolute; bottom:-20px; left:5%; width:160px; height:100px;
  background:radial-gradient(ellipse,rgba(0,212,191,0.05) 0%,transparent 70%);
  pointer-events:none; animation:floatSmoke 9s ease-in-out infinite 3s; }
@keyframes floatSmoke { 0%,100%{transform:translate(0,0) scale(1);opacity:1;} 50%{transform:translate(10px,-8px) scale(1.08);opacity:.7;} }
/* Left triple-color bar */
.valo-vbar { position:absolute; left:2px; top:20px; bottom:0; width:3px;
  background:linear-gradient(180deg,var(--r) 0%,var(--g) 45%,var(--t) 80%,transparent 100%);
  box-shadow:0 0 8px rgba(255,70,85,0.4); opacity:.8; }

/* Status row */
.valo-status-row { display:flex; align-items:center; justify-content:center; gap:7px; margin-bottom:12px; }
/* Animated dot with pulse rings */
.valo-status-dot-wrap { position:relative; width:16px; height:16px; display:flex; align-items:center; justify-content:center; }
.valo-status-dot { width:7px; height:7px; background:var(--t); border-radius:50%;
  box-shadow:0 0 10px var(--t),0 0 4px var(--t2); z-index:1; position:relative; }
.valo-status-ring { position:absolute; border-radius:50%;
  border:1px solid rgba(0,212,191,0.4); animation:ringPulse 2s ease-out infinite; }
.valo-status-ring.r1 { width:12px; height:12px; animation-delay:0s; }
.valo-status-ring.r2 { width:18px; height:18px; animation-delay:.4s; border-color:rgba(0,212,191,0.2); }
@keyframes ringPulse { 0%{transform:scale(0.5);opacity:.8;} 100%{transform:scale(1.8);opacity:0;} }
.valo-status-text { font-family:'Barlow Condensed',sans-serif; font-size:10px; font-weight:700;
  letter-spacing:3px; color:var(--t2); text-transform:uppercase;
  text-shadow:0 0 10px rgba(0,255,231,0.6); }

.valo-greeting-icon { font-size:clamp(28px,5vw,36px); display:block; text-align:center; margin-bottom:10px;
  filter:drop-shadow(0 0 12px rgba(255,70,85,0.7));
  animation:iconGlow 3s ease-in-out infinite; }
@keyframes iconGlow { 0%,100%{filter:drop-shadow(0 0 12px rgba(255,70,85,0.7));} 50%{filter:drop-shadow(0 0 22px rgba(255,130,60,0.9));} }
.valo-greeting-title { font-family:'Rajdhani',sans-serif; font-size:clamp(15px,4vw,22px); font-weight:700;
  color:var(--w); text-align:center; text-transform:uppercase; letter-spacing:2px; margin-bottom:8px; }
.valo-greeting-sub { font-size:clamp(12px,3vw,13.5px); color:var(--s); text-align:center; line-height:1.7; }
.valo-stats { display:flex; justify-content:center; gap:clamp(12px,3vw,28px);
  margin-top:14px; padding-top:12px; border-top:1px solid rgba(255,255,255,0.07); }
.valo-stat { text-align:center; line-height:1.2; }
.valo-stat-num { font-family:'Rajdhani',sans-serif; font-size:clamp(18px,4vw,24px); font-weight:700;
  color:var(--r); display:block; text-shadow:0 0 12px rgba(255,70,85,0.6); }
.valo-stat-label { font-family:'Barlow Condensed',sans-serif; font-size:9px;
  letter-spacing:2px; color:var(--d); text-transform:uppercase; }
.valo-stat-div { width:1px; background:rgba(255,255,255,0.09); align-self:stretch; }

/* ═══════════════════════════
   SUGGEST LABEL
═══════════════════════════ */
.valo-suggest-label { display:flex; align-items:center; gap:10px; margin:10px 0 12px; }
.valo-suggest-label::before { content:''; flex:1; height:1px; background:linear-gradient(90deg,transparent,rgba(255,70,85,0.5)); }
.valo-suggest-label::after  { content:''; flex:1; height:1px; background:linear-gradient(90deg,rgba(0,212,191,0.5),transparent); }
.valo-suggest-label span {
  background:linear-gradient(90deg,var(--r2),var(--r));
  color:var(--w); font-family:'Barlow Condensed',sans-serif;
  font-size:12px; font-weight:800; letter-spacing:3px; text-transform:uppercase;
  padding:5px 20px;
  clip-path:polygon(10px 0,100% 0,calc(100% - 10px) 100%,0 100%);
  box-shadow:0 0 18px rgba(255,70,85,0.45),0 0 36px rgba(255,70,85,0.15);
}

/* ═══════════════════════════
   BUTTONS — dark teal, clearly visible text
═══════════════════════════ */
.stButton > button {
  /* Darker background so text pops */
  background:linear-gradient(90deg,rgba(0,60,55,0.88),rgba(6,12,22,0.96)) !important;
  color:#e0f8f5 !important;
  border:1px solid rgba(0,212,191,0.32) !important;
  border-left:3px solid var(--t) !important;
  clip-path:polygon(0 0,100% 0,100% calc(100% - 8px),calc(100% - 8px) 100%,0 100%) !important;
  border-radius:0 !important;
  font-family:'Barlow Condensed',sans-serif !important;
  font-size:clamp(12px,3vw,14px) !important; font-weight:700 !important; letter-spacing:.5px !important;
  padding:12px 14px !important; width:100% !important; text-align:left !important;
  white-space:normal !important; min-height:50px !important; line-height:1.45 !important;
  transition:all .15s ease !important;
  box-shadow:0 0 10px rgba(0,212,191,0.1),0 2px 10px rgba(0,0,0,0.7),inset 0 1px 0 rgba(0,212,191,0.06) !important;
  text-shadow:0 1px 4px rgba(0,0,0,0.6) !important;
}
.stButton > button:hover {
  background:linear-gradient(90deg,rgba(0,212,191,0.2),rgba(255,70,85,0.12)) !important;
  border-left-color:var(--r) !important; border-color:rgba(0,212,191,0.5) !important;
  color:#ffffff !important; transform:translateX(5px) !important;
  box-shadow:0 0 22px rgba(0,212,191,0.4),0 0 44px rgba(0,212,191,0.15),0 4px 16px rgba(0,0,0,0.7) !important;
  text-shadow:0 0 8px rgba(0,255,231,0.3) !important;
}

/* ═══════════════════════════
   AVATARS — sharp angular
═══════════════════════════ */
[data-testid="chatAvatarIcon-user"] {
  background:linear-gradient(135deg,#5c0e1a,#200508) !important;
  border:2px solid var(--r) !important; border-radius:0 !important;
  clip-path:polygon(0 0,100% 0,100% calc(100% - 9px),calc(100% - 9px) 100%,0 100%) !important;
  box-shadow:0 0 14px rgba(255,70,85,0.6),0 0 28px rgba(255,70,85,0.2) !important;
  overflow:hidden !important;
}
[data-testid="chatAvatarIcon-user"]>*{display:none !important;}
[data-testid="chatAvatarIcon-user"]::before{content:'';display:block;width:100%;height:100%;
  background:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 36 36'%3E%3Crect width='36' height='36' fill='%235c0e1a'/%3E%3Cpolygon points='18,3 31,10.5 31,25.5 18,33 5,25.5 5,10.5' fill='none' stroke='%23ff4655' stroke-width='1.8'/%3E%3Cpolygon points='18,9 25,13 25,23 18,27 11,23 11,13' fill='rgba(255,70,85,0.15)'/%3E%3Ctext x='18' y='22' text-anchor='middle' font-family='Rajdhani,sans-serif' font-size='9' font-weight='700' fill='%23ff8090' letter-spacing='0.5'%3EUSR%3C/text%3E%3Cline x1='5' y1='10.5' x2='11' y2='16.5' stroke='%23ff4655' stroke-width='0.8' opacity='0.5'/%3E%3Ccircle cx='18' cy='31' r='1.5' fill='%23ff4655'/%3E%3C/svg%3E") center/cover no-repeat !important;}

[data-testid="chatAvatarIcon-assistant"] {
  background:linear-gradient(135deg,#003c38,#000e0d) !important;
  border:2px solid var(--t) !important; border-radius:0 !important;
  clip-path:polygon(9px 0,100% 0,100% 100%,0 100%,0 9px) !important;
  box-shadow:0 0 14px rgba(0,212,191,0.6),0 0 28px rgba(0,212,191,0.2) !important;
  overflow:hidden !important;
}
[data-testid="chatAvatarIcon-assistant"]>*{display:none !important;}
[data-testid="chatAvatarIcon-assistant"]::before{content:'';display:block;width:100%;height:100%;
  background:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 36 36'%3E%3Crect width='36' height='36' fill='%23003c38'/%3E%3Cpolygon points='18,2 32,10 32,26 18,34 4,26 4,10' fill='none' stroke='%2300d4bf' stroke-width='1.8'/%3E%3Ccircle cx='18' cy='18' r='6.5' fill='none' stroke='%2300d4bf' stroke-width='1.2' opacity='0.8'/%3E%3Ccircle cx='18' cy='18' r='2.8' fill='%2300ffe7'/%3E%3Cline x1='18' y1='2' x2='18' y2='10' stroke='%2300d4bf' stroke-width='1' opacity='0.6'/%3E%3Cline x1='18' y1='26' x2='18' y2='34' stroke='%2300d4bf' stroke-width='1' opacity='0.6'/%3E%3Cline x1='4' y1='18' x2='11' y2='18' stroke='%2300d4bf' stroke-width='1' opacity='0.5'/%3E%3Cline x1='25' y1='18' x2='32' y2='18' stroke='%2300d4bf' stroke-width='1' opacity='0.5'/%3E%3C/svg%3E") center/cover no-repeat !important;}

/* ═══════════════════════════
   CHAT BUBBLES — Valorant panels
   Dark enough but NOT black
═══════════════════════════ */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
  background:
    radial-gradient(ellipse 80% 80% at 100% 50%, rgba(255,50,60,0.05) 0%, transparent 60%),
    linear-gradient(135deg,rgba(80,14,22,0.95) 0%,rgba(48,8,14,0.97) 40%,rgba(16,8,12,0.98) 100%) !important;
  border:1px solid rgba(255,70,85,0.35) !important;
  clip-path:polygon(0 0,calc(100% - 14px) 0,100% 14px,100% 100%,14px 100%,0 calc(100% - 14px)) !important;
  border-radius:0 !important;
  padding:15px 20px !important; margin:8px 0 !important;
  box-shadow:3px 0 20px rgba(255,70,85,0.1),0 4px 20px rgba(0,0,0,0.75) !important;
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
  background:
    radial-gradient(ellipse 80% 80% at 0% 50%, rgba(0,212,191,0.05) 0%, transparent 60%),
    linear-gradient(135deg,rgba(5,52,50,0.95) 0%,rgba(4,30,30,0.97) 40%,rgba(5,10,16,0.98) 100%) !important;
  border:1px solid rgba(0,212,191,0.28) !important;
  clip-path:polygon(14px 0,100% 0,100% calc(100% - 14px),calc(100% - 14px) 100%,0 100%,0 14px) !important;
  border-radius:0 !important;
  padding:15px 20px !important; margin:8px 0 !important;
  box-shadow:-3px 0 20px rgba(0,212,191,0.08),0 4px 20px rgba(0,0,0,0.75) !important;
}

/* ═══════════════════════════
   CHAT TEXT — high contrast
═══════════════════════════ */
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li {
  font-size:clamp(13.5px,3.8vw,15px) !important; line-height:1.82 !important;
  color:#f4ede7 !important; text-shadow:0 1px 6px rgba(0,0,0,0.95) !important;
}
[data-testid="stChatMessage"] h3 {
  font-family:'Rajdhani',sans-serif !important; font-size:clamp(14px,4vw,19px) !important;
  font-weight:700 !important; text-transform:uppercase !important; letter-spacing:2.5px !important;
  color:#ffffff !important; margin-bottom:8px !important; padding-bottom:6px !important;
  border-bottom:1px solid rgba(255,255,255,0.09) !important;
  text-shadow:0 0 14px rgba(255,255,255,0.12) !important;
}
[data-testid="stChatMessage"] strong { color:#ffbfc6 !important; font-weight:700 !important; text-shadow:0 0 8px rgba(255,70,85,0.3) !important; }
[data-testid="stChatMessage"] em { color:var(--t2) !important; font-style:normal !important; font-size:11px !important; }
[data-testid="stChatMessage"] code { background:rgba(0,212,191,0.13) !important; color:#70ffee !important;
  border:1px solid rgba(0,212,191,0.38) !important; border-radius:2px !important;
  padding:2px 7px !important; font-size:12px !important; }

/* ═══════════════════════════
   CHAT INPUT — FIXED TEXT VISIBILITY
   Critical: textarea text must be white/cream
═══════════════════════════ */
.stChatInput > div {
  background:linear-gradient(135deg,rgba(14,18,28,0.99),rgba(10,12,22,0.99)) !important;
  border:1px solid rgba(255,70,85,0.2) !important;
  clip-path:polygon(0 0,calc(100% - 10px) 0,100% 10px,100% 100%,0 100%) !important;
  border-radius:0 !important;
  box-shadow:0 0 18px rgba(255,70,85,0.06),0 4px 18px rgba(0,0,0,0.7) !important;
}
/* THE FIX: textarea itself */
.stChatInput textarea {
  background:transparent !important;
  color:#ece8e1 !important;             /* cream — clearly visible */
  -webkit-text-fill-color:#ece8e1 !important;
  border:none !important;
  border-bottom:2px solid rgba(255,70,85,0.28) !important;
  border-radius:0 !important;
  font-family:'Barlow',sans-serif !important;
  font-size:clamp(13px,3.5vw,14px) !important;
  caret-color:var(--r) !important;
  opacity:1 !important;
}
.stChatInput textarea:focus {
  border-bottom-color:var(--r) !important;
  box-shadow:0 3px 14px rgba(255,70,85,0.12) !important;
  color:#ece8e1 !important;
  -webkit-text-fill-color:#ece8e1 !important;
}
.stChatInput textarea::placeholder {
  color:rgba(236,232,225,0.28) !important;
  -webkit-text-fill-color:rgba(236,232,225,0.28) !important;
  font-style:italic !important;
}
/* Also target any child text inputs */
.stChatInput input {
  color:#ece8e1 !important;
  -webkit-text-fill-color:#ece8e1 !important;
}

/* ═══════════════════════════
   SIDEBAR
═══════════════════════════ */
section[data-testid="stSidebar"]{background:linear-gradient(180deg,#08090e,#0b0d16) !important;border-right:1px solid rgba(255,70,85,0.16) !important;}
section[data-testid="stSidebar"] p,section[data-testid="stSidebar"] span,section[data-testid="stSidebar"] div,section[data-testid="stSidebar"] small{color:#60625e !important;font-size:13px !important;}
section[data-testid="stSidebar"] h2{font-family:'Rajdhani',sans-serif !important;font-size:17px !important;color:var(--c) !important;text-transform:uppercase !important;letter-spacing:3px !important;}
section[data-testid="stSidebar"] .stButton>button{background:transparent !important;border:1px solid rgba(255,70,85,0.2) !important;border-left:2px solid var(--r) !important;color:#606060 !important;clip-path:polygon(0 0,100% 0,100% calc(100% - 6px),calc(100% - 6px) 100%,0 100%) !important;border-radius:0 !important;box-shadow:none !important;font-family:'Barlow Condensed',sans-serif !important;font-weight:700 !important;letter-spacing:1px !important;}
section[data-testid="stSidebar"] .stButton>button:hover{background:rgba(255,70,85,0.07) !important;color:var(--c) !important;transform:none !important;}

/* ═══════════════════════════
   SPINNER
═══════════════════════════ */
[data-testid="stSpinner"] p{color:var(--t) !important;font-family:'Barlow Condensed',sans-serif !important;letter-spacing:4px !important;font-size:11px !important;text-transform:uppercase !important;text-shadow:0 0 10px rgba(0,212,191,0.6) !important;}

/* ═══════════════════════════
   SCROLLBAR + misc
═══════════════════════════ */
::-webkit-scrollbar{width:4px;}
::-webkit-scrollbar-track{background:var(--bg);}
::-webkit-scrollbar-thumb{background:rgba(255,70,85,0.45);}
::-webkit-scrollbar-thumb:hover{background:var(--r);box-shadow:0 0 6px var(--r);}
#MainMenu,footer,header{visibility:hidden !important;}
.block-container{padding-top:1.2rem !important;padding-bottom:1.5rem !important;max-width:760px !important;}

@media(max-width:600px){
  .block-container{padding:.7rem .5rem 4.5rem !important;}
  .valo-author{position:relative !important;top:0 !important;justify-content:center !important;margin-bottom:8px !important;}
  .valo-author::before{display:none;}
  [data-testid="stChatMessage"]{padding:10px 14px !important;margin:4px 0 !important;}
  .stButton>button{min-height:46px !important;padding:10px 11px !important;}
  .valo-greeting{padding:16px 12px !important;}
}
</style>
""", unsafe_allow_html=True)

# ======================== GROQ ========================
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
def load_raw():
    if os.path.exists("database_pc.json"):
        with open("database_pc.json","r",encoding="utf-8") as f: return f.read()
    return "{}"

data_pc=load_db(); raw_json=load_raw()
db_loi=len(data_pc.get("loi_he_thong",[])); db_lk=len(data_pc.get("linh_kien_pc",[]))

# SIDEBAR
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

LVC="""<svg viewBox="0 0 52 52" xmlns="http://www.w3.org/2000/svg">
<defs>
  <linearGradient id="rg" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:#ff2233"/><stop offset="100%" style="stop-color:#ff4655"/></linearGradient>
  <linearGradient id="tg" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:#00d4bf"/><stop offset="100%" style="stop-color:#007a70"/></linearGradient>
  <filter id="glow"><feGaussianBlur stdDeviation="1.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
<polygon points="26,2 48,14 48,38 26,50 4,38 4,14" fill="rgba(255,30,50,0.09)" stroke="url(#rg)" stroke-width="2" filter="url(#glow)"/>
<polygon points="26,8 42,17 42,35 26,44 10,35 10,17" fill="rgba(0,212,191,0.06)" stroke="url(#tg)" stroke-width="1.2" opacity="0.75"/>
<line x1="4" y1="14" x2="16" y2="26" stroke="#ff4655" stroke-width="1.5" opacity="0.45"/>
<line x1="48" y1="38" x2="36" y2="26" stroke="#00d4bf" stroke-width="1.5" opacity="0.45"/>
<text x="26" y="32" text-anchor="middle" font-family="Rajdhani,sans-serif" font-size="13" font-weight="700" fill="white" letter-spacing="0.5" filter="url(#glow)">LVC</text>
<circle cx="26" cy="40" r="2" fill="#ff4655" opacity="0.85"/>
<circle cx="26" cy="40" r="4" fill="none" stroke="#ff4655" stroke-width="0.5" opacity="0.35"/>
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
<div class="valo-divider">
  <div class="valo-divider-inner"><div class="vd r"></div><div class="vdbar"></div><div class="vd t"></div></div>
</div>
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
    ("✕  Lỗi 0xc0000005 văng game","Game bị lỗi 0xc0000005 không mở được cách fix?"),
    ("✕  Lỗi 0xc000021a không boot","Máy báo lỗi 0xc000021a không boot được vào Windows"),
    ("⚠  PC tự reboot khi chơi game","PC tự reboot đột ngột trong lúc chơi game nặng"),
    ("▪  Không nhận chuột bàn phím USB","Cắm USB chuột bàn phím vào máy không nhận lỗi gì?"),
    ("◈  SSD NVMe không nhận trong BIOS","BIOS không nhận ổ SSD NVMe sau khi lắp mainboard"),
    ("◉  No Boot Device Found","Máy báo No Boot Device Found không vào được hệ điều hành"),
    ("🌡  CPU 95°C overheat","CPU nhiệt độ lên đến 95 độ C khi chạy game nguy hiểm không?"),
    ("◆  RAM 8GB đủ cho game 2024?","RAM 8GB có đủ dùng để chơi game hiện đại 2024 không?"),
    ("⚡  Nguồn bao nhiêu W cho RTX 3060?","RTX 3060 cần nguồn bao nhiêu W dùng 500W được không?"),
    ("◆  Tản nhiệt nước hay khí?","Nên dùng tản nhiệt nước hay khí cho i5-12400F?"),
    ("▶  SSD NVMe vs SSD SATA?","SSD NVMe và SATA khác nhau ở điểm gì nên mua loại nào?"),
    ("◉  2x8GB vs 1x16GB RAM?","Lắp 2 thanh 8GB hay 1 thanh 16GB thì nhanh hơn?"),
    ("◆  i5-12400F chơi game 2024?","i5-12400F hiệu năng thế nào chơi game 2024 đủ không?"),
    ("▶  i5 vs Ryzen 5 tầm 3-4 triệu","Tầm 3-4 triệu nên chọn Intel i5 hay AMD Ryzen 5?"),
    ("◈  i3-12100F + RTX 3060 bottleneck?","i3-12100F dùng với RTX 3060 có bị cổ chai không?"),
    ("⚡  Ryzen 5 5600X cần tản nhiệt rời?","Ryzen 5 5600X tản nhiệt box dùng được không?"),
    ("🎮  GTX 1650 chơi game gì 1080p?","GTX 1650 chơi mượt những game nào ở 1080p?"),
    ("▶  RTX 3060 vs RX 6600?","So sánh RTX 3060 và RX 6600 nên chọn card nào?"),
    ("◆  RTX 4060 đáng mua hơn RTX 3060?","RTX 4060 có đáng mua hơn RTX 3060 không?"),
    ("◉  iGPU Intel UHD đủ văn phòng?","Dùng Intel UHD Graphics cho văn phòng có đủ không?"),
    ("◆  H610 hay B660?","Mainboard H610 và B660 khác nhau thế nào nên mua loại nào?"),
    ("▪  Socket LGA1700 dùng CPU đời mấy?","Socket LGA1700 hỗ trợ CPU Intel đời mấy?"),
    ("◈  B550 dùng được Ryzen 5 5600X?","Mainboard B550 có tương thích Ryzen 5 5600X không?"),
    ("📱  Snapdragon 888 nóng máy?","Chip Snapdragon 888 bị nóng nhiều có phải lỗi không?"),
    ("📱  Dimensity 9200 vs Snap 8 Gen2","So sánh Dimensity 9200 với Snapdragon 8 Gen 2?"),
    ("📱  Apple A17 Pro mạnh cỡ nào?","Chip Apple A17 Pro mạnh đến đâu so Android cao cấp?"),
    ("⚡  Build PC 10 triệu chơi FHD","Gợi ý cấu hình 10 triệu chơi game Full HD mượt"),
    ("◆  i5-12400F + RTX 3060 combo?","Combo i5-12400F với RTX 3060 12GB có bottleneck không?"),
]
if not st.session_state.suggestions:
    st.session_state.suggestions=random.sample(ALL_S,4)

st.markdown(f"""
<div class="valo-greeting scan-wrap">
  <div class="valo-bracket tl"></div><div class="valo-bracket tr"></div>
  <div class="valo-bracket bl"></div><div class="valo-bracket br"></div>
  <div class="vg-topline"></div><div class="vg-leftline"></div>
  <div class="vg-cut-h"></div><div class="vg-cut-v"></div>
  <div class="vg-br-line"></div>
  <div class="vg-smoke-r"></div><div class="vg-smoke-t"></div>
  <div class="valo-vbar"></div>
  <div class="valo-status-row">
    <div class="valo-status-dot-wrap">
      <div class="valo-status-ring r1"></div>
      <div class="valo-status-ring r2"></div>
      <div class="valo-status-dot"></div>
    </div>
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

# Smoke particles on page
st.markdown("""<div class="smoke-1"></div><div class="smoke-2"></div><div class="smoke-3"></div>""", unsafe_allow_html=True)

st.markdown('<div class="valo-suggest-label"><span>CHỌN NHANH VẤN ĐỀ</span></div>', unsafe_allow_html=True)
col1,col2=st.columns(2,gap="small")
for i,(lb,qr) in enumerate(st.session_state.suggestions):
    with (col1 if i%2==0 else col2):
        if st.button(lb,key=f"s{i}"):
            st.session_state.greeted=True; st.session_state.pending_query=qr; st.rerun()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

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

def dtype(q):
    ql=q.lower()
    hw=["i3","i5","i7","i9","ryzen","gtx","rtx","rx","vga","card","cpu","ram","ssd","mainboard","main","nguồn","psu","tản nhiệt","socket","ddr","mua","so sánh","nên chọn","upgrade","nâng cấp","combo","build","cấu hình","snapdragon","dimensity","exynos","helio","chip","điện thoại","iphone","samsung","apple"]
    er=["lỗi","bsod","xanh","đen","bíp","crash","sập","đơ","treo","chậm","lag","không bật","không lên","restart","khởi động","update","0x","error","fix","sửa","boot","không nhận","không vào"]
    for w in hw:
        if w in ql: return "hw"
    for w in er:
        if w in ql: return "err"
    return "gen"

BR="KHÔNG dùng: 'AI','LLM','Groq','Meta','Llama','trí tuệ nhân tạo'. Đọc KỸ câu hỏi. Trả lời ĐÚNG và ĐỦ."
PE=f"Bạn là hệ thống chẩn đoán lỗi của Lê Văn Chung 10A4.\n{BR}\nKho:{raw_json}\nQUY TẮC: 1 câu nguyên nhân + ≤4 bước ngắn + 1 tip. Không dài dòng."
PH=f"Bạn là chuyên gia tư vấn linh kiện PC của Lê Văn Chung 10A4.\n{BR}\nKho:{raw_json}\nQUY TẮC: Thông số quan trọng, so sánh nếu cần, gợi ý combo, kết 1 khuyến nghị. Mở đầu: 'Dựa trên cơ sở dữ liệu kỹ thuật của tác giả Lê Văn Chung 10A4...'"
PG=f"Bạn là hệ thống hỗ trợ kỹ thuật của Lê Văn Chung 10A4.\n{BR}\nKho:{raw_json}\nTrả lời tiếng Việt, súc tích."

def ask(uq,ch):
    t=dtype(uq)
    if t=="err": sy,mt,tp=PE,500,0.3
    elif t=="hw": sy,mt,tp=PH,800,0.5
    else: sy,mt,tp=PG,600,0.4
    ms=[{"role":"system","content":sy}]
    for m in ch[-6:]: ms.append({"role":m["role"],"content":m["content"]})
    ms.append({"role":"user","content":uq})
    r=client.chat.completions.create(model="llama-3.3-70b-versatile",messages=ms,max_tokens=mt,temperature=tp)
    return r.choices[0].message.content

def handle(p):
    st.session_state.messages.append({"role":"user","content":p})
    with st.chat_message("user"): st.markdown(p)
    with st.chat_message("assistant"):
        with st.spinner("ĐANG PHÂN TÍCH DỮ LIỆU..."):
            try:
                a=search_db(p) or ask(p,st.session_state.messages)
                st.markdown(a)
                st.session_state.messages.append({"role":"assistant","content":a})
            except: st.error("❌ Hệ thống gián đoạn.")

if st.session_state.pending_query:
    q=st.session_state.pending_query; st.session_state.pending_query=None; handle(q)
if p:=st.chat_input("Nhập mã lỗi hoặc linh kiện cần phân tích..."):
    st.session_state.greeted=True; handle(p)