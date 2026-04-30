import streamlit as st
from streamlit_gsheets import GSheetsConnection

# دروستکردنی پەیوەندی
conn = st.connection("gsheets", type=GSheetsConnection)

# خوێندنەوەی هەموو داتاکان بەبێ ناونانی Worksheet
try:
    df = conn.read(ttl=0)
    
    # دۆزینەوەی زانیاری بەکارهێنەر
    user_row = df[df['Username'] == 'Test_user'].iloc[0]
    balance = float(user_row['Wallet_balance'])

    st.sidebar.title("💰 هەژماری من")
    st.sidebar.metric("باڵانسی ئێستا", f"${balance:,.2f}")

    # بەشی بارگاویکردن
    with st.sidebar.expander("💳 بارگاویکردنی واڵێت"):
        st.write("بۆ بارگاویکردن، وێنەی وەسڵ بنێرە بۆ تێلیگرام:")
        st.link_button("🚀 ناردنی وەسڵ", "https://t.me/YOUR_USERNAME")

    st.title("📈 سەکۆی وەبەرهێنان")
    st.write(f"بەخێربێیت **Test_user**")
    
    amount = st.number_input("بڕی وەبەرهێنان ($)", min_value=1.0, max_value=balance)
    if st.button("ئێستا بکڕە"):
        st.balloons()
        st.success("داواکارییەکەت وەرگیرا")

except Exception as e:
    st.error("کێشەیەک لە پەیوەندی هەیە. تکایە دڵنیابە لینکی Google Sheets لە بەشی Secrets ڕاستە.")
