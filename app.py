import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# ١. پەیوەندی
conn = st.connection("gsheets", type=GSheetsConnection)

# ٢. خوێندنەوەی داتا بە شێوەیەک کە تێک نەچێت
df = conn.read(ttl=0) # ttl=0 بۆ ئەوەی هەمیشە نوێترین ژمارە ببینیت

# دڵنیابوون لەوەی باڵانس ژمارەیە
df['Wallet_balance'] = pd.to_numeric(df['Wallet_balance'], errors='coerce').fillna(0)

try:
    user_index = df[df['Username'] == 'Test_user'].index[0]
    balance = float(df.at[user_index, 'Wallet_balance'])
except:
    st.error("Username نەدۆزرایەوە لە ناو شیتەکەدا")
    st.stop()

# دیزاینی Sidebar
st.sidebar.title("💰 هەژماری من")
st.sidebar.metric("باڵانسی ئێستا", f"${balance:,.2f}")

# بەشی فۆرێکس
st.title("📈 فۆڕێکس")
st.write(f"بەخێربێیت **Test_user**")

amount = st.number_input("($) بڕی وەبەرهێنان", min_value=1.0, step=1.0)

if st.button("✅ ئێستا بکڕە"):
    if balance >= amount:
        # ئەنجامدانی حیسابات
        profit = float(amount) * 0.05
        new_balance = balance + profit
        
        # نوێکردنەوەی نرخەکە لە ناو لیستەکەدا
        df.at[user_index, 'Wallet_balance'] = new_balance
        
        # --- ئەمە دێڕە گرنگەکەیە بۆ چارەسەری TypeError ---
        conn.update(data=df) 
        
        st.balloons()
        st.success(f"سەرکەوتوو بوو! باڵانسی نوێ: ${new_balance:,.2f}")
        st.info("تکایە لاپەڕەکە ڕیفریش بکەرەوە بۆ بینینی گۆڕانکارییەکە.")
    else:
        st.error("⚠️ باڵانسەکەت بەش ناکات")
