import streamlit as st
import requests

# 1. إعداد الصفحة (نفس الكود الجميل الخاص بك)
st.set_page_config(page_title="شفق | SHFQ", page_icon="🌅", layout="centered")

# 2. تطبيق هوية شفق البصرية (الألوان التي اعتمدناها)
st.markdown("""
    <style>
    .stApp {
        background-color: #ffffff;
    }
    .stTitle {
        color: #0B1622; /* الكحلي الداكن */
        font-family: 'Arial';
        text-align: center;
        font-weight: bold;
    }
    .stSubheader {
        color: #2C4251; /* لون الجبال في الشفق */
        text-align: center;
    }
    /* تنسيق زر الرفع */
    .stFileUploader section {
        background-color: #E8D9C0; /* لون السماء الفاتح */
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. العنوان والترحيب
st.title("شفق | SHFQ")
st.subheader("نورٌ هادئ، لمستقبلٍ مهنيٍ واضح")
st.write("---")

# 4. واجهة الرفع
uploaded_file = st.file_uploader("ارفع سيرتك الذاتية لتحليلها بمنهجية SNA (PDF فقط)", type=["pdf"])

# رابط ميك (تأكد من وضعه في Secrets أو استبداله هنا مباشرة)
# أنصح بوضعه في Secrets باسم MAKE_WEBHOOK_URL
MAKE_URL = st.secrets.get("MAKE_WEBHOOK_URL", "ضع_رابط_ميك_هنا")

if uploaded_file is not None:
    st.success("تم استلام الملف بنجاح!")
    
    # زر تأكيد الإرسال للتحليل
    if st.button("إرسال للتحليل الاستراتيجي"):
        with st.spinner('جاري نقل البيانات إلى محرك شفق...'):
            try:
                # تجهيز البيانات للإرسال لميك
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                payload = {"filename": uploaded_file.name}
                
                # إرسال الطلب لميك
                response = requests.post(MAKE_URL, data=payload, files=files)
                
                if response.status_code == 200:
                    st.balloons()
                    st.success("تمت العملية! سيرتك الآن في عهدة شفق، وستجد التحديث في نوشن فوراً.")
                else:
                    st.error(f"حدثت مشكلة في الاتصال (كود: {response.status_code})")
            except Exception as e:
                st.error(f"عذراً، حدث خطأ تقني: {e}")

st.write("---")
st.caption("جميع الحقوق محفوظة - مشروع شفق التطوعي 2026")
