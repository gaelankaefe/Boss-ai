import streamlit as st
import pandas as pd
import numpy as np
import requests
import ta
from sklearn.ensemble import RandomForestClassifier

API_KEY = "YOUR_API_KEY"

# =============================
# 📥 DATA
# =============================
def get_data(symbol, interval):
    url = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval={interval}&apikey={API_KEY}&outputsize=500"
    data = requests.get(url).json()

    if "values" not in data:
        return None

    df = pd.DataFrame(data['values'])
    df = df.astype(float)
    df = df[::-1]
    return df

# =============================
# 📊 INDICATORS
# =============================
def indicators(df):
    df['rsi'] = ta.momentum.RSIIndicator(df['close'], 14).rsi()

    df['ema20'] = ta.trend.EMAIndicator(df['close'], 20).ema_indicator()
    df['ema50'] = ta.trend.EMAIndicator(df['close'], 50).ema_indicator()
    df['ema200'] = ta.trend.EMAIndicator(df['close'], 200).ema_indicator()

    macd = ta.trend.MACD(df['close'])
    df['macd'] = macd.macd()
    df['macd_signal'] = macd.macd_signal()

    bb = ta.volatility.BollingerBands(df['close'])
    df['bb_high'] = bb.bollinger_hband()
    df['bb_low'] = bb.bollinger_lband()

    df['adx'] = ta.trend.ADXIndicator(df['high'], df['low'], df['close']).adx()

    return df

# =============================
# 🕯 Candle Pattern
# =============================
def engulfing(df):
    if len(df) < 2:
        return 0
    prev = df.iloc[-2]
    last = df.iloc[-1]

    # Bullish
    if prev['close'] < prev['open'] and last['close'] > last['open']:
        return 1
    # Bearish
    if prev['close'] > prev['open'] and last['close'] < last['open']:
        return -1
    return 0

# =============================
# 🤖 AI MODEL
# =============================
def train_ai(df):
    df['future'] = df['close'].shift(-5)
    df['target'] = (df['future'] > df['close']).astype(int)

    features = ['rsi','ema20','ema50','macd','adx']
    df = df.dropna()

    X = df[features]
    y = df['target']

    model = RandomForestClassifier(n_estimators=200)
    model.fit(X, y)

    return model

# =============================
# 🧠 STRATEGY
# =============================
def strategy(df):
    last = df.iloc[-1]
    buy, sell = 0, 0

    # Trend
    if last['close'] > last['ema200']:
        buy += 3
    else:
        sell += 3

    # EMA Cross
    if last['ema20'] > last['ema50']:
        buy += 2
    else:
        sell += 2

    # RSI
    if last['rsi'] < 30:
        buy += 2
    elif last['rsi'] > 70:
        sell += 2

    # MACD
    if last['macd'] > last['macd_signal']:
        buy += 2
    else:
        sell += 2

    # BB
    if last['close'] < last['bb_low']:
        buy += 2
    elif last['close'] > last['bb_high']:
        sell += 2

    # Candle Pattern
    pattern = engulfing(df)
    if pattern == 1:
        buy += 2
    elif pattern == -1:
        sell += 2

    strong = last['adx'] > 25

    total = buy + sell
    conf = max(buy, sell) / total if total else 0

    if not strong or conf < 0.65:
        return "NO TRADE", conf

    return ("BUY", conf) if buy > sell else ("SELL", conf)

# =============================
# 🔥 FINAL AI + STRATEGY
# =============================
def predict(symbol):
    df1 = get_data(symbol, "1min")
    df5 = get_data(symbol, "5min")

    if df1 is None or df5 is None:
        return "ERROR", 0

    df1 = indicators(df1)
    df5 = indicators(df5)

    model = train_ai(df1)

    features = ['rsi','ema20','ema50','macd','adx']
    last = df1[features].dropna().tail(1)

    ai_pred = model.predict(last)[0]
    ai_conf = model.predict_proba(last)[0].max()

    s1, c1 = strategy(df1)
    s5, c5 = strategy(df5)

    # FINAL DECISION
    if s1 == s5 and s1 != "NO TRADE" and ai_conf > 0.6:
        final = "BUY" if ai_pred == 1 else "SELL"
        confidence = (ai_conf + c1 + c5) / 3
        return final, confidence

    return "NO TRADE", (ai_conf + c1 + c5) / 3

# =============================
# 🌐 UI
# =============================
st.set_page_config(page_title="AI TRADING BOT", layout="centered")

st.title("🤖 AI Trading Bot (ULTRA PRO MAX)")

symbol = st.selectbox("دراو", ["EUR/USD", "BTC/USD"])
auto = st.checkbox("Auto Refresh (5s)")

if st.button("🚀 پێشبینی بکە"):
    signal, confidence = predict(symbol)

    if signal == "BUY":
        st.success(f"📈 BUY\n\nConfidence: {confidence:.2f}")
    elif signal == "SELL":
        st.error(f"📉 SELL\n\nConfidence: {confidence:.2f}")
    elif signal == "ERROR":
        st.warning("⚠️ هەڵە لە داتا")
    else:
        st.info(f"⏳ NO TRADE\n\nConfidence: {confidence:.2f}")

# Auto Refresh
if auto:
    import time
    time.sleep(5)
    st.rerun()
