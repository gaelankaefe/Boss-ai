import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# ١. پەیوەندی لەگەڵ گوگڵ شیت
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(ttl=5)
    user_row = df[df['Username'] == 'Test_user'].iloc[0]
    balance = float(user_row['Wallet_balance'])
except Exception as e:
    st.error("⚠️ کێشە لە پەیوەندی گوگڵ شیت هەیە. دڵنیابە کە شیتەکەت Public کراوە.")
    st.stop()

# ٢. دیزاینی لای چەپ (Sidebar)
st.sidebar.title("💰 هەژماری من")
st.sidebar.metric("باڵانسی ئێستا", f"${balance:,.2f}")

st.sidebar.markdown("---")

# بەشی بارگاویکردن (هەموو ڕێگاکان)
with st.sidebar.expander("💳 بارگاویکردنی واڵێت"):
    st.write("**USDT (TRC20):**")
    st.code("TMR7DR8EtB3aNp2inXt8zfTVsXbHm9dv8M")
    
    st.write("**ناونیشانی تێلیگرام:**")
    # ناوی بەکارهێنەری خۆت لێرە دابنێ
    telegram_url = "https://t.me/YOUR_USERNAME" 
    st.link_button("🚀 ناردنی وەسڵ", telegram_url)

# ٣. بەشی سەرەکی سایت
st.title("📈 سەکۆی وەبەرهێنانی فۆرێکس")
st.write(f"بەخێربێیت **Test_user**")

amount = st.number_input("بڕی وەبەرهێنان ($)", min_value=1.0)

if st.button("✅ ئێستا بکڕە"):
    if balance >= amount:
        new_balance = balance + (amount * 0.05)
        # نوێکردنەوەی داتا لەناو سایت و ناردنی بۆ گوگڵ شیت
        df.loc[df['Username'] == 'Test_user', 'Wallet_balance'] = new_balance
        conn.update(data=df)
        
        st.balloons()
        st.success(f"سەرکەوتوو بوو! باڵانسی نوێ: ${new_balance:,.2f}")
    else:
        st.error("⚠️ باڵانسەکەت بەش ناکات")
