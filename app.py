st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Barlow:wght@300;400;500;600&display=swap');

/* =========================
   VALORANT THEME V2
========================= */

:root{
    --red:#ff4655;
    --red-soft:#ff5f6d;
    --bg:#0b0e13;
    --bg2:#11141b;
    --panel:#171c25;
    --panel2:#1c2230;
    --text:#f3f4f6;
    --muted:#b6bcc8;
    --line:#ffffff12;
}

/* =========================
   BASE
========================= */

html, body, .stApp{
    background:
        radial-gradient(circle at top right, rgba(255,70,85,0.08), transparent 25%),
        linear-gradient(180deg,#0a0c11 0%, #0f131a 100%);
    color:var(--text);
    font-family:'Barlow',sans-serif;
}

/* giảm texture để chữ nổi hơn */
.stApp::before{
    content:"";
    position:fixed;
    inset:0;
    background:
    repeating-linear-gradient(
        -55deg,
        transparent,
        transparent 55px,
        rgba(255,70,85,0.015) 56px
    );
    pointer-events:none;
    z-index:0;
}

/* =========================
   HEADER
========================= */

.valo-header{
    text-align:center;
    padding-top:10px;
    margin-bottom:10px;
}

.valo-eyebrow{
    color:var(--red);
    letter-spacing:4px;
    font-size:11px;
    font-weight:600;
    margin-bottom:8px;
    text-transform:uppercase;
}

.valo-title{
    font-family:'Rajdhani',sans-serif;
    font-size:62px;
    line-height:0.95;
    font-weight:700;
    color:white;
    letter-spacing:-1px;

    text-shadow:
    0 0 18px rgba(255,70,85,0.15);
}

.valo-title span{
    color:var(--red);
}

.valo-subtitle{
    margin-top:10px;

    color:#d4dae3;

    letter-spacing:3px;
    text-transform:uppercase;

    font-size:12px;
    font-weight:500;
}

/* =========================
   DIVIDER
========================= */

.valo-divider{
    width:100%;
    height:1px;
    background:linear-gradient(
    90deg,
    transparent,
    rgba(255,70,85,0.6),
    transparent
    );

    margin:18px 0 22px 0;
}

/* =========================
   GREETING
========================= */

.valo-greeting{
    background:linear-gradient(
    145deg,
    rgba(23,28,37,0.95),
    rgba(18,22,30,0.98)
    );

    border:1px solid rgba(255,70,85,0.15);

    border-left:4px solid var(--red);

    border-radius:14px;

    padding:28px;

    box-shadow:
    0 0 25px rgba(255,70,85,0.06);

    margin-bottom:14px;
}

.valo-agent-icon{
    font-size:42px;
    display:block;
    text-align:center;
    margin-bottom:10px;
}

.valo-greeting-title{
    text-align:center;
    font-family:'Rajdhani',sans-serif;
    font-size:25px;
    font-weight:700;
    color:white;
    margin-bottom:8px;
}

.valo-greeting-sub{
    text-align:center;
    color:#c5ccd8;
    line-height:1.8;
    font-size:14px;
}

/* =========================
   BUTTONS
========================= */

.stButton > button{

    background:linear-gradient(
    145deg,
    #1b2230,
    #151a23
    ) !important;

    color:#dce1ea !important;

    border:1px solid rgba(255,255,255,0.05) !important;

    border-left:3px solid transparent !important;

    border-radius:10px !important;

    padding:14px !important;

    transition:0.18s ease !important;

    font-weight:500 !important;

    min-height:58px !important;
}

.stButton > button:hover{

    border-left:3px solid var(--red) !important;

    transform:translateY(-2px);

    background:linear-gradient(
    145deg,
    #232c3d,
    #1a1f2b
    ) !important;

    box-shadow:
    0 0 18px rgba(255,70,85,0.12);

    color:white !important;
}

/* =========================
   CHAT
========================= */

/* USER */

[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]){

    background:
    linear-gradient(
    145deg,
    rgba(255,70,85,0.08),
    rgba(255,70,85,0.03)
    );

    border:1px solid rgba(255,70,85,0.15);

    border-right:3px solid var(--red);

    border-radius:14px;

    padding:16px;

    margin:10px 0;
}

/* ASSISTANT */

[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-assistant"]){

    background:
    linear-gradient(
    145deg,
    rgba(25,31,42,0.96),
    rgba(18,22,30,0.98)
    );

    border:1px solid rgba(255,255,255,0.06);

    border-left:3px solid var(--red);

    border-radius:14px;

    padding:16px;

    margin:10px 0;

    box-shadow:
    0 0 20px rgba(255,70,85,0.04);
}

/* TEXT */

[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li{

    color:#eef2f7 !important;

    line-height:1.85 !important;

    font-size:15px !important;
}

[data-testid="stChatMessage"] strong{
    color:#ff7b87 !important;
}

[data-testid="stChatMessage"] code{
    background:rgba(255,70,85,0.12);
    color:#ff8d97;
    padding:2px 6px;
    border-radius:6px;
}

/* =========================
   INPUT
========================= */

.stChatInput textarea{

    background:#151b24 !important;

    color:white !important;

    border:1px solid rgba(255,255,255,0.08) !important;

    border-radius:12px !important;

    padding:12px !important;

    font-size:15px !important;
}

.stChatInput textarea:focus{

    border-color:rgba(255,70,85,0.5) !important;

    box-shadow:
    0 0 18px rgba(255,70,85,0.15) !important;
}

/* =========================
   SIDEBAR
========================= */

section[data-testid="stSidebar"]{
    background:#0a0d12 !important;
    border-right:1px solid rgba(255,70,85,0.1);
}

section[data-testid="stSidebar"] *{
    color:#d0d6e0 !important;
}

/* =========================
   SCROLLBAR
========================= */

::-webkit-scrollbar{
    width:8px;
}

::-webkit-scrollbar-thumb{
    background:rgba(255,70,85,0.35);
    border-radius:10px;
}

/* =========================
   HIDE STREAMLIT
========================= */

#MainMenu,
footer,
header{
    visibility:hidden;
}

.block-container{
    max-width:850px !important;
    padding-top:1rem !important;
}

/* =========================
   MOBILE
========================= */

@media(max-width:768px){

    .valo-title{
        font-size:42px;
    }

    .valo-greeting{
        padding:20px;
    }

    [data-testid="stChatMessage"]{
        padding:14px !important;
    }
}

</style>
""", unsafe_allow_html=True)
