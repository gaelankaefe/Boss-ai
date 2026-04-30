import streamlit as st

# 1. ڕێکخستنی بنەڕەتی
st.set_page_config(page_title="Boss Invest Pro", layout="centered")

# 2. دروستکردنی میمۆری
if 'page' not in st.session_state:
    st.session_state.page = "🏠 Home"
if 'balance' not in st.session_state:
    st.session_state.balance = 1908.50

# 3. CSS بۆ دیزاینێکی زۆر پڕۆفیشناڵ (Premium Look)
st.markdown("""
    <style>
    /* لابردنی هەموو شتە زیادەکانی ستریملیت */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stApp { background-color: #050505; color: white; }
    
    /* کارتی باڵانس وەک شووشە (Glassmorphism) */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 25px;
        text-align: center;
        margin-bottom: 20px;
    }
    
    /* بازنەی نێوان شاشەکە (Progress Circle) */
    .main-circle {
        width: 200px;
        height: 200px;
        border-radius: 50%;
        background: radial-gradient(circle, #050505 60%, #ccff00 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        margin: auto;
        border: 4px solid #1a1a1a;
        box-shadow: 0 0 30px rgba(204, 255, 0, 0.2);
    }
    
    /* دوگمە ڕەشەکان */
    div.stButton > button {
        background-color: #ccff00;
        color: black;
        border: none;
        border-radius: 16px;
        padding: 15px;
        font-size: 18px;
        font-weight: 800;
        width: 100%;
        transition: 0.4s;
    }
    div.stButton > button:hover {
        background-color: #e6ff80;
        transform: translateY(-3px);
        box-shadow: 0 10px 20px rgba(204, 255, 0, 0.3);
    }

    /* مێنیوی خوارەوە */
    .nav-container {
        position: fixed;
        bottom: 20px;
        left: 5%;
        right: 5%;
        background: rgba(20, 20, 20, 0.9);
        border-radius: 30px;
        padding: 10px;
        display: flex;
        justify-content: space-around;
        border: 1px solid rgba(255,255,255,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# 4. دیزاینی لاپەڕەکان

# لاپەڕەی سەرەکی
if st.session_state.page == "🏠 Home":
    # بەشی سەرەوە (Header)
    st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div style="background: rgba(204, 255, 0, 0.1); padding: 8px 15px; border-radius: 20px; color: #ccff00;">
                🪙 {st.session_state.balance:,.0f}
            </div>
            <div style="font-size: 24px;">👤</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("#")
    
    # ئاڤاتار و بازنە
    st.markdown("<center><img src='https://cdn-icons-png.flaticon.com/512/6212/6212627.png' width='120'></center>", unsafe_allow_html=True)
    st.markdown(f"""
        <div class="main-circle">
            <h1 style="font-size: 55px; color: white; margin:0;">306</h1>
        </div>
        <p style="text-align:center; color: #888; margin-top:10px;">Limit: 10000</p>
    """, unsafe_allow_html=True)

    # دوگمەی گۆڕین
    if st.button("Convert to Profit"):
        st.balloons()
        st.session_state.balance += 30
        st.rerun()

# لاپەڕەی واڵێت (Wallet)
elif st.session_state.page == "💼 Wallet":
    st.markdown("<h2 style='text-align:center;'>My Wallet</h2>", unsafe_allow_html=True)
    st.markdown(f"""
        <div class="glass-card">
            <p style="color: #888; margin:0;">Total Balance</p>
            <h1 style="color: #ccff00; font-size: 45px;">${st.session_state.balance/1000:.2f}</h1>
            <p style="color: white;">≈ {st.session_state.balance:,.0f} Coins</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("### Withdraw")
    st.markdown("""
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
            <div style="background:#1a1a1a; padding:20px; border-radius:15px; text-align:center; border: 1px solid #333;">$30</div>
            <div style="background:#1a1a1a; padding:20px; border-radius:15px; text-align:center; border: 1px solid #333;">$50</div>
        </div>
    """, unsafe_allow_html=True)

# 5. مێنیوی پڕۆفیشناڵی خوارەوە (Navigation)
st.write("<br><br><br><br>", unsafe_allow_html=True)
nav_cols = st.columns(4)
with nav_cols[0]:
    if st.button("🏠"): st.session_state.page = "🏠 Home"; st.rerun()
with nav_cols[1]:
    if st.button("📋"): st.session_state.page = "📋 Tasks"; st.rerun()
with nav_cols[2]:
    if st.button("💼"): st.session_state.page = "💼 Wallet"; st.rerun()
with nav_cols[3]:
    if st.button("⭐"): st.session_state.page = "⭐ Rank"; st.rerun()
