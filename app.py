import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Golden Radar AI", layout="centered")

# ستایلی تایبەت بۆ ئەوەی سیگناڵەکان زۆر دیار بن
st.markdown("""
    <style>
    .stButton>button { width: 100%; height: 50px; background-color: #00ffcc; color: black; font-weight: bold; }
    .gold-box { padding: 30px; border-radius: 20px; text-align: center; font-weight: bold; font-size: 25px; border: 5px solid gold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎯 ڕاداری هەلە زێڕینەکان")

assets = {"Bitcoin (BTC)": "BTC-USD", "Ethereum (ETH)": "ETH-USD", "Gold": "GC=F"}
selected = st.selectbox("دراوێک هەڵبژێرە:", list(assets.keys()))
tf = st.selectbox("تایمفرێم:", ["1m", "5m", "15m"])

if st.button("🚀 دەستپێکردنی ڕاداری پشکنین"):
    with st.spinner('خەریکی ڕاوکردنی هەلە زێڕینەکانم...'):
        try:
            # وەرگرتنی داتا بە نوێترین شێواز
            df = yf.download(assets[selected], period="2d", interval=tf, progress=False, auto_adjust=True)
            
            if not df.empty and len(df) > 20:
                # سادەکردنەوەی داتا
                if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
                
                # ستراتیژییەکان
                df['RSI'] = 100 - (100 / (1 + (df['Close'].diff().where(df['Close'].diff() > 0, 0).rolling(14).mean() / 
                                              -df['Close'].diff().where(df['Close'].diff() < 0, 0).rolling(14).mean())))
                df['MA20'] = df['Close'].rolling(20).mean()
                df['Upper'] = df['MA20'] + (df['Close'].rolling(20).std() * 2)
                df['Lower'] = df['MA20'] - (df['Close'].rolling(20).std() * 2)

                last = df.dropna().iloc[-1]
                price, rsi = float(last['Close']), float(last['RSI'])
                upper, lower = float(last['Upper']), float(last['Lower'])

                st.divider()

                # --- لۆجیکی هەلی زێڕین (کەمێک نەرمتر بۆ ئەوەی هەلەکان لەدەست نەچن) ---
                if rsi < 35 and price <= lower * 1.001:
                    st.balloons()
                    st.markdown("<div class='gold-box' style='background-color: #00ff88; color: black;'>"
                                "💰 هەلی زێڕینی کڕین (CALL)<br>کات: ٢ مۆمی داهاتوو</div>", unsafe_allow_html=True)
                
                elif rsi > 65 and price >= upper * 0.999:
                    st.snow()
                    st.markdown("<div class='gold-box' style='background-color: #ff4444; color: white;'>"
                                "💰 هەلی زێڕینی فرۆشتن (PUT)<br>کات: ٢ مۆمی داهاتوو</div>", unsafe_allow_html=True)
                
                else:
                    st.info("🔎 ڕادارەکە چاودێری دەکات... تا ئێستا هیچ هەلێکی ١٠٠٪ نییە. تکایە چەند چرکەیەکی تر دوگمەکە دابگرەوە.")
                    st.write(f"نرخی ئێستا: {price:.2f} | RSI: {rsi:.1f}")
            
        except Exception as e:
            st.error(f"تکایە دووبارە هەوڵ بدەرەوە. هەڵە: {e}")
