import streamlit as st
import pandas as pd

# ١. ڕێکخستنی سەرەتایی (App Mode)
st.set_page_config(page_title="Boss Invest App", page_icon="⚡", layout="centered")

# ٢. بەکارهێنانی CSS بۆ دیزاینی "Neon App"
st.markdown("""
    <style>
    /* لابردنی ناونیشانی زیادی سەرەوە */
    header {visibility: hidden;}
    .main { background-color: #000000; }
    
    /* سندوقی باڵانس (وەک بازنەکەی ناو وێنەکە) */
    .balance-container {
        background: linear-gradient(145deg, #1a1a1a, #000000);
        border: 3px solid #ccff00;
        border-radius: 50%;
        width: 200px;
        height: 200px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        margin: 0 auto;
        box-shadow: 0 0 20px rgba(204, 255, 0, 0.4);
    }
    
    /* دوگمەی Convert (وەک ناو وێنەکە) */
    div.stButton > button {
        background-color: #ccff00;
        color: black;
        border-radius: 30px;
        border: none;
        font-size: 20px;
        font-weight: bold;
        height: 3.5em;
        width: 100%;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #e6ff80;
        transform: scale(1.02);
    }

    /* کارتەکانی خوارەوە */
    .feature-card {
        background-color: #1a1a1a;
        padding: 15px;
        border-radius: 15px;
        text-align: center;
        border-left: 5px solid #ccff00;
    }
    </style>
    """, unsafe_allow_html=True)

# ٣. ناوەڕۆکی ئەپەکە
if 'balance' not in st.session_state:
    st.session_state.balance = 100.0

# وێنەی سەرەکی (Avatar) - لێرە دەتوانیت لینکی GIF دابنێیت
st.markdown("<center><img src='https://cdn-icons-png.flaticon.com/512/6212/6212627.png' width='80'></center>", unsafe_allow_html=True)

# نیشاندانی باڵانس لە ناو بازنە
st.markdown(f"""
    <div class="balance-container">
        <h1 style='color: white; margin: 0; font-size: 45px;'>{st.session_state.balance}</h1>
        <p style='color: #ccff00; margin: 0;'>Limit: 10000</p>
    </div>
    """, unsafe_allow_html=True)

st.write("##")

# دوگمەی سەرەکی
if st.button("🚀 Convert to USDT"):
    st.balloons()
    st.session_state.balance += 5.0
    st.rerun()

st.write("---")

# بەشی کارتەکانی خوارەوە (وەک Claim)
col1, col2 = st.columns(2)
with col1:
    st.markdown("<div class='feature-card'><h3 style='color:white;'>🏆</h3><p style='color:gray;'>Rank</p></div>", unsafe_allow_html=True)
with col2:
    st.markdown("<div class='feature-card'><h3 style='color:white;'>🎁</h3><p style='color:gray;'>Bonus</p></div>", unsafe_allow_html=True)

# لای چەپ بۆ واڵێت
with st.sidebar:
    st.title("💳 Wallet Settings")
    st.write("Your USDT Address:")
    st.code("TMR7DR8EtB3aNp2inXt8zfTVsXbHm9dv8M")
    st.info("بۆ بارگاویکردن، وەسڵ بنێرە بۆ تێلیگرام.")
    st.link_button("Telegram Support", "https://t.me/YOUR_USERNAME")
