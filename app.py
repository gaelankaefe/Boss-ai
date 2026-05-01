import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="AI Expert Trader", layout="centered")

st.title("🛡️ AI Expert Committee")

assets = {"EUR/USD": "EURUSD=X", "GBP/USD": "GBPUSD=X", "Bitcoin": "BTC-USD", "Gold": "GC=F"}
selected = st.selectbox("دراوێک هەڵبژێرە:", list(assets.keys()))
tf = st.selectbox("کاتی چارت (Timeframe):", ["1m", "5m", "15m", "1h"])

if st.button("🚀 دەستپێکردنی شیکردنەوەی قووڵ", use_container_width=True):
    with st.spinner('کۆمیتەی شارەزایان خەریکی پشکنینن...'):
        try:
            # وەرگرتنی داتای پێویست
            df = yf.download(assets[selected], period="5d", interval=tf, progress=False)
            
            if not df.empty and len(df) > 30:
                # حیسابکردنی RSI
                delta = df['Close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                df['RSI'] = 100 - (100 / (1 + (gain / loss)))

                # حیسابکردنی MACD
                ema12 = df['Close'].ewm(span=12, adjust=False).mean()
                ema26 = df['Close'].ewm(span=26, adjust=False).mean()
                df['MACD'] = ema12 - ema26
                df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()

                # پاککردنەوەی هەموو ئەو ڕیزانەی داتایان تێدا نییە (زۆر گرنگە بۆ لابردنی ValueError)
                df_clean = df.dropna()

                if not df_clean.empty:
                    last = df_clean.iloc[-1]
                    
                    # وەرگرتنی نرخەکان و دڵنیابوونەوە لەوەی ژمارەن
                    rsi_val = float(last['RSI'])
                    macd_val = float(last['MACD'])
                    sig_val = float(last['Signal'])
                    price = float(last['Close'])

                    score = 0
                    if rsi_val < 30: score += 1
                    elif rsi_val > 70: score -= 1
                    if macd_val > sig_val: score += 1
                    else: score -= 1

                    st.divider()
                    duration = "2-3 خولەک" if tf == "1m" else "10-15 خولەک"

                    if score >= 1:
                        st.success(f"🟢 STRONG CALL بۆ ماوەی {duration} \n\n RSI: {rsi_val:.2f}")
                    elif score <= -1:
                        st.error(f"🔴 STRONG PUT بۆ ماوەی {duration} \n\n RSI: {rsi_val:.2f}")
                    else:
                        st.warning("⚖️ بڕیار مەدە - بازاڕ ڕوون نییە")
                    
                    st.info(f"💵 نرخی ئێستا: {price:.5f}")
                else:
                    st.error("⚠️ داتای پێویست ئامادە نییە، کەمێکی تر تاقی بکەرەوە.")
            else:
                st.error("⚠️ داتا وەرنەگیرا. دڵنیابە بازاڕ کراوەیە.")
        except Exception as e:
            st.error(f"هەڵەیەک ڕوویدا: {e}")
