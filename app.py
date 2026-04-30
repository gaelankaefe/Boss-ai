import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# پەیوەندی لەگەڵ گوگڵ شیت
conn = st.connection("gsheets", type=GSheetsConnection)

# خوێندنەوەی داتاکان لە شیتەکە
df_users = conn.read(worksheet="Sheet1", ttl=0)
user_row = df_users[df_users['Username'] == 'Test_user'].iloc[0]
balance = float(user_row['Wallet_balance'])

# دیزاینی لای چەپ (Sidebar)
st.sidebar.title("💰 هەژماری من")
st.sidebar.metric("باڵانسی ئێستا", f"${balance:,.2f}")

st.sidebar.markdown("---")

# بەشی بارگاویکردن بە USDT
with st.sidebar.expander("💎 بارگاویکردن بە USDT"):
    st.warning("⚠️ تەنها تۆڕی (TRC20) بەکاربهێنە")
    
    st.write("**ناونیشانی واڵێتی من:**")
    # ناونیشانی واڵێتەکەی تۆ لێرە جێگیر کراوە
    st.code("TMR7DR8EtB3aNp2inXt8zfTVsXbHm9dv8M") 
    
    st.info("دوای ناردنی پارەکە، وێنەی وەسڵەکە (Screenshot) بنێرە بۆ تێلیگرامەکەمان بۆ ئەوەی باڵانسەکەت بۆ زیاد بکەین.")
    
    # لێرە لە جیاتی YOUR_USERNAME ناوی یوزەری تێلیگرامی خۆت بنووسە
    telegram_url = "https://t.me/YOUR_USERNAME" 
    st.link_button("🚀 ناردنی وەسڵ بۆ تێلیگرام", telegram_url)

# بەشی سەرەکی سایت
st.title("📈 سەکۆی وەبەرهێنانی فۆرێکس")
st.write(f"بەخێربێیت **Test_user**")

trade_amount = st.number_input("بڕی وەبەرهێنان ($)", min_value=1.0, max_value=balance)

if st.button("ئێستا بکڕە و قازانج وەرگرە"):
    if balance >= trade_amount:
        st.balloons()
        st.success(f"داواکارییەکەت بۆ وەبەرهێنانی ${trade_amount} بە سەرکەوتوویی تۆمارکرا.")
    else:
        st.error("باڵانسەکەت بەش ناکات. تکایە واڵێتەکەت بارگاوی بکەرەوە.")
