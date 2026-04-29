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
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from datetime import datetime

# ڕێکخستنی سەرەتایی لاپەڕە
st.set_page_config(page_title="Forex & Crypto AI", layout="wide")

st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    h1 {
        color: #00ffcc;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 سەەکۆی پێشبینیکردنی زیرەک (Forex, Gold, Crypto)")
st.write("---")

# لیستی دراوە نوێیەکان
symbol_map = {
    "EUR/USD (یۆرۆ بەرامبەر دۆلار)": "EURUSD=X",
    "GBP/USD (پاوەند بەرامبەر دۆلار)": "GBPUSD=X",
    "Gold (زێڕ)": "GC=F",
    "Bitcoin (بیتکۆین)": "BTC-USD",
    "Crude Oil (نەوتی خاو)": "CL=F",
    "USD/JPY (دۆلار بەرامبەر یەن)": "USDJPY=X",
    "Ethereum (ئیسێریۆم)": "ETH-USD"
}

# هەڵبژاردنی دراو لەلایەن بەکارهێنەرەوە
selected_display = st.sidebar.selectbox("دراوێک یان کاڵایەک هەڵبژێرە:", list(symbol_map.keys()))
symbol = symbol_map[selected_display]

# ماوەی کاتی
period = st.sidebar.slider("ماوەی داتاکان (بە مانگ):", 1, 24, 6)

# هێنانی داتا لە Yahoo Finance
@st.cache_data
def load_data(ticker, months):
    data = yf.download(ticker, period=f"{months}mo", interval="1d")
    return data

data = load_data(symbol, period)

if not data.empty:
    # نیشاندانی نرخی ئێستا
    current_price = data['Close'].iloc[-1]
    st.metric(label=f"نرخی ئێستای {selected_display}", value=f"{current_price:,.2f}")

    # دروستکردنی گرافیکی نرخەکان
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='نرخی ڕاستەقینە', line=dict(color='#00ffcc')))
    
    fig.update_layout(title=f"گرافیکی نرخی {selected_display}", template="plotly_dark", xaxis_title="کاتی", yaxis_title="نرخ")
    st.plotly_chart(fig, use_container_pro_寬=True)

    # بەشی پێشبینی بە ژیریی دەستکرد
    st.write("---")
    st.subheader("🤖 پێشبینی زیرەک بۆ ٣٠ ڕۆژی داهاتوو")
    
    if st.button("دەستپێکردنی شیکردنەوە و پێشبینی"):
        with st.spinner('خەریکی شیکردنەوەی داتاکانم...'):
            # مۆدێلی Exponential Smoothing بۆ پێشبینی
            model = ExponentialSmoothing(data['Close'], trend='add', seasonal=None)
            model_fit = model.fit()
            forecast = model_fit.forecast(30)
            
            # دروستکردنی کاتی داهاتوو بۆ گرافیکەکە
            last_date = data.index[-1]
            forecast_dates = pd.date_range(start=last_date, periods=31)[1:]

            # نیشاندانی پێشبینی لەسەر گرافیک
            fig_forecast = go.Figure()
            fig_forecast.add_trace(go.Scatter(x=data.index[-50:], y=data['Close'].iloc[-50:], name='نرخی کۆتایی', line=dict(color='#00ffcc')))
            fig_forecast.add_trace(go.Scatter(x=forecast_dates, y=forecast, name='پێشبینی AI', line=dict(color='#ff9900', dash='dash')))
            
            fig_forecast.update_layout(title="پێشبینی ئاراستەی نرخ", template="plotly_dark")
            st.plotly_chart(fig_forecast, use_container_width=True)
            
            st.success("پێشبینییەکە تەواو بوو! هێڵە پچڕپچڕە پرتەقاڵییەکە ئاراستەی چاوەڕوانکراو نیشان دەدات.")
else:
    st.error("نەتوانرا داتاکان بهێنرێت. تکایە دواتر تاقی بکەرەوە.")

st.sidebar.write("---")
st.sidebar.info("ئەم پڕۆژەیە وەک نموونەیەک بۆ فێربوون دروست کراوە و نابێت وەک ئامۆژگاری دارایی بەکاربهێنرێت.")
