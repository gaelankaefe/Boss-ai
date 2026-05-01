import streamlit as st
import yfinance as yf
import pandas as pd

# ڕێکخستنی شاشە
st.set_page_config(page_title="AI Expert Trader", layout="centered")
st.markdown("<h1 style='text-align: center; color: #ccff00;'>🛡️ AI Expert Committee</h1>", unsafe_allow_html=True)

# لیستی گشتگیر
assets = {
    "EUR/USD": "EURUSD=X",
    "GBP/USD": "GBPUSD=X",
    "Gold (ئاڵتون)": "GC=F",
    "Bitcoin (BTC)": "BTC-USD",
    "Ethereum (ETH)": "ETH-USD",
    "Solana (SOL)": "SOL-USD"
}

selected_name = st.selectbox("بژاردەیەک هەڵبژێرە:", list(assets.keys()))
selected_symbol = assets[selected_name]
tf = st.selectbox("کاتی چارت (Timeframe):", ["1m", "5m", "15m", "1h", "4h"])

if st.button("🚀 دەستپێکردنی شیکردنەوە", use_container_width=True):
    with st.spinner('خەریکی پشکنینی وردم...'):
        try:
            # کلیل لێرەیە: بەکارهێنانی group_by='column' بۆ ڕێگری لە Multi-index error
            data = yf.download(selected_symbol, period="5d", interval=tf, progress=False, group_by='column')
            
            if not data.empty and len(data) > 30:
                # سادەکردنەوەی داتا بۆ ئەوەی دڵنیابین تەنها یەک ستوونمان هەیە
                df = data.copy()
                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = df.columns.get_level_values(-1)

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

                # پاککردنەوەی داتا
                df_clean = df.dropna()

                if not df_clean.empty:
                    last = df_clean.iloc[-1]
                    
                    # وەرگرتنی نرخەکان و دڵنیابوون لەوەی تەنها یەک ژمارەن (.item() بەکارهاتووە)
                    price = float(last['Close'].iloc[0]) if hasattr(last['Close'], '__len__') else float(last['Close'])
                    rsi_val = float(last['RSI'].iloc[0]) if hasattr(last['RSI'], '__len__') else float(last['RSI'])
                    macd_val = float(last['MACD'].iloc[0]) if hasattr(last['MACD'], '__len__') else float(last['MACD'])
                    sig_val = float(last['Signal'].iloc[0]) if hasattr(last['Signal'], '__len__') else float(last['Signal'])

                    score = 0
                    if rsi_val < 32: score += 1
                    elif rsi_val > 68: score -= 1
                    if macd_val > sig_val: score += 1
                    else: score -= 1

                    st.divider()
                    
                    if score >= 1:
                        st.success(f"🟢 **STRONG CALL** \n\n RSI: {rsi_val:.2f}")
                    elif score <= -1:
                        st.error(f"🔴 **STRONG PUT** \n\n RSI: {rsi_val:.2f}")
                    else:
                        st.warning("⚖️ **WAIT** - بازاڕ ڕوون نییە")
                    
                    st.info(f"💵 نرخی ئێستا: {price:.5f}")
                else:
                    st.error("⚠️ داتا پاک نەکراوەتەوە.")
            else:
                st.error("⚠️ داتا بەردەست نییە. (ئەگەر فۆرێکسە، بازاڕ داخراوە).")
        except Exception as e:
            st.error(f"هەڵەی تەکنیکی: {e}")
