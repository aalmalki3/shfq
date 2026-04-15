import streamlit as st
import streamlit.components.v1 as components
from notion_client import Client
import time

# 1. إعداد الصفحة
st.set_page_config(page_title="شفق | SHFQ", page_icon="🌅", layout="centered")

# دالة لجلب التقرير من نوشن (البحث بالبريد + كود الاستعلام)
def get_report_from_notion(email, access_code):
    try:
        notion = Client(auth=st.secrets["NOTION_TOKEN"])
        database_id = st.secrets["NOTION_DATABASE_ID"]
        
        # استعلام مزدوج: البريد الإلكتروني وكود الوصول
        query = notion.databases.query(
            database_id=database_id,
            filter={
                "and": [
                    {
                        "property": "Email",
                        "email": {"equals": email}
                    },
                    {
                        "property": "Access Code", # تأكد من تسمية العمود في نوشن بهذا الاسم ونوعه Number
                        "number": {"equals": int(access_code)}
                    }
                ]
            }
        )
        
        results = query.get("results")
        if results:
            page_id = results[0]["id"]
            # جلب البلوكات للتأكد من أن ميك (Make) انتهى من الكتابة
            blocks = notion.blocks.children.list(block_id=page_id)
            if len(blocks.get("results")) > 0:
                report_text = ""
                for block in blocks.get("results"):
                    if block["type"] == "paragraph":
                        rich_text = block["paragraph"]["rich_text"]
                        if rich_text:
                            report_text += rich_text[0]["plain_text"] + "\n\n"
                return report_text
    except Exception:
        return None
    return None

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

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
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
    st.session_state.page = "main"

# --- الصفحة الرئيسية (الاستبيان + الدخول الآمن) ---
if st.session_state.page == "main":
    st.markdown("<h1 class='stTitle'>مرحباً بك في شفق</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#2C4251; font-size:1.2rem;'>نورٌ هادئ، لمستقبلٍ مهنيٍ واضح.</p>", unsafe_allow_html=True)
    
    st.write("---")
    st.subheader("🛡️ استعلام آمن عن التقرير")
    col_a, col_b = st.columns(2)
    with col_a:
        email_input = st.text_input("البريد الإلكتروني المستخدم في النموذج:", placeholder="example@mail.com")
    with col_b:
        code_input = st.text_input("كود الاستعلام (4 أرقام):", placeholder="1234", type="password")

    if st.button("التحقق من جاهزية التقرير وبدء الاستخراج 🚀"):
        if email_input and code_input:
            if len(code_input) == 4 and code_input.isdigit():
                st.session_state.user_email = email_input
                st.session_state.user_code = code_input
                st.session_state.page = "waiting"
                st.rerun()
            else:
                st.error("يرجى إدخال كود مكون من 4 أرقام فقط.")
        else:
            st.error("يرجى إدخال البريد الإلكتروني والكود للمتابعة.")

    st.write("---")
    st.markdown("<p style='text-align:center;'>إذا لم تقم بتعبئة النموذج بعد، يرجى إكماله أدناه:</p>", unsafe_allow_html=True)

    tally_embed_html = """
    <iframe data-tally-src="https://tally.so/embed/lb7DVN?alignLeft=1&hideTitle=1&transparentBackground=1&dynamicHeight=1" 
    loading="lazy" width="100%" height="1000" frameborder="0" marginheight="0" marginwidth="0" 
    title="بنك السير الذاتية | CV Bank"></iframe>
    <script src="https://tally.so/widgets/embed.js"></script>
    """
    components.html(tally_embed_html, height=1000, scrolling=True)

# --- صفحة الانتظار والعداد الذكي ---
elif st.session_state.page == "waiting":
    st.markdown("<h2 style='text-align:center;'>ذكاء شفق يحلل بياناتك الآن...</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>يتم الآن فحص السيرة الذاتية وبناء التقرير الاستراتيجي. يرجى الانتظار.</p>", unsafe_allow_html=True)
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    report = None
    for percent_complete in range(1, 101):
        # فحص نوشن كل 5 خطوات في العداد (لإعطاء مساحة زمنية لمعالجة ميك)
        if percent_complete % 5 == 0:
            report = get_report_from_notion(st.session_state.user_email, st.session_state.user_code)
            if report:
                progress_bar.progress(100)
                status_text.text("تم العثور على التقرير! جاري العرض...")
                st.session_state.final_report = report
                st.session_state.page = "result"
                time.sleep(1)
                st.rerun()
        
        if percent_complete < 95:
            progress_bar.progress(percent_complete)
            status_text.text(f"جاري استخراج السجل ومعالجته... {percent_complete}%")
            time.sleep(0.6) # سرعة العداد (حوالي دقيقة للوصول لـ 95%)
        else:
            status_text.text("اللمسات النهائية للتحليل... لحظات من فضلك")
            # استمرار الفحص المكثف في النهاية
            report = get_report_from_notion(st.session_state.user_email, st.session_state.user_code)
            if report:
                progress_bar.progress(100)
                st.session_state.final_report = report
                st.session_state.page = "result"
                st.rerun()
            time.sleep(2)

# --- صفحة عرض النتيجة النهائية ---
elif st.session_state.page == "result":
    st.markdown(f"<h2 style='text-align:center;'>📄 التقرير الاستراتيجي لـ {st.session_state.user_email}</h2>", unsafe_allow_html=True)
    st.write("---")
    st.markdown(st.session_state.final_report)
    
    if st.button("استعلام جديد 🔄"):
        st.session_state.page = "main"
        if "final_report" in st.session_state: del st.session_state.final_report
        st.rerun()

# 6. التذييل
st.write("---")
st.markdown("<p style='text-align:center; opacity:0.5; color:#0B1622;'>جميع الحقوق محفوظة - شفق 2026</p>", unsafe_allow_html=True)
