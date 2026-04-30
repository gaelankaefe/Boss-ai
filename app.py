import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Boss AI Advisor", layout="centered")

st.markdown("<h1 style='text-align: center; color: #ccff00;'>🤖 AI Market Advisor</h1>", unsafe_allow_html=True)

asset_dict = {"EUR/USD": "EURUSD=X", "GBP/USD": "GBPUSD=X", "Bitcoin": "BTC-USD", "Gold": "GC=F"}
selected = st.selectbox("دراوێک هەڵبژێرە:", list(asset_dict.keys()))
timeframe = st.selectbox("کاتی چارت (Timeframe):", ["1m", "5m", "15m", "1h"])

if st.button("🔍 دەستپێکردنی شیکردنەوە", use_container_width=True):
    with st.spinner('خەریکی وەرگرتنی داتام...'):
        df = yf.download(asset_dict[selected], period="2d", interval=timeframe, progress=False)
        
        if not df.empty:
            # حیسابکردنی RSI بە شێوەی ماتماتیکی سادە
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            df['RSI'] = 100 - (100 / (1 + rs))
            
            # حیسابکردنی MACD
            exp1 = df['Close'].ewm(span=12, adjust=False).mean()
            exp2 = df['Close'].ewm(span=26, adjust=False).mean()
            df['MACD'] = exp1 - exp2
            df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()

            last = df.iloc[-1]
            rsi_val = last['RSI']
            macd_val = last['MACD']
            sig_val = last['Signal']
            price = last['Close']

            st.divider()
            if rsi_val < 35 and macd_val > sig_val:
                st.success(f"🟢 پێشنیار: CALL (کڕین) \n\n RSI: {rsi_val:.2f}")
            elif rsi_val > 65 and macd_val < sig_val:
                st.error(f"🔴 پێشنیار: PUT (فرۆشتن) \n\n RSI: {rsi_val:.2f}")
            else:
                st.warning("⚖️ بڕیار مەدە - ستراتیژییەکان هاوڕا نین")
            
            st.write(f"💵 نرخی ئێستا: **{price:.5f}**")
        else:
            st.error("داتا پەیدا نەکرا")
