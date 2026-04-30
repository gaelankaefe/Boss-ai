import streamlit as st
import pandas as pd

# 1. ڕێکخستنی شاشە و دیزاینی ئەپ
st.set_page_config(page_title="Boss Market", page_icon="🛒", layout="centered")

# 2. دروستکردنی داتای کاڵاکان و میمۆری ئەپەکە
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'balance' not in st.session_state:
    st.session_state.balance = 500.0  # باڵانسی سەرەتایی بەکارهێنەر

# داتای کاڵاکان (دەتوانیت زیادیان بکەیت)
products = [
    {"id": 1, "name": "iPhone 15 Pro", "price": 999, "image": "📱", "desc": "نوێترین مۆبایلی ئەپڵ"},
    {"id": 2, "name": "AirPods Pro 2", "price": 249, "image": "🎧", "desc": "باشترین جۆری بیستۆک"},
    {"id": 3, "name": "MacBook Air M3", "price": 1299, "image": "💻", "desc": "بۆ کاری دیزاین و پرۆگرامینگ"},
    {"id": 4, "name": "Apple Watch S9", "price": 399, "image": "⌚", "desc": "کاتژمێری زیرەکی وەرزشی"}
]

# 3. دیزاینی CSS بۆ ئەوەی وەک ئەپ دەربکەوێت
st.markdown("""
    <style>
    header {visibility: hidden;}
    .main { background-color: #f5f5f5; }
    .product-card {
        background-color: white;
        padding: 15px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 10px;
        text-align: center;
    }
    .stButton > button {
        border-radius: 10px;
        background-color: #007bff;
        color: white;
        width: 100%;
    }
    .bottom-nav {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: white;
        padding: 10px;
        display: flex;
        justify-content: space-around;
        border-top: 1px solid #ddd;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. دروستکردنی Navigation (مێنیوی گۆڕینی لاپەڕە)
menu = st.sidebar.selectbox("بڕۆ بۆ لاپەڕەی:", ["🛍️ فرۆشگا", "🛒 عارەبانەی کڕین", "👤 پڕۆفایل و باڵانس"])

# ---------------- لاپەڕەی فرۆشگا ----------------
if menu == "🛍️ فرۆشگا":
    st.title("Boss Market 🛒")
    st.write(f"باڵانسی تۆ: **${st.session_state.balance}**")
    st.markdown("---")
    
    # نیشاندانی کاڵاکان بە دوو ستوون
    col1, col2 = st.columns(2)
    for i, product in enumerate(products):
        target_col = col1 if i % 2 == 0 else col2
        with target_col:
            st.markdown(f"""
                <div class="product-card">
                    <h1 style="font-size: 50px;">{product['image']}</h1>
                    <h3>{product['name']}</h3>
                    <p style="color: green; font-weight: bold;">${product['price']}</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"زیادکردن بۆ عارەبانە", key=f"btn_{product['id']}"):
                st.session_state.cart.append(product)
                st.toast(f"{product['name']} زیادکرا!")

# ---------------- لاپەڕەی عارەبانە ----------------
elif menu == "🛒 عارەبانەی کڕین":
    st.title("عارەبانەی کڕین 🛒")
    if not st.session_state.cart:
        st.info("عارەبانەکەت بەتاڵە.")
    else:
        total_price = 0
        for item in st.session_state.cart:
            col_img, col_txt = st.columns([1, 3])
            col_img.write(f"### {item['image']}")
            col_txt.write(f"**{item['name']}** - ${item['price']}")
            total_price += item['price']
        
        st.markdown("---")
        st.write(f"### کۆی گشتی: ${total_price}")
        
        if st.button("✅ کۆتاییهێنان بە کڕین"):
            if st.session_state.balance >= total_price:
                st.session_state.balance -= total_price
                st.session_state.cart = []
                st.balloons()
                st.success("کڕینەکەت بە سەرکەوتوویی ئەنجامدرا!")
            else:
                st.error("باڵانسەکەت بەش ناکات!")

# ---------------- لاپەڕەی پڕۆفایل ----------------
elif menu == "👤 پڕۆفایل و باڵانس":
    st.title("پڕۆفایلی بەکارهێنەر 👤")
    st.markdown(f"""
        <div style="background-color: white; padding: 20px; border-radius: 15px; text-align: center;">
            <img src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png" width="100">
            <h2>Test_user</h2>
            <h1 style="color: #007bff;">${st.session_state.balance}</h1>
            <p>باڵانسی بەردەست</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📥 بارگاویکردنەوەی هەژمار")
    st.code("TMR7DR8EtB3aNp2inXt8zfTVsXbHm9dv8M")
    st.write("پارە بنێرە بۆ ئەم واڵێتە و وەسڵەکە بنێرە بۆ تێلیگرام.")
    st.link_button("🚀 ناردنی وەسڵ", "https://t.me/YOUR_USERNAME")

