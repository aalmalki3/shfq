import streamlit as st
import requests

# إعداد الصفحة
st.set_page_config(page_title="شفق | SHFQ", page_icon="🌅", layout="centered")

# التنسيق المحسن (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Cairo', sans-serif;
        direction: RTL;
        text-align: right;
    }

    .stApp {
        background: linear-gradient(-45deg, #E8D9C0, #F4D3C5, #F4C7A5, #A9CAD7, #2C4251, #0B1622);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }

    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .block-container {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 40px !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin-top: 30px;
    }

    /* إصلاح لون نص الزر وجعله مقروءاً */
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #2C4251, #0B1622) !important;
        color: #ffffff !important; /* نص أبيض ناصع */
        border-radius: 12px !important;
        border: none !important;
        padding: 15px !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
    }
    
    .stButton>button p {
        color: #ffffff !important; /* تأكيد اللون الأبيض داخل العناصر الفرعية للزر */
    }
    </style>
""", unsafe_allow_html=True)

# محتوى الصفحة
col1, col2, col3 = st.columns([1, 1.5, 1])
with col2:
    try:
        st.image("assets/shfq.jpg", use_container_width=True)
    except:
        st.markdown("<h2 style='text-align:center;'>🌅 شفق</h2>", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center; color:#0B1622;'>شفق | SHFQ</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#2C4251;'>نحلل سيرتك الذاتية لنرسم لك مستقبلاً مهنياً واضحاً.</p>", unsafe_allow_html=True)
st.write("---")

# منطقة الرفع
uploaded_file = st.file_uploader("ارفع ملف السيرة الذاتية (PDF)", type=["pdf"])

# جلب رابط ميك (تأكد من كتابة الاسم تماماً كما في Secrets)
# ملاحظة: إذا كنت تضعه في Secrets، تأكد من الضغط على Save هناك.
MAKE_URL = st.secrets.get("MAKE_WEBHOOK_URL")

if uploaded_file is not None:
    st.success("✅ تم استلام الملف")
    if st.button("بدء التحليل الاستراتيجي"):
        if not MAKE_URL:
            st.warning("⚠️ يرجى التأكد من إضافة MAKE_WEBHOOK_URL في إعدادات Secrets في Streamlit Cloud")
        else:
            with st.spinner('جاري نقل البيانات إلى ميك...'):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                    res = requests.post(MAKE_URL, data={"filename": uploaded_file.name}, files=files)
                    if res.status_code == 200:
                        st.balloons()
                        st.info("✨ تم بنجاح! فريق شفق سيهتم بالباقي.")
                    else:
                        st.error(f"حدث خطأ في الاتصال بميك: {res.status_code}")
                except Exception as e:
                    st.error(f"حدث خطأ تقني: {e}")

st.markdown("<br><p style='text-align:center; opacity:0.5; color:#0B1622;'>شفق 2026</p>", unsafe_allow_html=True)
