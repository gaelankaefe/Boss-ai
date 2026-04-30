import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# پەیوەندی لەگەڵ گوگڵ شیت
conn = st.connection("gsheets", type=GSheetsConnection)

# خوێندنەوەی باڵانسی بەکارهێنەر لە Sheet1
df_users = conn.read(worksheet="Sheet1", ttl=0)
user_row = df_users[df_users['Username'] == 'Test_user'].iloc[0]
balance = float(user_row['Wallet_balance'])

# دیزاینی لای چەپ (Sidebar)
st.sidebar.title("💰 هەژماری من")
st.sidebar.metric("باڵانسی ئێستا", f"${balance:,.2f}")

st.sidebar.markdown("---")

# بەشی بارگاویکردن
with st.sidebar.expander("💳 بارگاویکردنی واڵێت"):
    st.write("بڕی پارە بنێرە بۆ ئەم ژمارەیە:")
    st.code("0750XXXXXXX") # ژمارەی خۆت لێرە بنووسە
    dep_amount = st.number_input("بڕی نێردراو ($)", min_value=1.0)
    
    # دوگمەی ناردنی وەسڵ بۆ تێلیگرام
    st.write("وێنەی وەسڵەکە لێرە بنێرە:")
    telegram_url = f"https://t.me/YOUR_USERNAME" # ناوی بەکارهێنەری تێلیگرامی خۆت لێرە بنووسە
    st.link_button("🚀 ناردنی وەسڵ بۆ تێلیگرام", telegram_url)

# دیزاینی ناوەڕاستی سایتەکە
st.title("📈 سەکۆی وەبەرهێنان")
st.write(f"بەخێربێیت **Test_user**! ئێستا دەتوانیت دەست بکەیت بە وەبەرهێنان.")

trade_amount = st.number_input("بڕی وەبەرهێنان ($)", min_value=1.0, max_value=balance)

if st.button("ئێستا بکڕە و قازانج وەرگرە"):
    if balance >= trade_amount:
        st.balloons()
        st.success(f"داواکارییەکەت بە سەرکەوتوویی تۆمارکرا بۆ بڕی ${trade_amount}")
    else:
        st.error("باڵانسی پێویستت نییە. تکایە واڵێتەکەت بارگاوی بکەرەوە.")


