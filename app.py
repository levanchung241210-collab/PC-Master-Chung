import streamlit as st
import json
import re
import os
import random
from groq import Groq

st.set_page_config(
    page_title="PC Solving System — Lê Văn Chung 10A4",
    page_icon="⚡",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Barlow+Condensed:wght@300;400;600;700;800&family=Barlow:wght@300;400;500&display=swap');

:root {
    --R:  #ff4655;
    --R2: #ff2233;
    --T:  #00d4bf;
    --T2: #00ffe7;
    --G:  #e8c97a;
    --P:  #bd93f9;
    --BG: #0a0c12;
    --B1: #0f1320;
    --B2: #161b2a;
    --B3: #1d2238;
    --W:  #ffffff;
    --C:  #ece8e1;
    --S:  #b8b4ac;
    --M:  #6e6b65;
    --D:  #3a3d48;
}

html, body, .stApp {
    background: var(--BG) !important;
    color: var(--C) !important;
    font-family: 'Barlow', sans-serif !important;
}

/* ━━━━━ 1. BACKGROUND — tactical map ━━━━━ */
.stApp::before {
    content:''; position:fixed; inset:0; pointer-events:none; z-index:0;
    background:
        radial-gradient(ellipse 65% 55% at -8% -8%,   rgba(255,70,85,0.16) 0%,transparent 58%),
        radial-gradient(ellipse 65% 55% at 108% 108%, rgba(0,212,191,0.13) 0%,transparent 58%),
        radial-gradient(ellipse 40% 30% at 102% 2%,   rgba(189,147,249,0.07) 0%,transparent 52%),
        radial-gradient(ellipse 50% 25% at 50%  98%,  rgba(232,201,122,0.05) 0%,transparent 50%),
        repeating-linear-gradient(-52deg, transparent 0,transparent 50px,rgba(255,70,85,0.025) 50px,rgba(255,70,85,0.025) 51px),
        repeating-linear-gradient( 38deg, transparent 0,transparent 75px,rgba(0,212,191,0.015) 75px,rgba(0,212,191,0.015) 76px),
        repeating-linear-gradient(90deg,  transparent 0,transparent 79px,rgba(255,255,255,0.005) 79px,rgba(255,255,255,0.005) 80px),
        repeating-linear-gradient(180deg, transparent 0,transparent 79px,rgba(255,255,255,0.005) 79px,rgba(255,255,255,0.005) 80px);
}

/* ━━━━━ 2. TOP BAR — hard neon line ━━━━━ */
.stApp::after {
    content:''; position:fixed; top:0; left:0; right:0; height:3px; z-index:9999;
    background:linear-gradient(90deg,
        #ff2233 0%,#ff4655 70px,rgba(255,70,85,0.3) 220px,
        transparent 380px,transparent calc(100% - 380px),
        rgba(0,212,191,0.3) calc(100% - 220px),#00d4bf calc(100% - 70px),#00ffe7 100%);
    box-shadow:0 0 8px #ff4655,0 2px 20px rgba(255,70,85,0.25);
}

/* ━━━━━ 3. AUTHOR ━━━━━ */
.valo-author {
    font-family:'Barlow Condensed',sans-serif;
    font-size:10px; font-weight:700; letter-spacing:3px; text-transform:uppercase;
    color:#00f0ff; text-shadow:0 0 8px rgba(0,240,255,0.8);
    text-align:right; margin-bottom:4px;
    display:flex; align-items:center; justify-content:flex-end; gap:6px;
}
.valo-author::before { content:''; width:18px; height:1px; background:#00f0ff; box-shadow:0 0 4px #00f0ff; }
.valo-author::after  { content:'■'; font-size:5px; color:#00f0ff; }

/* ━━━━━ 4. EYEBROW ━━━━━ */
.valo-eyebrow {
    font-family:'Barlow Condensed',sans-serif;
    font-size:clamp(9px,2vw,11px); font-weight:800; letter-spacing:7px;
    color:var(--R); text-transform:uppercase; margin-bottom:6px;
    display:flex; align-items:center; justify-content:center; gap:12px;
    text-shadow:0 0 12px rgba(255,70,85,0.8);
}
.valo-eyebrow::before { content:''; width:40px; height:1px; background:linear-gradient(90deg,transparent,var(--R)); box-shadow:0 0 5px rgba(255,70,85,0.5); }
.valo-eyebrow::after  { content:''; width:40px; height:1px; background:linear-gradient(90deg,var(--R),transparent); box-shadow:0 0 5px rgba(255,70,85,0.5); }

/* ━━━━━ 5. LOGO + TITLE ━━━━━ */
.valo-logo-wrap { display:flex; align-items:center; justify-content:center; gap:16px; margin-bottom:4px; }
.lvc-logo { width:clamp(40px,7vw,54px); height:clamp(40px,7vw,54px); flex-shrink:0; filter:drop-shadow(0 0 6px rgba(255,70,85,0.7)) drop-shadow(0 0 14px rgba(255,70,85,0.3)); }
.lvc-logo svg { width:100%; height:100%; }

.valo-title {
    font-family:'Rajdhani',sans-serif;
    font-size:clamp(30px,8vw,68px); font-weight:700;
    letter-spacing:3px; line-height:1; text-transform:uppercase; margin:0;
    color:var(--W);
    text-shadow:0 0 30px rgba(255,255,255,0.1),0 2px 8px rgba(0,0,0,0.95);
}
.valo-title .red   { color:var(--R); text-shadow:0 0 16px rgba(255,70,85,0.9),0 0 40px rgba(255,70,85,0.3); }
.valo-title .slash { color:var(--R); opacity:.45; margin:0 2px; }

/* ━━━━━ 6. SUBTITLE ━━━━━ */
.valo-subtitle {
    font-family:'Barlow Condensed',sans-serif;
    font-size:clamp(11px,2.8vw,14px); font-weight:800; letter-spacing:5px;
    text-transform:uppercase; margin-top:8px;
    display:flex; align-items:center; justify-content:center; gap:8px; flex-wrap:wrap;
}
.sr { color:var(--R); text-shadow:0 0 8px rgba(255,70,85,0.8); }
.sw { color:var(--W); text-shadow:0 0 6px rgba(255,255,255,0.3); }
.st { color:var(--T); text-shadow:0 0 8px rgba(0,212,191,0.8); }
.sd { display:inline-block; width:4px; height:4px; transform:rotate(45deg); }
.sd.r { background:var(--R); box-shadow:0 0 5px var(--R); }
.sd.t { background:var(--T); box-shadow:0 0 5px var(--T); }

/* ━━━━━ 7. DIVIDER — tactical crosshair style ━━━━━ */
.valo-divider { display:flex; align-items:center; margin:12px 0 8px; }
.valo-divider::before, .valo-divider::after { content:''; flex:1; height:1px; background:rgba(255,255,255,0.06); }
.valo-div-inner { display:flex; align-items:center; gap:5px; padding:0 12px; }
.vdd { width:5px; height:5px; transform:rotate(45deg); }
.vdd.r { background:var(--R); box-shadow:0 0 8px var(--R),0 0 16px rgba(255,70,85,0.4); }
.vdd.t { background:var(--T); box-shadow:0 0 8px var(--T),0 0 16px rgba(0,212,191,0.4); width:4px; height:4px; }
.vdb {
    width:55px; height:2px;
    background:linear-gradient(90deg,var(--R),var(--G),var(--T));
    clip-path:polygon(5px 0%,100% 0%,calc(100% - 5px) 100%,0% 100%);
    box-shadow:0 0 8px rgba(0,212,191,0.4),0 0 4px rgba(255,70,85,0.3);
}

/* ━━━━━ 8. GREETING BOX — Valorant agent card panel ━━━━━ */
.vg-wrap {
    position:relative;
    margin:4px 0 14px;
}

/* Main panel — hard cut corners */
.valo-greeting {
    position:relative;
    background:linear-gradient(145deg,
        rgba(42,12,18,0.98)  0%,
        rgba(20,16,34,0.99) 45%,
        rgba(6,32,30,0.98)  100%);
    /* Hard clip-path cuts — Valorant agent card style */
    clip-path: polygon(
        0 22px, 22px 0,
        calc(100% - 10px) 0, 100% 10px,
        100% calc(100% - 22px), calc(100% - 22px) 100%,
        10px 100%, 0 calc(100% - 10px)
    );
    padding:clamp(18px,5vw,28px) clamp(16px,5vw,28px) clamp(14px,4vw,22px);
    overflow:hidden;
    animation:greetPulse 4s ease-in-out infinite;
}
@keyframes greetPulse {
    0%,100% { box-shadow:none; }
    50%      { box-shadow:0 0 0 1px rgba(255,70,85,0.15) inset; }
}

/* Border overlay — separate element so clip-path doesn't cut border */
.vg-border {
    position:absolute; inset:0; pointer-events:none; z-index:1;
    clip-path: polygon(
        0 22px, 22px 0,
        calc(100% - 10px) 0, 100% 10px,
        100% calc(100% - 22px), calc(100% - 22px) 100%,
        10px 100%, 0 calc(100% - 10px)
    );
    background:linear-gradient(145deg,rgba(255,70,85,0.5),rgba(255,70,85,0.1) 30%,rgba(0,212,191,0.15) 70%,rgba(0,212,191,0.4));
    -webkit-mask:linear-gradient(#fff 0 0) content-box,linear-gradient(#fff 0 0);
    -webkit-mask-composite:xor;
    mask-composite:exclude;
    padding:1px;
}

/* Red top bar inside panel */
.vg-topbar {
    position:absolute; top:0; left:22px; right:10px; height:2px;
    background:linear-gradient(90deg,var(--R),rgba(255,70,85,0.4),transparent);
    box-shadow:0 0 8px rgba(255,70,85,0.6);
}

/* Teal bottom bar */
.vg-btbar {
    position:absolute; bottom:0; left:10px; right:22px; height:1px;
    background:linear-gradient(90deg,transparent,rgba(0,212,191,0.5),var(--T));
}

/* Left red bar */
.vg-lbar {
    position:absolute; left:0; top:22px; bottom:10px; width:3px;
    background:linear-gradient(180deg,var(--R),rgba(255,70,85,0.3) 60%,transparent);
    box-shadow:1px 0 8px rgba(255,70,85,0.3);
}

/* Right teal subtle bar */
.vg-rbar {
    position:absolute; right:0; top:10px; bottom:22px; width:2px;
    background:linear-gradient(180deg,transparent,rgba(0,212,191,0.4),var(--T));
    box-shadow:-1px 0 6px rgba(0,212,191,0.2);
}

/* Teal glow corner BR */
.vg-glow-br {
    position:absolute; bottom:-30px; right:-30px; width:180px; height:180px;
    background:radial-gradient(circle,rgba(0,212,191,0.1) 0%,transparent 60%);
    pointer-events:none;
}
/* Red glow corner TL */
.vg-glow-tl {
    position:absolute; top:-20px; left:10%; width:150px; height:150px;
    background:radial-gradient(circle,rgba(255,70,85,0.07) 0%,transparent 65%);
    pointer-events:none;
}

/* Corner diamonds */
.vg-diam {
    position:absolute; width:8px; height:8px; transform:rotate(45deg);
}
.vg-diam.tl { top:8px;  left:8px;  background:var(--R); box-shadow:0 0 6px var(--R); }
.vg-diam.br { bottom:8px; right:8px; background:var(--T); box-shadow:0 0 6px var(--T); }

/* Scan line animation inside panel */
.vg-scan {
    position:absolute; inset:0; pointer-events:none; z-index:0;
    background:repeating-linear-gradient(180deg,
        transparent 0,transparent 3px,
        rgba(255,255,255,0.012) 3px,rgba(255,255,255,0.012) 4px);
}

/* STATUS */
.valo-status-row { display:flex; align-items:center; justify-content:center; gap:7px; margin-bottom:10px; position:relative; z-index:2; }
.valo-status-dot { width:7px; height:7px; background:var(--T); border-radius:50%; box-shadow:0 0 10px var(--T),0 0 4px var(--T2); animation:pulse 2s infinite; }
@keyframes pulse { 0%,100%{opacity:1;box-shadow:0 0 10px var(--T);}50%{opacity:.4;box-shadow:0 0 3px var(--T);} }
.valo-status-text { font-family:'Barlow Condensed',sans-serif; font-size:10px; font-weight:700; letter-spacing:3px; color:var(--T2); text-transform:uppercase; text-shadow:0 0 8px rgba(0,255,231,0.6); }

.valo-greeting-icon { font-size:clamp(28px,5vw,36px); display:block; text-align:center; margin-bottom:8px; position:relative; z-index:2; filter:drop-shadow(0 0 14px rgba(255,70,85,0.9)); animation:ipulse 3s infinite; }
@keyframes ipulse { 0%,100%{filter:drop-shadow(0 0 14px rgba(255,70,85,0.9));}50%{filter:drop-shadow(0 0 24px rgba(255,130,85,1));} }

.valo-greeting-title { font-family:'Rajdhani',sans-serif; font-size:clamp(15px,4vw,21px); font-weight:700; color:var(--W); text-align:center; text-transform:uppercase; letter-spacing:2px; margin-bottom:8px; text-shadow:0 0 16px rgba(255,255,255,0.12); position:relative; z-index:2; }
.valo-greeting-sub { font-size:clamp(12px,3vw,13.5px); color:var(--S); text-align:center; line-height:1.7; position:relative; z-index:2; }

/* STATS — sharp panel */
.valo-stats { display:flex; justify-content:center; gap:clamp(8px,2vw,20px); margin-top:14px; padding-top:12px; border-top:1px solid rgba(255,255,255,0.07); position:relative; z-index:2; }
.valo-stat { text-align:center; line-height:1.2; }
.valo-stat-num { font-family:'Rajdhani',sans-serif; font-size:clamp(16px,4vw,22px); font-weight:700; color:var(--R); display:block; text-shadow:0 0 12px rgba(255,70,85,0.7); }
.valo-stat-lbl { font-family:'Barlow Condensed',sans-serif; font-size:9px; letter-spacing:2px; color:var(--D); text-transform:uppercase; }
.valo-stat-sep { width:1px; background:linear-gradient(180deg,transparent,rgba(255,255,255,0.12),transparent); align-self:stretch; }

/* ━━━━━ 9. SUGGEST LABEL — sharp hextag ━━━━━ */
.valo-suggest-label { display:flex; align-items:center; gap:10px; margin:8px 0 12px; }
.valo-suggest-label::before { content:''; flex:1; height:1px; background:linear-gradient(90deg,transparent,rgba(255,70,85,0.6)); box-shadow:0 0 3px rgba(255,70,85,0.3); }
.valo-suggest-label::after  { content:''; flex:1; height:1px; background:linear-gradient(90deg,rgba(0,212,191,0.6),transparent); box-shadow:0 0 3px rgba(0,212,191,0.3); }
.valo-suggest-label span {
    font-family:'Barlow Condensed',sans-serif;
    font-size:12px; font-weight:800; letter-spacing:3px; text-transform:uppercase;
    color:var(--W); text-shadow:0 1px 4px rgba(0,0,0,0.8);
    background:linear-gradient(90deg,#b02030,#ff4655,#c0303d);
    padding:5px 20px;
    clip-path:polygon(10px 0,100% 0,calc(100% - 10px) 100%,0 100%);
    box-shadow:0 0 16px rgba(255,70,85,0.5),0 0 32px rgba(255,70,85,0.2),0 4px 10px rgba(0,0,0,0.5);
}

/* ━━━━━ 10. BUTTONS — sharp cut tactical ━━━━━ */
.stButton > button {
    background:linear-gradient(90deg,rgba(0,50,46,0.78),rgba(8,14,24,0.94)) !important;
    color:#c8f4f0 !important;
    border:none !important;
    outline:1px solid rgba(0,212,191,0.25) !important;
    outline-offset:0 !important;
    /* Sharp left cut */
    clip-path:polygon(8px 0,100% 0,100% calc(100% - 8px),calc(100% - 0px) 100%,0 100%,0 8px) !important;
    border-radius:0 !important;
    font-family:'Barlow Condensed',sans-serif !important;
    font-size:clamp(12px,3vw,14px) !important;
    font-weight:700 !important;
    letter-spacing:.5px !important;
    padding:12px 14px !important;
    width:100% !important; text-align:left !important;
    white-space:normal !important; min-height:50px !important; line-height:1.4 !important;
    transition:all .15s ease !important;
    box-shadow:
        inset 3px 0 0 rgba(0,212,191,0.5),
        0 2px 10px rgba(0,0,0,0.6),
        0 0 10px rgba(0,212,191,0.08) !important;
    position:relative !important;
}
.stButton > button:hover {
    background:linear-gradient(90deg,rgba(0,212,191,0.15),rgba(255,70,85,0.08)) !important;
    color:var(--W) !important;
    outline-color:rgba(0,212,191,0.5) !important;
    transform:translateX(5px) !important;
    box-shadow:
        inset 3px 0 0 var(--R),
        0 0 20px rgba(0,212,191,0.3),
        0 0 40px rgba(0,212,191,0.12),
        0 4px 16px rgba(0,0,0,0.6) !important;
}
.stButton > button:active {
    transform:translateX(2px) !important;
}

/* ━━━━━ 11. USER AVATAR ━━━━━ */
[data-testid="chatAvatarIcon-user"] {
    background:linear-gradient(135deg,#500d16,#180408) !important;
    border:none !important;
    clip-path:polygon(0 6px,6px 0,100% 0,100% calc(100% - 6px),calc(100% - 6px) 100%,0 100%) !important;
    border-radius:0 !important;
    box-shadow:0 0 12px rgba(255,70,85,0.6),0 0 24px rgba(255,70,85,0.2),inset 0 0 8px rgba(255,70,85,0.08) !important;
    overflow:hidden !important;
}
[data-testid="chatAvatarIcon-user"] > * { display:none !important; }
[data-testid="chatAvatarIcon-user"]::before {
    content:''; display:block; width:100%; height:100%;
    background:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 36 36'%3E%3Crect width='36' height='36' fill='%23500d16'/%3E%3Cpolygon points='18,4 32,12 32,24 18,32 4,24 4,12' fill='none' stroke='%23ff4655' stroke-width='1.5'/%3E%3Cpolygon points='18,9 27,14 27,22 18,27 9,22 9,14' fill='rgba(255,70,85,0.1)'/%3E%3Cline x1='4' y1='12' x2='11' y2='19' stroke='%23ff4655' stroke-width='1' opacity='0.5'/%3E%3Cline x1='32' y1='24' x2='25' y2='17' stroke='%23ff4655' stroke-width='1' opacity='0.3'/%3E%3Ctext x='18' y='22' text-anchor='middle' font-family='Rajdhani,sans-serif' font-size='9' font-weight='700' fill='%23ff7080' letter-spacing='1'%3EUSR%3C/text%3E%3Ccircle cx='18' cy='29' r='1.5' fill='%23ff4655' opacity='0.8'/%3E%3Cline x1='2' y1='2' x2='8' y2='2' stroke='%23ff4655' stroke-width='1' opacity='0.5'/%3E%3Cline x1='2' y1='2' x2='2' y2='8' stroke='%23ff4655' stroke-width='1' opacity='0.5'/%3E%3C/svg%3E") center/cover no-repeat !important;
}

/* ━━━━━ 12. BOT AVATAR ━━━━━ */
[data-testid="chatAvatarIcon-assistant"] {
    background:linear-gradient(135deg,#003830,#000e0c) !important;
    border:none !important;
    clip-path:polygon(0 6px,6px 0,100% 0,100% calc(100% - 6px),calc(100% - 6px) 100%,0 100%) !important;
    border-radius:0 !important;
    box-shadow:0 0 12px rgba(0,212,191,0.6),0 0 24px rgba(0,212,191,0.2),inset 0 0 8px rgba(0,212,191,0.06) !important;
    overflow:hidden !important;
}
[data-testid="chatAvatarIcon-assistant"] > * { display:none !important; }
[data-testid="chatAvatarIcon-assistant"]::before {
    content:''; display:block; width:100%; height:100%;
    background:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 36 36'%3E%3Crect width='36' height='36' fill='%23003830'/%3E%3Cpolygon points='18,3 33,11.5 33,24.5 18,33 3,24.5 3,11.5' fill='none' stroke='%2300d4bf' stroke-width='1.5'/%3E%3Ccircle cx='18' cy='18' r='5.5' fill='none' stroke='%2300d4bf' stroke-width='1.2' opacity='0.8'/%3E%3Ccircle cx='18' cy='18' r='2' fill='%2300ffe7'/%3E%3Cline x1='18' y1='3'  x2='18' y2='11' stroke='%2300d4bf' stroke-width='1' opacity='0.5'/%3E%3Cline x1='18' y1='25' x2='18' y2='33' stroke='%2300d4bf' stroke-width='1' opacity='0.5'/%3E%3Cline x1='3'  y1='18' x2='11' y2='18' stroke='%2300d4bf' stroke-width='1' opacity='0.4'/%3E%3Cline x1='25' y1='18' x2='33' y2='18' stroke='%2300d4bf' stroke-width='1' opacity='0.4'/%3E%3Cline x1='34' y1='2' x2='28' y2='2' stroke='%2300d4bf' stroke-width='1' opacity='0.4'/%3E%3Cline x1='34' y1='2' x2='34' y2='8' stroke='%2300d4bf' stroke-width='1' opacity='0.4'/%3E%3C/svg%3E") center/cover no-repeat !important;
}

/* ━━━━━ 13. USER BUBBLE — Omen / red zone ━━━━━ */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background:linear-gradient(135deg,
        rgba(80,14,22,0.96) 0%,
        rgba(50,8,15,0.98) 40%,
        rgba(16,8,12,0.99) 100%) !important;
    border:none !important;
    outline:1px solid rgba(255,70,85,0.35) !important;
    clip-path:polygon(
        0 0, calc(100% - 14px) 0, 100% 14px,
        100% 100%, 14px 100%, 0 calc(100% - 14px)
    ) !important;
    border-radius:0 !important;
    padding:14px 18px !important;
    margin:8px 0 !important;
    box-shadow:
        inset -3px 0 0 rgba(255,70,85,0.6),
        4px 0 20px rgba(255,70,85,0.12),
        0 4px 20px rgba(0,0,0,0.7) !important;
}

/* ━━━━━ 14. BOT BUBBLE — Cypher / teal zone ━━━━━ */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    background:linear-gradient(135deg,
        rgba(4,52,48,0.96) 0%,
        rgba(3,30,28,0.98) 40%,
        rgba(6,12,18,0.99) 100%) !important;
    border:none !important;
    outline:1px solid rgba(0,212,191,0.3) !important;
    clip-path:polygon(
        14px 0, 100% 0, 100% calc(100% - 14px),
        calc(100% - 0px) 100%, 0 100%, 0 14px
    ) !important;
    border-radius:0 !important;
    padding:14px 18px !important;
    margin:8px 0 !important;
    box-shadow:
        inset 3px 0 0 rgba(0,212,191,0.55),
        -4px 0 20px rgba(0,212,191,0.10),
        0 4px 20px rgba(0,0,0,0.7) !important;
}

/* ━━━━━ 15. CHAT TEXT ━━━━━ */
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li {
    font-size:clamp(13.5px,3.8vw,15px) !important;
    line-height:1.82 !important;
    color:#f2ede6 !important;
    text-shadow:0 1px 4px rgba(0,0,0,0.95) !important;
}
[data-testid="stChatMessage"] h3 {
    font-family:'Rajdhani',sans-serif !important;
    font-size:clamp(14px,4vw,18px) !important; font-weight:700 !important;
    text-transform:uppercase !important; letter-spacing:2px !important;
    color:var(--W) !important; margin-bottom:8px !important; padding-bottom:5px !important;
    border-bottom:1px solid rgba(255,255,255,0.08) !important;
    text-shadow:0 0 14px rgba(255,255,255,0.1) !important;
}
[data-testid="stChatMessage"] strong { color:#ffbcc2 !important; font-weight:700 !important; text-shadow:0 0 6px rgba(255,70,85,0.3) !important; }
[data-testid="stChatMessage"] em { color:var(--T2) !important; font-style:normal !important; font-size:11px !important; text-shadow:0 0 6px rgba(0,255,231,0.4) !important; }
[data-testid="stChatMessage"] code { background:rgba(0,212,191,0.1) !important; color:#6fffec !important; border:1px solid rgba(0,212,191,0.3) !important; border-radius:1px !important; padding:2px 7px !important; font-size:12px !important; }

/* ━━━━━ 16. CHAT INPUT ━━━━━ */
.stChatInput > div {
    background:linear-gradient(135deg,rgba(18,22,34,0.99),rgba(12,16,26,0.99)) !important;
    border:none !important;
    outline:1px solid rgba(255,70,85,0.2) !important;
    clip-path:polygon(8px 0,100% 0,100% calc(100% - 8px),calc(100% - 8px) 100%,0 100%,0 8px) !important;
    border-radius:0 !important;
    box-shadow:0 0 16px rgba(255,70,85,0.06),0 4px 20px rgba(0,0,0,0.7) !important;
}
.stChatInput textarea {
    background:transparent !important; color:var(--C) !important;
    border:none !important; border-bottom:1px solid rgba(255,70,85,0.25) !important;
    border-radius:0 !important;
    font-family:'Barlow',sans-serif !important;
    font-size:clamp(13px,3.5vw,14px) !important; caret-color:var(--R) !important;
}
.stChatInput textarea:focus { border-bottom-color:var(--R) !important; box-shadow:0 3px 16px rgba(255,70,85,0.1) !important; }
.stChatInput textarea::placeholder { color:var(--D) !important; font-style:italic !important; }

/* ━━━━━ 17. SIDEBAR ━━━━━ */
section[data-testid="stSidebar"] { background:linear-gradient(180deg,#080b11,#0b0f18) !important; border-right:1px solid rgba(255,70,85,0.15) !important; }
section[data-testid="stSidebar"] p,section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] div,section[data-testid="stSidebar"] small { color:var(--M) !important; font-size:13px !important; }
section[data-testid="stSidebar"] h2 { font-family:'Rajdhani',sans-serif !important; font-size:17px !important; color:var(--C) !important; text-transform:uppercase !important; letter-spacing:3px !important; }
section[data-testid="stSidebar"] .stButton > button {
    background:transparent !important; border:none !important;
    outline:1px solid rgba(255,70,85,0.18) !important;
    clip-path:polygon(6px 0,100% 0,100% calc(100% - 6px),calc(100% - 6px) 100%,0 100%,0 6px) !important;
    color:var(--M) !important; font-family:'Barlow Condensed',sans-serif !important;
    font-weight:700 !important; letter-spacing:1px !important; box-shadow:none !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background:rgba(255,70,85,0.07) !important; color:var(--C) !important; transform:none !important;
}

/* ━━━━━ 18. SPINNER ━━━━━ */
[data-testid="stSpinner"] p { color:var(--T) !important; font-family:'Barlow Condensed',sans-serif !important; letter-spacing:4px !important; font-size:11px !important; text-transform:uppercase !important; text-shadow:0 0 8px rgba(0,212,191,0.6) !important; }

/* ━━━━━ 19. SCROLLBAR ━━━━━ */
::-webkit-scrollbar { width:3px; }
::-webkit-scrollbar-track { background:var(--BG); }
::-webkit-scrollbar-thumb { background:var(--R); box-shadow:0 0 4px var(--R); }

/* ━━━━━ 20. MISC ━━━━━ */
#MainMenu, footer, header { visibility:hidden !important; }
.block-container { padding-top:1.2rem !important; padding-bottom:1.5rem !important; max-width:760px !important; }

@media (max-width:600px) {
    .block-container { padding:.7rem .5rem 4.5rem !important; }
    .valo-author { position:relative !important; top:0 !important; justify-content:center !important; margin-bottom:8px !important; }
    .valo-author::before { display:none; }
    [data-testid="stChatMessage"] { padding:10px 12px !important; margin:5px 0 !important; }
    .stButton > button { min-height:44px !important; padding:9px 11px !important; }
    .valo-greeting { padding:16px 12px !important; }
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

def load_database():
    if os.path.exists("database_pc.json"):
        with open("database_pc.json","r",encoding="utf-8") as f: return json.load(f)
    return {"loi_he_thong":[],"linh_kien_pc":[]}
def load_raw():
    if os.path.exists("database_pc.json"):
        with open("database_pc.json","r",encoding="utf-8") as f: return f.read()
    return "{}"

data_pc=load_database(); raw=load_raw()
n_loi=len(data_pc.get("loi_he_thong",[])); n_lk=len(data_pc.get("linh_kien_pc",[]))

with st.sidebar:
    st.markdown("## ⚡ PC Solving")
    st.markdown("---")
    st.markdown("Hệ thống chẩn đoán lỗi và tư vấn linh kiện máy tính chuyên sâu.")
    st.markdown("---")
    if st.button("⟳  PHIÊN MỚI", use_container_width=True):
        st.session_state.messages=[]; st.session_state.suggestions=[]; st.rerun()
    st.markdown("---")
    st.markdown("<small>Lê Văn Chung · Lớp 10A4 🎓</small>", unsafe_allow_html=True)

LVC = """<svg viewBox="0 0 52 52" xmlns="http://www.w3.org/2000/svg">
<defs>
<linearGradient id="rg" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#ff2233"/><stop offset="100%" stop-color="#ff4655"/></linearGradient>
<linearGradient id="tg" x1="0%" y1="100%" x2="100%" y2="0%"><stop offset="0%" stop-color="#00d4bf"/><stop offset="100%" stop-color="#00ffe7"/></linearGradient>
<filter id="glow"><feGaussianBlur stdDeviation="1.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
<polygon points="26,2 48,14 48,38 26,50 4,38 4,14" fill="rgba(255,40,60,0.06)" stroke="url(#rg)" stroke-width="2" filter="url(#glow)"/>
<polygon points="26,9 41,17.5 41,34.5 26,43 11,34.5 11,17.5" fill="none" stroke="url(#tg)" stroke-width="1" opacity="0.6"/>
<line x1="4" y1="14" x2="13" y2="23" stroke="#ff4655" stroke-width="1.5" opacity="0.5"/>
<line x1="48" y1="38" x2="39" y2="29" stroke="#00d4bf" stroke-width="1.5" opacity="0.5"/>
<line x1="4"  y1="38" x2="10" y2="38" stroke="#ff4655" stroke-width="1" opacity="0.35"/>
<line x1="48" y1="14" x2="42" y2="14" stroke="#00d4bf" stroke-width="1" opacity="0.35"/>
<text x="26" y="31" text-anchor="middle" font-family="Rajdhani,sans-serif" font-size="13" font-weight="700" fill="white" letter-spacing="1" filter="url(#glow)">LVC</text>
<circle cx="26" cy="38" r="2" fill="#ff4655" opacity="0.9" filter="url(#glow)"/>
<circle cx="26" cy="38" r="4" fill="none" stroke="#ff4655" stroke-width="0.5" opacity="0.35"/>
</svg>"""

st.markdown(f"""
<div style="padding:10px 0 2px; text-align:center; position:relative;">
    <div class="valo-author">Lê Văn Chung · 10A4</div>
    <div class="valo-eyebrow">⚡ STEM PROJECT ⚡</div>
    <div class="valo-logo-wrap">
        <div class="lvc-logo">{LVC}</div>
        <div class="valo-title">PC<span class="slash">/</span><span class="red">SOLVING</span></div>
    </div>
    <div class="valo-subtitle">
        <span class="sd r"></span><span class="sr">CHẨN ĐOÁN</span>
        <span class="sd r"></span><span class="sw">PHÂN TÍCH</span>
        <span class="sd t"></span><span class="st">XỬ LÝ TỰ ĐỘNG</span>
        <span class="sd t"></span>
    </div>
</div>
<div class="valo-divider">
    <div class="valo-div-inner"><div class="vdd r"></div><div class="vdb"></div><div class="vdd t"></div></div>
</div>
""", unsafe_allow_html=True)

if "messages"      not in st.session_state: st.session_state.messages=[]
if "suggestions"   not in st.session_state: st.session_state.suggestions=[]
if "pending_query" not in st.session_state: st.session_state.pending_query=None

ALL_SUG=[
    ("⚠  Màn hình xanh BSOD đột ngột","Máy tính bị màn hình xanh chết đột ngột, phải làm gì?"),
    ("▪  Màn hình đen không có tín hiệu","Máy lên nguồn nhưng màn hình đen, không có tín hiệu"),
    ("◈  PC bíp dài khi khởi động","Máy bíp dài liên tục khi bật, không vào được Windows"),
    ("◉  Windows boot loop liên tục","Máy cứ khởi động lại liên tục không vào được Windows"),
    ("✕  Lỗi 0xc0000005 văng game","Game bị lỗi 0xc0000005 không mở được cách fix?"),
    ("✕  Lỗi 0xc000021a không boot","Máy báo lỗi 0xc000021a không boot được vào Windows"),
    ("⚠  PC tự reboot khi chơi game","PC tự reboot đột ngột trong lúc chơi game nặng"),
    ("▪  Máy không nhận chuột USB","Cắm USB chuột bàn phím vào máy không nhận lỗi gì?"),
    ("◈  SSD NVMe không nhận trong BIOS","BIOS không nhận ổ SSD NVMe sau khi lắp vào mainboard"),
    ("◉  No Boot Device Found","Máy báo No Boot Device Found không vào được hệ điều hành"),
    ("🌡  CPU 95°C — overheat","CPU nhiệt độ lên đến 95 độ C khi chạy game nguy hiểm không?"),
    ("◆  RAM 8GB đủ chơi game 2024?","RAM 8GB có đủ dùng để chơi game hiện đại năm 2024 không?"),
    ("⚡  Nguồn W cho RTX 3060?","RTX 3060 cần nguồn bao nhiêu W dùng nguồn 500W được không?"),
    ("◆  Tản nhiệt nước hay khí?","Nên dùng tản nhiệt nước hay tản nhiệt khí cho i5-12400F?"),
    ("▶  SSD NVMe vs SATA khác gì?","SSD NVMe và SSD SATA khác nhau ở điểm gì nên mua loại nào?"),
    ("◉  RAM 2x8GB vs 1x16GB?","Lắp 2 thanh RAM 8GB hay 1 thanh 16GB thì nhanh hơn?"),
    ("◆  i5-12400F chơi game đủ không?","i5-12400F hiệu năng thế nào chơi game 2024 có đủ không?"),
    ("▶  i5 vs Ryzen 5 tầm 3-4 triệu","Tầm giá 3-4 triệu nên chọn Intel i5 hay AMD Ryzen 5?"),
    ("◈  i3-12100F + RTX 3060 bottleneck?","i3-12100F dùng với RTX 3060 có bị cổ chai hiệu năng không?"),
    ("⚡  Ryzen 5 5600X cần tản rời?","Ryzen 5 5600X có kèm tản nhiệt box dùng được không?"),
    ("🎮  GTX 1650 chơi game FHD?","GTX 1650 chơi mượt những game nào ở 1080p?"),
    ("▶  RTX 3060 vs RX 6600?","So sánh RTX 3060 và RX 6600 nên chọn card nào?"),
    ("◆  RTX 4060 đáng mua hơn 3060?","RTX 4060 có đáng mua hơn RTX 3060 về giá tiền không?"),
    ("◉  iGPU Intel UHD đủ văn phòng?","Dùng Intel UHD Graphics iGPU cho văn phòng có đủ không?"),
    ("◆  H610 hay B660?","Mainboard H610 và B660 khác nhau thế nào nên mua loại nào?"),
    ("▪  Socket LGA1700 CPU đời mấy?","Socket LGA1700 hỗ trợ những CPU Intel đời mấy?"),
    ("◈  B550 + Ryzen 5 5600X OK?","Mainboard B550 có tương thích với Ryzen 5 5600X không?"),
    ("📱  Snapdragon 888 nóng máy?","Chip Snapdragon 888 bị nóng máy nhiều có phải lỗi không?"),
    ("📱  Dimensity 9200 vs Snap 8 Gen2","So sánh Dimensity 9200 với Snapdragon 8 Gen 2 loại nào mạnh?"),
    ("📱  Apple A17 Pro mạnh cỡ nào?","Chip Apple A17 Pro mạnh đến đâu so với chip Android cao cấp?"),
    ("⚡  Build PC 10 triệu FHD","Gợi ý cấu hình PC build 10 triệu đồng chơi game Full HD mượt"),
    ("◆  i5-12400F + RTX 3060 tốt?","Combo i5-12400F với RTX 3060 12GB chơi game có bottleneck không?"),
]
if not st.session_state.suggestions:
    st.session_state.suggestions=random.sample(ALL_SUG,4)

st.markdown(f"""
<div class="vg-wrap">
    <div class="valo-greeting">
        <div class="vg-topbar"></div><div class="vg-btbar"></div>
        <div class="vg-lbar"></div><div class="vg-rbar"></div>
        <div class="vg-glow-br"></div><div class="vg-glow-tl"></div>
        <div class="vg-diam tl"></div><div class="vg-diam br"></div>
        <div class="vg-scan"></div>
        <div class="valo-status-row">
            <div class="valo-status-dot"></div>
            <div class="valo-status-text">Hệ thống sẵn sàng</div>
        </div>
        <span class="valo-greeting-icon">⚡</span>
        <div class="valo-greeting-title">Hệ thống phân tích phần cứng máy tính</div>
        <div class="valo-greeting-sub">
            Nhập mã hiệu linh kiện hoặc mô tả hiện tượng lỗi hệ thống.<br>
            Thuật toán phân tích tự động sẽ đưa ra giải pháp ngay lập tức.
        </div>
        <div class="valo-stats">
            <div class="valo-stat"><span class="valo-stat-num">{n_loi}</span><span class="valo-stat-lbl">Lỗi hệ thống</span></div>
            <div class="valo-stat-sep"></div>
            <div class="valo-stat"><span class="valo-stat-num">{n_lk}</span><span class="valo-stat-lbl">Linh kiện PC</span></div>
            <div class="valo-stat-sep"></div>
            <div class="valo-stat">
                <span class="valo-stat-num" style="color:var(--T);text-shadow:0 0 12px rgba(0,212,191,0.8)">24/7</span>
                <span class="valo-stat-lbl">Hỗ trợ</span>
            </div>
        </div>
    </div>
    <div class="vg-border"></div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="valo-suggest-label"><span>CHỌN NHANH VẤN ĐỀ</span></div>', unsafe_allow_html=True)
c1,c2=st.columns(2,gap="small")
for i,(lbl,qry) in enumerate(st.session_state.suggestions):
    with (c1 if i%2==0 else c2):
        if st.button(lbl,key=f"s{i}"):
            st.session_state.pending_query=qry; st.rerun()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

def score(item,qc,un):
    s=0; kws=[str(k).lower().strip() for k in item.get("keywords",[])]; uw=qc.split()
    for k in kws:
        if k in uw or (k.isdigit() and k in qc): s+=1
    if s==0: return 0
    ns=[re.sub(r'\D','',k) for k in kws if re.search(r'\d{3,}',k)]; ns=[n for n in ns if n]
    if ns and un:
        if not set(ns).intersection(set(un)): return 0
    return s

def search_db(q):
    qc=re.sub(r'[-–_,.\?!\(\)]',' ',q.lower().strip())
    un=[re.sub(r'\D','',w) for w in qc.split() if re.search(r'\d{3,}',w)]; un=[n for n in un if n]
    bm,ms,mp=None,0,""
    for it in data_pc.get("linh_kien_pc",[]):
        s=score(it,qc,un)
        if s>ms: ms,bm,mp=s,it,"lk"
    for it in data_pc.get("loi_he_thong",[]):
        s=score(it,qc,un)
        if s>ms: ms,bm,mp=s,it,"loi"
    if ms>=2 and bm:
        if mp=="loi":
            return f"### ✕  {bm['ten']}\n*— Lê Văn Chung 10A4*\n\n**⚠ Nguyên nhân:** {bm['nguyen_nhan']}\n\n**◈ Khắc phục:**\n{bm['giai_phap']}"
        return f"### ◆  {bm['ten']}\n*— Lê Văn Chung 10A4*\n\n**⚙ Thông số:** {bm.get('thong_so','')}\n\n**◉ Socket:** `{bm.get('socket','')}`\n\n**▶ Tư vấn:** {bm.get('chuyen_gia_tu_van','')}"
    return None

def dtype(q):
    ql=q.lower()
    for w in ["i3","i5","i7","i9","ryzen","gtx","rtx","rx","vga","card","cpu","ram","ssd","mainboard","main","nguồn","psu","tản nhiệt","socket","ddr","mua","so sánh","nên chọn","upgrade","nâng cấp","combo","build","cấu hình","snapdragon","dimensity","helio","chip","điện thoại","iphone","samsung","apple"]:
        if w in ql: return "hw"
    for w in ["lỗi","bsod","xanh","đen","bíp","crash","sập","đơ","treo","chậm","lag","không bật","không lên","restart","khởi động","update","0x","error","fix","sửa","boot","không nhận","không vào"]:
        if w in ql: return "err"
    return "gen"

BR="TUYỆT ĐỐI KHÔNG dùng: 'AI','LLM','Groq','Meta','Llama'. Đọc KỸ câu hỏi. Trả lời ĐÚNG và ĐỦ."
PE=f"Bạn là hệ thống chẩn đoán lỗi của Lê Văn Chung 10A4.\n{BR}\nKho:{raw}\nQUY TẮC: 1 câu nguyên nhân + tối đa 4 bước ngắn + 1 tip."
PH=f"Bạn là chuyên gia tư vấn linh kiện PC của Lê Văn Chung 10A4.\n{BR}\nKho:{raw}\nQUY TẮC: Thông số quan trọng, so sánh nếu cần, combo, 1 khuyến nghị. Mở đầu: 'Dựa trên cơ sở dữ liệu kỹ thuật của tác giả Lê Văn Chung 10A4...'"
PG=f"Bạn là hệ thống hỗ trợ kỹ thuật của Lê Văn Chung 10A4.\n{BR}\nKho:{raw}\nTrả lời tiếng Việt, súc tích."

def ask(q,hist):
    t=dtype(q)
    if t=="err": sy,mt,tp=PE,500,0.3
    elif t=="hw": sy,mt,tp=PH,800,0.5
    else: sy,mt,tp=PG,600,0.4
    ms=[{"role":"system","content":sy}]
    for m in hist[-6:]: ms.append({"role":m["role"],"content":m["content"]})
    ms.append({"role":"user","content":q})
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
            except: st.error("❌ Hệ thống gián đoạn. Vui lòng thử lại.")

if st.session_state.pending_query:
    q=st.session_state.pending_query; st.session_state.pending_query=None; handle(q)
if p:=st.chat_input("Nhập mã lỗi hoặc linh kiện cần phân tích..."):
    handle(p)
