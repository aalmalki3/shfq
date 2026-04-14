import streamlit as st
import streamlit.components.v1 as components
from notion_client import Client
import time

# 1. إعداد الصفحة
st.set_page_config(page_title="شفق | SHFQ", page_icon="🌅", layout="centered")

# دالة لجلب التقرير من نوشن
def get_report_from_notion(email):
    try:
        # الاتصال بنوشن باستخدام الـ Secrets
        notion = Client(auth=st.secrets["NOTION_TOKEN"])
        database_id = st.secrets["NOTION_DATABASE_ID"]
        
        # البحث عن السجل المرتبط بالإيميل
        query = notion.databases.query(
            database_id=database_id,
            filter={
                "property": "Email",  # تأكد أن اسم العمود في نوشن هو Email
                "email": {"equals": email}
            }
        )
        
        results = query.get("results")
        if results:
            page_id = results[0]["id"]
            # جلب محتوى الصفحة (Blocks)
            blocks = notion.blocks.children.list(block_id=page_id)
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

# 4. واجهة الاستخدام الرئيسية
if "report_ready" not in st.session_state:
    st.markdown("<h1 class='stTitle'>مرحباً بك في شفق</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#2C4251; font-size:1.2rem;'>نورٌ هادئ، لمستقبلٍ مهنيٍ واضح. يرجى إكمال النموذج أدناه لبدء التحليل.</p>", unsafe_allow_html=True)
    
    # حقل إدخال الإيميل للمتابعة (ضروري للربط)
    email_input = st.text_input("أدخل بريدك الإلكتروني المستخدم في النموذج لمتابعة التقرير:", placeholder="example@mail.com")
    
    st.write("---")

    # تضمين استبيان تالي (Tally)
    tally_embed_html = """
    <iframe data-tally-src="https://tally.so/embed/lb7DVN?alignLeft=1&hideTitle=1&transparentBackground=1&dynamicHeight=1" 
    loading="lazy" width="100%" height="1245" frameborder="0" marginheight="0" marginwidth="0" 
    title="بنك السير الذاتية | CV Bank"></iframe>
    <script src="https://tally.so/widgets/embed.js"></script>
    """
    components.html(tally_embed_html, height=1000, scrolling=True)

    # زر التحقق من الجاهزية
    if email_input:
        if st.button("التحقق من جاهزية التقرير الاستراتيجي 🔍"):
            with st.status("جاري البحث عن تقريرك في قاعدة بيانات شفق...", expanded=True) as status:
                report = get_report_from_notion(email_input)
                if report:
                    st.session_state.report_ready = report
                    st.rerun()
                else:
                    st.info("التقرير قيد التحليل حالياً من قبل الذكاء الاصطناعي.. يرجى الانتظار 30 ثانية والمحاولة مجدداً.")

# 5. عرض التقرير النهائي (عند الجاهزية)
else:
    st.markdown("<h2 style='text-align:center;'>📄 تقريرك الاستراتيجي جاهز</h2>", unsafe_allow_html=True)
    st.write("---")
    st.markdown(st.session_state.report_ready)
    if st.button("تحليل سيرة أخرى 🔄"):
        del st.session_state.report_ready
        st.rerun()

# 6. التذييل
st.write("---")
st.markdown("<p style='text-align:center; opacity:0.5; color:#0B1622;'>جميع الحقوق محفوظة - شفق 2026</p>", unsafe_allow_html=True)
