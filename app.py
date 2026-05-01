import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Pro AI Trader", layout="centered")

# ناونیشان و ستایل
st.markdown("<h1 style='text-align: center; color: #00ffcc;'>🛡️ Professional AI Predictor</h1>", unsafe_allow_html=True)

# لیستێکی وردتر بۆ دراو و کانزاکان
assets = {
    "Bitcoin (BTC)": "BTC-USD",
    "Gold (ئاڵتون)": "GC=F",
    "EUR/USD": "EURUSD=X",
    "GBP/USD": "GBPUSD=X",
    "Ethereum (ETH)": "ETH-USD"
}

selected = st.selectbox("دراوێک هەڵبژێرە:", list(assets.keys()))
tf = st.selectbox("تایمفرێم:", ["1m", "5m", "15m", "1h"])

if st.button("🔍 دەستپێکردنی شیکردنەوەی ورد", use_container_width=True):
    with st.spinner('خەریکی پشکنینی ڕەوتی بازاڕم...'):
        try:
            # وەرگرتنی داتا بە شێوەی خاو
            df = yf.download(assets[selected], period="3d", interval=tf, progress=False)
            
            if not df.empty and len(df) > 30:
                # چاککردنی ستوونەکان بۆ ئەوەی چیتر هەڵەی 'Close' نەدات
                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = df.columns.get_level_values(0)
                
                # 1. ستراتیژی RSI (دیاریکردنی کڕین و فرۆشتنی زۆر)
                delta = df['Close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                df['RSI'] = 100 - (100 / (1 + (gain / loss)))

                # 2. ستراتیژی MACD (دیاریکردنی ئاڕاستەی بازاڕ)
                ema12 = df['Close'].ewm(span=12, adjust=False).mean()
                ema26 = df['Close'].ewm(span=26, adjust=False).mean()
                df['MACD'] = ema12 - ema26
                df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()

                # 3. ستراتیژی Bollinger Bands (دیاریکردنی سنووری نرخ)
                df['MA20'] = df['Close'].rolling(window=20).mean()
                df['STD'] = df['Close'].rolling(window=20).std()
                df['Upper'] = df['MA20'] + (df['STD'] * 2)
                df['Lower'] = df['MA20'] - (df['STD'] * 2)

                # وەرگرتنی کۆتا داتا
                last = df.dropna().iloc[-1]
                rsi = float(last['RSI'])
                macd = float(last['MACD'])
                macd_sig = float(last['Signal'])
                price = float(last['Close'])
                upper = float(last['Upper'])
                lower = float(last['Lower'])

                # --- لۆجیکی پێشبینی (کۆدەنگی شارەزایان) ---
                score = 0
                if rsi < 30: score += 1 # ئاماژەی کڕین
                if macd > macd_sig: score += 1 # ئاماژەی کڕین
                if price <= lower: score += 1 # ئاماژەی کڕین

                if rsi > 70: score -= 1 # ئاماژەی فرۆشتن
                if macd < macd_sig: score -= 1 # ئاماژەی فرۆشتن
                if price >= upper: score -= 1 # ئاماژەی فرۆشتن

                st.divider()

                # نیشاندانی ئەنجام بەپێی کاتی پێویست
                duration = "2-3 خولەک" if tf == "1m" else "10-15 خولەک"

                if score >= 2:
                    st.success(f"🔥 **STRONG CALL (کڕین)** \n\n کاتی پێشنیارکراو: {duration} \n\n RSI: {rsi:.1f}")
                elif score <= -2:
                    st.error(f"🔥 **STRONG PUT (فرۆشتن)** \n\n کاتی پێشنیارکراو: {duration} \n\n RSI: {rsi:.1f}")
                else:
                    st.warning("⚖️ **چاوەڕێ بکە** - سیگناڵەکە بەهێز نییە")

                st.info(f"💵 نرخی ئێستا: {price:.5f}")
                
            else:
                st.error("داتا بەردەست نییە. دڵنیابە بازاڕ کراوەیە.")
        except Exception as e:
            st.error(f"هەڵەیەکی تەکنیکی ڕوویدا: {e}")
