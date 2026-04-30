import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# ١. پەیوەندی لەگەڵ گوگڵ شیت
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(ttl=5)
    
    # دڵنیابوونەوە لەوەی Wallet_balance ژمارەیە
    df['Wallet_balance'] = pd.to_numeric(df['Wallet_balance'], errors='coerce')
    
    user_row = df[df['Username'] == 'Test_user'].iloc[0]
    balance = float(user_row['Wallet_balance'])
except Exception as e:
    st.error("⚠️ کێشە لە خوێندنەوەی داتا هەیە.")
    st.stop()

# ٢. دیزاینی Sidebar
st.sidebar.title("💰 هەژماری من")
st.sidebar.metric("باڵانسی ئێستا", f"${balance:,.2f}")

# بەشی بارگاویکردن
with st.sidebar.expander("💳 بارگاویکردنی واڵێت"):
    st.write("**USDT (TRC20):**")
    st.code("TMR7DR8EtB3aNp2inXt8zfTVsXbHm9dv8M")
    telegram_url = "https://t.me/YOUR_USERNAME" # ناوی خۆت لێرە بنووسە
    st.link_button("🚀 ناردنی وەسڵ", telegram_url)

# ٣. بەشی سەرەکی
st.title("📈 فۆڕێکس")
st.write(f"بەخێربێیت **Test_user**")

amount = st.number_input("($) بڕی وەبەرهێنان", min_value=1.0, step=1.0)

if st.button("✅ ئێستا بکڕە"):
    if balance >= amount:
        # لێرەدا بە وردی ژمارەکان کۆدەکەینەوە
        profit = float(amount) * 0.05
        new_balance = float(balance) + profit
        
        # گۆڕینی نرخەکە لەناو داتاکان
        df.loc[df['Username'] == 'Test_user', 'Wallet_balance'] = new_balance
        
        # نوێکردنەوەی شیتەکە
        conn.update(data=df)
        
        st.balloons()
        st.success(f"سەرکەوتوو بوو! باڵانسی نوێ: ${new_balance:,.2f}")
    else:
        st.error("⚠️ باڵانسەکەت بەش ناکات")
