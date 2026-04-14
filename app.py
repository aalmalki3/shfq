import streamlit as st
import streamlit.components.v1 as components
from notion_client import Client
import time

# 1. إعداد الصفحة
st.set_page_config(page_title="شفق | SHFQ", page_icon="🌅", layout="centered")

# دالة لجلب التقرير من نوشن
def get_report_from_notion(email):
    try:
        notion = Client(auth=st.secrets["NOTION_TOKEN"])
        database_id = st.secrets["NOTION_DATABASE_ID"]
        
        query = notion.databases.query(
            database_id=database_id,
            filter={
                "property": "Email", 
                "email": {"equals": email}
            }
        )
        
        results = query.get("results")
        if results:
            page_id = results[0]["id"]
            # نتحقق من وجود محتوى (Blocks) داخل الصفحة
            blocks = notion.blocks.children.list(block_id=page_id)
            if len(blocks.get("results")) > 0:
                report_text = ""
                for block in blocks.get("results"):
                    if block["type"] == "paragraph":
                        rich_text = block["paragraph"]["rich_text"]
                        if rich_text:
                            report_text += rich_text[0]["plain_text"] + "\n\n"
                return report_text
    except Exception as e:
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

# 4. إدارة حالات الصفحة (Navigation Logic)
if "page" not in st.session_state:
    st.session_state.page = "main"

# --- الصفحة الرئيسية (الاستبيان) ---
if st.session_state.page == "main":
    st.markdown("<h1 class='stTitle'>مرحباً بك في شفق</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#2C4251; font-size:1.2rem;'>نورٌ هادئ، لمستقبلٍ مهنيٍ واضح. يرجى إكمال النموذج أدناه لبدء التحليل.</p>", unsafe_allow_html=True)
    
    email_input = st.text_input("أدخل بريدك الإلكتروني المستخدم في النموذج للمتابعة:", placeholder="example@mail.com")
    
    st.write("---")

    tally_embed_html = """
    <iframe data-tally-src="https://tally.so/embed/lb7DVN?alignLeft=1&hideTitle=1&transparentBackground=1&dynamicHeight=1" 
    loading="lazy" width="100%" height="1000" frameborder="0" marginheight="0" marginwidth="0" 
    title="بنك السير الذاتية | CV Bank"></iframe>
    <script src="https://tally.so/widgets/embed.js"></script>
    """
    components.html(tally_embed_html, height=1000, scrolling=True)

    if st.button("بدء معالجة التقرير الاستراتيجي 🚀"):
        if email_input:
            st.session_state.user_email = email_input
            st.session_state.page = "waiting"
            st.rerun()
        else:
            st.error("يرجى إدخال البريد الإلكتروني أولاً للمتابعة.")

# --- صفحة الانتظار والعداد الذكي ---
elif st.session_state.page == "waiting":
    st.markdown("<h2 style='text-align:center;'>ذكاء شفق يحلل سيرتك الآن...</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>يرجى عدم إغلاق الصفحة، يتم الآن استخراج البيانات وبناء خارطة الطريق المهنية.</p>", unsafe_allow_html=True)
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    report = None
    # محاكاة عداد يتقدم ببطء ليعطي انطباع المعالجة
    for percent_complete in range(1, 101):
        # في كل خطوة، العداد يتقدم 1%
        # لكن سنقوم بفحص نوشن فعلياً كل 3 ثوانٍ تقريباً
        if percent_complete % 5 == 0:
            report = get_report_from_notion(st.session_state.user_email)
            if report:
                # إذا وجد التقرير، اقفز بالعداد لـ 100% فوراً
                progress_bar.progress(100)
                status_text.text("اكتملت المعالجة بنسبة 100%!")
                st.session_state.final_report = report
                st.session_state.page = "result"
                time.sleep(1)
                st.rerun()
        
        # إذا لم يجهز بعد، استمر في التحميل البصري ببطء
        if percent_complete < 95:
            progress_bar.progress(percent_complete)
            status_text.text(f"جاري التحليل... {percent_complete}%")
            time.sleep(0.5) # سرعة العداد البصرية
        else:
            # تثبيت العداد عند 95% إذا تأخر الذكاء الاصطناعي
            status_text.text("اللمسات النهائية للتقرير... قد يستغرق ذلك لحظات إضافية")
            time.sleep(2)
            # فحص أخير مكثف
            report = get_report_from_notion(st.session_state.user_email)
            if report:
                progress_bar.progress(100)
                st.session_state.final_report = report
                st.session_state.page = "result"
                st.rerun()

# --- صفحة عرض النتيجة النهائية ---
elif st.session_state.page == "result":
    st.markdown("<h2 style='text-align:center;'>📄 تقريرك الاستراتيجي جاهز</h2>", unsafe_allow_html=True)
    st.write("---")
    st.markdown(st.session_state.final_report)
    
    if st.button("تحليل سيرة أخرى 🔄"):
        st.session_state.page = "main"
        if "final_report" in st.session_state: del st.session_state.final_report
        st.rerun()

# 6. التذييل
st.write("---")
st.markdown("<p style='text-align:center; opacity:0.5; color:#0B1622;'>جميع الحقوق محفوظة - شفق 2026</p>", unsafe_allow_html=True)
