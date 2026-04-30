import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# پەیوەندی لەگەڵ گوگڵ شیت
conn = st.connection("gsheets", type=GSheetsConnection)

# خوێندنەوەی داتا - لێرە تاقی دەکەینەوە ئەگەر هەڵە هەبوو نامەیەکمان بداتێ
try:
    df = conn.read(ttl=5) # ttl=5 واتا هەر ٥ چرکە جارێک زانیاری نوێ بێنە
    user_row = df[df['Username'] == 'Test_user'].iloc[0]
    balance = float(user_row['Wallet_balance'])
except Exception as e:
    st.error("کێشەیەک لە پەیوەندی گوگڵ شیت هەیە. تکایە دڵنیابە لە لینکەکە.")
    st.stop()

# لای چەپی سایتەکە
st.sidebar.title("💰 هەژماری من")
st.sidebar.metric("باڵانسی ئێستا", f"${balance:,.2f}")

# بەشی وەبەرهێنان
st.title("📈 سەکۆی وەبەرهێنانی فۆرێکس")
amount = st.number_input("بڕی وەبەرهێنان ($)", min_value=1.0)

if st.button("✅ ئێستا بکڕە"):
    if balance >= amount:
        new_balance = balance + (amount * 0.05)
        # گۆڕینی پارەکە لە ناو خشتەکەدا
        df.loc[df['Username'] == 'Test_user', 'Wallet_balance'] = new_balance
        # ناردنی بۆ گوگڵ شیت
        conn.update(data=df)
        
        st.balloons()
        st.success(f"سەرکەوتوو بوو! باڵانسی نوێ: ${new_balance}")
    else:
        st.error("باڵانسەکەت بەش ناکات")
