import streamlit as st
import yfinance as yf
import pandas_ta as ta
import pandas as pd

# ڕێکخستنی شاشە و ڕەنگەکان
st.set_page_config(page_title="AI Market Advisor", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .status-box {
        padding: 25px;
        border-radius: 15px;
        border: 2px solid #333;
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        margin: 20px 0;
    }
    .buy-signal { background-color: #1b2e1b; color: #ccff00; border-color: #ccff00; }
    .sell-signal { background-color: #2e1b1b; color: #ff4b4b; border-color: #ff4b4b; }
    .wait-signal { background-color: #1e1e1e; color: #888; border-color: #444; }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 ڕاوێژکاری زیرەکی بازاڕ")
st.write("شیکردنەوەی ستراتیژییەکانی RSI, MACD و Bollinger Bands")

# ئامادەکردنی دراوەکان
assets = {
    "EUR/USD": "EURUSD=X",
    "GBP/USD": "GBPUSD=X",
    "BTC (Bitcoin)": "BTC-USD",
    "ETH (Ethereum)": "ETH-USD",
    "Gold (زێڕ)": "GC=F"
}

selected_asset = st.selectbox("دراوێک هەڵبژێرە:", list(assets.keys()))
timeframe = st.selectbox("کاتی چارت (Timeframe):", ["1m", "5m", "15m", "1h"])

if st.button("🔍 دەستپێکردنی شیکردنەوەی خێرا", use_container_width=True):
    with st.spinner('خەریکی پشکنینی بازاڕم...'):
        # وەرگرتنی داتا
        symbol = assets[selected_asset]
        df = yf.download(symbol, period="2d", interval=timeframe, progress=False)
        
        if not df.empty:
            # حیسابکردنی ستراتیژییەکان
            df['RSI'] = ta.rsi(df['Close'], length=14)
            macd = ta.macd(df['Close'])
            df = pd.concat([df, macd], axis=1)
            bbands = ta.bbands(df['Close'], length=20)
            
            last = df.iloc[-1]
            rsi_val = last['RSI']
            macd_val = last['MACD_12_26_9']
            macd_s = last['MACDs_12_26_9']
            price = last['Close']
            low_bb = last['BBL_20_2.0']
            up_bb = last['BBU_20_2.0']

            # سستەمی خاڵبەندی (Scoring)
            score = 0
            details = []

            # پشکنینی RSI
            if rsi_val < 35: score += 1; details.append("✅ RSI ئاماژەی کڕین دەدات (Oversold)")
            elif rsi_val > 65: score -= 1; details.append("❌ RSI ئاماژەی فرۆشتن دەدات (Overbought)")

            # پشکنینی MACD
            if macd_val > macd_s: score += 1; details.append("✅ MACD ئاراستەی کڕینی بەهێزە")
            else: score -= 1; details.append("❌ MACD ئاراستەی فرۆشتنی بەهێزە")

            # پشکنینی Bollinger Bands
            if price <= low_bb: score += 1; details.append("✅ نرخ لە هێڵی خوارەوەی پۆڵینجەرە")
            elif price >= up_bb: score -= 1; details.append("❌ نرخ لە هێڵی سەرەوەی پۆڵینجەرە")

            # نیشاندانی دەرەنجام بە گوێرەی کۆدەنگی ستراتیژییەکان
            if score >= 2:
                st.markdown('<div class="status-box buy-signal">🟢 سیگناڵی بەهێز: CALL (کڕین)</div>', unsafe_allow_html=True)
                for d in details: st.write(d)
            elif score <= -2:
                st.markdown('<div class="status-box sell-signal">🔴 سیگناڵی بەهێز: PUT (فرۆشتن)</div>', unsafe_allow_html=True)
                for d in details: st.write(d)
            else:
                st.markdown('<div class="status-box wait-signal">⚖️ بڕیار مەدە (چاوەڕێ بکە)</div>', unsafe_allow_html=True)
                st.write("هۆکار: ستراتیژییەکان لەسەر یەک بڕیار کۆک نین.")
                
            st.divider()
            st.write(f"💵 نرخی ئێستا: **{price:.5f}**")
        else:
            st.error("نەتوانرا داتای بازاڕ وەربگیرێت!")

st.caption("ئەم کۆدە تەنها پێشنیارە و بەرپرسیاریەتی لە ئەستۆ ناگرێت.")
