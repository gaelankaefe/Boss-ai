import streamlit as st
import yfinance as yf
import pandas as pd

# ڕێکخستنی لاپەڕە
st.set_page_config(page_title="AI Expert Trader", layout="centered")
st.markdown("<h1 style='text-align: center; color: #ccff00;'>🛡️ AI Expert Committee</h1>", unsafe_allow_html=True)

# لیستی گشتگیر بۆ دراوەکان، کانزاکان و کریپتۆ
assets = {
    "--- FOREX (دراوەکان) ---": None,
    "EUR/USD": "EURUSD=X",
    "GBP/USD": "GBPUSD=X",
    "USD/JPY": "JPY=X",
    "AUD/USD": "AUDUSD=X",
    "USD/CAD": "CAD=X",
    "--- METALS (کانزاکان) ---": None,
    "Gold (ئاڵتون)": "GC=F",
    "Silver (زیو)": "SI=F",
    "--- CRYPTO (کریپتۆ) ---": None,
    "Bitcoin (BTC)": "BTC-USD",
    "Ethereum (ETH)": "ETH-USD",
    "Solana (SOL)": "SOL-USD",
    "Binance Coin (BNB)": "BNB-USD"
}

# فلتەرکردنی ناوەکان بۆ ئەوەی ناونیشانی بەشەکان نەبنە بژاردە
asset_list = [k for k, v in assets.items() if v is not None]

selected_name = st.selectbox("بژاردەیەک هەڵبژێرە:", asset_list)
selected_symbol = assets[selected_name]

tf = st.selectbox("کاتی چارت (Timeframe):", ["1m", "5m", "15m", "1h", "4h", "1d"])

if st.button("🚀 دەستپێکردنی شیکردنەوەی گشتگیر", use_container_width=True):
    with st.spinner(f'کۆمیتەی شارەزایان خەریکی پشکنینی {selected_name}ـن...'):
        try:
            # وەرگرتنی داتا بە auto_adjust بۆ ڕێگری لە Multi-index error
            data = yf.download(selected_symbol, period="5d", interval=tf, progress=False, auto_adjust=True)
            
            if not data.empty and len(data) > 30:
                df = data.copy()
                
                # --- حیساباتی تەکنیکی (RSI, MACD) ---
                delta = df['Close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                df['RSI'] = 100 - (100 / (1 + (gain / loss)))

                ema12 = df['Close'].ewm(span=12, adjust=False).mean()
                ema26 = df['Close'].ewm(span=26, adjust=False).mean()
                df['MACD'] = ema12 - ema26
                df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()

                # پاککردنەوەی داتا
                df_clean = df.dropna()

                if not df_clean.empty:
                    last = df_clean.iloc[-1]
                    rsi_val = float(last['RSI'])
                    macd_val = float(last['MACD'])
                    sig_val = float(last['Signal'])
                    price = float(last['Close'])

                    # لۆجیکی بڕیاردان
                    score = 0
                    if rsi_val < 30: score += 1
                    elif rsi_val > 70: score -= 1
                    if macd_val > sig_val: score += 1
                    else: score -= 1

                    st.divider()
                    
                    # پێشنیارکردنی ماوەی ترەید
                    duration_map = {"1m": "2-3m", "5m": "10-15m", "15m": "30-45m", "1h": "2-4h"}
                    duration = duration_map.get(tf, "بۆ ماوەیەکی گونجاو")

                    if score >= 1:
                        st.success(f"🟢 **STRONG CALL** \n\n پێشنیار دەکرێت بۆ: {duration}")
                    elif score <= -1:
                        st.error(f"🔴 **STRONG PUT** \n\n پێشنیار دەکرێت بۆ: {duration}")
                    else:
                        st.warning("⚖️ **WAIT** - بازاڕ جێگیر نییە")
                    
                    # نیشاندانی داتا تەکنیکییەکان
                    col1, col2 = st.columns(2)
                    col1.metric("نرخی ئێستا", f"{price:.5f}")
                    col2.metric("RSI (14)", f"{rsi_val:.1f}")
                else:
                    st.error("⚠️ داتای پێویست ئامادە نییە.")
            else:
                st.error("⚠️ داتا وەرنەگیرا. دڵنیابە بازاڕ کراوەیە (فۆرێکس شەممە و یەکشەممە داخراوە).")
        except Exception as e:
            st.error(f"هەڵەیەک ڕوویدا: {e}")
