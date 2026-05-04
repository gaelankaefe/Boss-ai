import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import time

st.set_page_config(page_title="Boss-AI Trading Bot", layout="wide")
st.title("📈 Boss-AI Real-Time Strategy Bot")

# --- بەشی وەرگرتنی نرخەکان ---
def get_live_data(symbol="BTC-USD"):
    data = yf.download(tickers=symbol, period="1d", interval="1m", progress=False)
    # ڕێکخستنی ناوەکان بۆ ئەوەی کار لەگەڵ لۆژیکی مۆمەکان بکەن
    df = data.copy()
    df.columns = ['Adj Close', 'Close', 'High', 'Low', 'Open', 'Volume']
    return df

# --- لۆژیکی شیکاری مۆمەکان بەپێی وێنەکان ---
def analyze_signal(df):
    if len(df) < 5: return None
    
    # وەرگرتنی ٣ مۆمی کۆتایی
    c1, c2, c3 = df.iloc[-3], df.iloc[-2], df.iloc[-1]
    
    def get_body(c): return abs(c['Close'] - c['Open'])
    
    body3 = get_body(c3)
    upper_wick3 = c3['High'] - max(c3['Open'], c3['Close'])
    lower_wick3 = min(c3['Open'], c3['Close']) - c3['Low']

    # ١. Hammer (چەقۆ) - کڕین
    if lower_wick3 > (2 * body3) and upper_wick3 < (0.2 * body3):
        return "🟢 BUY: Hammer Detected 🔨"

    # ٢. Bullish Engulfing - کڕین
    if c2['Close'] < c2['Open'] and c3['Close'] > c3['Open'] and c3['Close'] > c2['Open']:
        return "🟢 BUY: Bullish Engulfing 🔥"

    # ٣. Shooting Star - فرۆشتن
    if upper_wick3 > (2 * body3) and lower_wick3 < (0.2 * body3):
        return "🔴 SELL: Shooting Star Detected 🏹"

    # ٤. Morning Star - کڕین
    if c1['Close'] < c1['Open'] and get_body(c2) < (0.3 * get_body(c1)) and c3['Close'] > c3['Open']:
        return "🟢 BUY: Morning Star Pattern 🌅"

    # ٥. Doji - ئاگاداری
    if body3 < (0.1 * (c3['High'] - c3['Low'])):
        return "⚠️ WAIT: Doji Detected (دوودڵی بازاڕ)"

    return "🔎 چاوەڕوانی دەرفەتێکی زێڕین بە..."

# --- بەشی پیشاندان لە سایتەکە ---
symbol = st.sidebar.text_input("Symbol (e.g., BTC-USD, EURUSD=X)", "BTC-USD")

placeholder = st.empty()

while True:
    with placeholder.container():
        df = get_live_data(symbol)
        current_price = df['Close'].iloc[-1]
        signal = analyze_signal(df)

        col1, col2 = st.columns(2)
        col1.metric(f"Current Price ({symbol})", f"${current_price:,.2f}")
        
        if "BUY" in signal:
            col2.success(signal)
        elif "SELL" in signal:
            col2.error(signal)
        else:
            col2.info(signal)

        st.line_chart(df['Close'].tail(50))
        
        # ڕیفرێشکردن هەر ١٠ چرکە جارێک
        time.sleep(10)
        st.rerun()
