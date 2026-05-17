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
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Barlow+Condensed:wght@400;600;700;800&family=Barlow:wght@300;400;500;600&display=swap');

/* ══════════ PALETTE ══════════ */
:root {
    --red:    #ff4655;
    --red2:   #ff7080;
    --teal:   #00d4bf;
    --teal2:  #00ffe7;
    --gold:   #e8c97a;
    --purple: #bd93f9;
    --bg0:    #0a0c12;
    --bg1:    #10141e;
    --bg2:    #161b28;
    --bg3:    #1c2234;
    --white:  #ffffff;
    --cream:  #ece8e1;
    --silver: #c4c0b8;
}

/* ══ BASE ══ */
html, body, .stApp {
    background: var(--bg0) !important;
    color: var(--cream) !important;
    font-family: 'Barlow', sans-serif !important;
}

/* ══ 1. BACKGROUND — split map + neon grid ══ */
.stApp::before {
    content: '';
    position: fixed; inset: 0; pointer-events: none; z-index: 0;
    background:
        radial-gradient(ellipse 60% 50% at -5% -5%,  rgba(255,70,85,0.14)  0%, transparent 60%),
        radial-gradient(ellipse 60% 50% at 105% 105%, rgba(0,212,191,0.11)  0%, transparent 60%),
        radial-gradient(ellipse 35% 25% at 100% 0%,   rgba(189,147,249,0.06) 0%, transparent 55%),
        radial-gradient(ellipse 80% 30% at 50%  100%, rgba(232,201,122,0.04) 0%, transparent 50%),
        repeating-linear-gradient(-52deg, transparent 0, transparent 52px, rgba(255,70,85,0.022) 52px, rgba(255,70,85,0.022) 53px),
        repeating-linear-gradient( 38deg, transparent 0, transparent 78px, rgba(0,212,191,0.013) 78px, rgba(0,212,191,0.013) 79px),
        repeating-linear-gradient(180deg, transparent 0, transparent 6px, rgba(255,255,255,0.003) 6px, rgba(255,255,255,0.003) 7px);
}

/* ══ 2. TOP BAR — red to teal neon ══ */
.stApp::after {
    content: '';
    position: fixed; top:0; left:0; right:0; height:3px; z-index:9999;
    background: linear-gradient(90deg,
        #ff2233 0%, #ff4655 60px, #c0303d 140px,
        transparent 280px, transparent calc(100% - 280px),
        #006b63 calc(100% - 140px), #00d4bf calc(100% - 60px), #00ffe7 100%);
    box-shadow: 0 0 12px rgba(255,70,85,0.6), 0 0 24px rgba(255,70,85,0.2);
}

/* ══ 3. HEADER ══ */
.valo-header { text-align:center; padding:10px 0 2px; position:relative; }

/* 4. Author name — cyan neon */
.valo-author {
    font-family:'Barlow Condensed',sans-serif;
    font-size:11px; font-weight:700; letter-spacing:3px; text-transform:uppercase;
    color:#00f0ff; text-shadow:0 0 10px rgba(0,240,255,0.7), 0 0 20px rgba(0,240,255,0.3);
    text-align:right; margin-bottom:4px;
    display:flex; align-items:center; justify-content:flex-end; gap:6px;
}
.valo-author::before { content:''; width:20px; height:1px; background:linear-gradient(90deg,transparent,#00f0ff); box-shadow:0 0 4px #00f0ff; }

/* 5. Eyebrow */
.valo-eyebrow {
    font-family:'Barlow Condensed',sans-serif;
    font-size:clamp(9px,2vw,11px); font-weight:800; letter-spacing:7px;
    color:var(--red); text-transform:uppercase; margin-bottom:6px;
    display:flex; align-items:center; justify-content:center; gap:12px;
    text-shadow:0 0 14px rgba(255,70,85,0.7);
}
.valo-eyebrow::before { content:''; width:36px; height:1px; background:linear-gradient(90deg,transparent,var(--red)); box-shadow:0 0 6px rgba(255,70,85,0.5); }
.valo-eyebrow::after  { content:''; width:36px; height:1px; background:linear-gradient(90deg,var(--red),transparent); box-shadow:0 0 6px rgba(255,70,85,0.5); }

/* 6. LVC logo glow */
.valo-logo-wrap { display:flex; align-items:center; justify-content:center; gap:16px; margin-bottom:4px; }
.lvc-logo { width:clamp(40px,7vw,54px); height:clamp(40px,7vw,54px); flex-shrink:0;
    filter:drop-shadow(0 0 8px rgba(255,70,85,0.6)) drop-shadow(0 0 16px rgba(255,70,85,0.3)); }
.lvc-logo svg { width:100%; height:100%; }

/* 7. Title — Neon Odin style */
.valo-title {
    font-family:'Rajdhani',sans-serif;
    font-size:clamp(30px,8vw,66px); font-weight:700;
    letter-spacing:3px; line-height:1; text-transform:uppercase; margin:0;
    color:var(--white);
    text-shadow:0 0 30px rgba(255,255,255,0.15), 0 2px 6px rgba(0,0,0,0.9);
}
.valo-title .red   { color:var(--red); text-shadow:0 0 20px rgba(255,70,85,0.8), 0 0 40px rgba(255,70,85,0.3); }
.valo-title .slash { color:var(--red); opacity:.5; margin:0 2px; }

/* 8. Subtitle — colored + glowing */
.valo-subtitle {
    font-family:'Barlow Condensed',sans-serif;
    font-size:clamp(11px,2.8vw,14px); font-weight:800; letter-spacing:5px;
    text-transform:uppercase; margin-top:8px;
    display:flex; align-items:center; justify-content:center; gap:8px; flex-wrap:wrap;
}
.sub-r { color:var(--red);  text-shadow:0 0 10px rgba(255,70,85,0.7); }
.sub-w { color:var(--white); text-shadow:0 0 8px rgba(255,255,255,0.3); }
.sub-t { color:var(--teal); text-shadow:0 0 10px rgba(0,212,191,0.7); }
.sub-d { display:inline-block; width:4px; height:4px; transform:rotate(45deg); }
.sub-d.r { background:var(--red);  box-shadow:0 0 6px var(--red); }
.sub-d.t { background:var(--teal); box-shadow:0 0 6px var(--teal); }

/* 9. Divider */
.valo-divider { display:flex; align-items:center; margin:12px 0 8px; }
.valo-divider::before, .valo-divider::after { content:''; flex:1; height:1px; background:rgba(255,255,255,0.07); }
.valo-divider-inner { display:flex; align-items:center; gap:5px; padding:0 12px; }
.vd { width:5px; height:5px; transform:rotate(45deg); }
.vd.r { background:var(--red);  box-shadow:0 0 8px var(--red),  0 0 16px rgba(255,70,85,0.4); }
.vd.t { background:var(--teal); box-shadow:0 0 8px var(--teal), 0 0 16px rgba(0,212,191,0.4); width:4px; height:4px; }
.vdbar {
    width:55px; height:2px;
    background:linear-gradient(90deg,var(--red),var(--gold),var(--teal));
    clip-path:polygon(5px 0%,100% 0%,calc(100% - 5px) 100%,0% 100%);
    box-shadow:0 0 10px rgba(0,212,191,0.4), 0 0 6px rgba(255,70,85,0.3);
}

/* ══ 10. GREETING BOX — Valorant panel aura ══ */
.valo-greeting {
    position:relative;
    background:linear-gradient(135deg,
        rgba(35,14,18,0.97) 0%,
        rgba(18,20,34,0.98) 45%,
        rgba(8,28,30,0.97) 100%);
    border:1px solid rgba(255,70,85,0.3);
    border-top:2px solid var(--red);
    border-radius:2px;
    padding:clamp(18px,5vw,28px) clamp(16px,5vw,28px) clamp(14px,4vw,22px);
    margin:4px 0 14px;
    overflow:hidden;
    /* AURA GLOW */
    box-shadow:
        0 0 40px rgba(255,70,85,0.12),
        0 0 80px rgba(255,70,85,0.05),
        0 8px 40px rgba(0,0,0,0.7),
        inset 0 1px 0 rgba(255,255,255,0.05),
        inset 0 0 60px rgba(255,70,85,0.03);
    animation: greetPulse 4s ease-in-out infinite;
}
@keyframes greetPulse {
    0%,100% { box-shadow:0 0 40px rgba(255,70,85,0.12),0 0 80px rgba(255,70,85,0.05),0 8px 40px rgba(0,0,0,0.7),inset 0 1px 0 rgba(255,255,255,0.05); }
    50%      { box-shadow:0 0 60px rgba(255,70,85,0.18),0 0 100px rgba(0,212,191,0.06),0 8px 40px rgba(0,0,0,0.7),inset 0 1px 0 rgba(255,255,255,0.05); }
}

/* Corner cut TL */
.valo-greeting::before { content:''; position:absolute; top:0; left:0; border-style:solid; border-width:22px 22px 0 0; border-color:var(--bg0) transparent transparent transparent; }
/* Teal radial BR */
.valo-greeting::after  { content:''; position:absolute; bottom:-40px; right:-40px; width:200px; height:200px; background:radial-gradient(circle,rgba(0,212,191,0.09) 0%,transparent 65%); pointer-events:none; }
/* Extra red radial TR */
.vg-glow-tr { position:absolute; top:-20px; right:15%; width:160px; height:160px; background:radial-gradient(circle,rgba(255,70,85,0.07) 0%,transparent 65%); pointer-events:none; }
/* Gold corner BR */
.vg-corner-br { position:absolute; bottom:0; right:0; border-style:solid; border-width:0 0 14px 14px; border-color:transparent transparent rgba(232,201,122,0.25) transparent; }
/* Left triple-color bar */
.valo-vbar { position:absolute; left:0; top:10%; bottom:10%; width:3px;
    background:linear-gradient(180deg,transparent 0%,var(--red) 20%,var(--gold) 50%,var(--teal) 80%,transparent 100%);
    box-shadow:0 0 10px rgba(255,70,85,0.4); opacity:.8; }
/* Right subtle teal bar */
.vg-rbar { position:absolute; right:0; top:30%; bottom:30%; width:2px;
    background:linear-gradient(180deg,transparent 0%,var(--teal) 40%,transparent 100%);
    opacity:.3; }
/* Bottom red line */
.vg-bline { position:absolute; bottom:0; left:10%; right:10%; height:1px;
    background:linear-gradient(90deg,transparent,rgba(255,70,85,0.4),transparent); }

.valo-status-row { display:flex; align-items:center; justify-content:center; gap:6px; margin-bottom:10px; }
.valo-status-dot { width:7px; height:7px; background:var(--teal); border-radius:50%;
    box-shadow:0 0 12px var(--teal), 0 0 4px var(--teal2); animation:pulse 2s infinite; }
@keyframes pulse { 0%,100%{opacity:1;box-shadow:0 0 12px var(--teal);}50%{opacity:.4;box-shadow:0 0 3px var(--teal);} }
.valo-status-text { font-family:'Barlow Condensed',sans-serif; font-size:10px; font-weight:700;
    letter-spacing:3px; color:var(--teal2); text-transform:uppercase;
    text-shadow:0 0 10px rgba(0,255,231,0.6); }
.valo-greeting-icon { font-size:clamp(28px,5vw,36px); display:block; text-align:center; margin-bottom:8px;
    filter:drop-shadow(0 0 16px rgba(255,70,85,0.8));
    animation:iconpulse 3s infinite; }
@keyframes iconpulse { 0%,100%{filter:drop-shadow(0 0 16px rgba(255,70,85,0.8));}50%{filter:drop-shadow(0 0 26px rgba(255,150,85,1));} }
.valo-greeting-title { font-family:'Rajdhani',sans-serif;
    font-size:clamp(15px,4vw,21px); font-weight:700; color:var(--white);
    text-align:center; text-transform:uppercase; letter-spacing:2px; margin-bottom:8px;
    text-shadow:0 0 20px rgba(255,255,255,0.12); }
.valo-greeting-sub { font-size:clamp(12px,3vw,13.5px); color:var(--silver); text-align:center; line-height:1.7; }
.valo-stats { display:flex; justify-content:center; gap:clamp(12px,3vw,24px);
    margin-top:14px; padding-top:12px; border-top:1px solid rgba(255,255,255,0.07); }
.valo-stat { text-align:center; line-height:1.2; }
.valo-stat-num { font-family:'Rajdhani',sans-serif;
    font-size:clamp(16px,4vw,22px); font-weight:700; color:var(--red); display:block;
    text-shadow:0 0 14px rgba(255,70,85,0.6); }
.valo-stat-label { font-family:'Barlow Condensed',sans-serif; font-size:9px; letter-spacing:2px; color:#454851; text-transform:uppercase; }
.valo-stat-div { width:1px; background:rgba(255,255,255,0.09); align-self:stretch; }

/* ══ 11. SUGGEST LABEL — red badge with glow ══ */
.valo-suggest-label { display:flex; align-items:center; gap:10px; margin:8px 0 12px; }
.valo-suggest-label::before { content:''; flex:1; height:1px; background:linear-gradient(90deg,transparent,rgba(255,70,85,0.5)); box-shadow:0 0 4px rgba(255,70,85,0.3); }
.valo-suggest-label::after  { content:''; flex:1; height:1px; background:linear-gradient(90deg,rgba(0,212,191,0.5),transparent); box-shadow:0 0 4px rgba(0,212,191,0.3); }
.valo-suggest-label span {
    background:linear-gradient(90deg,#c0303d,#ff4655);
    color:var(--white);
    font-family:'Barlow Condensed',sans-serif;
    font-size:12px; font-weight:800; letter-spacing:2.5px; text-transform:uppercase;
    padding:5px 18px;
    clip-path:polygon(8px 0,100% 0,calc(100% - 8px) 100%,0 100%);
    box-shadow:0 0 20px rgba(255,70,85,0.5), 0 0 40px rgba(255,70,85,0.2), 0 4px 12px rgba(0,0,0,0.5);
    text-shadow:0 1px 4px rgba(0,0,0,0.8);
}

/* ══ 12. SUGGESTION BUTTONS — teal aura + hover neon ══ */
.stButton > button {
    background:linear-gradient(90deg,rgba(0,48,44,0.75),rgba(10,16,26,0.92)) !important;
    color: #d8f8f4 !important;
    border:1px solid rgba(0,212,191,0.28) !important;
    border-left:3px solid var(--teal) !important;
    border-radius:2px !important;
    font-family:'Barlow Condensed',sans-serif !important;
    font-size:clamp(12px,3vw,14px) !important;
    font-weight:700 !important;
    letter-spacing:.5px !important;
    padding:11px 14px !important;
    width:100% !important;
    text-align:left !important;
    white-space:normal !important;
    min-height:48px !important;
    line-height:1.4 !important;
    transition:all .15s ease !important;
    box-shadow:
        0 0 12px rgba(0,212,191,0.12),
        0 2px 8px rgba(0,0,0,0.5),
        inset 0 1px 0 rgba(0,212,191,0.07) !important;
}
.stButton > button:hover {
    background:linear-gradient(90deg,rgba(0,212,191,0.18),rgba(255,70,85,0.12)) !important;
    border-left-color:var(--red) !important;
    border-color:rgba(0,212,191,0.45) !important;
    color:var(--white) !important;
    transform:translateX(4px) !important;
    box-shadow:
        0 0 20px rgba(0,212,191,0.35),
        0 0 40px rgba(0,212,191,0.15),
        0 0 8px rgba(255,70,85,0.1),
        0 4px 16px rgba(0,0,0,0.5),
        inset 0 1px 0 rgba(0,212,191,0.12) !important;
}

/* ══ 13. USER AVATAR — red hexagon LVC ══ */
[data-testid="chatAvatarIcon-user"] {
    background:linear-gradient(135deg,#5a0e18,#1e0408) !important;
    border:2px solid #ff4655 !important;
    border-radius:3px !important;
    overflow:hidden !important;
    box-shadow:
        0 0 14px rgba(255,70,85,0.65),
        0 0 28px rgba(255,70,85,0.25),
        inset 0 0 10px rgba(255,70,85,0.1) !important;
}
[data-testid="chatAvatarIcon-user"] > * { display:none !important; }
[data-testid="chatAvatarIcon-user"]::before {
    content:'';
    display:block; width:100%; height:100%;
    background:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 36 36'%3E%3Crect width='36' height='36' fill='%235a0e18'/%3E%3Cpolygon points='18,3 30,10 30,26 18,33 6,26 6,10' fill='none' stroke='%23ff4655' stroke-width='1.8'/%3E%3Cline x1='6' y1='10' x2='14' y2='18' stroke='%23ff4655' stroke-width='1' opacity='0.4'/%3E%3Ctext x='18' y='23' text-anchor='middle' font-family='Rajdhani,sans-serif' font-size='10' font-weight='700' fill='%23ff7080' letter-spacing='0.5'%3EUSR%3C/text%3E%3Ccircle cx='18' cy='30' r='1.2' fill='%23ff4655'/%3E%3C/svg%3E") center/cover no-repeat !important;
}

/* ══ 14. BOT AVATAR — teal cypher ══ */
[data-testid="chatAvatarIcon-assistant"] {
    background:linear-gradient(135deg,#003832,#000d0c) !important;
    border:2px solid #00d4bf !important;
    border-radius:3px !important;
    overflow:hidden !important;
    box-shadow:
        0 0 14px rgba(0,212,191,0.65),
        0 0 28px rgba(0,212,191,0.25),
        inset 0 0 10px rgba(0,212,191,0.1) !important;
}
[data-testid="chatAvatarIcon-assistant"] > * { display:none !important; }
[data-testid="chatAvatarIcon-assistant"]::before {
    content:'';
    display:block; width:100%; height:100%;
    background:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 36 36'%3E%3Crect width='36' height='36' fill='%23003832'/%3E%3Cpolygon points='18,3 31,10.5 31,25.5 18,33 5,25.5 5,10.5' fill='none' stroke='%2300d4bf' stroke-width='1.8'/%3E%3Ccircle cx='18' cy='18' r='6' fill='none' stroke='%2300d4bf' stroke-width='1.2' opacity='0.8'/%3E%3Ccircle cx='18' cy='18' r='2.5' fill='%2300ffe7' opacity='0.9'/%3E%3Cline x1='18' y1='3' x2='18' y2='11' stroke='%2300d4bf' stroke-width='1' opacity='0.5'/%3E%3Cline x1='18' y1='25' x2='18' y2='33' stroke='%2300d4bf' stroke-width='1' opacity='0.5'/%3E%3Cline x1='5' y1='18' x2='11' y2='18' stroke='%2300d4bf' stroke-width='1' opacity='0.4'/%3E%3Cline x1='25' y1='18' x2='31' y2='18' stroke='%2300d4bf' stroke-width='1' opacity='0.4'/%3E%3C/svg%3E") center/cover no-repeat !important;
}

/* ══ 15. USER BUBBLE — Omen red panel ══ */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background:linear-gradient(135deg,
        rgba(90,18,25,0.95) 0%,
        rgba(55,10,16,0.97) 40%,
        rgba(18,8,12,0.99) 100%) !important;
    border:1px solid rgba(255,70,85,0.38) !important;
    border-right:4px solid #ff4655 !important;
    border-radius:4px !important;
    padding:14px 18px !important;
    margin:7px 0 !important;
    box-shadow:
        4px 0 20px rgba(255,70,85,0.12),
        0 4px 20px rgba(0,0,0,0.7),
        inset -1px 0 20px rgba(255,70,85,0.04),
        inset 0 1px 0 rgba(255,70,85,0.1) !important;
}

/* ══ 16. BOT BUBBLE — Cypher teal panel ══ */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    background:linear-gradient(135deg,
        rgba(6,52,50,0.95) 0%,
        rgba(4,30,30,0.97) 40%,
        rgba(6,12,18,0.99) 100%) !important;
    border:1px solid rgba(0,212,191,0.32) !important;
    border-left:4px solid #00d4bf !important;
    border-radius:4px !important;
    padding:14px 18px !important;
    margin:7px 0 !important;
    box-shadow:
        -4px 0 20px rgba(0,212,191,0.10),
        0 4px 20px rgba(0,0,0,0.7),
        inset 1px 0 20px rgba(0,212,191,0.03),
        inset 0 1px 0 rgba(0,212,191,0.08) !important;
}

/* ══ 17. CHAT TEXT — bright ══ */
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li {
    font-size:clamp(13.5px,3.8vw,15px) !important;
    line-height:1.8 !important;
    color:#f2ede6 !important;
    text-shadow:0 1px 5px rgba(0,0,0,0.95) !important;
}
[data-testid="stChatMessage"] h3 {
    font-family:'Rajdhani',sans-serif !important;
    font-size:clamp(14px,4vw,18px) !important;
    font-weight:700 !important; text-transform:uppercase !important;
    letter-spacing:2px !important; color:var(--white) !important;
    margin-bottom:8px !important; padding-bottom:5px !important;
    border-bottom:1px solid rgba(255,255,255,0.09) !important;
    text-shadow:0 0 16px rgba(255,255,255,0.12) !important;
}
[data-testid="stChatMessage"] strong {
    color:#ffbcc2 !important; font-weight:700 !important;
    text-shadow:0 0 8px rgba(255,70,85,0.35) !important;
}
[data-testid="stChatMessage"] em {
    color:var(--teal2) !important; font-style:normal !important; font-size:11px !important;
    text-shadow:0 0 8px rgba(0,255,231,0.4) !important;
}
[data-testid="stChatMessage"] code {
    background:rgba(0,212,191,0.12) !important; color:#6fffec !important;
    border:1px solid rgba(0,212,191,0.35) !important;
    border-radius:2px !important; padding:2px 7px !important; font-size:12px !important;
    text-shadow:0 0 6px rgba(0,255,231,0.3) !important;
}

/* ══ 18. CHAT INPUT ══ */
.stChatInput > div {
    background:linear-gradient(135deg,rgba(20,24,36,0.98),rgba(14,18,28,0.99)) !important;
    border:1px solid rgba(255,70,85,0.2) !important;
    border-radius:4px !important;
    box-shadow:0 0 20px rgba(255,70,85,0.06),0 4px 16px rgba(0,0,0,0.6) !important;
}
.stChatInput textarea {
    background:transparent !important;
    color:var(--cream) !important;
    border:none !important;
    border-bottom:2px solid rgba(255,70,85,0.3) !important;
    border-radius:0 !important;
    font-family:'Barlow',sans-serif !important;
    font-size:clamp(13px,3.5vw,14px) !important;
    caret-color:var(--red) !important;
}
.stChatInput textarea:focus {
    border-bottom-color:var(--red) !important;
    box-shadow:0 4px 20px rgba(255,70,85,0.1) !important;
}
.stChatInput textarea::placeholder { color:#3a3e4a !important; font-style:italic !important; }

/* ══ 19. SIDEBAR ══ */
section[data-testid="stSidebar"] {
    background:linear-gradient(180deg,#090c12,#0b0f18) !important;
    border-right:1px solid rgba(255,70,85,0.18) !important;
}
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] div,
section[data-testid="stSidebar"] small { color:#6e6b65 !important; font-size:13px !important; }
section[data-testid="stSidebar"] h2 {
    font-family:'Rajdhani',sans-serif !important; font-size:17px !important;
    color:var(--cream) !important; text-transform:uppercase !important; letter-spacing:3px !important;
}
section[data-testid="stSidebar"] .stButton > button {
    background:transparent !important;
    border:1px solid rgba(255,70,85,0.2) !important;
    border-left:2px solid var(--red) !important;
    color:#6e6b65 !important;
    box-shadow:none !important;
    font-family:'Barlow Condensed',sans-serif !important; font-weight:700 !important; letter-spacing:1px !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background:rgba(255,70,85,0.07) !important; color:var(--cream) !important; transform:none !important;
}

/* ══ 20. SPINNER + misc ══ */
[data-testid="stSpinner"] p {
    color:var(--teal) !important;
    font-family:'Barlow Condensed',sans-serif !important;
    letter-spacing:4px !important; font-size:11px !important; text-transform:uppercase !important;
    text-shadow:0 0 10px rgba(0,212,191,0.6) !important;
}
/* Scrollbar */
::-webkit-scrollbar { width:4px; }
::-webkit-scrollbar-track { background:var(--bg0); }
::-webkit-scrollbar-thumb { background:rgba(255,70,85,0.4); border-radius:2px; }
::-webkit-scrollbar-thumb:hover { background:var(--red); }

#MainMenu, footer, header { visibility:hidden !important; }
.block-container { padding-top:1.2rem !important; padding-bottom:1.5rem !important; max-width:760px !important; }

@media (max-width:600px) {
    .block-container { padding:.7rem .5rem 4.5rem !important; }
    .valo-author { position:relative !important; top:0 !important; justify-content:center !important; margin-bottom:8px !important; }
    .valo-author::before { display:none; }
    [data-testid="stChatMessage"] { padding:10px 12px !important; margin:4px 0 !important; }
    .stButton > button { min-height:44px !important; padding:9px 11px !important; }
    .valo-greeting { padding:16px 12px !important; }
}
</style>
""", unsafe_allow_html=True)

# ========================
# GROQ
# ========================
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except KeyError:
    st.error("❌ Chưa cấu hình GROQ_API_KEY trong Secrets!")
    st.stop()
except Exception as e:
    st.error(f"❌ {str(e)}")
    st.stop()

def load_database():
    if os.path.exists("database_pc.json"):
        with open("database_pc.json","r",encoding="utf-8") as f: return json.load(f)
    return {"loi_he_thong":[],"linh_kien_pc":[]}
def load_raw_json():
    if os.path.exists("database_pc.json"):
        with open("database_pc.json","r",encoding="utf-8") as f: return f.read()
    return "{}"

data_pc=load_database(); raw_json_context=load_raw_json()
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

LVC_SVG = """<svg viewBox="0 0 52 52" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="rg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#ff2233"/>
      <stop offset="100%" style="stop-color:#ff4655"/>
    </linearGradient>
    <linearGradient id="tg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#00d4bf"/>
      <stop offset="100%" style="stop-color:#007a70"/>
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="1.5" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <polygon points="26,2 48,14 48,38 26,50 4,38 4,14" fill="rgba(255,30,50,0.08)" stroke="url(#rg)" stroke-width="2" filter="url(#glow)"/>
  <polygon points="26,8 42,17 42,35 26,44 10,35 10,17" fill="rgba(0,212,191,0.05)" stroke="url(#tg)" stroke-width="1" opacity="0.7"/>
  <line x1="4" y1="14" x2="14" y2="24" stroke="#ff4655" stroke-width="1.5" opacity="0.5"/>
  <line x1="48" y1="38" x2="38" y2="28" stroke="#00d4bf" stroke-width="1.5" opacity="0.5"/>
  <text x="26" y="31" text-anchor="middle" font-family="Rajdhani,sans-serif" font-size="13" font-weight="700" fill="white" letter-spacing="1" filter="url(#glow)">LVC</text>
  <circle cx="26" cy="38" r="1.8" fill="#ff4655" opacity="0.9"/>
  <circle cx="26" cy="38" r="3.5" fill="none" stroke="#ff4655" stroke-width="0.5" opacity="0.4"/>
</svg>"""

st.markdown(f"""
<div class="valo-header">
    <div class="valo-author">Lê Văn Chung · 10A4</div>
    <div class="valo-eyebrow">⚡ STEM PROJECT ⚡</div>
    <div class="valo-logo-wrap">
        <div class="lvc-logo">{LVC_SVG}</div>
        <div class="valo-title">PC<span class="slash">/</span><span class="red">SOLVING</span></div>
    </div>
    <div class="valo-subtitle">
        <span class="sub-d r"></span>
        <span class="sub-r">CHẨN ĐOÁN</span>
        <span class="sub-d r"></span>
        <span class="sub-w">PHÂN TÍCH</span>
        <span class="sub-d t"></span>
        <span class="sub-t">XỬ LÝ TỰ ĐỘNG</span>
        <span class="sub-d t"></span>
    </div>
</div>
<div class="valo-divider">
    <div class="valo-divider-inner">
        <div class="vd r"></div><div class="vdbar"></div><div class="vd t"></div>
    </div>
</div>
""", unsafe_allow_html=True)

if "messages"      not in st.session_state: st.session_state.messages=[]
if "greeted"       not in st.session_state: st.session_state.greeted=False
if "suggestions"   not in st.session_state: st.session_state.suggestions=[]
if "pending_query" not in st.session_state: st.session_state.pending_query=None

ALL_SUGGESTIONS = [
    ("⚠  Màn hình xanh BSOD đột ngột",        "Máy tính bị màn hình xanh chết đột ngột, phải làm gì?"),
    ("▪  Màn hình đen không có tín hiệu",       "Máy lên nguồn nhưng màn hình đen, không có tín hiệu"),
    ("◈  PC bíp dài khi khởi động",             "Máy bíp dài liên tục khi bật, không vào được Windows"),
    ("◉  Windows boot loop liên tục",           "Máy cứ khởi động lại liên tục không vào được Windows"),
    ("✕  Lỗi 0xc0000005 văng game",             "Game bị lỗi 0xc0000005 không mở được cách fix?"),
    ("✕  Lỗi 0xc000021a không boot Windows",    "Máy báo lỗi 0xc000021a không boot được vào Windows"),
    ("⚠  PC tự reboot khi chơi game nặng",      "PC tự reboot đột ngột trong lúc chơi game nặng"),
    ("▪  Máy không nhận chuột bàn phím USB",    "Cắm USB chuột bàn phím vào máy không nhận lỗi gì?"),
    ("◈  SSD NVMe không nhận trong BIOS",       "BIOS không nhận ổ SSD NVMe sau khi lắp vào mainboard"),
    ("◉  No Boot Device Found khi bật máy",     "Máy báo No Boot Device Found không vào được hệ điều hành"),
    ("🌡  CPU 95°C — overheat nghiêm trọng",    "CPU nhiệt độ lên đến 95 độ C khi chạy game nguy hiểm không?"),
    ("◆  RAM 8GB có đủ cho game 2024?",          "RAM 8GB có đủ dùng để chơi game hiện đại năm 2024 không?"),
    ("⚡  Nguồn bao nhiêu W cho RTX 3060?",      "RTX 3060 cần nguồn bao nhiêu W dùng nguồn 500W được không?"),
    ("◆  Tản nhiệt nước hay tản nhiệt khí?",     "Nên dùng tản nhiệt nước hay tản nhiệt khí cho i5-12400F?"),
    ("▶  SSD NVMe vs SSD SATA khác gì?",         "SSD NVMe và SSD SATA khác nhau ở điểm gì nên mua loại nào?"),
    ("◉  RAM 2x8GB vs 1x16GB cái nào nhanh?",   "Lắp 2 thanh RAM 8GB hay 1 thanh 16GB thì nhanh hơn?"),
    ("◆  i5-12400F chơi game 2024 đủ không?",    "i5-12400F hiệu năng thế nào chơi game 2024 có đủ không?"),
    ("▶  i5 vs Ryzen 5 tầm 3-4 triệu",          "Tầm giá 3-4 triệu nên chọn Intel i5 hay AMD Ryzen 5?"),
    ("◈  i3-12100F + RTX 3060 có bottleneck?",   "i3-12100F dùng với RTX 3060 có bị cổ chai hiệu năng không?"),
    ("⚡  Ryzen 5 5600X cần tản nhiệt rời?",     "Ryzen 5 5600X có kèm tản nhiệt box dùng được không?"),
    ("🎮  GTX 1650 chơi game gì mượt ở FHD?",   "GTX 1650 chơi mượt những game nào ở độ phân giải 1080p?"),
    ("▶  RTX 3060 vs RX 6600 nên mua cái nào?", "So sánh RTX 3060 và RX 6600 nên chọn card nào?"),
    ("◆  RTX 4060 có đáng mua hơn RTX 3060?",   "RTX 4060 có đáng mua hơn RTX 3060 về giá tiền không?"),
    ("◉  iGPU Intel UHD đủ dùng văn phòng?",    "Dùng Intel UHD Graphics iGPU cho văn phòng có đủ không?"),
    ("◆  H610 hay B660 nên chọn mainboard nào?", "Mainboard H610 và B660 khác nhau thế nào nên mua loại nào?"),
    ("▪  Socket LGA1700 dùng CPU đời mấy?",      "Socket LGA1700 hỗ trợ những CPU Intel đời mấy?"),
    ("◈  B550 có dùng được Ryzen 5 5600X?",      "Mainboard B550 có tương thích với Ryzen 5 5600X không?"),
    ("📱  Snapdragon 888 nóng máy có bình thường?","Chip Snapdragon 888 bị nóng máy nhiều có phải lỗi không?"),
    ("📱  Dimensity 9200 vs Snapdragon 8 Gen2",   "So sánh Dimensity 9200 với Snapdragon 8 Gen 2 loại nào mạnh?"),
    ("📱  Apple A17 Pro mạnh cỡ nào vs Android?", "Chip Apple A17 Pro mạnh đến đâu so với chip Android cao cấp?"),
    ("⚡  Build PC 10 triệu chơi game FHD",       "Gợi ý cấu hình PC build 10 triệu đồng chơi game Full HD mượt"),
    ("◆  Combo i5-12400F + RTX 3060 tốt không?", "Combo i5-12400F với RTX 3060 12GB chơi game có bottleneck không?"),
]

if not st.session_state.suggestions:
    st.session_state.suggestions = random.sample(ALL_SUGGESTIONS, 4)

st.markdown(f"""
<div class="valo-greeting">
    <div class="valo-vbar"></div>
    <div class="vg-glow-tr"></div>
    <div class="vg-corner-br"></div>
    <div class="vg-rbar"></div>
    <div class="vg-bline"></div>
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
        <div class="valo-stat"><span class="valo-stat-num">{db_loi}</span><span class="valo-stat-label">Lỗi hệ thống</span></div>
        <div class="valo-stat-div"></div>
        <div class="valo-stat"><span class="valo-stat-num">{db_lk}</span><span class="valo-stat-label">Linh kiện PC</span></div>
        <div class="valo-stat-div"></div>
        <div class="valo-stat">
            <span class="valo-stat-num" style="color:var(--teal);text-shadow:0 0 14px rgba(0,212,191,0.7)">24/7</span>
            <span class="valo-stat-label">Hỗ trợ</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="valo-suggest-label"><span>CHỌN NHANH VẤN ĐỀ</span></div>', unsafe_allow_html=True)
col1, col2 = st.columns(2, gap="small")
for i,(label,query) in enumerate(st.session_state.suggestions):
    with (col1 if i%2==0 else col2):
        if st.button(label, key=f"sug_{i}"):
            st.session_state.greeted=True; st.session_state.pending_query=query; st.rerun()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

def calculate_match_score(item,q_clean,user_numbers):
    score=0; item_kws=[str(kw).lower().strip() for kw in item.get("keywords",[])]; user_words=q_clean.split()
    for kw in item_kws:
        if kw in user_words or (kw.isdigit() and kw in q_clean): score+=1
    if score==0: return 0
    item_nums=[re.sub(r'\D','',kw) for kw in item_kws if re.search(r'\d{3,}',kw)]; item_nums=[n for n in item_nums if n]
    if item_nums and user_numbers:
        if not set(item_nums).intersection(set(user_numbers)): return 0
    return score

def search_database(user_query):
    q_clean=re.sub(r'[-–_,.\?!\(\)]',' ',user_query.lower().strip())
    user_numbers=[re.sub(r'\D','',w) for w in q_clean.split() if re.search(r'\d{3,}',w)]; user_numbers=[n for n in user_numbers if n]
    best_match,max_score,match_pool=None,0,""
    for item in data_pc.get("linh_kien_pc",[]):
        s=calculate_match_score(item,q_clean,user_numbers)
        if s>max_score: max_score,best_match,match_pool=s,item,"linh_kien"
    for item in data_pc.get("loi_he_thong",[]):
        s=calculate_match_score(item,q_clean,user_numbers)
        if s>max_score: max_score,best_match,match_pool=s,item,"loi"
    if max_score>=2 and best_match:
        if match_pool=="loi":
            return f"### ✕  {best_match['ten']}\n*— Lê Văn Chung 10A4*\n\n**⚠ Nguyên nhân:** {best_match['nguyen_nhan']}\n\n**◈ Khắc phục:**\n{best_match['giai_phap']}"
        else:
            return f"### ◆  {best_match['ten']}\n*— Lê Văn Chung 10A4*\n\n**⚙ Thông số:** {best_match.get('thong_so','')}\n\n**◉ Socket:** `{best_match.get('socket','')}`\n\n**▶ Tư vấn:** {best_match.get('chuyen_gia_tu_van','')}"
    return None

def detect_type(query):
    q=query.lower()
    hw=["i3","i5","i7","i9","ryzen","gtx","rtx","rx","vga","card","cpu","ram","ssd","mainboard","main","nguồn","psu","tản nhiệt","socket","ddr","mua","so sánh","nên chọn","upgrade","nâng cấp","combo","build","cấu hình","snapdragon","dimensity","exynos","helio","chip","điện thoại","iphone","samsung","apple"]
    err=["lỗi","bsod","xanh","đen","bíp","crash","sập","đơ","treo","chậm","lag","không bật","không lên","restart","khởi động","update","0x","error","fix","sửa","boot","không nhận","không vào"]
    for w in hw:
        if w in q: return "hardware"
    for w in err:
        if w in q: return "error"
    return "general"

BASE="TUYỆT ĐỐI KHÔNG dùng: 'AI','mô hình ngôn ngữ','LLM','Groq','Meta','Llama','trí tuệ nhân tạo'. Đọc KỸ câu hỏi. Trả lời ĐÚNG và ĐỦ."
PE=f"Bạn là hệ thống chẩn đoán lỗi của Lê Văn Chung 10A4.\n{BASE}\nKho:{raw_json_context}\nQUY TẮC: 1 câu nguyên nhân + tối đa 4 bước ngắn + 1 tip. Không dài dòng."
PH=f"Bạn là chuyên gia tư vấn linh kiện PC của Lê Văn Chung 10A4.\n{BASE}\nKho:{raw_json_context}\nQUY TẮC: Thông số quan trọng, so sánh nếu cần, gợi ý combo, kết bằng 1 khuyến nghị. Mở đầu: 'Dựa trên cơ sở dữ liệu kỹ thuật của tác giả Lê Văn Chung 10A4...'"
PG=f"Bạn là hệ thống hỗ trợ kỹ thuật của Lê Văn Chung 10A4.\n{BASE}\nKho:{raw_json_context}\nTrả lời tiếng Việt, súc tích."

def ask_engine(user_query,chat_history):
    qt=detect_type(user_query)
    if qt=="error": sys,mt,t=PE,500,0.3
    elif qt=="hardware": sys,mt,t=PH,800,0.5
    else: sys,mt,t=PG,600,0.4
    msgs=[{"role":"system","content":sys}]
    for m in chat_history[-6:]: msgs.append({"role":m["role"],"content":m["content"]})
    msgs.append({"role":"user","content":user_query})
    r=client.chat.completions.create(model="llama-3.3-70b-versatile",messages=msgs,max_tokens=mt,temperature=t)
    return r.choices[0].message.content

def handle_message(prompt):
    st.session_state.messages.append({"role":"user","content":prompt})
    with st.chat_message("user"): st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("ĐANG PHÂN TÍCH DỮ LIỆU..."):
            try:
                ans=search_database(prompt) or ask_engine(prompt,st.session_state.messages)
                st.markdown(ans)
                st.session_state.messages.append({"role":"assistant","content":ans})
            except: st.error("❌ Hệ thống gián đoạn. Vui lòng thử lại.")

if st.session_state.pending_query:
    q=st.session_state.pending_query; st.session_state.pending_query=None; handle_message(q)
if prompt:=st.chat_input("Nhập mã lỗi hoặc linh kiện cần phân tích..."):
    st.session_state.greeted=True; handle_message(prompt)
