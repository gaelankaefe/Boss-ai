import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

# ڕێکخستنی شاشە بە شێوەی پڕۆفیشناڵ
st.set_page_config(page_title="AI Expert Trader", layout="centered")

st.markdown("""
    <style>
    .reportview-container { background: #0e1117; }
    .signal-card {
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        border: 2px solid #333;
        margin: 10px 0;
    }
    .buy { background-color: #002b1b; color: #00ff88; border-color: #00ff88; }
    .sell { background-color: #2b0000; color: #ff4444; border-color: #ff4444; }
    .neutral { background-color: #1e1e1e; color: #888; border-color: #444; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ AI Expert Committee")
st.write("سیستەمی کۆدەنگی شارەزایان بۆ پێشبینی بازاڕ")

# لیستی دراوەکان
assets = {"EUR/USD": "EURUSD=X", "GBP/USD": "GBPUSD=X", "Bitcoin": "BTC-USD", "Gold": "GC=F"}
selected = st.selectbox("دراوێک هەڵبژێرە:", list(assets.keys()))
tf = st.selectbox("کاتی چارت (Timeframe):", ["1m", "5m", "15m", "1h"])

if st.button("🚀 دەستپێکردنی شیکردنەوەی قووڵ", use_container_width=True):
    with st.spinner('کۆمیتەی شارەزایان خەریکی تاوتوێکردنی بازاڕن...'):
        # وەرگرتنی داتای پێویست (لانیکەم 100 داتا بۆ شیکردنەوەی ورد)
        df = yf.download(assets[selected], period="5d", interval=tf, progress=False)
        df = df.dropna()

        if len(df) > 50:
            # --- حیساباتی تەکنیکی ---
            # 1. RSI
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            df['RSI'] = 100 - (100 / (1 + (gain / loss)))

            # 2. MACD
            ema12 = df['Close'].ewm(span=12, adjust=False).mean()
            ema26 = df['Close'].ewm(span=26, adjust=False).mean()
            df['MACD'] = ema12 - ema26
            df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()

            # 3. Bollinger Bands
            df['MA20'] = df['Close'].rolling(window=20).mean()
            df['Std'] = df['Close'].rolling(window=20).std()
            df['Upper'] = df['MA20'] + (df['Std'] * 2)
            df['Lower'] = df['MA20'] - (df['Std'] * 2)

            # --- کۆمیتەی بڕیاردان ---
            last = df.dropna().iloc[-1]
            score = 0
            
            # شارەزای 1: RSI
            if last['RSI'] < 30: score += 1
            elif last['RSI'] > 70: score -= 1

            # شارەزای 2: MACD
            if last['MACD'] > last['Signal']: score += 1
            else: score -= 1

            # شارەزای 3: Bollinger Bands
            if last['Close'] <= last['Lower']: score += 1
            elif last['Close'] >= last['Upper']: score -= -1

            # --- ئەنجامی کۆتایی ---
            st.divider()
            
            # دیاریکردنی کاتی ترەید (Duration)
            # بۆ 1m ترەیدی 2-3 خولەک، بۆ 5m ترەیدی 10-15 خولەک
            duration = "2-3 خولەک" if tf == "1m" else "10-15 خولەک"

            if score >= 2:
                st.markdown(f"""<div class='signal-card buy'>
                    <h1>🔥 STRONG CALL</h1>
                    <p>هەموو شارەزایان لەسەر کڕین هاوڕان</p>
                    <h3>کاتی ترەید: {duration}</h3>
                </div>""", unsafe_allow_html=True)
            elif score <= -2:
                st.markdown(f"""<div class='signal-card sell'>
                    <h1>🔥 STRONG PUT</h1>
                    <p>هەموو شارەزایان لەسەر فرۆشتن هاوڕان</p>
                    <h3>کاتی ترەید: {duration}</h3>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown("""<div class='signal-card neutral'>
                    <h1>⚖️ WAIT</h1>
                    <p>بازاڕ جێگیر نییە، مەچۆ ناو ترەید</p>
                </div>""", unsafe_allow_html=True)

            # زانیاری زیاتر
            col1, col2, col3 = st.columns(3)
            col1.metric("Price", f"{last['Close']:.5f}")
            col2.metric("RSI", f"{last['RSI']:.1f}")
            col3.metric("Score", f"{score}")
            
        else:
            st.error("داتای تەواو نییە. تکایە کەمێکی تر تاقی بکەرەوە.")
