import streamlit as st

# 1. ڕێکخستنی سەرەتایی
st.set_page_config(page_title="CaloRun Clone", layout="centered")

# 2. دروستکردنی میمۆری (Database) بۆ ئەپەکە
if 'page' not in st.session_state:
    st.session_state.page = "Home"
if 'coins' not in st.session_state:
    st.session_state.coins = 1908
if 'steps' not in st.session_state:
    st.session_state.steps = 306

# 3. دیزاینی CSS بۆ ئەوەی ڕێک وەک ئەپەکە بێت
st.markdown("""
    <style>
    header {visibility: hidden;}
    .main { background: linear-gradient(180deg, #e6ff80 0%, #ffffff 100%); }
    
    /* بازنەی ناوەڕاست */
    .circle-container {
        border: 8px solid white;
        border-radius: 50%;
        width: 220px;
        height: 220px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        margin: auto;
        background-color: transparent;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* دوگمەی ڕەشی Convert */
    .black-button {
        background-color: #111;
        color: white;
        border-radius: 30px;
        padding: 15px;
        text-align: center;
        font-weight: bold;
        margin: 20px 0;
    }
    
    /* مێنیوی خوارەوە (Bottom Nav) */
    .nav-bar {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #111;
        display: flex;
        justify-content: space-around;
        padding: 15px 0;
        z-index: 1000;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. دروستکردنی لاپەڕەکان

# --- لاپەڕەی سەرەکی (Home) ---
if st.session_state.page == "Home":
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown(f"💰 **{st.session_state.coins}** ≈ ${st.session_state.coins/1000:.2f}")
    with col2:
        st.markdown("<p style='text-align:right;'>👤 ❓</p>", unsafe_allow_html=True)
    
    st.markdown("<br><center><img src='https://cdn-icons-png.flaticon.com/512/6212/6212627.png' width='100'></center>", unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="circle-container">
            <h1 style="font-size: 60px; margin:0;">{st.session_state.steps}</h1>
            <p style="color: gray;">Limit: 10000</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Convert to CaloCoin", use_container_width=True):
        st.session_state.coins += 30
        st.toast("🎉 30 Coins Added!")

# --- لاپەڕەی ئەرکەکان (Tasks) ---
elif st.session_state.page == "Tasks":
    st.title("Task Center")
    st.write("🎁 **Daily Tasks**")
    st.info("Check-in: +120 Coins")
    st.info("Lucky Spin: +1000 Coins")
    st.info("Play Lucky Slot: +1000 Coins")

# --- لاپەڕەی واڵێت (Wallet) ---
elif st.session_state.page == "Wallet":
    st.title("My Wallet")
    st.metric("Total Balance", f"${st.session_state.coins/1000:.2f}", f"{st.session_state.coins} Coins")
    st.markdown("---")
    st.write("Withdrawal Methods:")
    st.write("🅿️ PayPal | 🅰️ Amazon | 💳 Mastercard")

# --- لاپەڕەی کۆکراوەکان (Collection) ---
elif st.session_state.page == "Collection":
    st.title("My Collection")
    col1, col2 = st.columns(2)
    col1.warning("🔒 Fruit (0/9)")
    col2.warning("🔒 BuBu (0/9)")

# 5. مێنیوی خوارەوە (ئەمە وا دەکات وەک ئەپ لاپەڕەکان بگۆڕێت)
st.write("<br><br><br>", unsafe_allow_html=True) # بۆشایی بۆ ئەوەی مێنیوەکە شت نەشارێتەوە
cols = st.columns(4)
if cols[0].button("🏠"): st.session_state.page = "Home"; st.rerun()
if cols[1].button("📋"): st.session_state.page = "Tasks"; st.rerun()
if cols[2].button("💼"): st.session_state.page = "Wallet"; st.rerun()
if cols[3].button("⭐"): st.session_state.page = "Collection"; st.rerun()
