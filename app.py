import streamlit as st
import requests

# 1. إعداد الصفحة الأساسي
st.set_page_config(page_title="شفق | SHFQ", page_icon="🌅", layout="centered")

# 2. حقن التنسيق بطريقة الطبقات (لضمان عدم ظهور الأكواد كنصوص)
def local_css():
    st.markdown("""
        <style>
        /* إعدادات الاتجاه والخط */
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
        
        html, body, [data-testid="stAppViewContainer"] {
            font-family: 'Cairo', sans-serif;
            direction: RTL;
            text-align: right;
        }

        /* خلفية الشفق المتدرجة */
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

        /* الحاوية البيضاء الوسطى */
        .block-container {
            background-color: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 40px !important;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            margin-top: 30px;
        }

        /* تنسيق النصوص */
        h1, h2, h3, p, span, label {
            text-align: right !important;
            direction: RTL !important;
            color: #0B1622 !important;
        }

        /* زر الإرسال */
        .stButton>button {
            width: 100%;
            background: linear-gradient(to left, #0B1622, #2C4251);
            color: white !important;
            border-radius: 10px;
            border: none;
            padding: 10px;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)

local_css()

# 3. محتوى الصفحة
col1, col2, col3 = st.columns([1, 1.5, 1])
with col2:
    try:
        st.image("assets/shfq.jpg", use_container_width=True)
    except:
        st.markdown("<h2 style='text-align:center;'>🌅 شفق</h2>", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;'>شفق | SHFQ</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:1.1rem;'>نحلل سيرتك الذاتية لنرسم لك مستقبلاً مهنياً واضحاً.</p>", unsafe_allow_html=True)
st.write("---")

# 4. منطقة الرفع والعمليات
uploaded_file = st.file_uploader("ارفع ملف السيرة الذاتية (PDF)", type=["pdf"])
MAKE_URL = st.secrets.get("MAKE_WEBHOOK_URL", "")

if uploaded_file is not None:
    st.success("✅ تم استلام الملف")
    if st.button("بدء التحليل الاستراتيجي"):
        if not MAKE_URL:
            st.warning("يرجى التأكد من إضافة الرابط في Secrets")
        else:
            with st.spinner('جاري النقل...'):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                    res = requests.post(MAKE_URL, data={"filename": uploaded_file.name}, files=files)
                    if res.status_code == 200:
                        st.balloons()
                        st.info("تم بنجاح، فريق شفق سيهتم بالباقي.")
                except:
                    st.error("حدث خطأ في الاتصال.")

st.markdown("<br><p style='text-align:center; opacity:0.5;'>شفق 2026</p>", unsafe_allow_html=True)
