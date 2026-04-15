import streamlit as st
import streamlit.components.v1 as components
from notion_client import Client
import time

# 1. إعداد الصفحة
st.set_page_config(page_title="شفق | SHFQ", page_icon="🌅", layout="centered")

# --- تهيئة الحالة ---
if "page" not in st.session_state:
    st.session_state.page = "main"
if "can_start_analysis" not in st.session_state:
    st.session_state.can_start_analysis = False

# دالة فحص الحالة
def check_report_status(email, access_code):
    try:
        notion = Client(auth=st.secrets["NOTION_TOKEN"])
        database_id = st.secrets["NOTION_DATABASE_ID"]
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
        if not results: return "NOT_FOUND", None
        
        page_id = results[0]["id"]
        blocks = notion.blocks.children.list(block_id=page_id)
        
        # إذا كانت الصفحة فارغة (لا توجد بلوكات باراجراف)
        if len(blocks.get("results")) == 0:
            return "PROCESSING", None
            
        report_text = ""
        for block in blocks.get("results"):
            if block["type"] == "paragraph":
                rich_text = block["paragraph"]["rich_text"]
                if rich_text: report_text += rich_text[0]["plain_text"] + "\n\n"
        
        return "READY", report_text if report_text.strip() else "PROCESSING"
    except Exception: return "ERROR", None

# [كود CSS كما هو...]
st.markdown("<style> @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap'); html, body, [data-testid='stAppViewContainer'] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; } .stApp { background: linear-gradient(-45deg, #E8D9C0, #F4D3C5, #F4C7A5, #A9CAD7, #2C4251, #0B1622); background-size: 400% 400%; animation: gradient 15s ease infinite; } .block-container { background-color: rgba(255, 255, 255, 0.95); border-radius: 20px; padding: 40px !important; box-shadow: 0 10px 30px rgba(0,0,0,0.1); margin-top: 30px; } </style>", unsafe_allow_html=True)

# الصفحة الرئيسية
if st.session_state.page == "main":
    st.markdown("<h1 style='text-align:center;'>مرحباً بك في شفق</h1>", unsafe_allow_html=True)
    tally_embed_html = '<iframe data-tally-src="https://tally.so/embed/lb7DVN?alignLeft=1&hideTitle=1&transparentBackground=1&dynamicHeight=1" loading="lazy" width="100%" height="1000" frameborder="0"></iframe><script src="https://tally.so/widgets/embed.js"></script>'
    components.html(tally_embed_html, height=1000, scrolling=True)
    if st.button("🔍 استخراج تقرير سابق", use_container_width=True):
        st.session_state.page = "query_page"
        st.rerun()

# صفحة الاستعلام (التحقق من الهوية فقط)
elif st.session_state.page == "query_page":
    st.markdown("<h2 style='text-align:center;'>🛡️ التحقق من سجلات شفق</h2>", unsafe_allow_html=True)
    email_in = st.text_input("البريد الإلكتروني:")
    code_in = st.text_input("كود الاستعلام:", type="password")
    
    if st.button("التحقق من وجود السجل ✅", use_container_width=True):
        status, data = check_report_status(email_in, code_in)
        if status == "NOT_FOUND":
            st.error("❌ لم نجد بيانات بهذا البريد والكود.")
        else:
            st.session_state.user_email = email_in
            st.session_state.user_code = code_in
            st.session_state.can_start_analysis = True
            st.success("✔️ تم العثور على بياناتك بنجاح في سجلاتنا.")

    # إذا وجد السجل، يظهر خيار بدء التحليل (هنا يظهر العداد)
    if st.session_state.can_start_analysis:
        st.write("---")
        st.info("سجلّك موجود في النظام وجاهز للمعالجة.")
        if st.button("بدء تحليل ومعالجة التقرير 🚀", use_container_width=True):
            st.session_state.page = "waiting"
            st.rerun()

# صفحة الانتظار (هنا فقط يظهر العداد)
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
        status_text.text(f"جاري تحليل البيانات واستخلاص النتائج... {p}%")
        time.sleep(0.4)
    
    # إذا انتهى العداد ولم يجهز التقرير
    st.warning("⚠️ التقرير يستغرق وقتاً أطول من المعتاد. يرجى إعادة المحاولة بعد دقيقة.")
    if st.button("إعادة المحاولة 🔄"): st.rerun()

# صفحة النتائج
elif st.session_state.page == "result":
    st.markdown(f"### 📄 التقرير الاستراتيجي لـ {st.session_state.user_email}")
    st.markdown(st.session_state.final_report)
    if st.button("استعلام جديد 🔄"):
        st.session_state.can_start_analysis = False
        st.session_state.page = "query_page"
        st.rerun()
