import streamlit as st
import yfinance as yf
import pandas as pd
from prophet import Prophet
import plotly.graph_objects as go

# 1. ڕێکخستنی لاپەڕە
st.set_page_config(page_title="Forex Multi-Page AI", layout="wide")

# 2. دروستکردنی Menu بۆ گۆڕینی لاپەڕەکان
page = st.selectbox("بڕۆ بۆ لاپەڕەی:", ["🏠 سەرەکی", "🔮 پێشبینی AI", "📚 فێربوونی فۆرێکس"])


def _download(ticker: str, start: str) -> pd.DataFrame:
    df = yf.download(ticker, start=start, auto_adjust=False, progress=False)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    return df


# --- لاپەڕەی یەکەم: سەرەکی ---
if page == "🏠 سەرەکی":
    st.title("بەخێرهێیت بۆ سەکۆی زیرەکی فۆرێکس")
    st.write("لێرە دەتوانیت نوێترین نرخەکانی بازاڕ ببینی.")

    ticker = st.selectbox("دراوێک هەڵبژێرە:", ["EURUSD=X", "GBPUSD=X", "GC=F", "BTC-USD"])
    data = _download(ticker, "2024-01-01")

    fig = go.Figure(data=[go.Scatter(x=data.index, y=data['Close'], line=dict(color='#00fbff'))])
    fig.update_layout(title=f"نرخی ئێستای {ticker}", template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

# --- لاپەڕەی دووەم: پێشبینی ---
elif page == "🔮 پێشبینی AI":
    st.title("شیکاری و پێشبینی ورد")
    ticker = st.selectbox("دراوێک هەڵبژێرە بۆ پێشبینی:", ["EURUSD=X", "GC=F", "BTC-USD"])

    with st.spinner('AI خەریکی حیسابکردنە...'):
        data = _download(ticker, "2023-01-01")
        df_p = data.reset_index()[['Date', 'Close']].rename(columns={'Date':'ds', 'Close':'y'})
        m = Prophet(daily_seasonality=True)
        m.fit(df_p)
        future = m.make_future_dataframe(periods=30)
        forecast = m.predict(future)

        fig_f = go.Figure()
        fig_f.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], name="پێشبینی", line=dict(color='orange')))
        fig_f.update_layout(template="plotly_dark")
        st.plotly_chart(fig_f, use_container_width=True)

# --- لاپەڕەی سێیەم: فێربوون ---
elif page == "📚 فێربوونی فۆرێکس":
    st.title("وانەکانی فۆرێکس و ئابووری")
    st.markdown("""
    ### فۆرێکس چییە؟
    بازاڕی ئاڵوگۆڕی دراوە بیانییەکانە کە تێیدا دراوەکان بە جووت مامەڵەیان پێوە دەکرێت.
    
    * **PIP چییە؟** بچووکترین یەکەی گۆڕانکاری نرخە.
    * **RSI چییە؟** نیشاندەرێکە بۆ زانینی هێزی کڕین و فرۆشتن.
    """)
    st.info("ئەم بەشە دەتوانیت ڤیدیۆ یان کتێبی تێدا دابنێیت.")
