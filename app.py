import streamlit as st
import json, re, os, random
from groq import Groq

st.set_page_config(page_title="PC Solving System — Lê Văn Chung 10A4", page_icon="⚡", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Barlow+Condensed:wght@400;600;700;800&family=Barlow:wght@300;400;500;600&display=swap');

:root {
    --R:  #ff4655;  --R2: #ff7080;  --R3: rgba(255,70,85,0.18);
    --T:  #00d4bf;  --T2: #00ffe7;  --T3: rgba(0,212,191,0.15);
    --G:  #e8c97a;
    --bg: #090b11;  --p1: #0f1320;  --p2: #151929;  --p3: #1c2236;
    --W:  #ffffff;  --C:  #ece8e1;  --S:  #b8b4ac;
}

html, body, .stApp { background:var(--bg) !important; color:var(--C) !important; font-family:'Barlow',sans-serif !important; }

/* ══ BACKGROUND: angled panels ══ */
.stApp::before {
    content:''; position:fixed; inset:0; pointer-events:none; z-index:0;
    background:
        /* Red zone — angled top-left */
        linear-gradient(135deg, rgba(255,70,85,0.09) 0%, transparent 45%),
        /* Teal zone — angled bottom-right */
        linear-gradient(315deg, rgba(0,212,191,0.07) 0%, transparent 45%),
        /* Purple top-right */
        radial-gradient(ellipse 40% 30% at 100% 0%, rgba(189,147,249,0.05) 0%, transparent 60%),
        /* Tactical grid */
        repeating-linear-gradient(-55deg, transparent 0, transparent 48px, rgba(255,70,85,0.018) 48px, rgba(255,70,85,0.019) 49px),
        repeating-linear-gradient( 35deg, transparent 0, transparent 72px, rgba(0,212,191,0.012) 72px, rgba(0,212,191,0.013) 73px),
        /* Scanlines */
        repeating-linear-gradient(0deg, transparent 0, transparent 3px, rgba(255,255,255,0.004) 3px, rgba(255,255,255,0.004) 4px);
}

/* Top glow bar */
.stApp::after {
    content:''; position:fixed; top:0; left:0; right:0; height:2px; z-index:9999;
    background:linear-gradient(90deg,transparent 0%,#ff4655 15%,#ff7080 30%,transparent 45%,transparent 55%,#00d4bf 70%,#00ffe7 85%,transparent 100%);
    filter:drop-shadow(0 0 6px #ff4655);
}

/* ══ CORNER BRACKET MIXIN — reused via class ══ */
.cb { position:absolute; width:14px; height:14px; }
.cb-tl { top:0; left:0;  border-top:2px solid var(--R); border-left:2px solid var(--R); }
.cb-tr { top:0; right:0; border-top:2px solid var(--R); border-right:2px solid var(--R); }
.cb-bl { bottom:0; left:0;  border-bottom:2px solid var(--T); border-left:2px solid var(--T); }
.cb-br { bottom:0; right:0; border-bottom:2px solid var(--T); border-right:2px solid var(--T); }
.cb-glow-r { box-shadow:inset 0 0 8px rgba(255,70,85,0.2); }
.cb-glow-t { box-shadow:inset 0 0 8px rgba(0,212,191,0.2); }

/* ══ HEADER ══ */
.valo-header { text-align:center; padding:12px 0 2px; position:relative; }

.valo-author {
    font-family:'Barlow Condensed',sans-serif; font-size:10px; font-weight:700;
    letter-spacing:3px; text-transform:uppercase; color:#00f0ff;
    text-shadow:0 0 12px rgba(0,240,255,0.8), 0 0 24px rgba(0,240,255,0.3);
    text-align:right; margin-bottom:5px;
    display:flex; align-items:center; justify-content:flex-end; gap:6px;
}
.valo-author::before { content:''; width:22px; height:1px; background:linear-gradient(90deg,transparent,#00f0ff); box-shadow:0 0 5px #00f0ff; }

.valo-eyebrow {
    font-family:'Barlow Condensed',sans-serif; font-size:clamp(9px,2vw,11px); font-weight:800;
    letter-spacing:7px; color:var(--R); text-transform:uppercase; margin-bottom:6px;
    display:flex; align-items:center; justify-content:center; gap:14px;
    text-shadow:0 0 16px rgba(255,70,85,0.8);
}
.valo-eyebrow::before { content:''; width:40px; height:1px; background:linear-gradient(90deg,transparent,var(--R)); box-shadow:0 0 8px rgba(255,70,85,0.6); }
.valo-eyebrow::after  { content:''; width:40px; height:1px; background:linear-gradient(90deg,var(--R),transparent); box-shadow:0 0 8px rgba(255,70,85,0.6); }

.valo-logo-wrap { display:flex; align-items:center; justify-content:center; gap:18px; margin-bottom:4px; }
.lvc-logo { width:clamp(42px,7vw,56px); height:clamp(42px,7vw,56px); flex-shrink:0; filter:drop-shadow(0 0 10px rgba(255,70,85,0.7)) drop-shadow(0 0 20px rgba(255,70,85,0.3)); }
.lvc-logo svg { width:100%; height:100%; }

.valo-title {
    font-family:'Rajdhani',sans-serif; font-size:clamp(32px,8vw,68px); font-weight:700;
    letter-spacing:4px; line-height:1; text-transform:uppercase; margin:0; color:var(--W);
    text-shadow:0 2px 8px rgba(0,0,0,0.9), 0 0 40px rgba(255,255,255,0.08);
}
.valo-title .red   { color:var(--R); text-shadow:0 0 20px rgba(255,70,85,0.9), 0 0 40px rgba(255,70,85,0.4), 0 2px 8px rgba(0,0,0,0.9); }
.valo-title .slash { color:var(--R); opacity:.4; margin:0 3px; }

.valo-subtitle {
    font-family:'Barlow Condensed',sans-serif; font-size:clamp(11px,2.8vw,14px); font-weight:800;
    letter-spacing:5px; text-transform:uppercase; margin-top:10px;
    display:flex; align-items:center; justify-content:center; gap:10px; flex-wrap:wrap;
}
.sub-r { color:var(--R);  text-shadow:0 0 12px rgba(255,70,85,0.8); }
.sub-w { color:var(--W);  text-shadow:0 0 10px rgba(255,255,255,0.3); }
.sub-t { color:var(--T);  text-shadow:0 0 12px rgba(0,212,191,0.8); }
.sub-d { display:inline-block; width:5px; height:5px; transform:rotate(45deg); }
.sub-d.r { background:var(--R); box-shadow:0 0 8px var(--R), 0 0 16px rgba(255,70,85,0.4); }
.sub-d.t { background:var(--T); box-shadow:0 0 8px var(--T), 0 0 16px rgba(0,212,191,0.4); }

/* Divider */
.valo-divider { display:flex; align-items:center; margin:14px 0 10px; gap:0; }
.valo-divider::before, .valo-divider::after { content:''; flex:1; height:1px; background:rgba(255,255,255,0.07); }
.valo-divider-inner { display:flex; align-items:center; gap:6px; padding:0 14px; }
.vd  { width:6px; height:6px; transform:rotate(45deg); }
.vd.r { background:var(--R); box-shadow:0 0 10px var(--R),0 0 20px rgba(255,70,85,0.5); }
.vd.t { background:var(--T); box-shadow:0 0 10px var(--T),0 0 20px rgba(0,212,191,0.5); width:5px; height:5px; }
.vdbar {
    width:60px; height:2px;
    background:linear-gradient(90deg,var(--R) 0%,var(--G) 50%,var(--T) 100%);
    clip-path:polygon(6px 0%,100% 0%,calc(100% - 6px) 100%,0% 100%);
    box-shadow:0 0 12px rgba(0,212,191,0.5), 0 0 6px rgba(255,70,85,0.4);
}

/* ══ GREETING BOX — sharp Valorant panel ══ */
.valo-greeting {
    position:relative;
    background:linear-gradient(140deg, rgba(40,12,18,0.97) 0%, rgba(16,18,32,0.98) 50%, rgba(6,26,28,0.97) 100%);
    margin:4px 0 16px; overflow:hidden;
    /* Sharp diagonal cut bottom-right */
    clip-path:polygon(0 0, 100% 0, 100% calc(100% - 18px), calc(100% - 18px) 100%, 0 100%);
    padding:clamp(18px,5vw,28px) clamp(16px,5vw,28px) clamp(18px,4vw,26px);
    box-shadow:
        0 0 50px rgba(255,70,85,0.14), 0 0 100px rgba(255,70,85,0.06),
        0 8px 40px rgba(0,0,0,0.8),
        inset 0 0 80px rgba(255,70,85,0.03);
    animation:greetGlow 5s ease-in-out infinite;
}
@keyframes greetGlow {
    0%,100% { box-shadow:0 0 50px rgba(255,70,85,0.14),0 0 100px rgba(255,70,85,0.05),0 8px 40px rgba(0,0,0,0.8); }
    50%      { box-shadow:0 0 70px rgba(255,70,85,0.20),0 0 120px rgba(0,212,191,0.07),0 8px 40px rgba(0,0,0,0.8); }
}

/* Red top border line */
.vg-top { position:absolute; top:0; left:0; right:0; height:2px; background:linear-gradient(90deg,var(--R) 0%,rgba(255,70,85,0.4) 60%,transparent 100%); box-shadow:0 0 10px rgba(255,70,85,0.6); }
/* Teal left bar */
.vg-lbar { position:absolute; left:0; top:15%; bottom:15%; width:3px; background:linear-gradient(180deg,transparent,var(--R) 25%,var(--G) 50%,var(--T) 75%,transparent); box-shadow:0 0 12px rgba(255,70,85,0.4); opacity:.85; }
/* Bottom teal glow */
.vg-bot { position:absolute; bottom:0; left:10%; right:20%; height:1px; background:linear-gradient(90deg,transparent,var(--T),rgba(0,212,191,0.3)); box-shadow:0 0 8px rgba(0,212,191,0.4); }
/* Corner brackets */
.vg-cb-tl { position:absolute; top:6px; left:6px; width:16px; height:16px; border-top:2px solid var(--R); border-left:2px solid var(--R); box-shadow:inset 1px 1px 8px rgba(255,70,85,0.15); }
.vg-cb-tr { position:absolute; top:6px; right:6px; width:16px; height:16px; border-top:2px solid rgba(255,70,85,0.5); border-right:2px solid rgba(255,70,85,0.5); }
/* Red radial glow inside */
.vg-glow { position:absolute; top:-30px; right:10%; width:200px; height:200px; background:radial-gradient(circle,rgba(255,70,85,0.08) 0%,transparent 65%); pointer-events:none; }
.vg-glow2 { position:absolute; bottom:-40px; right:-20px; width:220px; height:220px; background:radial-gradient(circle,rgba(0,212,191,0.09) 0%,transparent 65%); pointer-events:none; }

.valo-status-row { display:flex; align-items:center; justify-content:center; gap:7px; margin-bottom:12px; }
.valo-status-dot { width:7px; height:7px; background:var(--T); border-radius:50%; box-shadow:0 0 12px var(--T),0 0 24px rgba(0,212,191,0.4); animation:sdot 2s infinite; }
@keyframes sdot{0%,100%{opacity:1;box-shadow:0 0 12px var(--T),0 0 24px rgba(0,212,191,0.4);}50%{opacity:.4;box-shadow:0 0 3px var(--T);}}
.valo-status-text { font-family:'Barlow Condensed',sans-serif; font-size:10px; font-weight:700; letter-spacing:4px; color:var(--T2); text-transform:uppercase; text-shadow:0 0 12px rgba(0,255,231,0.7); }

.valo-greeting-icon { font-size:clamp(28px,5vw,36px); display:block; text-align:center; margin-bottom:8px; filter:drop-shadow(0 0 18px rgba(255,70,85,0.9)); animation:iglow 2.5s infinite; }
@keyframes iglow{0%,100%{filter:drop-shadow(0 0 18px rgba(255,70,85,0.9));}50%{filter:drop-shadow(0 0 30px rgba(255,150,80,1));}}
.valo-greeting-title { font-family:'Rajdhani',sans-serif; font-size:clamp(15px,4vw,21px); font-weight:700; color:var(--W); text-align:center; text-transform:uppercase; letter-spacing:2px; margin-bottom:8px; }
.valo-greeting-sub { font-size:clamp(12px,3vw,13.5px); color:var(--S); text-align:center; line-height:1.7; }
.valo-stats { display:flex; justify-content:center; gap:clamp(12px,3vw,24px); margin-top:14px; padding-top:12px; border-top:1px solid rgba(255,255,255,0.07); }
.valo-stat { text-align:center; line-height:1.2; }
.valo-stat-n { font-family:'Rajdhani',sans-serif; font-size:clamp(16px,4vw,22px); font-weight:700; color:var(--R); display:block; text-shadow:0 0 16px rgba(255,70,85,0.7); }
.valo-stat-l { font-family:'Barlow Condensed',sans-serif; font-size:9px; letter-spacing:2px; color:#454851; text-transform:uppercase; }
.valo-stat-d { width:1px; background:rgba(255,255,255,0.09); align-self:stretch; }

/* ══ SUGGEST LABEL ══ */
.valo-suggest-label { display:flex; align-items:center; gap:10px; margin:8px 0 12px; }
.valo-suggest-label::before { content:''; flex:1; height:1px; background:linear-gradient(90deg,transparent,rgba(255,70,85,0.6)); box-shadow:0 0 5px rgba(255,70,85,0.3); }
.valo-suggest-label::after  { content:''; flex:1; height:1px; background:linear-gradient(90deg,rgba(0,212,191,0.6),transparent); box-shadow:0 0 5px rgba(0,212,191,0.3); }
.valo-suggest-label span {
    background:linear-gradient(90deg,#b02030,#ff4655);
    color:var(--W); font-family:'Barlow Condensed',sans-serif;
    font-size:12px; font-weight:800; letter-spacing:3px; text-transform:uppercase;
    padding:5px 20px;
    clip-path:polygon(10px 0,100% 0,calc(100% - 10px) 100%,0 100%);
    box-shadow:0 0 24px rgba(255,70,85,0.55),0 0 48px rgba(255,70,85,0.2),0 4px 12px rgba(0,0,0,0.6);
}

/* ══ SUGGESTION BUTTONS — sharp left cut ══ */
.stButton > button {
    background:linear-gradient(90deg,rgba(0,55,50,0.8) 0%,rgba(8,14,24,0.95) 100%) !important;
    color:#d8f8f4 !important;
    border:1px solid rgba(0,212,191,0.25) !important;
    border-left:3px solid var(--T) !important;
    border-radius:0 2px 2px 0 !important;
    font-family:'Barlow Condensed',sans-serif !important;
    font-size:clamp(12px,3vw,14px) !important; font-weight:700 !important; letter-spacing:.5px !important;
    padding:11px 14px 11px 16px !important;
    width:100% !important; text-align:left !important; white-space:normal !important;
    min-height:50px !important; line-height:1.4 !important; transition:all .15s ease !important;
    clip-path:polygon(0 0,100% 0,100% 100%,8px 100%) !important;
    box-shadow:0 0 16px rgba(0,212,191,0.14),0 2px 8px rgba(0,0,0,0.6),inset 0 1px 0 rgba(0,212,191,0.08) !important;
}
.stButton > button:hover {
    background:linear-gradient(90deg,rgba(0,212,191,0.20) 0%,rgba(255,70,85,0.14) 100%) !important;
    border-left-color:var(--R) !important; border-color:rgba(0,212,191,0.45) !important;
    color:var(--W) !important; transform:translateX(5px) !important;
    box-shadow:0 0 28px rgba(0,212,191,0.4),0 0 56px rgba(0,212,191,0.15),0 4px 16px rgba(0,0,0,0.6) !important;
}

/* ══ USER AVATAR ══ */
[data-testid="chatAvatarIcon-user"] {
    background:linear-gradient(135deg,#5c0e1a,#1e040a) !important;
    border:2px solid #ff4655 !important; border-radius:2px !important;
    overflow:hidden !important;
    box-shadow:0 0 16px rgba(255,70,85,0.7),0 0 32px rgba(255,70,85,0.3),inset 0 0 12px rgba(255,70,85,0.12) !important;
}
[data-testid="chatAvatarIcon-user"]>*{display:none !important;}
[data-testid="chatAvatarIcon-user"]::before{
    content:'';display:block;width:100%;height:100%;
    background:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 36 36'%3E%3Crect width='36' height='36' fill='%235c0e1a'/%3E%3Cpolygon points='18,3 31,10.5 31,25.5 18,33 5,25.5 5,10.5' fill='none' stroke='%23ff4655' stroke-width='1.8'/%3E%3Cline x1='5' y1='10.5' x2='13' y2='18' stroke='%23ff4655' stroke-width='1' opacity='0.5'/%3E%3Cline x1='31' y1='25.5' x2='23' y2='18' stroke='%23ff4655' stroke-width='1' opacity='0.5'/%3E%3Crect x='13' y='14' width='10' height='9' rx='1' fill='none' stroke='%23ff7080' stroke-width='1' opacity='0.7'/%3E%3Ccircle cx='18' cy='18.5' r='2' fill='%23ff4655' opacity='0.9'/%3E%3C/svg%3E") center/cover no-repeat !important;
}

/* ══ BOT AVATAR ══ */
[data-testid="chatAvatarIcon-assistant"] {
    background:linear-gradient(135deg,#003c38,#000e0c) !important;
    border:2px solid #00d4bf !important; border-radius:2px !important;
    overflow:hidden !important;
    box-shadow:0 0 16px rgba(0,212,191,0.7),0 0 32px rgba(0,212,191,0.3),inset 0 0 12px rgba(0,212,191,0.12) !important;
}
[data-testid="chatAvatarIcon-assistant"]>*{display:none !important;}
[data-testid="chatAvatarIcon-assistant"]::before{
    content:'';display:block;width:100%;height:100%;
    background:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 36 36'%3E%3Crect width='36' height='36' fill='%23003c38'/%3E%3Cpolygon points='18,3 31,10.5 31,25.5 18,33 5,25.5 5,10.5' fill='none' stroke='%2300d4bf' stroke-width='1.8'/%3E%3Ccircle cx='18' cy='18' r='7' fill='none' stroke='%2300d4bf' stroke-width='1.2' opacity='0.8'/%3E%3Ccircle cx='18' cy='18' r='3' fill='%2300ffe7' opacity='0.9'/%3E%3Ccircle cx='18' cy='18' r='5' fill='none' stroke='%2300d4bf' stroke-width='0.5' opacity='0.4'/%3E%3Cline x1='18' y1='3' x2='18' y2='10' stroke='%2300d4bf' stroke-width='1.2' opacity='0.6'/%3E%3Cline x1='18' y1='26' x2='18' y2='33' stroke='%2300d4bf' stroke-width='1.2' opacity='0.6'/%3E%3Cline x1='5' y1='18' x2='12' y2='18' stroke='%2300d4bf' stroke-width='1' opacity='0.5'/%3E%3Cline x1='24' y1='18' x2='31' y2='18' stroke='%2300d4bf' stroke-width='1' opacity='0.5'/%3E%3C/svg%3E") center/cover no-repeat !important;
}

/* ══ USER BUBBLE — sharp diagonal cut, red panel ══ */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background:linear-gradient(135deg,rgba(100,16,24,0.96) 0%,rgba(60,8,14,0.97) 35%,rgba(16,6,10,0.99) 100%) !important;
    border:1px solid rgba(255,70,85,0.35) !important;
    border-right:4px solid var(--R) !important;
    border-radius:2px !important;
    clip-path:polygon(0 0,calc(100% - 12px) 0,100% 12px,100% 100%,12px 100%,0 calc(100% - 12px)) !important;
    padding:14px 18px !important; margin:8px 0 !important;
    box-shadow:5px 0 25px rgba(255,70,85,0.15),0 4px 24px rgba(0,0,0,0.8),inset -1px 0 30px rgba(255,70,85,0.05) !important;
}

/* ══ BOT BUBBLE — sharp diagonal cut, teal panel ══ */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    background:linear-gradient(135deg,rgba(6,60,56,0.96) 0%,rgba(4,32,32,0.97) 35%,rgba(6,10,18,0.99) 100%) !important;
    border:1px solid rgba(0,212,191,0.30) !important;
    border-left:4px solid var(--T) !important;
    border-radius:2px !important;
    clip-path:polygon(12px 0,100% 0,100% calc(100% - 12px),calc(100% - 12px) 100%,0 100%,0 12px) !important;
    padding:14px 18px !important; margin:8px 0 !important;
    box-shadow:-5px 0 25px rgba(0,212,191,0.13),0 4px 24px rgba(0,0,0,0.8),inset 1px 0 30px rgba(0,212,191,0.04) !important;
}

/* ══ CHAT TEXT ══ */
[data-testid="stChatMessage"] p,[data-testid="stChatMessage"] li {
    font-size:clamp(13.5px,3.8vw,15px) !important; line-height:1.8 !important;
    color:#f5f0e8 !important; text-shadow:0 1px 6px rgba(0,0,0,0.95) !important;
}
[data-testid="stChatMessage"] h3 {
    font-family:'Rajdhani',sans-serif !important; font-size:clamp(14px,4vw,18px) !important;
    font-weight:700 !important; text-transform:uppercase !important; letter-spacing:2px !important;
    color:var(--W) !important; margin-bottom:8px !important; padding-bottom:5px !important;
    border-bottom:1px solid rgba(255,255,255,0.09) !important;
}
[data-testid="stChatMessage"] strong { color:#ffbcc2 !important; font-weight:700 !important; text-shadow:0 0 10px rgba(255,70,85,0.4) !important; }
[data-testid="stChatMessage"] em     { color:var(--T2) !important; font-style:normal !important; font-size:11px !important; text-shadow:0 0 8px rgba(0,255,231,0.5) !important; }
[data-testid="stChatMessage"] code   { background:rgba(0,212,191,0.12) !important; color:#70ffed !important; border:1px solid rgba(0,212,191,0.4) !important; border-radius:2px !important; padding:2px 7px !important; font-size:12px !important; }

/* ══ CHAT INPUT — dark sharp ══ */
.stChatInput>div {
    background:linear-gradient(135deg,rgba(22,18,30,0.98),rgba(12,14,22,0.99)) !important;
    border:1px solid rgba(255,70,85,0.2) !important; border-radius:3px !important;
    clip-path:polygon(0 0,100% 0,100% calc(100% - 8px),calc(100% - 8px) 100%,0 100%) !important;
    box-shadow:0 0 24px rgba(255,70,85,0.08),0 4px 20px rgba(0,0,0,0.7) !important;
}
.stChatInput textarea {
    background:transparent !important; color:var(--C) !important;
    border:none !important; border-bottom:2px solid rgba(255,70,85,0.35) !important;
    border-radius:0 !important; font-family:'Barlow',sans-serif !important;
    font-size:clamp(13px,3.5vw,14px) !important; caret-color:var(--R) !important;
}
.stChatInput textarea:focus { border-bottom-color:var(--R) !important; box-shadow:0 4px 20px rgba(255,70,85,0.12) !important; }
.stChatInput textarea::placeholder { color:#353840 !important; font-style:italic !important; }

/* ══ SIDEBAR ══ */
section[data-testid="stSidebar"] { background:linear-gradient(180deg,#080b10,#0a0d16) !important; border-right:1px solid rgba(255,70,85,0.18) !important; }
section[data-testid="stSidebar"] p,section[data-testid="stSidebar"] span,section[data-testid="stSidebar"] div,section[data-testid="stSidebar"] small { color:#6e6b65 !important; font-size:13px !important; }
section[data-testid="stSidebar"] h2 { font-family:'Rajdhani',sans-serif !important; font-size:17px !important; color:var(--C) !important; text-transform:uppercase !important; letter-spacing:3px !important; }
section[data-testid="stSidebar"] .stButton>button {
    background:transparent !important; border:1px solid rgba(255,70,85,0.2) !important; border-left:2px solid var(--R) !important;
    color:#6e6b65 !important; clip-path:none !important; box-shadow:none !important;
    font-family:'Barlow Condensed',sans-serif !important; font-weight:700 !important; letter-spacing:1px !important;
}
section[data-testid="stSidebar"] .stButton>button:hover { background:rgba(255,70,85,0.07) !important; color:var(--C) !important; transform:none !important; }

[data-testid="stSpinner"] p { color:var(--T) !important; font-family:'Barlow Condensed',sans-serif !important; letter-spacing:4px !important; font-size:11px !important; text-transform:uppercase !important; text-shadow:0 0 12px rgba(0,212,191,0.7) !important; }

::-webkit-scrollbar{width:3px;} ::-webkit-scrollbar-track{background:var(--bg);} ::-webkit-scrollbar-thumb{background:rgba(255,70,85,0.5);border-radius:1px;} ::-webkit-scrollbar-thumb:hover{background:var(--R);}

#MainMenu,footer,header{visibility:hidden !important;}
.block-container{padding-top:1.2rem !important;padding-bottom:1.5rem !important;max-width:760px !important;}

@media(max-width:600px){
    .block-container{padding:.7rem .5rem 4.5rem !important;}
    .valo-author{position:relative !important;top:0 !important;justify-content:center !important;margin-bottom:8px !important;}
    .valo-author::before{display:none;}
    [data-testid="stChatMessage"]{padding:10px 12px !important;margin:4px 0 !important;}
    .stButton>button{min-height:44px !important;padding:9px 11px !important;}
    .valo-greeting{padding:16px 12px !important;}
}
</style>
""", unsafe_allow_html=True)

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
    if st.button("⟳  PHIÊN MỚI", use_container_width=True):
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
    ("⚠  Màn hình xanh BSOD đột ngột",       "Máy tính bị màn hình xanh chết đột ngột, phải làm gì?"),
    ("▪  Màn hình đen không có tín hiệu",      "Máy lên nguồn nhưng màn hình đen, không có tín hiệu"),
    ("◈  PC bíp dài khi khởi động",            "Máy bíp dài liên tục khi bật, không vào được Windows"),
    ("◉  Windows boot loop liên tục",          "Máy cứ khởi động lại liên tục không vào được Windows"),
    ("✕  Lỗi 0xc0000005 văng game",            "Game bị lỗi 0xc0000005 không mở được cách fix?"),
    ("⚠  PC tự reboot khi chơi game nặng",     "PC tự reboot đột ngột trong lúc chơi game nặng"),
    ("◈  SSD NVMe không nhận trong BIOS",      "BIOS không nhận ổ SSD NVMe sau khi lắp vào mainboard"),
    ("🌡  CPU 95°C — overheat nghiêm trọng",   "CPU nhiệt độ lên đến 95 độ C khi chạy game nguy hiểm không?"),
    ("◆  RAM 8GB có đủ cho game 2024?",         "RAM 8GB có đủ dùng để chơi game hiện đại năm 2024 không?"),
    ("⚡  Nguồn bao nhiêu W cho RTX 3060?",     "RTX 3060 cần nguồn bao nhiêu W dùng nguồn 500W được không?"),
    ("◆  i5-12400F chơi game 2024 đủ không?",  "i5-12400F hiệu năng thế nào chơi game 2024 có đủ không?"),
    ("▶  i5 vs Ryzen 5 tầm 3-4 triệu",         "Tầm giá 3-4 triệu nên chọn Intel i5 hay AMD Ryzen 5?"),
    ("🎮  GTX 1650 chơi game gì mượt ở FHD?",  "GTX 1650 chơi mượt những game nào ở độ phân giải 1080p?"),
    ("▶  RTX 3060 vs RX 6600 nên mua cái nào?","So sánh RTX 3060 và RX 6600 nên chọn card nào?"),
    ("◆  H610 hay B660 nên chọn mainboard nào?","Mainboard H610 và B660 khác nhau thế nào nên mua loại nào?"),
    ("📱  Snapdragon 888 nóng máy bình thường?","Chip Snapdragon 888 bị nóng máy nhiều có phải lỗi không?"),
    ("📱  Dimensity 9200 vs Snapdragon 8 Gen2", "So sánh Dimensity 9200 với Snapdragon 8 Gen 2 loại nào mạnh?"),
    ("⚡  Build PC 10 triệu chơi game FHD",      "Gợi ý cấu hình PC build 10 triệu đồng chơi game Full HD mượt"),
    ("◆  Combo i5-12400F + RTX 3060 tốt không?","Combo i5-12400F với RTX 3060 12GB chơi game có bottleneck không?"),
    ("◉  RAM 2x8GB vs 1x16GB cái nào nhanh?",  "Lắp 2 thanh RAM 8GB hay 1 thanh 16GB thì nhanh hơn?"),
    ("▶  SSD NVMe vs SSD SATA khác gì?",        "SSD NVMe và SSD SATA khác nhau ở điểm gì nên mua loại nào?"),
    ("◈  i3-12100F + RTX 3060 có bottleneck?",  "i3-12100F dùng với RTX 3060 có bị cổ chai hiệu năng không?"),
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
        if mp=="loi": return f"### ✕  {bm['ten']}\n*— Lê Văn Chung 10A4*\n\n**⚠ Nguyên nhân:** {bm['nguyen_nhan']}\n\n**◈ Khắc phục:**\n{bm['giai_phap']}"
        else: return f"### ◆  {bm['ten']}\n*— Lê Văn Chung 10A4*\n\n**⚙ Thông số:** {bm.get('thong_so','')}\n\n**◉ Socket:** `{bm.get('socket','')}`\n\n**▶ Tư vấn:** {bm.get('chuyen_gia_tu_van','')}"
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
