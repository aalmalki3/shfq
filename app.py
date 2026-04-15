import streamlit as st
import streamlit.components.v1 as components
from notion_client import Client
import time

# 1. إعداد الصفحة (يجب أن يكون أول أمر برمي)
st.set_page_config(page_title="شفق | SHFQ", page_icon="🌅", layout="centered")

# --- 2. دالة جلب البيانات من نوشن (نسخة صارمة) ---
def check_report_status(email, access_code):
    try:
        notion = Client(auth=st.secrets["NOTION_TOKEN"])
        database_id = st.secrets["NOTION_DATABASE_ID"]
        
        # استعلام يبحث عن تطابق الإيميل والكود
        query = notion.databases.query(
            database_id=database_id,
            filter={
                "and": [
                    {"property": "Email", "email": {"equals": email}},
                    {"property": "Access Code", "number": {"equals": int(access_code)}}
                ]
            }
        )
        
        results = query.get("results")
        
        # فلترة النتائج للتأكد من أنها ليست أسطر فارغة في نوشن
        valid_results = []
        for res in results:
            properties = res.get("properties", {})
            # التأكد من أن حقل الإيميل يحتوي على القيمة المطلوبة فعلياً
            email_prop = properties.get("Email", {}).get("email")
            if email_prop and email_prop.lower() == email.lower():
                valid_results.append(res)

        if not valid_results:
            return "NOT_FOUND", None
            
        page_id = valid_results[0]["id"]
        # جلب محتوى الصفحة (Blocks)
        blocks = notion.blocks.children.list(block_id=page_id)
        
        # إذا كانت الصفحة موجودة ولكنها فارغة من المحتوى
        if len(blocks.get("results")) == 0:
            return "PROCESSING", None
            
        report_text = ""
        for block in blocks.get("results"):
            if block["type"] == "paragraph":
                rich_text = block["paragraph"]["rich_text"]
                if rich_text:
                    report_text += rich_text[0]["plain_text"] + "\n\n"
        
        # إذا وجدنا السجل ولكن لم يكتب فيه نص بعد
        if not report_text.strip():
            return "PROCESSING", None
            
        return "READY", report_text
    except Exception:
        return "ERROR", None

# --- 3. تهيئة حالة الصفحة (Session State) ---
if "page" not in st.session_state:
    params = st.query_params
    if params.get("action") == "query":
        st.session_state.page = "query_page"
    else:
        st.session_state.page = "main"

if "can_start_analysis" not in st.session_state:
    st.session_state.can_start_analysis = False

# --- 4. التنسيق البصري (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [data-testid="stAppViewContainer"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background: linear-gradient(-45deg, #E8D9C0, #F4D3C5, #F4C7A5, #A9CAD7, #2C4251, #0B1622); background-size: 400% 400%; animation: gradient 15s ease infinite; }
    @keyframes gradient { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
    .block-container { background-color: rgba(255, 255, 255, 0.95); border-radius: 20px; padding: 40px !important; box-shadow: 0 10px 30px rgba(0,0,0,0.1); margin-top: 30px; }
    .stTitle { font-weight: 700; color: #0B1622; text-align: center; }
    #MainMenu, footer, header { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

# عرض الشعار
col1, col2, col3 = st.columns([1, 1.5, 1])
with col2:
    try: st.image("assets/shfq.jpg", use_container_width=True)
    except: st.markdown("<h2 style='text-align:center;'>🌅 شفق</h2>", unsafe_allow_html=True)

# --- 5. منطق الصفحات ---

# أ. الصفحة الرئيسية (النموذج)
if st.session_state.page == "main":
    st.markdown("<h1 class='stTitle'>مرحباً بك في شفق</h1>", unsafe_allow_html=True)
    tally_embed_html = '<iframe data-tally-src="https://tally.so/embed/lb7DVN?alignLeft=1&hideTitle=1&transparentBackground=1&dynamicHeight=1" loading="lazy" width="100%" height="1000" frameborder="0" title="بنك السير الذاتية"></iframe><script src="https://tally.so/widgets/embed.js"></script>'
    components.html(tally_embed_html, height=1000, scrolling=True)
    st.write("---")
    if st.button("🔍 استخراج تقرير سابق", use_container_width=True):
        st.session_state.page = "query_page"
        st.rerun()

# ب. صفحة الاستعلام والتحقق الصارم
elif st.session_state.page == "query_page":
    st.markdown("<h2 class='stTitle'>🛡️ التحقق من سجلات شفق</h2>", unsafe_allow_html=True)
    email_in = st.text_input("البريد الإلكتروني المستخدم في النموذج:")
    code_in = st.text_input("كود الاستعلام (4 أرقام):", type="password")
    
    if st.button("التحقق من وجود السجل ✅", use_container_width=True):
        if email_in and code_in:
            with st.spinner("جاري فحص قاعدة البيانات..."):
                status, data = check_report_status(email_in, code_in)
                if status == "NOT_FOUND":
                    st.session_state.can_start_analysis = False
                    st.error("❌ لم نجد أي بيانات مطابقة. تأكد من البريد الإلكتروني وكود الوصول.")
                else:
                    st.session_state.user_email = email_in
                    st.session_state.user_code = code_in
                    st.session_state.can_start_analysis = True
                    st.success("✔️ تم العثور على بياناتك بنجاح في سجلاتنا.")
        else:
            st.warning("يرجى إكمال جميع الحقول.")

    if st.session_state.can_start_analysis:
        st.write("---")
        if st.button("بدء تحليل ومعالجة التقرير 🚀", use_container_width=True):
            st.session_state.page = "waiting"
            st.rerun()
    
    if st.button("↩️ العودة للرئيسية"):
        st.session_state.page = "main"
        st.rerun()

# ج. صفحة الانتظار والعداد
elif st.session_state.page == "waiting":
    st.markdown("<h2 style='text-align:center;'>ذكاء شفق يحلل بياناتك الآن...</h2>", unsafe_allow_html=True)
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for p in range(1, 101):
        if p % 15 == 0:
            status, data = check_report_status(st.session_state.user_email, st.session_state.user_code)
            if status == "READY":
                st.session_state.final_report = data
                st.session_state.page = "result"
                st.rerun()
        progress_bar.progress(p)
        status_text.text(f"جاري معالجة البيانات... {p}%")
        time.sleep(0.4)
    
    st.warning("⚠️ يستغرق التقرير وقتاً أطول. يمكنك الضغط على تحديث أو الانتظار قليلاً.")
    if st.button("تحديث الحالة 🔄"): st.rerun()

# د. صفحة النتائج
elif st.session_state.page == "result":
    st.success("✅ تم الاستخراج بنجاح")
    st.markdown(f"### 📄 تقرير: {st.session_state.user_email}")
    st.write("---")
    st.markdown(st.session_state.final_report)
    if st.button("بحث جديد 🔄"):
        st.session_state.can_start_analysis = False
        st.session_state.page = "query_page"
        st.rerun()

st.write("---")
st.markdown("<p style='text-align:center; opacity:0.5;'>جميع الحقوق محفوظة - شفق 2026</p>", unsafe_allow_html=True)
