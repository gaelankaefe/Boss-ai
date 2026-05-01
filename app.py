import streamlit as st
import yfinance as yf
import pandas as pd
import time

# --- ١. ڕێکخستنی شاشە و ستایل ---
st.set_page_config(page_title="Pro Golden Radar AI", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { width: 100%; height: 60px; background-color: #00ffcc; color: black; font-weight: bold; border-radius: 15px; font-size: 20px; }
    .gold-card { padding: 30px; border-radius: 20px; text-align: center; border: 5px solid gold; margin-top: 20px; }
    .status-box { padding: 10px; border-radius: 10px; text-align: center; background-color: #1e2130; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎯 ڕاداری هەلە زێڕینەکان (PRO)")
st.write("ئەم ئەپە شیکردنەوەی قووڵ بۆ دراو و کانزاکان دەکات")

# --- ٢. لیستی گشتگیری دراوەکان ---
assets = {
    "Bitcoin (BTC)": "BTC-USD",
    "Ethereum (ETH)": "ETH-USD",
    "Solana (SOL)": "SOL-USD",
    "Gold (ئاڵتون)": "GC=F",
    "EUR/USD": "EURUSD=X",
    "GBP/USD": "GBPUSD=X",
    "USD/JPY": "JPY=X",
    "AUD/USD": "AUDUSD=X"
}

col1, col2 = st.columns(2)
with col1:
    selected_name = st.selectbox("دراو هەڵبژێرە:", list(assets.keys()))
with col2:
    tf = st.selectbox("تایمفرێم:", ["1m", "5m", "15m", "1h"])

selected_symbol = assets[selected_name]

# --- ٣. کرداری شیکردنەوە ---
if st.button("🚀 دەستپێکردنی ڕاداری پشکنین"):
    with st.spinner('کۆمیتەی شارەزایان خەریکی پشکنینن...'):
        try:
            # وەرگرتنی داتا بە auto_adjust بۆ ڕێگری لە هەڵەی ستوونەکان
            df = yf.download(selected_symbol, period="3d", interval=tf, progress=False, auto_adjust=True)
            
            if not df.empty and len(df) > 30:
                # دڵنیابوونەوە لەوەی ستوونەکان تێکەڵ نین
                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = df.columns.get_level_values(0)

                # --- ٤. حیساباتی تەکنیکی (بەهێزکراو) ---
                # RSI
                delta = df['Close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
                df['RSI'] = 100 - (100 / (1 + (gain / loss)))

                # MACD
                df['EMA12'] = df['Close'].ewm(span=12, adjust=False).mean()
                df['EMA26'] = df['Close'].ewm(span=26, adjust=False).mean()
                df['MACD'] = df['EMA12'] - df['EMA26']
                df['Signal_L'] = df['MACD'].ewm(span=9, adjust=False).mean()

                # Bollinger Bands
                df['MA20'] = df['Close'].rolling(20).mean()
                df['STD'] = df['Close'].rolling(20).std()
                df['Upper'] = df['MA20'] + (df['STD'] * 2)
                df['Lower'] = df['MA20'] - (df['STD'] * 2)

                # وەرگرتنی کۆتا نرخەکان
                last = df.dropna().iloc[-1]
                price = float(last['Close'])
                rsi_v = float(last['RSI'])
                macd_v = float(last['MACD'])
                sig_v = float(last['Signal_L'])
                up_v = float(last['Upper'])
                lo_v = float(last['Lower'])

                # --- ٥. لۆجیکی "هەلی زێڕین" (سێ قۆناغی) ---
                # مەرجی کڕین: RSI نزم + MACD بڕین + نرخ نێزیک لە هێڵی خوارەوەی بۆڵینگەر
                is_call = (rsi_v < 35) and (macd_v > sig_v) and (price <= lo_v * 1.001)
                
                # مەرجی فرۆشتن: RSI بەرز + MACD بڕین + نرخ نێزیک لە هێڵی سەرەوەی بۆڵینگەر
                is_put = (rsi_v > 65) and (macd_v < sig_v) and (price >= up_v * 0.999)

                st.divider()

                if is_call:
                    st.balloons()
                    st.markdown(f"""
                        <div class="gold-card" style="background-color: #00ff88; color: black;">
                            <h1>💰 هەلی زێڕینی کڕین (CALL)</h1>
                            <p style="font-size: 22px;">سیگناڵێکی زۆر بەهێز بۆ دراوی {selected_name}</p>
                            <p style="font-size: 18px;">کات: ٢ مۆمی داهاتوو (٢ خولەک بۆ 1m)</p>
                        </div>
                    """, unsafe_allow_html=True)
                
                elif is_put:
                    st.snow()
                    st.markdown(f"""
                        <div class="gold-card" style="background-color: #ff4444; color: white;">
                            <h1>💰 هەلی زێڕینی فرۆشتن (PUT)</h1>
                            <p style="font-size: 22px;">سیگناڵێکی زۆر بەهێز بۆ دراوی {selected_name}</p>
                            <p style="font-size: 18px;">کات: ٢ مۆمی داهاتوو (٢ خولەک بۆ 1m)</p>
                        </div>
                    """, unsafe_allow_html=True)
                
                else:
                    st.info("🔎 ڕادارەکە چاودێری دەکات... تا ئێستا هیچ هەلێکی ١٠٠٪ نییە.")
                    
                    # نیشاندانی داتا بۆ ئەوەی بزانیت چەند نێزیکیت لە سیگناڵ
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Price", f"{price:.4f}")
                    c2.metric("RSI", f"{rsi_v:.1f}")
                    c3.metric("MACD", "Bullish" if macd_v > sig_v else "Bearish")

            else:
                st.warning("⚠️ داتا بەردەست نییە. (فۆرێکس شەممە و یەکشەممە داخراوە).")
        except Exception as e:
            st.error(f"هەڵەیەکی تەکنیکی: {e}")
