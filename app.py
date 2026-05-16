```python
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@600;700&family=Barlow+Condensed:wght@400;600;700&family=Barlow:wght@300;400;500&display=swap');

/* ==============================
   VALORANT CORE PALETTE
============================== */
:root {
    --red:     #ff4655;
    --red-dim: #c0303d;
    --red-glow:#ff465540;
    --dark:    #0b0f15;
    --dark2:   #121720;
    --dark3:   #181d27;
    --panel:   #0d1117cc;
    --border:  #ff465520;
    --border2: #ffffff10;
    --text:    #f3f6fb;
    --muted:   #9ba3af;
    --accent:  #ffffff;
}

/* ==============================
   BASE
============================== */
html, body, .stApp {
    background:
    radial-gradient(circle at top right,
    rgba(255,70,85,0.10),
    transparent 30%),

    linear-gradient(
    180deg,
    #0a0d12 0%,
    #10141c 100%
    ) !important;

    color: var(--text) !important;
    font-family: 'Barlow', sans-serif !important;
}

/* Texture background nhẹ hơn */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;

    background:
        repeating-linear-gradient(
            -55deg,
            transparent,
            transparent 65px,
            rgba(255,70,85,0.008) 66px
        );

    pointer-events: none;
    z-index: 0;
}

/* Top glow */
.stApp::after {
    content: '';
    position: fixed;
    top: 0;
    left: 0;

    width: 100%;
    height: 2px;

    background:
    linear-gradient(
    90deg,
    transparent,
    var(--red),
    transparent
    );

    box-shadow:
    0 0 20px rgba(255,70,85,0.4);

    z-index: 999;
}

/* ==============================
   HEADER
============================== */
.valo-header {
    position: relative;
    text-align: center;
    padding: 10px 0 4px;
    margin-bottom: 4px;
}

.valo-eyebrow {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: clamp(10px, 2vw, 12px);
    font-weight: 700;
    letter-spacing: 5px;
    color: var(--red);
    text-transform: uppercase;
    margin-bottom: 8px;

    display:flex;
    align-items:center;
    justify-content:center;
    gap:10px;
}

.valo-eyebrow::before,
.valo-eyebrow::after {
    content:'';
    width:28px;
    height:1px;
    background:var(--red);
    opacity:0.7;
}

.valo-title {

    font-family: 'Rajdhani', sans-serif;

    font-size: clamp(34px, 7vw, 64px);

    font-weight: 700;

    letter-spacing: -1px;

    line-height: 1;

    color: var(--accent);

    text-transform: uppercase;

    margin: 0;

    text-shadow:
    0 0 20px rgba(255,70,85,0.10);
}

.valo-title span {
    color: var(--red);
}

.valo-subtitle {

    font-family: 'Barlow Condensed', sans-serif;

    font-size: clamp(11px, 2.5vw, 13px);

    font-weight: 600;

    letter-spacing: 4px;

    color: #d9dee7;

    text-transform: uppercase;

    margin-top: 8px;

    text-shadow:
    0 0 10px rgba(255,255,255,0.05),
    0 0 16px rgba(255,70,85,0.08);
}

/* Divider */
.valo-divider {
    display: flex;
    align-items: center;
    gap: 0;
    margin: 14px 0 12px;
    height: 2px;
}

.valo-divider::before,
.valo-divider::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border2);
}

.valo-divider-bar {
    width: 70px;
    height: 2px;

    background: var(--red);

    box-shadow:
    0 0 14px rgba(255,70,85,0.4);

    clip-path:
    polygon(4px 0%, 100% 0%, calc(100% - 4px) 100%, 0% 100%);
}

/* ==============================
   GREETING BOX
============================== */
.valo-greeting {

    position: relative;

    background:
    linear-gradient(
    145deg,
    rgba(26,31,41,0.96),
    rgba(16,20,28,0.98)
    );

    border: 1px solid rgba(255,255,255,0.05);

    border-left: 3px solid var(--red);

    border-radius: 14px;

    padding: clamp(18px, 4vw, 26px);

    margin: 8px 0 4px;

    overflow: hidden;

    box-shadow:
    0 0 24px rgba(255,70,85,0.06);
}

.valo-greeting::before {
    content: '';
    position: absolute;
    top: 0;
    right: 0;

    width:120px;
    height:120px;

    background:
    linear-gradient(
    135deg,
    rgba(255,70,85,0.18),
    transparent
    );

    clip-path:
    polygon(100% 0,0 0,100% 100%);
}

.valo-agent-icon {
    font-size: clamp(30px, 6vw, 40px);
    margin-bottom: 10px;
    display: block;
    text-align: center;
}

.valo-greeting-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: clamp(18px, 4vw, 24px);
    font-weight: 700;
    color: white;
    text-align: center;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 8px;
}

.valo-greeting-sub {
    font-size: clamp(13px, 3vw, 14px);
    color: #d2d8e2;
    text-align: center;
    line-height: 1.8;
}

/* ==============================
   SUGGEST LABEL
============================== */
.valo-suggest-label {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 16px 0 10px;
}

.valo-suggest-label::before,
.valo-suggest-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border2);
}

.valo-suggest-label span {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 10px;
    letter-spacing: 4px;
    color: #6f7885;
    text-transform: uppercase;
}

/* ==============================
   BUTTONS
============================== */
.stButton > button {

    background:
    linear-gradient(
    145deg,
    #1b2230,
    #141a24
    ) !important;

    color: #eef2f8 !important;

    border: 1px solid rgba(255,255,255,0.05) !important;

    border-left: 2px solid transparent !important;

    border-radius: 12px !important;

    font-family: 'Barlow Condensed', sans-serif !important;

    font-size: clamp(12px, 3vw, 14px) !important;

    font-weight: 600 !important;

    letter-spacing: 0.5px !important;

    padding: 12px 15px !important;

    width: 100% !important;

    text-align: left !important;

    white-space: normal !important;

    min-height: 52px !important;

    line-height: 1.5 !important;

    transition: all 0.18s ease !important;
}

.stButton > button:hover {

    background:
    linear-gradient(
    145deg,
    #232d3f,
    #1a2230
    ) !important;

    border-left-color: var(--red) !important;

    transform: translateY(-2px) !important;

    box-shadow:
    0 0 18px rgba(255,70,85,0.12);

    color: white !important;
}

/* ==============================
   CHAT USER
============================== */
[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) {

    background:
    linear-gradient(
    145deg,
    rgba(255,70,85,0.08),
    rgba(255,70,85,0.03)
    );

    border: 1px solid rgba(255,70,85,0.12);

    border-right: 3px solid var(--red);

    border-radius: 14px;

    padding: 16px;

    margin: 8px 0;
}

/* ==============================
   CHAT BOT
============================== */
[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-assistant"]) {

    background:
    linear-gradient(
    145deg,
    rgba(28,32,42,0.96),
    rgba(18,22,30,0.98)
    );

    border: 1px solid rgba(255,255,255,0.05);

    border-left: 3px solid var(--red);

    border-radius: 14px;

    padding: 16px;

    margin: 8px 0;

    box-shadow:
    0 0 18px rgba(255,70,85,0.05);
}

/* CHAT TEXT */
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li {

    font-size: clamp(14px, 3.5vw, 15px) !important;

    line-height: 1.9 !important;

    color: #f1f4f9 !important;

    font-weight: 400;

    text-shadow:
    0 0 8px rgba(255,255,255,0.02);
}

[data-testid="stChatMessage"] h3 {

    font-family: 'Rajdhani', sans-serif !important;

    font-size: clamp(15px, 4vw, 18px) !important;

    font-weight: 700 !important;

    text-transform: uppercase !important;

    letter-spacing: 1px !important;

    color: white !important;

    margin-bottom: 8px !important;
}

[data-testid="stChatMessage"] strong {
    color: #ff8590 !important;
}

[data-testid="stChatMessage"] code {

    background:
    rgba(255,70,85,0.10) !important;

    color: #ff9ca5 !important;

    border-radius: 6px !important;

    padding: 2px 6px !important;

    font-size: 12px !important;
}

/* ==============================
   CHAT INPUT
============================== */
.stChatInput textarea {

    background:
    rgba(24,29,39,0.98) !important;

    color: white !important;

    border: 1px solid rgba(255,255,255,0.08) !important;

    border-radius: 14px !important;

    font-family: 'Barlow', sans-serif !important;

    font-size: 15px !important;

    caret-color: var(--red) !important;
}

.stChatInput textarea:focus {

    border-color: rgba(255,70,85,0.4) !important;

    box-shadow:
    0 0 20px rgba(255,70,85,0.12) !important;
}

.stChatInput textarea::placeholder {
    color: #68707d !important;
}

/* ==============================
   SIDEBAR
============================== */
section[data-testid="stSidebar"] {

    background:
    linear-gradient(
    180deg,
    #0a0d12,
    #0d1117
    ) !important;

    border-right:
    1px solid rgba(255,70,85,0.08) !important;
}

section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] div,
section[data-testid="stSidebar"] small {

    color: #b8c0cb !important;

    font-size: 13px !important;

    font-family: 'Barlow', sans-serif !important;
}

section[data-testid="stSidebar"] h2 {

    font-family: 'Rajdhani', sans-serif !important;

    color: white !important;

    text-transform: uppercase !important;

    letter-spacing: 2px !important;
}

/* Sidebar button */
section[data-testid="stSidebar"] .stButton > button {

    background: transparent !important;

    border: 1px solid rgba(255,70,85,0.15) !important;

    border-left: 2px solid var(--red) !important;

    color: #c8d0db !important;
}

section[data-testid="stSidebar"] .stButton > button:hover {

    background:
    rgba(255,70,85,0.08) !important;

    color: white !important;
}

/* ==============================
   SPINNER
============================== */
[data-testid="stSpinner"] p {

    color: #d7dde6 !important;

    font-family: 'Barlow Condensed', sans-serif !important;

    letter-spacing: 2px !important;

    font-size: 12px !important;
}

/* ==============================
   HIDE STREAMLIT UI
============================== */
#MainMenu,
footer,
header {
    visibility: hidden !important;
}

.block-container {
    padding-top: 1.2rem !important;
    padding-bottom: 1.5rem !important;
    max-width: 820px !important;
}

/* ==============================
   MOBILE
============================== */
@media (max-width: 600px) {

    .block-container {
        padding: 0.8rem 0.5rem 4.5rem !important;
    }

    .valo-title {
        font-size: 44px;
    }

    [data-testid="stChatMessage"] {
        padding: 12px !important;
    }

    .stButton > button {
        min-height: 46px !important;
    }

    .valo-greeting {
        padding: 18px;
    }
}
</style>
""", unsafe_allow_html=True)
```
