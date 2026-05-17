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

/* ═══════════════════════════════
   PALETTE
═══════════════════════════════ */
:root {
    --red:    #ff4655;
    --red2:   #ff6b77;
    --teal:   #00d4bf;
    --teal2:  #00ffe7;
    --gold:   #e8c97a;
    --gold2:  #ffd980;
    --purple: #bd93f9;
    --bg0:    #0b0e14;
    --bg1:    #111520;
    --bg2:    #181c2a;
    --bg3:    #1f2438;
    --cream:  #ece8e1;
    --white:  #ffffff;
    --silver: #c8c4bc;
}

/* ═══════════════════════════════
   1. BASE
═══════════════════════════════ */
html, body, .stApp {
    background: var(--bg0) !important;
    color: var(--cream) !important;
    font-family: 'Barlow', sans-serif !important;
}

/* ═══════════════════════════════
   2. BACKGROUND — map zones
═══════════════════════════════ */
.stApp::before {
    content: '';
    position: fixed; inset: 0;
    pointer-events: none; z-index: 0;
    background:
        radial-gradient(ellipse 55% 45% at -5% 0%,   rgba(255,70,85,0.13) 0%, transparent 60%),
        radial-gradient(ellipse 55% 45% at 105% 100%, rgba(0,212,191,0.10) 0%, transparent 60%),
        radial-gradient(ellipse 50% 30% at 50% 50%,   rgba(232,201,122,0.03) 0%, transparent 55%),
        radial-gradient(ellipse 30% 25% at 100% 5%,   rgba(189,147,249,0.05) 0%, transparent 60%),
        repeating-linear-gradient(-52deg, transparent 0, transparent 55px, rgba(255,70,85,0.022) 55px, rgba(255,70,85,0.022) 56px),
        repeating-linear-gradient( 38deg, transparent 0, transparent 80px, rgba(0,212,191,0.013) 80px, rgba(0,212,191,0.013) 81px),
        repeating-linear-gradient(180deg, transparent 0, transparent 5px,  rgba(255,255,255,0.003) 5px, rgba(255,255,255,0.003) 6px);
}

/* ═══════════════════════════════
   3. TOP BAR glow
═══════════════════════════════ */
.stApp::after {
    content: '';
    position: fixed; top:0; left:0; right:0; height:3px; z-index:9999;
    background: linear-gradient(90deg,
        #ff4655 0%, #ff4655 80px, #c0303d 160px,
        transparent 280px, transparent calc(100% - 280px),
        #007a70 calc(100% - 160px), #00d4bf calc(100% - 80px), #00ffe7 100%);
    box-shadow: 0 0 12px rgba(255,70,85,0.5), 0 0 24px rgba(255,70,85,0.2);
    filter: drop-shadow(0 2px 6px rgba(0,212,191,0.4));
}

/* ═══════════════════════════════
   4. FIX WHITE CONTAINER — chat input area
═══════════════════════════════ */
.stChatFloatingInputContainer,
[data-testid="stBottom"],
[data-testid="stBottom"] > div,
section.main > div:last-child,
.stChatInputContainer,
div[class*="chatInputContainer"],
div[class*="stChatInput"] {
    background: transparent !important;
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
}
/* Kill the white pill container */
[data-testid="stBottom"] > div > div {
    background: transparent !important;
    backdrop-filter: none !important;
}

/* ═══════════════════════════════
   5. CHAT INPUT redesign
═══════════════════════════════ */
.stChatInput > div {
    background: linear-gradient(135deg, rgba(20,24,38,0.98), rgba(12,16,26,0.99)) !important;
    border: 1px solid rgba(255,70,85,0.2) !important;
    border-radius: 3px !important;
    box-shadow: 0 0 20px rgba(255,70,85,0.06), 0 0 40px rgba(0,212,191,0.03) !important;
}
.stChatInput textarea {
    background: transparent !important;
    color: var(--cream) !important;
    border: none !important;
    border-bottom: 2px solid rgba(255,70,85,0.25) !important;
    border-radius: 0 !important;
    font-family: 'Barlow', sans-serif !important;
    font-size: clamp(13px,3.5vw,14px) !important;
    caret-color: var(--red) !important;
}
.stChatInput textarea:focus {
    border-bottom-color: var(--red) !important;
    box-shadow: 0 2px 16px rgba(255,70,85,0.12) !important;
}
.stChatInput textarea::placeholder { color: #454851 !important; }

/* Send button */
.stChatInput button {
    background: linear-gradient(135deg, rgba(255,70,85,0.15), rgba(192,48,61,0.1)) !important;
    border: 1px solid rgba(255,70,85,0.3) !important;
    border-radius: 2px !important;
    color: var(--red) !important;
    transition: all .15s ease !important;
}
.stChatInput button:hover {
    background: rgba(255,70,85,0.25) !important;
    box-shadow: 0 0 12px rgba(255,70,85,0.4) !important;
}

/* ═══════════════════════════════
   6. HEADER
═══════════════════════════════ */
.valo-header { text-align:center; padding:10px 0 2px; position:relative; }
.valo-author {
    font-family:'Barlow Condensed',sans-serif;
    font-size:10px; font-weight:700; letter-spacing:2.5px; text-transform:uppercase;
    background:linear-gradient(90deg,#00f0ff,#00d4bf);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
    filter:drop-shadow(0 0 8px rgba(0,240,255,0.5));
    text-align:right; margin-bottom:4px;
    display:flex; align-items:center; justify-content:flex-end; gap:6px;
}
.valo-author::before { content:''; display:block; width:20px; height:1px; background:linear-gradient(90deg,transparent,#00f0ff); }

.valo-eyebrow {
    font-family:'Barlow Condensed',sans-serif;
    font-size:clamp(9px,2vw,11px); font-weight:800; letter-spacing:6px;
    color:var(--red); text-transform:uppercase; margin-bottom:6px;
    display:flex; align-items:center; justify-content:center; gap:12px;
    text-shadow:0 0 14px rgba(255,70,85,0.6);
}
.valo-eyebrow::before { content:''; width:36px; height:1px; background:linear-gradient(90deg,transparent,var(--red)); }
.valo-eyebrow::after  { content:''; width:36px; height:1px; background:linear-gradient(90deg,var(--red),transparent); }

/* ═══════════════════════════════
   7. LOGO + TITLE
═══════════════════════════════ */
.valo-logo-wrap { display:flex; align-items:center; justify-content:center; gap:16px; margin-bottom:4px; }
.lvc-logo {
    width:clamp(40px,7vw,54px); height:clamp(40px,7vw,54px); flex-shrink:0;
    filter:drop-shadow(0 0 12px rgba(255,70,85,0.55)) drop-shadow(0 0 4px rgba(0,212,191,0.3));
    animation:logopulse 4s ease-in-out infinite;
}
@keyframes logopulse {
    0%,100%{filter:drop-shadow(0 0 12px rgba(255,70,85,0.55)) drop-shadow(0 0 4px rgba(0,212,191,0.3));}
    50%{filter:drop-shadow(0 0 20px rgba(255,70,85,0.8)) drop-shadow(0 0 8px rgba(0,212,191,0.5));}
}
.lvc-logo svg { width:100%; height:100%; }
.valo-title {
    font-family:'Rajdhani',sans-serif;
    font-size:clamp(30px,7.5vw,64px); font-weight:700;
    letter-spacing:3px; line-height:1; text-transform:uppercase; margin:0;
    color:var(--white);
    text-shadow:0 0 30px rgba(255,70,85,0.2), 0 2px 4px rgba(0,0,0,0.8);
}
.valo-title .red   { color:var(--red); text-shadow:0 0 24px rgba(255,70,85,0.7); }
.valo-title .slash { color:var(--red); opacity:.5; margin:0 2px; }

/* ═══════════════════════════════
   8. SUBTITLE colored words
═══════════════════════════════ */
.valo-subtitle {
    font-family:'Barlow Condensed',sans-serif;
    font-size:clamp(11px,2.8vw,14px); font-weight:800;
    letter-spacing:4px; text-transform:uppercase; margin-top:8px;
    display:flex; align-items:center; justify-content:center; gap:8px; flex-wrap:wrap;
}
.sub-r { color:var(--red);  text-shadow:0 0 10px rgba(255,70,85,0.7); }
.sub-w { color:var(--white);}
.sub-t { color:var(--teal); text-shadow:0 0 10px rgba(0,212,191,0.7); }
.sub-d { display:inline-block; width:4px; height:4px; transform:rotate(45deg); }
.sub-d.r { background:var(--red);  box-shadow:0 0 6px var(--red); }
.sub-d.t { background:var(--teal); box-shadow:0 0 6px var(--teal); }

/* ═══════════════════════════════
   9. DIVIDER
═══════════════════════════════ */
.valo-divider { display:flex; align-items:center; margin:12px 0 8px; }
.valo-divider::before,.valo-divider::after { content:''; flex:1; height:1px; background:rgba(255,255,255,0.07); }
.valo-divider-inner { display:flex; align-items:center; gap:5px; padding:0 12px; }
.vd { width:5px; height:5px; transform:rotate(45deg); }
.vd.r { background:var(--red);  box-shadow:0 0 8px var(--red); }
.vd.t { background:var(--teal); box-shadow:0 0 8px var(--teal); width:4px; height:4px; opacity:.85; }
.vdbar {
    width:55px; height:2px;
    background:linear-gradient(90deg,var(--red),var(--gold),var(--teal));
    clip-path:polygon(5px 0%,100% 0%,calc(100% - 5px) 100%,0% 100%);
    box-shadow:0 0 10px rgba(0,212,191,0.35);
}

/* ═══════════════════════════════
   10. GREETING BOX — STRONG AURA
═══════════════════════════════ */
.valo-greeting {
    position:relative;
    background:
        linear-gradient(135deg,
            rgba(40,14,18,0.96) 0%,
            rgba(18,20,34,0.97) 45%,
            rgba(8,30,30,0.96) 100%);
    border:1px solid rgba(255,70,85,0.35);
    border-top:2px solid var(--red);
    border-radius:3px;
    padding:clamp(18px,5vw,28px) clamp(16px,5vw,28px) clamp(14px,4vw,22px);
    margin:4px 0 14px;
    overflow:hidden;
    /* STRONG AURA */
    box-shadow:
        0 0 0 1px rgba(255,70,85,0.08),
        0 8px 40px rgba(0,0,0,0.7),
        0 0 40px rgba(255,70,85,0.10),
        0 0 80px rgba(255,70,85,0.05),
        inset 0 1px 0 rgba(255,255,255,0.05),
        inset 0 0 60px rgba(255,70,85,0.03);
    animation:greetpulse 4s ease-in-out infinite;
}
@keyframes greetpulse {
    0%,100%{box-shadow:0 0 0 1px rgba(255,70,85,0.08),0 8px 40px rgba(0,0,0,0.7),0 0 40px rgba(255,70,85,0.10),0 0 80px rgba(255,70,85,0.05),inset 0 1px 0 rgba(255,255,255,0.05);}
    50%{box-shadow:0 0 0 1px rgba(255,70,85,0.15),0 8px 40px rgba(0,0,0,0.7),0 0 60px rgba(255,70,85,0.16),0 0 100px rgba(255,70,85,0.08),inset 0 1px 0 rgba(255,255,255,0.07);}
}
/* Corner cut TL */
.valo-greeting::before {
    content:''; position:absolute; top:0; left:0;
    border-style:solid; border-width:22px 22px 0 0;
    border-color:var(--bg0) transparent transparent transparent;
}
/* Teal glow BR */
.valo-greeting::after {
    content:''; position:absolute; bottom:-40px; right:-40px;
    width:220px; height:220px;
    background:radial-gradient(circle,rgba(0,212,191,0.10) 0%,transparent 65%);
    pointer-events:none;
}
.vg-red-glow {
    position:absolute; top:-30px; right:15%;
    width:180px; height:180px;
    background:radial-gradient(circle,rgba(255,70,85,0.08) 0%,transparent 65%);
    pointer-events:none;
}
.vg-gold-glow {
    position:absolute; top:30%; left:30%;
    width:120px; height:120px;
    background:radial-gradient(circle,rgba(232,201,122,0.04) 0%,transparent 65%);
    pointer-events:none;
}
.vg-corner-br {
    position:absolute; bottom:0; right:0;
    border-style:solid; border-width:0 0 16px 16px;
    border-color:transparent transparent rgba(0,212,191,0.25) transparent;
}
.valo-vbar {
    position:absolute; left:0; top:10%; bottom:10%;
    width:3px;
    background:linear-gradient(180deg,transparent 0%,var(--red) 20%,var(--gold) 50%,var(--teal) 80%,transparent 100%);
    opacity:.8;
    box-shadow:0 0 10px rgba(255,70,85,0.4), 0 0 20px rgba(0,212,191,0.2);
}

.valo-status-row { display:flex; align-items:center; justify-content:center; gap:6px; margin-bottom:10px; }
.valo-status-dot {
    width:7px; height:7px; background:var(--teal); border-radius:50%;
    box-shadow:0 0 10px var(--teal), 0 0 20px rgba(0,212,191,0.4);
    animation:pulse 2s infinite;
}
@keyframes pulse { 0%,100%{box-shadow:0 0 10px var(--teal),0 0 20px rgba(0,212,191,0.4);}50%{box-shadow:0 0 4px var(--teal),0 0 8px rgba(0,212,191,0.2);} }
.valo-status-text {
    font-family:'Barlow Condensed',sans-serif; font-size:10px; font-weight:700;
    letter-spacing:3px; color:var(--teal2); text-transform:uppercase;
    text-shadow:0 0 10px rgba(0,255,231,0.6);
}
.valo-greeting-icon {
    font-size:clamp(28px,5vw,36px); display:block; text-align:center; margin-bottom:8px;
    filter:drop-shadow(0 0 16px rgba(255,70,85,0.8));
    animation:iconpulse 3s ease-in-out infinite;
}
@keyframes iconpulse {
    0%,100%{filter:drop-shadow(0 0 16px rgba(255,70,85,0.8));}
    50%{filter:drop-shadow(0 0 28px rgba(255,70,85,1.0)) drop-shadow(0 0 6px rgba(232,201,122,0.4));}
}
.valo-greeting-title {
    font-family:'Rajdhani',sans-serif;
    font-size:clamp(15px,4vw,21px); font-weight:700;
    color:var(--white); text-align:center; text-transform:uppercase;
    letter-spacing:2px; margin-bottom:8px;
    text-shadow:0 0 20px rgba(255,255,255,0.12);
}
.valo-greeting-sub { font-size:clamp(12px,3vw,13.5px); color:var(--silver); text-align:center; line-height:1.7; }

.valo-stats {
    display:flex; justify-content:center; gap:clamp(12px,3vw,24px);
    margin-top:14px; padding-top:12px; border-top:1px solid rgba(255,255,255,0.07);
}
.valo-stat { text-align:center; line-height:1.2; }
.valo-stat-num {
    font-family:'Rajdhani',sans-serif;
    font-size:clamp(16px,4vw,22px); font-weight:700; color:var(--red); display:block;
    text-shadow:0 0 14px rgba(255,70,85,0.6);
}
.valo-stat-label { font-family:'Barlow Condensed',sans-serif; font-size:9px; letter-spacing:2px; color:#454851; text-transform:uppercase; }
.valo-stat-div { width:1px; background:rgba(255,255,255,0.1); align-self:stretch; }

/* ═══════════════════════════════
   11. SUGGEST LABEL — aura glow
═══════════════════════════════ */
.valo-suggest-label {
    display:flex; align-items:center; gap:10px; margin:8px 0 12px;
}
.valo-suggest-label::before { content:''; flex:1; height:1px; background:linear-gradient(90deg,transparent,rgba(255,70,85,0.5)); box-shadow:0 0 6px rgba(255,70,85,0.2); }
.valo-suggest-label::after  { content:''; flex:1; height:1px; background:linear-gradient(90deg,rgba(0,212,191,0.5),transparent); box-shadow:0 0 6px rgba(0,212,191,0.2); }
.valo-suggest-label span {
    background:linear-gradient(90deg,#c0303d,#ff4655);
    color:var(--white);
    font-family:'Barlow Condensed',sans-serif;
    font-size:12px; font-weight:800; letter-spacing:2.5px; text-transform:uppercase;
    padding:5px 18px;
    clip-path:polygon(8px 0,100% 0,calc(100% - 8px) 100%,0 100%);
    box-shadow:0 0 20px rgba(255,70,85,0.5), 0 4px 20px rgba(255,70,85,0.3);
    text-shadow:0 0 8px rgba(255,200,200,0.4);
}

/* ═══════════════════════════════
   12. BUTTONS — aura on hover + active
═══════════════════════════════ */
.stButton > button {
    background:linear-gradient(90deg,rgba(0,45,42,0.75),rgba(10,16,26,0.92)) !important;
    color:var(--white) !important;
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
    box-shadow:0 2px 10px rgba(0,0,0,0.5), inset 0 1px 0 rgba(0,212,191,0.07) !important;
}
.stButton > button:hover {
    background:linear-gradient(90deg,rgba(0,212,191,0.18),rgba(255,70,85,0.10)) !important;
    border-left-color:var(--red) !important;
    border-color:rgba(0,212,191,0.45) !important;
    transform:translateX(4px) !important;
    box-shadow:
        0 4px 20px rgba(0,212,191,0.30),
        0 0 30px rgba(0,212,191,0.15),
        0 0 60px rgba(0,212,191,0.06),
        inset 0 1px 0 rgba(0,212,191,0.12) !important;
}
.stButton > button:active {
    transform:translateX(2px) !important;
    box-shadow:
        0 2px 10px rgba(255,70,85,0.4),
        0 0 20px rgba(255,70,85,0.2) !important;
    border-left-color:var(--red) !important;
    background:linear-gradient(90deg,rgba(255,70,85,0.18),rgba(0,212,191,0.08)) !important;
}

/* ═══════════════════════════════
   13. USER AVATAR — force override
═══════════════════════════════ */
[data-testid="chatAvatarIcon-user"],
[data-testid="chatAvatarIcon-user"] > *,
div[data-testid="chatAvatarIcon-user"] {
    background: linear-gradient(135deg,#5a0a14,#2a0508) !important;
    background-color: #5a0a14 !important;
    border: 2px solid var(--red) !important;
    border-radius: 3px !important;
    box-shadow:
        0 0 14px rgba(255,70,85,0.6),
        0 0 28px rgba(255,70,85,0.25),
        inset 0 0 12px rgba(255,70,85,0.12) !important;
    color: var(--red) !important;
    overflow: hidden !important;
}
[data-testid="chatAvatarIcon-user"] svg,
[data-testid="chatAvatarIcon-user"] img { display:none !important; }
[data-testid="chatAvatarIcon-user"]::after {
    content: '⚡';
    font-size: 15px;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%; height: 100%;
    filter: drop-shadow(0 0 4px rgba(255,70,85,0.8));
}

/* ═══════════════════════════════
   14. BOT AVATAR — force override
═══════════════════════════════ */
[data-testid="chatAvatarIcon-assistant"],
[data-testid="chatAvatarIcon-assistant"] > *,
div[data-testid="chatAvatarIcon-assistant"] {
    background: linear-gradient(135deg,#003d38,#001410) !important;
    background-color: #003d38 !important;
    border: 2px solid var(--teal) !important;
    border-radius: 3px !important;
    box-shadow:
        0 0 14px rgba(0,212,191,0.55),
        0 0 28px rgba(0,212,191,0.22),
        inset 0 0 12px rgba(0,212,191,0.10) !important;
    color: var(--teal) !important;
    overflow: hidden !important;
}
[data-testid="chatAvatarIcon-assistant"] svg,
[data-testid="chatAvatarIcon-assistant"] img { display:none !important; }
[data-testid="chatAvatarIcon-assistant"]::after {
    content: '🖥';
    font-size: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%; height: 100%;
    filter: drop-shadow(0 0 4px rgba(0,212,191,0.7));
}

/* ═══════════════════════════════
   15. USER CHAT BUBBLE — deep red
   Force override gray default
═══════════════════════════════ */
div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]),
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background:
        linear-gradient(135deg,
            rgba(90,15,22,0.94) 0%,
            rgba(55,8,14,0.96) 40%,
            rgba(22,8,12,0.98) 100%) !important;
    border: 1px solid rgba(255,70,85,0.42) !important;
    border-right: 4px solid var(--red) !important;
    border-radius: 4px !important;
    padding: 14px 18px !important;
    margin: 7px 0 !important;
    box-shadow:
        0 4px 24px rgba(0,0,0,0.65),
        4px 0 24px rgba(255,70,85,0.10),
        0 0 40px rgba(255,70,85,0.04),
        inset 0 1px 0 rgba(255,70,85,0.12),
        inset 0 0 40px rgba(255,70,85,0.04) !important;
}

/* ═══════════════════════════════
   16. BOT CHAT BUBBLE — deep teal
═══════════════════════════════ */
div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-assistant"]),
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    background:
        linear-gradient(135deg,
            rgba(8,55,50,0.93) 0%,
            rgba(5,30,30,0.96) 40%,
            rgba(8,14,20,0.98) 100%) !important;
    border: 1px solid rgba(0,212,191,0.35) !important;
    border-left: 4px solid var(--teal) !important;
    border-radius: 4px !important;
    padding: 14px 18px !important;
    margin: 7px 0 !important;
    box-shadow:
        0 4px 24px rgba(0,0,0,0.65),
        -4px 0 24px rgba(0,212,191,0.08),
        0 0 40px rgba(0,212,191,0.03),
        inset 0 1px 0 rgba(0,212,191,0.10),
        inset 0 0 40px rgba(0,212,191,0.025) !important;
}

/* ═══════════════════════════════
   17. CHAT TEXT — bright & crisp
═══════════════════════════════ */
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li {
    font-size: clamp(13.5px,3.8vw,15px) !important;
    line-height: 1.8 !important;
    color: #f5f1e9 !important;
    text-shadow: 0 1px 5px rgba(0,0,0,0.95) !important;
}
[data-testid="stChatMessage"] h3 {
    font-family: 'Rajdhani',sans-serif !important;
    font-size: clamp(14px,4vw,18px) !important; font-weight:700 !important;
    text-transform: uppercase !important; letter-spacing:2px !important;
    color: var(--white) !important;
    margin-bottom:8px !important; padding-bottom:5px !important;
    border-bottom: 1px solid rgba(255,255,255,0.09) !important;
    text-shadow: 0 0 16px rgba(255,255,255,0.1) !important;
}
[data-testid="stChatMessage"] strong {
    color: #ffbcc2 !important; font-weight:700 !important;
    text-shadow: 0 0 8px rgba(255,70,85,0.35) !important;
}
[data-testid="stChatMessage"] em {
    color: var(--teal2) !important; font-style:normal !important; font-size:11px !important;
    text-shadow: 0 0 6px rgba(0,255,231,0.4) !important;
}
[data-testid="stChatMessage"] code {
    background: rgba(0,212,191,0.12) !important; color:#55ffeb !important;
    border: 1px solid rgba(0,212,191,0.35) !important;
    border-radius:2px !important; padding:2px 7px !important; font-size:12px !important;
    text-shadow: 0 0 6px rgba(0,255,231,0.3) !important;
}

/* ═══════════════════════════════
   18. SIDEBAR
═══════════════════════════════ */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#090c11,#0a0e16) !important;
    border-right: 1px solid rgba(255,70,85,0.18) !important;
}
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] div,
section[data-testid="stSidebar"] small { color:#7a7875 !important; font-size:13px !important; }
section[data-testid="stSidebar"] h2 {
    font-family:'Rajdhani',sans-serif !important; font-size:17px !important;
    color:var(--cream) !important; text-transform:uppercase !important; letter-spacing:3px !important;
}
section[data-testid="stSidebar"] .stButton > button {
    background:transparent !important;
    border:1px solid rgba(255,70,85,0.2) !important; border-left:2px solid var(--red) !important;
    color:#7a7875 !important; font-family:'Barlow Condensed',sans-serif !important;
    font-weight:700 !important; letter-spacing:1px !important; box-shadow:none !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background:rgba(255,70,85,0.07) !important; color:var(--cream) !important; transform:none !important;
}

/* ═══════════════════════════════
   19. SPINNER + MISC
═══════════════════════════════ */
[data-testid="stSpinner"] p {
    color:var(--teal) !important; font-family:'Barlow Condensed',sans-serif !important;
    letter-spacing:4px !important; font-size:11px !important; text-transform:uppercase !important;
    text-shadow:0 0 10px rgba(0,212,191,0.6) !important;
}

/* ═══════════════════════════════
   20. SCROLLBAR Valorant style
═══════════════════════════════ */
::-webkit-scrollbar { width:4px; }
::-webkit-scrollbar-track { background:var(--bg0); }
::-webkit-scrollbar-thumb { background:linear-gradient(180deg,var(--red),var(--teal)); border-radius:2px; }
::-webkit-scrollbar-thumb:hover { background:var(--red); box-shadow:0 0 6px var(--red); }

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
    st.error(f"❌ Lỗi kết nối: {str(e)}")
    st.stop()

# ========================
# DATABASE
# ========================
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

# ========================
# SIDEBAR
# ========================
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

# ========================
# LVC LOGO
# ========================
LVC_SVG = """<svg viewBox="0 0 52 52" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="rg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#ff4655"/><stop offset="100%" style="stop-color:#c0303d"/>
    </linearGradient>
    <linearGradient id="tg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#00d4bf"/><stop offset="100%" style="stop-color:#007a70"/>
    </linearGradient>
  </defs>
  <polygon points="26,2 48,14 48,38 26,50 4,38 4,14" fill="none" stroke="url(#rg)" stroke-width="2.2"/>
  <polygon points="26,8 42,17 42,35 26,44 10,35 10,17" fill="rgba(255,70,85,0.07)" stroke="url(#tg)" stroke-width="1" opacity="0.75"/>
  <line x1="4" y1="14" x2="15" y2="25" stroke="#ff4655" stroke-width="1.5" opacity="0.45"/>
  <line x1="48" y1="38" x2="37" y2="27" stroke="#00d4bf" stroke-width="1.5" opacity="0.45"/>
  <text x="26" y="31" text-anchor="middle" font-family="Rajdhani,sans-serif" font-size="13" font-weight="700" fill="white" letter-spacing="1">LVC</text>
  <circle cx="26" cy="39" r="1.8" fill="#ff4655" opacity="0.85"/>
  <circle cx="26" cy="39" r="3.5" fill="none" stroke="#ff4655" stroke-width="0.5" opacity="0.3"/>
</svg>"""

# ========================
# HEADER
# ========================
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

# ========================
# SESSION
# ========================
if "messages"      not in st.session_state: st.session_state.messages=[]
if "greeted"       not in st.session_state: st.session_state.greeted=False
if "suggestions"   not in st.session_state: st.session_state.suggestions=[]
if "pending_query" not in st.session_state: st.session_state.pending_query=None

# ========================
# 32 GỢI Ý
# ========================
ALL_SUGGESTIONS = [
    ("⚠  Màn hình xanh BSOD đột ngột",        "Máy tính bị màn hình xanh chết đột ngột, phải làm gì?"),
    ("▪  Màn hình đen không có tín hiệu",       "Máy lên nguồn nhưng màn hình đen không có tín hiệu"),
    ("◈  PC bíp dài khi khởi động",             "Máy bíp dài liên tục khi bật không vào được Windows"),
    ("◉  Windows boot loop liên tục",           "Máy cứ khởi động lại liên tục không vào được Windows"),
    ("✕  Lỗi 0xc0000005 văng game",             "Game bị lỗi 0xc0000005 không mở được cách fix?"),
    ("✕  Lỗi 0xc000021a không boot Windows",    "Máy báo lỗi 0xc000021a không boot được vào Windows"),
    ("⚠  PC tự reboot khi chơi game nặng",      "PC tự reboot đột ngột trong lúc chơi game nặng"),
    ("▪  Máy không nhận chuột bàn phím USB",    "Cắm USB chuột bàn phím vào máy không nhận lỗi gì?"),
    ("◈  SSD NVMe không nhận trong BIOS",       "BIOS không nhận ổ SSD NVMe sau khi lắp vào mainboard"),
    ("◉  No Boot Device Found khi bật máy",     "Máy báo No Boot Device Found không vào được hệ điều hành"),
    ("🌡  CPU 95°C overheat nghiêm trọng",      "CPU nhiệt độ lên đến 95 độ C khi chạy game nguy hiểm không?"),
    ("◆  RAM 8GB có đủ cho game 2024?",          "RAM 8GB có đủ dùng để chơi game hiện đại năm 2024 không?"),
    ("⚡  Nguồn bao nhiêu W cho RTX 3060?",      "RTX 3060 cần nguồn bao nhiêu W dùng nguồn 500W được không?"),
    ("◆  Tản nhiệt nước hay tản nhiệt khí?",     "Nên dùng tản nhiệt nước hay tản nhiệt khí cho i5-12400F?"),
    ("▶  SSD NVMe vs SSD SATA khác gì?",         "SSD NVMe và SSD SATA khác nhau điểm gì nên mua loại nào?"),
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

# ========================
# GREETING
# ========================
st.markdown(f"""
<div class="valo-greeting">
    <div class="valo-vbar"></div>
    <div class="vg-red-glow"></div>
    <div class="vg-gold-glow"></div>
    <div class="vg-corner-br"></div>
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
        <div class="valo-stat">
            <span class="valo-stat-num">{db_loi}</span>
            <span class="valo-stat-label">Lỗi hệ thống</span>
        </div>
        <div class="valo-stat-div"></div>
        <div class="valo-stat">
            <span class="valo-stat-num">{db_lk}</span>
            <span class="valo-stat-label">Linh kiện PC</span>
        </div>
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
for i, (label, query) in enumerate(st.session_state.suggestions):
    with (col1 if i % 2 == 0 else col2):
        if st.button(label, key=f"sug_{i}"):
            st.session_state.greeted=True; st.session_state.pending_query=query; st.rerun()

# ========================
# CHAT HISTORY
# ========================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

# ========================
# DATABASE SEARCH
# ========================
def calculate_match_score(item, q_clean, user_numbers):
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

BASE_RULE="TUYỆT ĐỐI KHÔNG dùng: 'AI','mô hình ngôn ngữ','LLM','Groq','Meta','Llama','trí tuệ nhân tạo'. QUAN TRỌNG: Đọc KỸ câu hỏi. Trả lời ĐÚNG và ĐỦ. Không khuôn mẫu cứng nhắc."
PROMPT_ERROR=f"Bạn là hệ thống chẩn đoán lỗi máy tính của Lê Văn Chung 10A4.\n{BASE_RULE}\nKho dữ liệu: {raw_json_context}\nQUY TẮC LỖI: 1 câu nguyên nhân + tối đa 4 bước ngắn + 1 tip phòng tránh nếu cần. Không dài dòng."
PROMPT_HARDWARE=f"Bạn là chuyên gia tư vấn linh kiện PC và điện tử của Lê Văn Chung 10A4.\n{BASE_RULE}\nKho dữ liệu: {raw_json_context}\nQUY TẮC LINH KIỆN: Thông số quan trọng, so sánh nếu hỏi, gợi ý combo, kết bằng 1 khuyến nghị. Mở đầu: 'Dựa trên cơ sở dữ liệu kỹ thuật của tác giả Lê Văn Chung 10A4...'"
PROMPT_GENERAL=f"Bạn là hệ thống hỗ trợ kỹ thuật máy tính của Lê Văn Chung 10A4.\n{BASE_RULE}\nKho dữ liệu: {raw_json_context}\nTrả lời tiếng Việt, súc tích, đúng trọng tâm."

def ask_engine(user_query, chat_history):
    qtype=detect_type(user_query)
    if qtype=="error": system,max_tok,temp=PROMPT_ERROR,500,0.3
    elif qtype=="hardware": system,max_tok,temp=PROMPT_HARDWARE,800,0.5
    else: system,max_tok,temp=PROMPT_GENERAL,600,0.4
    messages=[{"role":"system","content":system}]
    for msg in chat_history[-6:]: messages.append({"role":msg["role"],"content":msg["content"]})
    messages.append({"role":"user","content":user_query})
    response=client.chat.completions.create(model="llama-3.3-70b-versatile",messages=messages,max_tokens=max_tok,temperature=temp)
    return response.choices[0].message.content

def handle_message(prompt):
    st.session_state.messages.append({"role":"user","content":prompt})
    with st.chat_message("user"): st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("ĐANG PHÂN TÍCH DỮ LIỆU..."):
            try:
                answer=search_database(prompt) or ask_engine(prompt,st.session_state.messages)
                st.markdown(answer)
                st.session_state.messages.append({"role":"assistant","content":answer})
            except: st.error("❌ Hệ thống gián đoạn. Vui lòng thử lại.")

if st.session_state.pending_query:
    q=st.session_state.pending_query; st.session_state.pending_query=None; handle_message(q)
if prompt:=st.chat_input("Nhập mã lỗi hoặc linh kiện cần phân tích..."):
    st.session_state.greeted=True; handle_message(prompt)
