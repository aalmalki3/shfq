import streamlit as st
import requests

# 1. إعداد الصفحة
st.set_page_config(page_title="شفق | SHFQ", page_icon="🌅", layout="centered")

# 2. تطبيق هوية شفق البصرية (التدرج الكامل)
st.markdown("""
    <style>
    /* التدرج اللوني للخلفية باستخدام ألوان شفق الستة */
    .stApp {
        background: linear-gradient(180deg, 
            #E8D9C0 0%, 
            #F4D3C5 20%, 
            #F4C7A5 40%, 
            #A9CAD7 60%, 
            #2C4251 80%, 
            #0B1622 100%);
        background-attachment: fixed;
    }
    
    /* تنسيق الحاوية الرئيسية */
    .block-container {
        background-color: rgba(255, 255, 255, 0.85); /* خلفية بيضاء شفافة للنصوص */
        border-radius: 20px;
        padding: 40px !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin-top: 50px;
    }

    .stTitle {
        color: #0B1622 !important;
        font-family: 'Arial';
        text-align: center;
        font-weight: bold;
    }
    
    .stSubheader {
        color: #2C4251 !important;
        text-align: center;
    }

    /* تنسيق زر الرفع */
    .stFileUploader {
        padding: 20px;
    }
    
    /* زر الإرسال */
    .stButton>button {
        width: 100%;
        background-color: #0B1622;
        color: white;
        border: none;
        padding: 10px;
        border-radius: 8px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. عرض الشعار (تأكد أن الملف موجود في مسار assets/shfq.jpg)
# إذا كان الشعار في المجلد الرئيسي، احذف كلمة assets/
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    try:
        st.image("assets/shfq.jpg", use_container_width=True)
    except:
        st.write("⚠️ يرجى رفع ملف الشعار في مجلد assets")

# 4. العنوان والترحيب
st.title("شفق | SHFQ")
st.subheader("نورٌ هادئ، لمستقبلٍ مهنيٍ واضح")
st.write("---")

# 5. واجهة الرفع والربط بميك
uploaded_file = st.file_uploader("ارفع سيرتك الذاتية لتحليلها بمنهجية SNA", type=["pdf"])
MAKE_URL = st.secrets.get("MAKE_WEBHOOK_URL", "ضع_رابط_ميك_هنا")

if uploaded_file is not None:
    st.success("✅ تم استلام الملف بنجاح!")
    
    if st.button("إرسال للتحليل الاستراتيجي"):
        with st.spinner('جاري نقل البيانات إلى محرك شفق...'):
            try:
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                payload = {"filename": uploaded_file.name}
                response = requests.post(MAKE_URL, data=payload, files=files)
                
                if response.status_code == 200:
                    st.balloons()
                    st.success("تمت العملية! راجع قاعدة بيانات نوشن الآن.")
                else:
                    st.error(f"مشكلة في الاتصال بميك: {response.status_code}")
            except Exception as e:
                st.error(f"خطأ تقني: {e}")
