import streamlit as st
import json, re, os, random
from groq import Groq

st.set_page_config(page_title="PC Solving — LVC 10A4", page_icon="⚡", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Barlow+Condensed:wght@400;600;700;800&family=Barlow:wght@300;400;500&display=swap');

:root {
  --r:#ff4655; --r2:#ff2233; --r3:rgba(255,70,85,0.18);
  --t:#00d4bf; --t2:#00ffe7; --t3:rgba(0,212,191,0.15);
  --g:#e8c97a; --p:#bd93f9;
  --bg:#0a0c12; --bg1:#0f1320; --bg2:#151929; --bg3:#1c2236;
  --w:#ffffff; --c:#ece8e1; --s:#b8b4ac; --d:#3e4252;
}
html,body,.stApp { background:var(--bg) !important; color:var(--c) !important; font-family:'Barlow',sans-serif !important; }

/* ═══════════════════════════════════════
   1. BACKGROUND — visible diagonal grid
═══════════════════════════════════════ */
.stApp::before {
  content:''; position:fixed; inset:0; pointer-events:none; z-index:0;
  background:
    radial-gradient(ellipse 65% 55% at -10% -10%, rgba(255,70,85,0.16) 0%, transparent 60%),
    radial-gradient(ellipse 65% 55% at 110% 110%, rgba(0,212,191,0.13) 0%, transparent 60%),
    radial-gradient(ellipse 40% 30% at 110% 0%,   rgba(189,147,249,0.07) 0%, transparent 55%),
    /* VISIBLE GRID */
    linear-gradient(rgba(255,70,85,0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,70,85,0.04) 1px, transparent 1px),
    /* Slash overlays */
    repeating-linear-gradient(-52deg, transparent 0, transparent 80px, rgba(255,70,85,0.028) 80px, rgba(255,70,85,0.028) 81px),
    repeating-linear-gradient( 38deg, transparent 0, transparent 120px, rgba(0,212,191,0.018) 120px, rgba(0,212,191,0.018) 121px);
  background-size: auto, auto, auto, 40px 40px, 40px 40px, auto, auto;
}

/* ═══════════════════════════════════════
   2. TOP NEON BAR (brighter, taller)
═══════════════════════════════════════ */
.stApp::after {
  content:''; position:fixed; top:0; left:0; right:0; height:4px; z-index:9999;
  background:linear-gradient(90deg, var(--r2) 0%, var(--r) 100px, var(--g) 50%, var(--t) calc(100% - 100px), var(--t2) 100%);
  box-shadow: 0 0 16px rgba(255,70,85,0.8), 0 0 32px rgba(255,70,85,0.3), 0 2px 8px rgba(0,212,191,0.3);
}

/* ═══════════════════════════════════════
   3. SCAN LINE sweep animation
═══════════════════════════════════════ */
.scan-wrap { position:relative; overflow:hidden; }
.scan-wrap::after {
  content:''; position:absolute; top:-100%; left:0; right:0; height:40%;
  background:linear-gradient(180deg, transparent 0%, rgba(0,212,191,0.04) 50%, transparent 100%);
  animation: scanDown 5s linear infinite; pointer-events:none; z-index:1;
}
@keyframes scanDown { 0%{top:-40%} 100%{top:120%} }

/* ═══════════════════════════════════════
   4. AUTHOR — neon teal
═══════════════════════════════════════ */
.valo-header { text-align:center; padding:10px 0 2px; position:relative; }
.valo-author {
  font-family:'Barlow Condensed',sans-serif; font-size:11px; font-weight:700;
  letter-spacing:3px; text-transform:uppercase; color:var(--t2);
  text-shadow:0 0 12px rgba(0,255,231,0.8), 0 0 24px rgba(0,255,231,0.3);
  text-align:right; margin-bottom:4px;
  display:flex; align-items:center; justify-content:flex-end; gap:6px;
}
.valo-author::before { content:''; width:24px; height:1px;
  background:linear-gradient(90deg,transparent,var(--t2));
  box-shadow:0 0 6px var(--t2); }

/* ═══════════════════════════════════════
   5. EYEBROW
═══════════════════════════════════════ */
.valo-eyebrow {
  font-family:'Barlow Condensed',sans-serif; font-size:clamp(9px,2vw,11px);
  font-weight:800; letter-spacing:7px; color:var(--r); text-transform:uppercase;
  margin-bottom:6px; display:flex; align-items:center; justify-content:center; gap:12px;
  text-shadow:0 0 16px rgba(255,70,85,0.9);
}
.valo-eyebrow::before { content:''; width:40px; height:1px;
  background:linear-gradient(90deg,transparent,var(--r));
  box-shadow:0 0 8px rgba(255,70,85,0.6); }
.valo-eyebrow::after  { content:''; width:40px; height:1px;
  background:linear-gradient(90deg,var(--r),transparent);
  box-shadow:0 0 8px rgba(255,70,85,0.6); }

/* ═══════════════════════════════════════
   6. LOGO + TITLE
═══════════════════════════════════════ */
.valo-logo-wrap { display:flex; align-items:center; justify-content:center; gap:16px; margin-bottom:4px; }
.lvc-logo { width:clamp(40px,7vw,56px); height:clamp(40px,7vw,56px); flex-shrink:0;
  filter:drop-shadow(0 0 10px rgba(255,70,85,0.7)) drop-shadow(0 0 20px rgba(255,70,85,0.3)); }
.lvc-logo svg { width:100%; height:100%; }
.valo-title {
  font-family:'Rajdhani',sans-serif;
  font-size:clamp(30px,8vw,68px); font-weight:700;
  letter-spacing:3px; line-height:1; text-transform:uppercase; margin:0;
  color:var(--w); text-shadow:0 0 30px rgba(255,255,255,0.12), 0 2px 8px rgba(0,0,0,0.95);
}
.valo-title .red { color:var(--r); text-shadow:0 0 20px rgba(255,70,85,0.9),0 0 40px rgba(255,70,85,0.4); }
.valo-title .slash { color:var(--r); opacity:.5; margin:0 3px; }

/* ═══════════════════════════════════════
   7. SUBTITLE — 3 colored words
═══════════════════════════════════════ */
.valo-subtitle {
  font-family:'Barlow Condensed',sans-serif; font-size:clamp(11px,2.8vw,14px);
  font-weight:800; letter-spacing:5px; text-transform:uppercase; margin-top:8px;
  display:flex; align-items:center; justify-content:center; gap:8px; flex-wrap:wrap;
}
.sub-r { color:var(--r);  text-shadow:0 0 12px rgba(255,70,85,0.8); }
.sub-w { color:var(--w);  text-shadow:0 0 8px rgba(255,255,255,0.25); }
.sub-t { color:var(--t);  text-shadow:0 0 12px rgba(0,212,191,0.8); }
.sub-d { display:inline-block; width:5px; height:5px; transform:rotate(45deg); }
.sub-d.r { background:var(--r); box-shadow:0 0 8px var(--r), 0 0 16px rgba(255,70,85,0.4); }
.sub-d.t { background:var(--t); box-shadow:0 0 8px var(--t), 0 0 16px rgba(0,212,191,0.4); }

/* ═══════════════════════════════════════
   8. DIVIDER — visible with glow
═══════════════════════════════════════ */
.valo-divider { display:flex; align-items:center; margin:12px 0 8px; }
.valo-divider::before,.valo-divider::after { content:''; flex:1; height:1px; background:rgba(255,255,255,0.08); }
.valo-divider-inner { display:flex; align-items:center; gap:6px; padding:0 14px; }
.vd { width:6px; height:6px; transform:rotate(45deg); }
.vd.r { background:var(--r); box-shadow:0 0 10px var(--r), 0 0 20px rgba(255,70,85,0.5); }
.vd.t { background:var(--t); width:5px; height:5px; box-shadow:0 0 10px var(--t), 0 0 20px rgba(0,212,191,0.5); }
.vdbar {
  width:60px; height:2px;
  background:linear-gradient(90deg,var(--r),var(--g),var(--t));
  clip-path:polygon(6px 0%,100% 0%,calc(100% - 6px) 100%,0% 100%);
  box-shadow:0 0 10px rgba(0,212,191,0.5), 0 0 6px rgba(255,70,85,0.4);
}

/* ═══════════════════════════════════════
   9. CORNER BRACKETS — Valorant UI detail
═══════════════════════════════════════ */
.valo-bracket {
  position:absolute; width:14px; height:14px;
}
.valo-bracket.tl { top:6px; left:6px;
  border-top:2px solid var(--r); border-left:2px solid var(--r);
  box-shadow:-2px -2px 8px rgba(255,70,85,0.4); }
.valo-bracket.tr { top:6px; right:6px;
  border-top:2px solid var(--t); border-right:2px solid var(--t);
  box-shadow:2px -2px 8px rgba(0,212,191,0.4); }
.valo-bracket.bl { bottom:6px; left:6px;
  border-bottom:2px solid var(--t); border-left:2px solid var(--t);
  box-shadow:-2px 2px 8px rgba(0,212,191,0.4); }
.valo-bracket.br { bottom:6px; right:6px;
  border-bottom:2px solid var(--r); border-right:2px solid var(--r);
  box-shadow:2px 2px 8px rgba(255,70,85,0.4); }

/* ═══════════════════════════════════════
   10. GREETING BOX — CLIP-PATH cut + aura
═══════════════════════════════════════ */
.valo-greeting {
  position:relative;
  background:linear-gradient(135deg, rgba(42,10,16,0.97) 0%, rgba(16,20,34,0.98) 50%, rgba(6,28,30,0.97) 100%);
  /* Sharp diagonal cut top-left AND bottom-right */
  clip-path: polygon(22px 0%, 100% 0%, 100% calc(100% - 16px), calc(100% - 16px) 100%, 0% 100%, 0% 22px);
  padding:clamp(18px,5vw,28px) clamp(16px,5vw,28px) clamp(14px,4vw,22px);
  margin:4px 0 14px; overflow:hidden;
  /* AURA breathing */
  box-shadow:
    0 0 50px rgba(255,70,85,0.15),
    0 0 100px rgba(255,70,85,0.06),
    0 0 50px rgba(0,212,191,0.06),
    0 8px 40px rgba(0,0,0,0.8);
  animation:greetAura 4s ease-in-out infinite;
  border:1px solid rgba(255,70,85,0.3);
}
@keyframes greetAura {
  0%,100%{ box-shadow:0 0 50px rgba(255,70,85,0.15),0 0 100px rgba(255,70,85,0.06),0 8px 40px rgba(0,0,0,0.8); }
  50%    { box-shadow:0 0 70px rgba(255,70,85,0.22),0 0 120px rgba(0,212,191,0.08),0 8px 40px rgba(0,0,0,0.8); }
}

/* Red top border on clip-path box */
.vg-topline {
  position:absolute; top:0; left:22px; right:0; height:2px;
  background:linear-gradient(90deg,var(--r),rgba(255,70,85,0.3));
  box-shadow:0 0 12px rgba(255,70,85,0.7);
}
.vg-leftline {
  position:absolute; left:0; top:22px; bottom:0; width:2px;
  background:linear-gradient(180deg,var(--r),rgba(0,212,191,0.3));
  box-shadow:0 0 10px rgba(255,70,85,0.5);
}
/* Inner teal accent line */
.vg-inner-tl {
  position:absolute; top:22px; left:22px; width:30px; height:1px;
  background:var(--t); opacity:0.5; box-shadow:0 0 6px var(--t);
}
.vg-inner-tl2 {
  position:absolute; top:22px; left:22px; width:1px; height:20px;
  background:var(--t); opacity:0.4; box-shadow:0 0 6px var(--t);
}
/* Teal glow bottom-right */
.vg-glow-br { position:absolute; bottom:-50px; right:-50px; width:220px; height:220px;
  background:radial-gradient(circle,rgba(0,212,191,0.1) 0%,transparent 65%); pointer-events:none; }
/* Red glow top-center */
.vg-glow-tc { position:absolute; top:-20px; left:30%; right:30%; height:60px;
  background:radial-gradient(ellipse,rgba(255,70,85,0.1) 0%,transparent 70%); pointer-events:none; }
/* Left gradient bar */
.valo-vbar { position:absolute; left:2px; top:22px; bottom:0; width:3px;
  background:linear-gradient(180deg,var(--r) 0%,var(--g) 45%,var(--t) 80%,transparent 100%);
  box-shadow:0 0 10px rgba(255,70,85,0.5); opacity:.9; }

.valo-status-row { display:flex; align-items:center; justify-content:center; gap:7px; margin-bottom:12px; }
.valo-status-dot { width:8px; height:8px; background:var(--t); border-radius:50%;
  box-shadow:0 0 14px var(--t),0 0 6px var(--t2); animation:blink 2s infinite; }
@keyframes blink { 0%,100%{opacity:1;box-shadow:0 0 14px var(--t);}50%{opacity:.3;box-shadow:0 0 4px var(--t);} }
.valo-status-text { font-family:'Barlow Condensed',sans-serif; font-size:10px; font-weight:700;
  letter-spacing:3px; color:var(--t2); text-transform:uppercase;
  text-shadow:0 0 12px rgba(0,255,231,0.7); }
.valo-greeting-icon { font-size:clamp(28px,5vw,36px); display:block; text-align:center; margin-bottom:10px;
  filter:drop-shadow(0 0 18px rgba(255,70,85,0.9));
  animation:iconGlow 3s ease-in-out infinite; }
@keyframes iconGlow { 0%,100%{filter:drop-shadow(0 0 18px rgba(255,70,85,0.9));} 50%{filter:drop-shadow(0 0 28px rgba(255,150,70,1));} }
.valo-greeting-title { font-family:'Rajdhani',sans-serif; font-size:clamp(15px,4vw,22px); font-weight:700;
  color:var(--w); text-align:center; text-transform:uppercase; letter-spacing:2px; margin-bottom:8px; }
.valo-greeting-sub { font-size:clamp(12px,3vw,13.5px); color:var(--s); text-align:center; line-height:1.7; }
.valo-stats { display:flex; justify-content:center; gap:clamp(12px,3vw,28px);
  margin-top:14px; padding-top:12px; border-top:1px solid rgba(255,255,255,0.07); }
.valo-stat { text-align:center; line-height:1.2; }
.valo-stat-num { font-family:'Rajdhani',sans-serif; font-size:clamp(18px,4vw,24px);
  font-weight:700; color:var(--r); display:block;
  text-shadow:0 0 16px rgba(255,70,85,0.7); }
.valo-stat-label { font-family:'Barlow Condensed',sans-serif; font-size:9px;
  letter-spacing:2px; color:var(--d); text-transform:uppercase; }
.valo-stat-div { width:1px; background:rgba(255,255,255,0.1); align-self:stretch; }

/* ═══════════════════════════════════════
   11. SUGGEST LABEL — bright red badge
═══════════════════════════════════════ */
.valo-suggest-label { display:flex; align-items:center; gap:10px; margin:10px 0 12px; }
.valo-suggest-label::before { content:''; flex:1; height:1px; background:linear-gradient(90deg,transparent,rgba(255,70,85,0.6)); box-shadow:0 0 6px rgba(255,70,85,0.3); }
.valo-suggest-label::after  { content:''; flex:1; height:1px; background:linear-gradient(90deg,rgba(0,212,191,0.6),transparent); box-shadow:0 0 6px rgba(0,212,191,0.3); }
.valo-suggest-label span {
  background:linear-gradient(90deg,var(--r2),var(--r));
  color:var(--w); font-family:'Barlow Condensed',sans-serif;
  font-size:12px; font-weight:800; letter-spacing:3px; text-transform:uppercase;
  padding:5px 20px;
  clip-path:polygon(10px 0, 100% 0, calc(100% - 10px) 100%, 0 100%);
  box-shadow:0 0 24px rgba(255,70,85,0.6),0 0 48px rgba(255,70,85,0.2);
}

/* ═══════════════════════════════════════
   12. BUTTONS — teal dark + glow on hover
═══════════════════════════════════════ */
.stButton > button {
  background:linear-gradient(90deg,rgba(0,55,50,0.8),rgba(8,14,24,0.95)) !important;
  color:#d4f8f4 !important;
  border:1px solid rgba(0,212,191,0.3) !important;
  border-left:3px solid var(--t) !important;
  /* Sharp cut bottom-right */
  clip-path:polygon(0 0, 100% 0, 100% calc(100% - 8px), calc(100% - 8px) 100%, 0 100%) !important;
  border-radius:0 !important;
  font-family:'Barlow Condensed',sans-serif !important;
  font-size:clamp(12px,3vw,14px) !important; font-weight:700 !important; letter-spacing:.5px !important;
  padding:11px 14px !important; width:100% !important; text-align:left !important;
  white-space:normal !important; min-height:48px !important; line-height:1.4 !important;
  transition:all .15s ease !important;
  box-shadow:0 0 14px rgba(0,212,191,0.14),0 2px 8px rgba(0,0,0,0.6) !important;
}
.stButton > button:hover {
  background:linear-gradient(90deg,rgba(0,212,191,0.22),rgba(255,70,85,0.14)) !important;
  border-left-color:var(--r) !important; border-color:rgba(0,212,191,0.5) !important;
  color:var(--w) !important; transform:translateX(5px) !important;
  box-shadow:0 0 28px rgba(0,212,191,0.5),0 0 56px rgba(0,212,191,0.2),0 4px 16px rgba(0,0,0,0.6) !important;
}

/* ═══════════════════════════════════════
   13. USER AVATAR — glowing red
═══════════════════════════════════════ */
[data-testid="chatAvatarIcon-user"] {
  background:linear-gradient(135deg,#5c0e1a,#1e050a) !important;
  border:2px solid var(--r) !important; border-radius:0 !important;
  clip-path:polygon(0 0,100% 0,100% calc(100% - 8px),calc(100% - 8px) 100%,0 100%) !important;
  box-shadow:0 0 18px rgba(255,70,85,0.8),0 0 36px rgba(255,70,85,0.3) !important;
  overflow:hidden !important;
}
[data-testid="chatAvatarIcon-user"] > * { display:none !important; }
[data-testid="chatAvatarIcon-user"]::before {
  content:'';
  display:block; width:100%; height:100%;
  background:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 36 36'%3E%3Crect width='36' height='36' fill='%235c0e1a'/%3E%3Cpolygon points='18,3 31,10.5 31,25.5 18,33 5,25.5 5,10.5' fill='none' stroke='%23ff4655' stroke-width='1.8'/%3E%3Cpolygon points='18,9 25,13 25,23 18,27 11,23 11,13' fill='rgba(255,70,85,0.15)'/%3E%3Ctext x='18' y='22' text-anchor='middle' font-family='Rajdhani,sans-serif' font-size='9' font-weight='700' fill='%23ff7080' letter-spacing='0.5'%3EUSR%3C/text%3E%3Cline x1='5' y1='10.5' x2='12' y2='17.5' stroke='%23ff4655' stroke-width='0.8' opacity='0.5'/%3E%3Ccircle cx='18' cy='31' r='1.5' fill='%23ff4655'/%3E%3C/svg%3E") center/cover no-repeat !important;
}

/* ═══════════════════════════════════════
   14. BOT AVATAR — glowing teal
═══════════════════════════════════════ */
[data-testid="chatAvatarIcon-assistant"] {
  background:linear-gradient(135deg,#003c38,#000e0d) !important;
  border:2px solid var(--t) !important; border-radius:0 !important;
  clip-path:polygon(8px 0,100% 0,100% 100%,0 100%,0 8px) !important;
  box-shadow:0 0 18px rgba(0,212,191,0.8),0 0 36px rgba(0,212,191,0.3) !important;
  overflow:hidden !important;
}
[data-testid="chatAvatarIcon-assistant"] > * { display:none !important; }
[data-testid="chatAvatarIcon-assistant"]::before {
  content:'';
  display:block; width:100%; height:100%;
  background:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 36 36'%3E%3Crect width='36' height='36' fill='%23003c38'/%3E%3Cpolygon points='18,2 32,10 32,26 18,34 4,26 4,10' fill='none' stroke='%2300d4bf' stroke-width='1.8'/%3E%3Ccircle cx='18' cy='18' r='6.5' fill='none' stroke='%2300d4bf' stroke-width='1.2' opacity='0.8'/%3E%3Ccircle cx='18' cy='18' r='2.8' fill='%2300ffe7'/%3E%3Cline x1='18' y1='2' x2='18' y2='10' stroke='%2300d4bf' stroke-width='1' opacity='0.6'/%3E%3Cline x1='18' y1='26' x2='18' y2='34' stroke='%2300d4bf' stroke-width='1' opacity='0.6'/%3E%3Cline x1='4' y1='18' x2='11' y2='18' stroke='%2300d4bf' stroke-width='1' opacity='0.5'/%3E%3Cline x1='25' y1='18' x2='32' y2='18' stroke='%2300d4bf' stroke-width='1' opacity='0.5'/%3E%3C/svg%3E") center/cover no-repeat !important;
}

/* ═══════════════════════════════════════
   15. USER BUBBLE — red cut panel
═══════════════════════════════════════ */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
  background:linear-gradient(135deg,rgba(95,16,24,0.97) 0%,rgba(55,8,14,0.98) 45%,rgba(18,6,10,0.99) 100%) !important;
  border:1px solid rgba(255,70,85,0.4) !important;
  /* SHARP CUTS on corners */
  clip-path:polygon(0 0,calc(100% - 16px) 0,100% 16px,100% 100%,16px 100%,0 calc(100% - 16px)) !important;
  border-radius:0 !important;
  padding:16px 20px !important; margin:8px 0 !important;
  box-shadow:4px 0 28px rgba(255,70,85,0.18),0 0 50px rgba(255,70,85,0.06),0 4px 20px rgba(0,0,0,0.8) !important;
  position:relative !important;
}

/* ═══════════════════════════════════════
   16. BOT BUBBLE — teal cut panel
═══════════════════════════════════════ */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
  background:linear-gradient(135deg,rgba(5,58,55,0.97) 0%,rgba(4,32,32,0.98) 45%,rgba(5,10,16,0.99) 100%) !important;
  border:1px solid rgba(0,212,191,0.35) !important;
  clip-path:polygon(16px 0,100% 0,100% calc(100% - 16px),calc(100% - 16px) 100%,0 100%,0 16px) !important;
  border-radius:0 !important;
  padding:16px 20px !important; margin:8px 0 !important;
  box-shadow:-4px 0 28px rgba(0,212,191,0.14),0 0 50px rgba(0,212,191,0.05),0 4px 20px rgba(0,0,0,0.8) !important;
}

/* ═══════════════════════════════════════
   17. CHAT TEXT — bright
═══════════════════════════════════════ */
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li {
  font-size:clamp(13.5px,3.8vw,15px) !important; line-height:1.82 !important;
  color:#f3ede7 !important; text-shadow:0 1px 6px rgba(0,0,0,0.95) !important;
}
[data-testid="stChatMessage"] h3 {
  font-family:'Rajdhani',sans-serif !important;
  font-size:clamp(14px,4vw,19px) !important; font-weight:700 !important;
  text-transform:uppercase !important; letter-spacing:2.5px !important;
  color:var(--w) !important; margin-bottom:8px !important; padding-bottom:6px !important;
  border-bottom:1px solid rgba(255,255,255,0.1) !important;
  text-shadow:0 0 16px rgba(255,255,255,0.15) !important;
}
[data-testid="stChatMessage"] strong { color:#ffc0c8 !important; font-weight:700 !important; text-shadow:0 0 10px rgba(255,70,85,0.4) !important; }
[data-testid="stChatMessage"] em { color:var(--t2) !important; font-style:normal !important; font-size:11px !important; text-shadow:0 0 8px rgba(0,255,231,0.5) !important; }
[data-testid="stChatMessage"] code { background:rgba(0,212,191,0.13) !important; color:#70ffee !important;
  border:1px solid rgba(0,212,191,0.4) !important; border-radius:2px !important;
  padding:2px 7px !important; font-size:12px !important;
  text-shadow:0 0 6px rgba(0,255,231,0.3) !important; }

/* ═══════════════════════════════════════
   18. CHAT INPUT — styled
═══════════════════════════════════════ */
.stChatInput > div {
  background:linear-gradient(135deg,rgba(18,22,34,0.99),rgba(12,16,26,0.99)) !important;
  border:1px solid rgba(255,70,85,0.22) !important;
  clip-path:polygon(0 0,calc(100% - 10px) 0,100% 10px,100% 100%,0 100%) !important;
  border-radius:0 !important;
  box-shadow:0 0 24px rgba(255,70,85,0.08),0 4px 20px rgba(0,0,0,0.7) !important;
}
.stChatInput textarea {
  background:transparent !important; color:var(--c) !important;
  border:none !important; border-bottom:2px solid rgba(255,70,85,0.35) !important;
  border-radius:0 !important; font-family:'Barlow',sans-serif !important;
  font-size:clamp(13px,3.5vw,14px) !important; caret-color:var(--r) !important;
}
.stChatInput textarea:focus { border-bottom-color:var(--r) !important; box-shadow:0 3px 16px rgba(255,70,85,0.15) !important; }
.stChatInput textarea::placeholder { color:#30333e !important; font-style:italic !important; }

/* ═══════════════════════════════════════
   19. SIDEBAR
═══════════════════════════════════════ */
section[data-testid="stSidebar"] { background:linear-gradient(180deg,#090c13,#0b0f1a) !important; border-right:1px solid rgba(255,70,85,0.2) !important; }
section[data-testid="stSidebar"] p,section[data-testid="stSidebar"] span,section[data-testid="stSidebar"] div,section[data-testid="stSidebar"] small { color:#68645e !important; font-size:13px !important; }
section[data-testid="stSidebar"] h2 { font-family:'Rajdhani',sans-serif !important; font-size:17px !important; color:var(--c) !important; text-transform:uppercase !important; letter-spacing:3px !important; }
section[data-testid="stSidebar"] .stButton > button {
  background:transparent !important; border:1px solid rgba(255,70,85,0.22) !important;
  border-left:2px solid var(--r) !important; color:#68645e !important;
  clip-path:polygon(0 0,100% 0,100% calc(100% - 6px),calc(100% - 6px) 100%,0 100%) !important;
  border-radius:0 !important; box-shadow:none !important;
  font-family:'Barlow Condensed',sans-serif !important; font-weight:700 !important; letter-spacing:1px !important;
}
section[data-testid="stSidebar"] .stButton > button:hover { background:rgba(255,70,85,0.08) !important; color:var(--c) !important; transform:none !important; }

/* ═══════════════════════════════════════
   20. SPINNER + scrollbar + misc
═══════════════════════════════════════ */
[data-testid="stSpinner"] p { color:var(--t) !important; font-family:'Barlow Condensed',sans-serif !important; letter-spacing:4px !important; font-size:11px !important; text-transform:uppercase !important; text-shadow:0 0 12px rgba(0,212,191,0.7) !important; }
::-webkit-scrollbar { width:4px; }
::-webkit-scrollbar-track { background:var(--bg); }
::-webkit-scrollbar-thumb { background:rgba(255,70,85,0.5); }
::-webkit-scrollbar-thumb:hover { background:var(--r); box-shadow:0 0 6px var(--r); }
#MainMenu,footer,header { visibility:hidden !important; }
.block-container { padding-top:1.2rem !important; padding-bottom:1.5rem !important; max-width:760px !important; }

@media(max-width:600px){
  .block-container{padding:.7rem .5rem 4.5rem !important;}
  .valo-author{position:relative !important;top:0 !important;justify-content:center !important;margin-bottom:8px !important;}
  .valo-author::before{display:none;}
  [data-testid="stChatMessage"]{padding:10px 14px !important;margin:4px 0 !important;}
  .stButton > button{min-height:44px !important;padding:9px 11px !important;}
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

# ======================== SIDEBAR ========================
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

# ======================== LVC SVG ========================
LVC = """<svg viewBox="0 0 52 52" xmlns="http://www.w3.org/2000/svg">
<defs>
  <linearGradient id="rg" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:#ff2233"/><stop offset="100%" style="stop-color:#ff4655"/></linearGradient>
  <linearGradient id="tg" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:#00d4bf"/><stop offset="100%" style="stop-color:#007a70"/></linearGradient>
  <filter id="glow"><feGaussianBlur stdDeviation="1.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
<polygon points="26,2 48,14 48,38 26,50 4,38 4,14" fill="rgba(255,30,50,0.1)" stroke="url(#rg)" stroke-width="2" filter="url(#glow)"/>
<polygon points="26,8 42,17 42,35 26,44 10,35 10,17" fill="rgba(0,212,191,0.06)" stroke="url(#tg)" stroke-width="1.2" opacity="0.8"/>
<line x1="4" y1="14" x2="16" y2="26" stroke="#ff4655" stroke-width="1.5" opacity="0.5"/>
<line x1="48" y1="38" x2="36" y2="26" stroke="#00d4bf" stroke-width="1.5" opacity="0.5"/>
<text x="26" y="32" text-anchor="middle" font-family="Rajdhani,sans-serif" font-size="13" font-weight="700" fill="white" letter-spacing="0.5" filter="url(#glow)">LVC</text>
<circle cx="26" cy="40" r="2" fill="#ff4655" opacity="0.9"/>
<circle cx="26" cy="40" r="4" fill="none" stroke="#ff4655" stroke-width="0.5" opacity="0.4"/>
</svg>"""

# ======================== HEADER ========================
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

# ======================== SESSION ========================
if "messages"      not in st.session_state: st.session_state.messages=[]
if "greeted"       not in st.session_state: st.session_state.greeted=False
if "suggestions"   not in st.session_state: st.session_state.suggestions=[]
if "pending_query" not in st.session_state: st.session_state.pending_query=None

ALL_S=[
    ("⚠  Màn hình xanh BSOD đột ngột",       "Máy tính bị màn hình xanh chết đột ngột, phải làm gì?"),
    ("▪  Màn hình đen không có tín hiệu",      "Máy lên nguồn nhưng màn hình đen, không có tín hiệu"),
    ("◈  PC bíp dài khi khởi động",            "Máy bíp dài liên tục khi bật, không vào được Windows"),
    ("◉  Windows boot loop liên tục",          "Máy cứ khởi động lại liên tục không vào được Windows"),
    ("✕  Lỗi 0xc0000005 văng game",            "Game bị lỗi 0xc0000005 không mở được cách fix?"),
    ("✕  Lỗi 0xc000021a không boot",           "Máy báo lỗi 0xc000021a không boot được vào Windows"),
    ("⚠  PC tự reboot khi chơi game nặng",     "PC tự reboot đột ngột trong lúc chơi game nặng"),
    ("▪  Không nhận chuột bàn phím USB",       "Cắm USB chuột bàn phím vào máy không nhận lỗi gì?"),
    ("◈  SSD NVMe không nhận trong BIOS",      "BIOS không nhận ổ SSD NVMe sau khi lắp vào mainboard"),
    ("◉  No Boot Device Found khi bật",        "Máy báo No Boot Device Found không vào được hệ điều hành"),
    ("🌡  CPU 95°C overheat nghiêm trọng",     "CPU nhiệt độ lên đến 95 độ C khi chạy game nguy hiểm không?"),
    ("◆  RAM 8GB đủ cho game 2024?",           "RAM 8GB có đủ dùng để chơi game hiện đại 2024 không?"),
    ("⚡  Nguồn bao nhiêu W cho RTX 3060?",    "RTX 3060 cần nguồn bao nhiêu W dùng nguồn 500W được không?"),
    ("◆  Tản nhiệt nước hay khí?",             "Nên dùng tản nhiệt nước hay khí cho i5-12400F?"),
    ("▶  SSD NVMe vs SSD SATA khác gì?",       "SSD NVMe và SATA khác nhau ở điểm gì nên mua loại nào?"),
    ("◉  2x8GB vs 1x16GB RAM cái nào nhanh?",  "Lắp 2 thanh RAM 8GB hay 1 thanh 16GB thì nhanh hơn?"),
    ("◆  i5-12400F chơi game 2024 đủ không?",  "i5-12400F hiệu năng thế nào chơi game 2024 có đủ không?"),
    ("▶  i5 vs Ryzen 5 tầm 3-4 triệu",        "Tầm giá 3-4 triệu nên chọn Intel i5 hay AMD Ryzen 5?"),
    ("◈  i3-12100F + RTX 3060 bottleneck?",    "i3-12100F dùng với RTX 3060 có bị cổ chai không?"),
    ("⚡  Ryzen 5 5600X cần tản nhiệt rời?",   "Ryzen 5 5600X có kèm tản nhiệt box dùng được không?"),
    ("🎮  GTX 1650 chơi game gì mượt FHD?",   "GTX 1650 chơi mượt những game nào ở 1080p?"),
    ("▶  RTX 3060 vs RX 6600 mua cái nào?",   "So sánh RTX 3060 và RX 6600 nên chọn card nào?"),
    ("◆  RTX 4060 đáng mua hơn RTX 3060?",    "RTX 4060 có đáng mua hơn RTX 3060 không?"),
    ("◉  iGPU Intel UHD đủ văn phòng?",       "Dùng Intel UHD Graphics cho văn phòng có đủ không?"),
    ("◆  H610 hay B660 nên mua mainboard nào?","Mainboard H610 và B660 khác nhau thế nào?"),
    ("▪  Socket LGA1700 dùng CPU đời mấy?",    "Socket LGA1700 hỗ trợ CPU Intel đời mấy?"),
    ("◈  B550 dùng được Ryzen 5 5600X?",       "Mainboard B550 có tương thích với Ryzen 5 5600X không?"),
    ("📱  Snapdragon 888 nóng máy bình thường?","Chip Snapdragon 888 bị nóng nhiều có phải lỗi không?"),
    ("📱  Dimensity 9200 vs Snapdragon 8 Gen2", "So sánh Dimensity 9200 với Snapdragon 8 Gen 2?"),
    ("📱  Apple A17 Pro mạnh cỡ nào?",          "Chip Apple A17 Pro mạnh đến đâu so Android cao cấp?"),
    ("⚡  Build PC 10 triệu chơi FHD",          "Gợi ý cấu hình PC 10 triệu chơi game Full HD mượt"),
    ("◆  i5-12400F + RTX 3060 có tốt không?",  "Combo i5-12400F với RTX 3060 12GB có bottleneck không?"),
]
if not st.session_state.suggestions:
    st.session_state.suggestions=random.sample(ALL_S,4)

# ======================== GREETING ========================
st.markdown(f"""
<div class="valo-greeting scan-wrap">
  <div class="valo-bracket tl"></div><div class="valo-bracket tr"></div>
  <div class="valo-bracket bl"></div><div class="valo-bracket br"></div>
  <div class="vg-topline"></div><div class="vg-leftline"></div>
  <div class="vg-inner-tl"></div><div class="vg-inner-tl2"></div>
  <div class="vg-glow-br"></div><div class="vg-glow-tc"></div>
  <div class="valo-vbar"></div>
  <div class="valo-status-row">
    <div class="valo-status-dot"></div>
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
    <div class="valo-stat"><span class="valo-stat-num" style="color:var(--t);text-shadow:0 0 16px rgba(0,212,191,0.8)">24/7</span><span class="valo-stat-label">Hỗ trợ</span></div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="valo-suggest-label"><span>CHỌN NHANH VẤN ĐỀ</span></div>', unsafe_allow_html=True)
col1,col2=st.columns(2,gap="small")
for i,(lb,qr) in enumerate(st.session_state.suggestions):
    with (col1 if i%2==0 else col2):
        if st.button(lb,key=f"s{i}"):
            st.session_state.greeted=True; st.session_state.pending_query=qr; st.rerun()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

# ======================== LOGIC ========================
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
