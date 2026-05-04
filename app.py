import streamlit as st
import yfinance as yf
import pandas as pd
import time

# ڕێکخستنی لاپەڕە
st.set_page_config(page_title="Boss-AI Bot", layout="wide")

def get_data(symbol):
    # وەرگرتنی داتا لە Yahoo Finance بۆ ئەوەی ڕاستەوخۆ بێت
    df = yf.download(symbol, period="1d", interval="1m", progress=False)
    return df

def check_patterns(df):
    if len(df) < 3: return None
    
    # وەرگرتنی مۆمەکان (Open, High, Low, Close)
    c2 = df.iloc[-2] # مۆمی پێشوو
    c3 = df.iloc[-1] # مۆمی ئێستا
    
    body = abs(c3['Close'] - c3['Open'])
    upper_wick = c3['High'] - max(c3['Open'], c3['Close'])
    lower_wick = min(c3['Open'], c3['Close']) - c3['Low']
    
    # --- ستراتیژییەکان بەپێی وێنەکان ---
    
    # Hammer (چەقۆ) -
    if lower_wick > (2 * body) and upper_wick < (0.2 * body):
        return "🟢 کڕین (BUY): Hammer Detected 🔨"
    
    # Shooting Star (ئەستێرەی تەقەکردن) -
    if upper_wick > (2 * body) and lower_wick < (0.2 * body):
        return "🔴 فرۆشتن (SELL): Shooting Star Detected 🏹"
        
    # Bullish Engulfing -
    if c2['Close'] < c2['Open'] and c3['Close'] > c3['Open'] and c3['Close'] > c2['Open']:
        return "🟢 کڕین (BUY): Bullish Engulfing 🔥"

    return "🔎 چاوەڕێی دەرفەتێکی زێڕین..."

# بەشی پیشاندان لە سایتەکە
st.title("Boss-AI Trading Signal")
symbol = st.text_input("ناوی دراو بنووسە (بۆ نموونە: BTC-USD یان EURUSD=X)", "BTC-USD")

placeholder = st.empty()

while True:
    try:
        with placeholder.container():
            data = get_data(symbol)
            if not data.empty:
                current_price = data['Close'].iloc[-1]
                signal = check_patterns(data)
                
                st.metric("نرخی ئێستا", f"${current_price:,.2f}")
                
                if "BUY" in signal: st.success(signal)
                elif "SELL" in signal: st.error(signal)
                else: st.info(signal)
                
                st.line_chart(data['Close'].tail(30))
                
        time.sleep(10) # هەر ١٠ چرکە جارێک نوێ دەبێتەوە
    except:
        st.error("کێشەیەک لە پەیوەندی هەیە...")
        time.sleep(5)
