import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="AI Expert Trader", layout="centered")
st.markdown("<h1 style='text-align: center; color: #ccff00;'>🛡️ AI Expert Committee</h1>", unsafe_allow_html=True)

assets = {
    "EUR/USD": "EURUSD=X",
    "GBP/USD": "GBPUSD=X",
    "Gold (ئاڵتون)": "GC=F",
    "Bitcoin (BTC)": "BTC-USD",
    "Ethereum (ETH)": "ETH-USD"
}

selected_name = st.selectbox("بژاردەیەک هەڵبژێرە:", list(assets.keys()))
selected_symbol = assets[selected_name]
tf = st.selectbox("کاتی چارت (Timeframe):", ["1m", "5m", "15m", "1h"])

if st.button("🚀 دەستپێکردنی شیکردنەوە", use_container_width=True):
    with st.spinner('خەریکی چاککردنی داتا و پشکنینم...'):
        try:
            # وەرگرتنی داتا بەبێ هیچ فلتەرێک لە سەرەتادا
            data = yf.download(selected_symbol, period="3d", interval=tf, progress=False)
            
            if not data.empty:
                # --- ڕێکخستنی ستوونەکان بە شێوەیەکی توند ---
                df = data.copy()
                
                # ئەگەر ستوونەکان تێکەڵ بوون (MultiIndex)، تەنها ئاستی کۆتایی وەردەگرین
                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]
                
                # دڵنیابوونەوە لەوەی ناوی ستوونەکان پیتی گەورەن (وەک ئەوەی yfinance دەینێرێت)
                # ئەگەر 'Close' نەبوو، یەکەم ستوون کە داتای تێدایە بەکاردێنین
                if 'Close' not in df.columns:
                    df = df.rename(columns={df.columns[0]: 'Close'})

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

                df_clean = df.dropna()

                if not df_clean.empty:
                    last = df_clean.iloc[-1]
                    
                    # وەرگرتنی نرخەکان بە دڵنیایی ۱۰۰٪
                    def get_val(val):
                        if hasattr(val, 'iloc'): return float(val.iloc[0])
                        return float(val)

                    price = get_val(last['Close'])
                    rsi_val = get_val(last['RSI'])
                    macd_val = get_val(last['MACD'])
                    sig_val = get_val(last['Signal'])

                    score = 0
                    if rsi_val < 30: score += 1
                    elif rsi_val > 70: score -= 1
                    if macd_val > sig_val: score += 1
                    else: score -= 1

                    st.divider()
                    if score >= 1:
                        st.success(f"🟢 **STRONG CALL** \n\n RSI: {rsi_val:.2f}")
                    elif score <= -1:
                        st.error(f"🔴 **STRONG PUT** \n\n RSI: {rsi_val:.2f}")
                    else:
                        st.warning("⚖️ **WAIT** - بازاڕ جێگیر نییە")
                    
                    st.info(f"💵 نرخی ئێستا: {price:.5f}")
                else:
                    st.error("داتای پێویست بۆ شیکردنەوە ئامادە نییە.")
            else:
                st.error("داتا لە یاهوو وەرنەگیرا.")
        except Exception as e:
            st.error(f"هەڵەی تەکنیکی: {e}")
