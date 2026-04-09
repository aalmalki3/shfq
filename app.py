import streamlit as st
import requests

# 1. إعداد الصفحة
st.set_page_config(page_title="شفق | مستقبل مهني واضح", page_icon="🌅", layout="centered")

# 2. هندسة التصميم (CSS المصحح)
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap" rel="stylesheet">
    <style>
    /* الإعدادات العامة */
    [data-testid="stAppViewContainer"] {
        font-family: 'Cairo', sans-serif;
        direction: RTL;
        text-align: right;
    }

    /* خلفية الشفق المتدرجة والمتحركة */
    .stApp {
        background: linear-gradient(-45deg, #E8D9C0, #F4D3C5, #F4C7A5, #A9CAD7, #2C4251, #0B1622);
        background-size: 400% 400%;
        animation: gradientAnimation 15s ease infinite;
    }

    @keyframes gradientAnimation {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* حاوية المحتوى البيضاء */
    .block-container {
        background-color: rgba(255, 255, 255, 0.94);
        border-radius: 25px;
        padding: 50px !important;
        box-shadow: 0 20px 50px rgba(0,0,0,0.15);
        margin-top: 20px;
        direction: RTL;
    }

    /* تنسيق العناوين والنصوص */
    h1, h2, h3, p, span, label, .stMarkdown {
        text-align: right !important;
        direction: RTL !important;
        color: #0B1622;
    }

    .stTitle {
        font-weight: 700;
        font-size: 2.8rem !important;
        margin-bottom: 0.5rem;
    }

    /* تحسين شكل منطقة الرفع */
    [data-testid="stFileUploadDropzone"] {
        border: 2px dashed #A9CAD7 !important;
        background-color: #F8F9FA !important;
        border-radius: 15px !important;
    }

    /* الزر الاحترافي */
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #2C4251, #0B1622);
        color: white !important;
        border: none;
        padding: 12px 0;
        font-size: 1.2rem;
        font-weight: 700;
        border-radius: 12px;
        transition: 0.3s;
    }
    
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    </style>
    """, unsafe_allow_html=True)

# 3. عرض الشعار
col1, col2, col3 = st.columns([1, 1.5, 1])
with col2:
    try:
        st.image("assets/shfq.jpg", use_container_width=True)
    except:
        st.write("✨ شفق | SHFQ")

# 4. النصوص التعريفية
st.markdown("<h1 class='stTitle'>شفق | SHFQ</h1>", unsafe_allow_html=True)
st.markdown("<p style='font-size:1.2rem; color:#2C4251;'>نورٌ هادئ لمستقبلٍ مهنيٍ واضح. ارفع سيرتك الذاتية الآن لنبدأ رحلة التحليل بمنهجية SNA.</p>", unsafe_allow_html=True)
st.write("---")

# 5. منطقة العمليات
uploaded_file = st.file_uploader("يرجى اختيار ملف السيرة الذاتية (PDF)", type=["pdf"])

# جلب الرابط من Secrets
MAKE_URL = st.secrets.get("MAKE_WEBHOOK_URL", "")

if uploaded_file is not None:
    st.success("✅ تم استقبال الملف بنجاح.")
    
    if st.button("بدء التحليل الاستراتيجي"):
        if not MAKE_URL:
            st.error("⚠️ يرجى ضبط MAKE_WEBHOOK_URL في إعدادات Secrets.")
        else:
            with st.spinner('جاري النقل والمعالجة...'):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                    payload = {"filename": uploaded_file.name}
                    response = requests.post(MAKE_URL, data=payload, files=files)
                    
                    if response.status_code == 200:
                        st.balloons()
                        st.markdown("<div style='text-align:center; padding:15px; background-color:#d4edda; border-radius:10px; color:#155724;'>✨ تمت العملية! فريق شفق سيقوم بالمراجعة، ترقب التحديث في نوشن.</div>", unsafe_allow_html=True)
                    else:
                        st.error(f"خطأ في الاتصال: {response.status_code}")
                except Exception as e:
                    st.error(f"حدث خطأ: {e}")

st.markdown("<br><p style='text-align:center; opacity:0.6;'>جميع الحقوق محفوظة - شفق 2026</p>", unsafe_allow_html=True)
