import streamlit as st
import streamlit.components.v1 as components
from notion_client import Client
import time

# 1. إعداد الصفحة
st.set_page_config(page_title="شفق | SHFQ", page_icon="🌅", layout="centered")

# --- 2. دالة جلب البيانات (تأكيد الاتصال الفعلي بنوشن) ---
def check_report_status(email, access_code):
    try:
        # إنشاء الاتصال في كل مرة لضمان عدم وجود Cache قديم
        notion = Client(auth=st.secrets["NOTION_TOKEN"])
        database_id = st.secrets["NOTION_DATABASE_ID"]
        
        # البحث في نوشن
        response = notion.databases.query(
            database_id=database_id,
            filter={
                "and": [
                    {"property": "Email", "email": {"equals": email.strip().lower()}},
                    {"property": "Access Code", "number": {"equals": int(access_code)}}
                ]
            }
        )
        
        results = response.get("results", [])

        # إذا كانت القائمة فارغة تماماً من نوشن
        if not results:
            return "NOT_FOUND", None
            
        # فحص النتائج يدوياً لضمان عدم وجود أسطر وهمية
        for res in results:
            props = res.get("properties", {})
            
            # استخراج القيم الحقيقية
            n_email = props.get("Email", {}).get("email")
            n_code = props.get("Access Code", {}).get("number")
            # التحقق من وجود "عنوان" أو "اسم" في الصفحة لضمان أنها ليست مسودة فارغة
            n_name_list = props.get("Full Name", {}).get("title", [])
            n_name = n_name_list[0].get("plain_text") if n_name_list else None

            # شرط صارم جداً للمطابقة
            if n_email and n_email.strip().lower() == email.strip().lower() and \
               n_code == int(access_code) and \
               n_name is not None:
                
                # جلب محتوى التقرير (Blocks)
                page_id = res["id"]
                blocks = notion.blocks.children.list(block_id=page_id).get("results", [])
                
                report_text = ""
                for block in blocks:
                    if block["type"] == "paragraph":
                        rich = block["paragraph"]["rich_text"]
                        if rich:
                            report_text += rich[0]["plain_text"] + "\n\n"
                
                if report_text.strip():
                    return "READY", report_text
                else:
                    return "PROCESSING", None

        return "NOT_FOUND", None

    except Exception as e:
        # في حال وجود خطأ في التوكن أو قاعدة البيانات سيظهر هنا
        return "ERROR", str(e)

# --- 3. التنسيق البصري (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [data-testid="stAppViewContainer"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background: linear-gradient(-45deg, #E8D9C0, #F4D3C5, #F4C7A5, #A9CAD7, #2C4251, #0B1622); background-size: 400% 400%; animation: gradient 15s ease infinite; }
    .block-container { background-color: rgba(255, 255, 255, 0.95); border-radius: 20px; padding: 40px !important; box-shadow: 0 10px 30px rgba(0,0,0,0.1); margin-top: 30px; }
    #MainMenu, footer, header { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

# 4. منطق الصفحات
if "page" not in st.session_state:
    st.session_state.page = "main"

if st.session_state.page == "main":
    st.markdown("<h1 style='text-align:center;'>🌅 شفق | SHFQ</h1>", unsafe_allow_html=True)
    tally_embed = '<iframe data-tally-src="https://tally.so/embed/lb7DVN?alignLeft=1&hideTitle=1&transparentBackground=1&dynamicHeight=1" loading="lazy" width="100%" height="1000" frameborder="0"></iframe><script src="https://tally.so/widgets/embed.js"></script>'
    components.html(tally_embed, height=1000, scrolling=True)
    if st.button("🔍 استخراج تقرير سابق", use_container_width=True):
        st.session_state.page = "query_page"
        st.rerun()

elif st.session_state.page == "query_page":
    st.markdown("<h2 style='text-align:center;'>🛡️ نظام التحقق الذكي</h2>", unsafe_allow_html=True)
    email_in = st.text_input("البريد الإلكتروني المعتمد:")
    code_in = st.text_input("كود الاستعلام (4 أرقام):", type="password")
    
    if st.button("التحقق من سجلات نوشن ⚡", use_container_width=True):
        if email_in and code_in:
            with st.spinner("يتم الاتصال بقاعدة بيانات نوشن الآن..."):
                time.sleep(1.5) # تأخير اصطناعي لضمان تجربة مستخدم واضحة
                status, data = check_report_status(email_in, code_in)
                
                if status == "NOT_FOUND":
                    st.error("❌ فشل التحقق: لم نجد أي سجل حقيقي يطابق هذه البيانات.")
                    st.session_state.can_analyze = False
                elif status == "ERROR":
                    st.warning(f"⚠️ خطأ في الاتصال: {data}")
                else:
                    st.success("✅ متصل: تم العثور على سجلّك ومطابقة بياناتك بنجاح.")
                    st.session_state.user_email = email_in
                    st.session_state.user_code = code_in
                    st.session_state.can_analyze = True
        else:
            st.warning("يرجى إدخال البيانات المطلوبة.")

    if st.session_state.get("can_analyze"):
        if st.button("بدء المعالجة والاستخراج 🚀", use_container_width=True):
            st.session_state.page = "waiting"
            st.rerun()

elif st.session_state.page == "waiting":
    st.markdown("<h2 style='text-align:center;'>جاري معالجة البيانات...</h2>", unsafe_allow_html=True)
    progress_bar = st.progress(0)
    for p in range(1, 101):
        if p % 20 == 0:
            status, data = check_report_status(st.session_state.user_email, st.session_state.user_code)
            if status == "READY":
                st.session_state.final_report = data
                st.session_state.page = "result"
                st.rerun()
        progress_bar.progress(p)
        time.sleep(0.3)
    st.info("التقرير لم يجهز بعد. اضغط تحديث.")
    if st.button("تحديث 🔄"): st.rerun()

elif st.session_state.page == "result":
    st.success("✅ تم الاستخراج بنجاح")
    st.markdown(st.session_state.final_report)
    if st.button("بحث جديد 🔄"):
        st.session_state.can_analyze = False
        st.session_state.page = "query_page"
        st.rerun()
