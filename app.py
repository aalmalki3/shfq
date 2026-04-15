import streamlit as st
import streamlit.components.v1 as components
from notion_client import Client
import time

# 1. إعداد الصفحة
st.set_page_config(page_title="شفق | SHFQ", page_icon="🌅", layout="centered")

# دالة مطورة لفحص الحالة (جاهز، قيد المعالجة، غير موجود)
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
        
        if not results:
            return "NOT_FOUND", None
            
        page_id = results[0]["id"]
        blocks = notion.blocks.children.list(block_id=page_id)
        
        if len(blocks.get("results")) == 0:
            return "PROCESSING", None
            
        report_text = ""
        for block in blocks.get("results"):
            if block["type"] == "paragraph":
                rich_text = block["paragraph"]["rich_text"]
                if rich_text:
                    report_text += rich_text[0]["plain_text"] + "\n\n"
        
        return "READY", report_text
    except Exception:
        return "ERROR", None

# 2. التنسيق المحسن (CSS)
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
    .stTitle {
        font-weight: 700;
        color: #0B1622;
        text-align: center;
    }
    #MainMenu, footer, header { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

# 3. عرض الشعار
col1, col2, col3 = st.columns([1, 1.5, 1])
with col2:
    try:
        st.image("assets/shfq.jpg", use_container_width=True)
    except:
        st.markdown("<h2 style='text-align:center;'>🌅 شفق</h2>", unsafe_allow_html=True)

# 4. إدارة حالات الصفحة
if "page" not in st.session_state:
    params = st.query_params
    if params.get("action") == "query":
        st.session_state.page = "query_page"
    else:
        st.session_state.page = "main"

# --- المرحلة 1: الصفحة الرئيسية (الاستبيان) ---
if st.session_state.page == "main":
    st.markdown("<h1 class='stTitle'>مرحباً بك في شفق</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#2C4251; font-size:1.2rem;'>نورٌ هادئ، لمستقبلٍ مهنيٍ واضح.</p>", unsafe_allow_html=True)
    st.write("---")
    tally_embed_html = """
    <iframe data-tally-src="https://tally.so/embed/lb7DVN?alignLeft=1&hideTitle=1&transparentBackground=1&dynamicHeight=1" 
    loading="lazy" width="100%" height="1000" frameborder="0" title="بنك السير الذاتية"></iframe>
    <script src="https://tally.so/widgets/embed.js"></script>
    """
    components.html(tally_embed_html, height=1000, scrolling=True)
    st.markdown("<p style='text-align:center; opacity:0.7;'>لديك كود استعلام مسبق؟ <a href='?action=query' target='_self'>اضغط هنا للاستخراج</a></p>", unsafe_allow_html=True)

# --- المرحلة 2: صفحة الاستعلام الآمن ---
elif st.session_state.page == "query_page":
    st.markdown("<h2 class='stTitle'>🛡️ استعلام آمن عن التقرير</h2>", unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        email_input = st.text_input("البريد الإلكتروني المستخدم:")
    with col_b:
        code_input = st.text_input("كود الاستعلام (4 أرقام):", type="password")

    if st.button("التحقق وبدء الاستخراج 🚀"):
        if email_input and code_input:
            st.session_state.user_email = email_input
            st.session_state.user_code = code_input
            st.session_state.page = "waiting"
            st.rerun()
        else:
            st.error("يرجى إدخال البيانات المطلوبة.")

# --- المرحلة 3: صفحة الانتظار (النسخة الحاسمة للقطع الفوري) ---
elif st.session_state.page == "waiting":
    # حاويات فارغة لتسهيل مسح العناصر من الشاشة عند الخطأ
    header_placeholder = st.empty()
    progress_placeholder = st.empty()
    status_placeholder = st.empty()
    
    header_placeholder.markdown("<h2 style='text-align:center;'>ذكاء شفق يحلل بياناتك الآن...</h2>", unsafe_allow_html=True)
    
    for percent in range(1, 101):
        # فحص الحالة مبكراً (عند 10%) وكل 10 خطوات
        if percent % 10 == 0:
            status, data = check_report_status(st.session_state.user_email, st.session_state.user_code)
            
            if status == "NOT_FOUND":
                # مسح العداد والعناوين فوراً
                header_placeholder.empty()
                progress_placeholder.empty()
                status_placeholder.empty()
                
                # إظهار رسالة الخطأ والقطع
                st.error(f"❌ لم نجد أي سجل للبريد: {st.session_state.user_email}")
                st.info("تأكد من كتابة البريد بشكل صحيح وكود الوصول (4 أرقام) الذي استخدمته في النموذج.")
                if st.button("العودة للتصحيح ↩️"):
                    st.session_state.page = "query_page"
                    st.rerun()
                st.stop() # إيقاف المحرك نهائياً لضمان عدم استمرار العداد

            elif status == "READY":
                header_placeholder.empty()
                progress_placeholder.empty()
                status_placeholder.empty()
                st.session_state.final_report = data
                st.session_state.page = "result"
                st.rerun()

        # تحديث العداد بصرياً فقط إذا استمرت العملية
        progress_placeholder.progress(percent)
        if percent < 95:
            status_placeholder.text(f"جاري استرجاع السجل وتحليله... {percent}%")
            time.sleep(0.4)
        else:
            status_placeholder.text("اللمسات النهائية... لحظات قليلة")
            time.sleep(1)

# --- المرحلة 4: عرض النتائج ---
elif st.session_state.page == "result":
    st.markdown(f"<h3 style='text-align:center;'>📄 التقرير الاستراتيجي لـ {st.session_state.user_email}</h3>", unsafe_allow_html=True)
    st.write("---")
    st.markdown(st.session_state.final_report)
    if st.button("استعلام جديد 🔄"):
        for key in ["user_email", "user_code", "final_report"]:
            if key in st.session_state: del st.session_state[key]
        st.session_state.page = "main"
        st.rerun()

# 6. التذييل
st.write("---")
st.markdown("<p style='text-align:center; opacity:0.5; color:#0B1622;'>جميع الحقوق محفوظة - شفق 2026</p>", unsafe_allow_html=True)
