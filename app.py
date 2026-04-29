import streamlit as st
import pandas as pd
import yfinance as download_data # ئەگەر بۆ داتاکان بەکاری دێنیت

# --- ١. ڕێکخستنی سەرەتایی واڵێت ---
if 'wallet' not in st.session_state:
    st.session_state.wallet = 100.0  # بڕی پارەی سەرەتایی دیارییە

# --- ٢. دیزاینی Sidebar (لای چەپ) ---
st.sidebar.title("💰 هەژماری من")
st.sidebar.metric(label="بڕی پارەی ناو واڵێت", value=f"${st.session_state.wallet:,.2f}")

# بەشی بارگاویکردن بۆ تاقیکردنەوە
with st.sidebar.expander("💳 بارگاویکردنی واڵێت"):
    amount_to_add = st.number_input("بڕی پارە (USD)", min_value=0)
    if st.button("زیادکردن"):
        st.session_state.wallet += amount_to_add
        st.success("سەرکەوتووبوو!")
        st.rerun()

# --- ٣. ناونیشانی سەرەکی سایتەکە ---
st.title("🚀 سەکۆی زیرەکی فۆرێکس")
st.write(f"بەخێربێیت! ئێستا دەتوانیت وەبەرهێنان بکەیت.")

# لێرەدا کۆدی چارتەکەت دادەنێیت (ئەوەی پێشتر هەبوو)
# بۆ نموونە:
symbol = st.selectbox("دراوێک هەڵبژێرە:", ["EURUSD=X", "GBPUSD=X", "BTC-USD"])
st.info(f"نرخی ئێستای {symbol} لە چارتەکە نیشان دراوە.")

# --- ٤. سیستەمی کڕین و قازانج ---
st.write("---")
st.header("🛒 بازاڕی وەبەرهێنان")

col1, col2 = st.columns(2)

with col1:
    trade_amount = st.number_input("بڕی وەبەرهێنان ($)", min_value=1.0, max_value=float(st.session_state.wallet))
    st.caption(f"تێبینی: ٥٪ قازانج وەردەگریت لەسەر ئەم بڕە.")

with col2:
    if st.button("✅ ئێستا بکڕە و قازانج وەرگرە"):
        if st.session_state.wallet >= trade_amount:
            # کەمکردنەوەی پارەکە
            st.session_state.wallet -= trade_amount
            
            # حیسابکردنی قازانج (بۆ نموونە ٥٪)
            profit = trade_amount * 0.05
            st.session_state.wallet += (trade_amount + profit)
            
            st.balloons() # ئاهەنگگێڕان بە پەرشبوونی باڵۆن
            st.success(f"پیرۆزە! بڕی ${profit} قازانجمان خستە سەر واڵێتەکەت.")
            st.rerun()
        else:
            st.error("پارەی پێویستت نییە!")

# --- ٥. مێژووی چالاکییەکان (Optional) ---
st.write("---")
with st.expander("🕒 مێژووی چالاکییەکان"):
    st.write("هێشتا هیچ کڕینێکی تۆمارکراو نییە.")

