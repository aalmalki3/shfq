import streamlit as st
import requests

# 1. إعداد الصفحة مع دعم اللغة العربية في العنوان
st.set_page_config(page_title="شفق | مستقبل مهني واضح", page_icon="🌅", layout="centered")

# 2. هندسة التصميم المتقدمة (CSS) لرفع الجودة بنسبة 80%
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap" rel="stylesheet">
    <style>
    /* إعدادات الخط والاتجاه العام */
    html, body, [data-testid="stAppViewContainer"], .main {
        font-family: 'Cairo', sans-serif;
        direction: RTL;
        text-align: right;
    }

    /* خلفية الشفق المتحركة */
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

    /* حاوية المحتوى الرئيسية */
    .block-container {
        background-color: rgba(255, 255, 255, 0.92);
        border-radius: 25px;
        padding: 50px !important;
        box-shadow: 0 20px 50px rgba(0,0,0,0.2);
        margin-top: 30px;
        max-width: 800px;
    }

    /* تنسيق النصوص RTL */
    h1, h2, h3, p, span, label {
        text-align: right !important;
        direction: RTL !important;
    }

    .stTitle {
        color: #0B1622;
        font-size: 2.5rem !important;
        font-weight: 700;
        margin-bottom: 10px;
    }

    .stSubheader {
        color: #2C4251;
        font-weight: 400;
        margin-bottom: 30px;
    }

    /* تحسين شكل منطقة رفع الملفات */
    [data-testid="stFileUploadDropzone"] {
        border: 2px dashed #A9CAD7;
        background-color: #fcfcfc;
        border-radius: 15px;
        padding: 20px;
    }

    /* تنسيق زر الإرسال الاحترافي */
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #2C4251 0%, #0B1622 100%);
        color: white !important;
        border: none;
        padding: 15px 30px;
        font-size: 1.2rem;
        font-weight: 700;
        border-radius: 12px;
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.3);
        background: linear-gradient(90deg, #0B1622 0%, #2C4251 100%);
    }

    /* إخفاء القوائم الافتراضية لزيادة الخصوصية */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 3. تنظيم العناصر البصرية
col1, col2, col3 = st.columns([1, 1.5, 1])
with col2:
    try:
        # استخدام الشعار الحالي shfq.jpg
        st.image("assets/shfq.jpg", use_container_width=True)
    except:
        st.info("نحن الآن في عهدة شفق")

# 4. المحتوى الرئيسي باللغة العربية
st.markdown("<h1 class='stTitle'>شفق | SHFQ</h1>", unsafe_allow_html=True)
st.markdown("<h3 class='stSubheader'>نورٌ هادئ لمستقبلٍ مهنيٍ واضح. نحلل سيرتك بمنهجية SNA لنرسم لك طريق النجاح.</h3>", unsafe_allow_html=True)

st.markdown("---")

# 5. منطقة العمليات
with st.container():
    uploaded_file = st.file_uploader("يرجى سحب وإفلات السيرة الذاتية هنا (صيغة PDF)", type=["pdf"])
    
    # جلب الرابط من Secrets
    MAKE_URL = st.secrets.get("MAKE_WEBHOOK_URL", "")

    if uploaded_file is not None:
        st.success("✅ تم استقبال الملف بنجاح، أنت الآن على بعد خطوة واحدة.")
        
        if st.button("بدء التحليل الاستراتيجي"):
            if not MAKE_URL:
                st.error("⚠️ خطأ: لم يتم ضبط رابط الأتمتة (Webhook) في الإعدادات.")
            else:
                with st.spinner('جاري نقل بياناتك بأمان إلى محرك شفق...'):
                    try:
                        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                        payload = {"filename": uploaded_file.name}
                        response = requests.post(MAKE_URL, data=payload, files=files)
                        
                        if response.status_code == 200:
                            st.balloons()
                            st.markdown("<div style='text-align:center; padding:20px; background-color:#d4edda; border-radius:10px; color:#155724;'>✨ تمت العملية بنجاح! فريق شفق سيعمل على مراجعة ملفك، تابع تحديثاتك في نوشن.</div>", unsafe_allow_html=True)
                        else:
                            st.error(f"حدث خلل في الاتصال بميك (كود: {response.status_code})")
                    except Exception as e:
                        st.error(f"خطأ تقني: {e}")

# 6. تذييل الصفحة
st.markdown("<br><p style='text-align: center; color: #777;'>جميع الحقوق محفوظة لمبادرة شفق 2026</p>", unsafe_allow_html=True)
