import streamlit as st

# إعداد الصفحة
st.set_page_config(page_title="شفق | SHFQ", page_icon="🌅", layout="centered")

# تطبيق هوية شفق البصرية
st.markdown("""
    <style>
    .main {
        background-color: #ffffff;
    }
    .stTitle {
        color: #0B1622;
        font-family: 'Arial';
        text-align: center;
    }
    .stSubheader {
        color: #2C4251;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# العنوان والترحيب
st.title("شفق | SHFQ")
st.subheader("نورٌ هادئ، لمستقبلٍ مهنيٍ واضح")

st.write("---")

# واجهة الرفع
uploaded_file = st.file_uploader("ارفع سيرتك الذاتية لتحليلها بمنهجية SNA (PDF فقط)", type=["pdf"])

if uploaded_file is not None:
    st.info("تم استلام الملف بنجاح. نحن بصدد تفعيل محرك التحليل الذكي...")
