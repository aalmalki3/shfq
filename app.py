import streamlit as st
import streamlit.components.v1 as components
from notion_client import Client
import time

# 1. إعداد الصفحة
st.set_page_config(page_title="شفق | SHFQ", page_icon="🌅", layout="centered")

# --- 2. دالة جلب البيانات (تطابق يدوي صارم) ---
def check_report_status(email, access_code):
    try:
        notion = Client(auth=st.secrets["NOTION_TOKEN"])
        database_id = st.secrets["NOTION_DATABASE_ID"]
        
        # استعلام Notion
        query = notion.databases.query(
            database_id=database_id,
            filter={
                "and": [
                    {"property": "Email", "email": {"equals": email.strip().lower()}},
                    {"property": "Access Code", "number": {"equals": int(access_code)}}
                ]
            }
        )
        
        results = query.get("results")
        
        # --- التحقق اليدوي الصارم (Double Verification) ---
        found_page = None
        for res in results:
            props = res.get("properties", {})
            
            # جلب القيمة الفعلية للإيميل من نوشن
            notion_email = props.get("Email", {}).get("email", "")
            # جلب القيمة الفعلية للكود من نوشن
            notion_code = props.get("Access Code", {}).get("number", 0)
            # جلب الاسم للتأكد أن السطر ليس فارغاً تماماً
            notion_name = props.get("Full Name", {}).get("title", [])
            
            # شرط التطابق الثلاثي: الإيميل صحيح + الكود صحيح + السطر يحتوي على اسم (ليس فارغاً)
            if (notion_email.strip().lower() == email.strip().lower()) and \
               (int(notion_code) == int(access_code)) and \
               (len(notion_name) > 0):
                found_page = res
                break # وجدنا السجل الصحيح، توقف عن البحث

        if not found_page:
            return "NOT_FOUND", None
            
        # فحص محتوى الصفحة (Blocks)
        page_id = found_page["id"]
        blocks = notion.blocks.children.list(block_id=page_id)
        
        report_text = ""
        for block in blocks.get("results"):
            if block["type"] == "paragraph":
                rich_text = block["paragraph"]["rich_text"]
                if rich_text:
                    report_text += rich_text[0]["plain_text"] + "\n\n"
        
        if not report_text.strip():
            return "PROCESSING", None
            
        return "READY", report_text
    except Exception:
        return "ERROR", None

# --- 3. تهيئة حالة الصفحة ---
if "page" not in st.session_state:
    params = st.query_params
    st.session_state.page = "query_page" if params.get("action") == "query" else "main"

if "can_start_analysis" not in st.session_state:
    st.session_state.can_start_analysis = False

# --- 4. التنسيق البصري (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [data-testid="stAppViewContainer"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background: linear-gradient(-45deg, #E8D9C0, #F4D3C5, #F4C7A5, #A9CAD7, #2C4251, #0B1622); background-size: 400% 400%; animation: gradient 15s ease infinite; }
    .block-container { background-color: rgba(255, 255, 255, 0.95); border-radius: 20px; padding: 40px !important; box-shadow: 0 10px 30px rgba(0,0,0,0.1); margin-top: 30px; }
    #MainMenu, footer, header { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

# عرض الشعار
col1, col2, col3 = st.columns([1, 1.5, 1])
with col2:
    try: st.image("assets/shfq.jpg", use_container_width=True)
    except: st.markdown("<h2 style='text-align:center;'>🌅 شفق</h2>", unsafe_allow_html=True)

# --- 5. منطق الصفحات ---

if st.session_state.page == "main":
    st.markdown("<h1 style='text-align:center;'>مرحباً بك في شفق</h1>", unsafe_allow_html=True)
    tally_embed_html = '<iframe data-tally-src="https://tally.so/embed/lb7DVN?alignLeft=1&hideTitle=1&transparentBackground=1&dynamicHeight=1" loading="lazy" width="100%" height="1000" frameborder="0"></iframe><script src="https://tally.so/widgets/embed.js"></script>'
    components.html(tally_embed_html, height=1000, scrolling=True)
    if st.button("🔍 استخراج تقرير سابق", use_container_width=True):
        st.session_state.page = "query_page"
        st.rerun()

elif st.session_state.page == "query_page":
    st.markdown("<h2 style='text-align:center;'>🛡️ التحقق من سجلات شفق</h2>", unsafe_allow_html=True)
    email_in = st.text_input("البريد الإلكتروني المستخدم:")
    code_in = st.text_input("كود الاستعلام (4 أرقام):", type="password")
    
    if st.button("التحقق من وجود السجل ✅", use_container_width=True):
        if email_in and code_in:
            with st.spinner("جاري مطابقة البيانات..."):
                status, data = check_report_status(email_in, code_in)
                if status == "NOT_FOUND":
                    st.session_state.can_start_analysis = False
                    st.error("❌ لم نجد أي سجل مطابق للبريد والكود المدخلين.")
                else:
                    st.session_state.user_email = email_in
                    st.session_state.user_code = code_in
                    st.session_state.can_start_analysis = True
                    st.success("✔️ تم العثور على بياناتك ومطابقتها بنجاح.")
        else:
            st.warning("يرجى إدخال البيانات.")

    if st.session_state.can_start_analysis:
        if st.button("بدء تحليل ومعالجة التقرير 🚀", use_container_width=True):
            st.session_state.page = "waiting"
            st.rerun()

elif st.session_state.page == "waiting":
    st.markdown("<h2 style='text-align:center;'>ذكاء شفق يحلل بياناتك الآن...</h2>", unsafe_allow_html=True)
    progress_bar = st.progress(0)
    for p in range(1, 101):
        if p % 15 == 0:
            status, data = check_report_status(st.session_state.user_email, st.session_state.user_code)
            if status == "READY":
                st.session_state.final_report = data
                st.session_state.page = "result"
                st.rerun()
        progress_bar.progress(p)
        time.sleep(0.4)
    st.warning("⏳ التقرير قيد التجهيز، اضغط تحديث بعد لحظات.")
    if st.button("تحديث 🔄"): st.rerun()

elif st.session_state.page == "result":
    st.success("✅ تم الاستخراج!")
    st.markdown(st.session_state.final_report)
    if st.button("بحث جديد 🔄"):
        st.session_state.can_start_analysis = False
        st.session_state.page = "query_page"
        st.rerun()

st.write("---")
st.markdown("<p style='text-align:center; opacity:0.5;'>جميع الحقوق محفوظة - شفق 2026</p>", unsafe_allow_html=True)
