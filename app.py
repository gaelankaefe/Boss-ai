import streamlit as st
from engine import multi_tf_signal, suggest_expiry
from tracker import log_trade, stats

st.set_page_config(page_title="Pocket Option Bot", layout="centered")

st.title("💰 Pocket Option Signal Bot")

symbol = st.selectbox("Currency", ["EUR/USD", "GBP/USD", "BTC/USD"])

if st.button("🚀 Get Signal"):
    signal, conf = multi_tf_signal(symbol)
    expiry = suggest_expiry()

    if signal == "BUY":
        st.success(f"📈 UP (BUY)\nConfidence: {conf:.2f}\nExpiry: {expiry}")
    elif signal == "SELL":
        st.error(f"📉 DOWN (SELL)\nConfidence: {conf:.2f}\nExpiry: {expiry}")
    elif signal == "ERROR":
        st.warning("⚠️ Data Error")
    else:
        st.info(f"⏳ NO TRADE\nConfidence: {conf:.2f}")

st.divider()

st.subheader("📊 Result Tracker")

col1, col2 = st.columns(2)

with col1:
    if st.button("✅ Win"):
        log_trade(symbol, "last", "win")

with col2:
    if st.button("❌ Loss"):
        log_trade(symbol, "last", "loss")

total, wins, winrate = stats()

st.write(f"Total Trades: {total}")
st.write(f"Wins: {wins}")
st.write(f"Winrate: {winrate:.2f}%")
