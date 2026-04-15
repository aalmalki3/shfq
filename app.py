import streamlit as st
import streamlit.components.v1 as components
from notion_client import Client
import time

# 1. إعداد الصفحة
st.set_page_config(page_title="شفق | SHFQ", page_icon="🌅", layout="centered")

# --- 2. دالة جلب البيانات (المحسنة والآمنة) ---
def check_report_status(email, access_code):
    try:
        notion = Client(auth=st.secrets["NOTION_TOKEN"])
        db_id = st.secrets["NOTION_DATABASE_ID"]
        
        # استعلام نوشن باستخدام الفلترة الصارمة
        response = notion.databases.query(
            **{
                "database_id": db_id,
                "filter": {
                    "and": [
                        {"property": "Email", "email": {"equals": email.strip().lower()}},
                        {"property": "Access Code", "number": {"equals": int(access_code)}}
                    ]
                }
            }
        )
        
        results = response.get("results", [])
        if not results:
            return "NOT_FOUND", None
            
        for res in results:
            props = res.get("properties", {})
            # التأكد أن السجل يحتوي على اسم (ليس فارغاً)
            n_name_list = props.get("Full Name", {}).get("title", [])
            
            if n_name_list:
                page_id = res["id"]
                blocks_resp = notion.blocks.children.list(block_id=page_id)
                blocks = blocks_resp.get("results", [])
                
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
        return "ERROR", str(e)

# --- 3. تحسين التصميم (Modern UI CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Cairo', sans-serif;
        direction: RTL;
        text-align: right;
        background-color: #f8f9fa;
    }

    /* خلفية متدرجة انسيابية */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }

    /* تصميم الحاوية الرئيسية كبطاقة */
    .block-container {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 24px;
        padding: 3rem 2rem !important;
        box-shadow: 0 20px 40px rgba(0,0,0,0.05);
        margin-top: 2rem;
        border: 1px solid rgba(255,255,255,0.3);
    }

    /* تحسين شكل الأزرار */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.5rem;
        background-color: #2c4251 !important;
        color: white !important;
        font-weight: 600;
        font-size: 1.1rem;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(44, 66, 81, 0.2);
    }

    .stButton>button:hover {
        background-color: #0b1622 !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(44, 66, 81, 0.3);
    }

    /* تحسين شكل الحقول */
    .stTextInput>div>div>input {
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        padding: 1rem;
    }

    /* إخفاء القوائم غير الضرورية */
    #MainMenu, footer, header { visibility: hidden; }
    
    .status-box {
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# 4. منطق إدارة الصفحات
if "page" not in st.session_state:
    st.session_state.page = "main"

# --- المرحلة 1: الصفحة الرئيسية ---
if st.session_state.page == "main":
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        try: st.image("assets/shfq.jpg", use_container_width=True)
        except: st.markdown("<h1 style='text-align:center;'>🌅 شفق</h1>", unsafe_allow_html=True)
    
    st.markdown("<h2 style='text-align:center; color:#2c4251; margin-bottom:0;'>مرحباً بك في شفق</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#666;'>نورٌ هادئ، لمستقبلٍ مهنيٍ واضح</p>", unsafe_allow_html=True)
    st.write("")
    
    tally_embed = '<iframe data-tally-src="https://tally.so/embed/lb7DVN?alignLeft=1&hideTitle=1&transparentBackground=1&dynamicHeight=1" loading="lazy" width="100%" height="800" frameborder="0"></iframe><script src="https://tally.so/widgets/embed.js"></script>'
    components.html(tally_embed, height=800, scrolling=True)
    
    st.markdown("<p style='text-align:center; margin-top:1rem;'>هل قمت بالتسجيل مسبقاً؟</p>", unsafe_allow_html=True)
    if st.button("🔍 استخراج تقريري الآن", use_container_width=True):
        st.session_state.page = "query_page"
        st.rerun()

# --- المرحلة 2: صفحة الاستعلام ---
elif st.session_state.page == "query_page":
    st.markdown("<h3 style='text-align:center;'>🛡️ مركز الاستعلام الآمن</h3>", unsafe_allow_html=True)
    st.write("---")
    
    email_in = st.text_input("البريد الإلكتروني المعتمد:", placeholder="example@mail.com")
    code_in = st.text_input("كود الاستعلام الخاص بك:", type="password", placeholder="****")
    
    if st.button("التحقق من البيانات ⚡"):
        if email_in and code_in:
            with st.spinner("جاري فحص السجلات..."):
                time.sleep(1)
                status, data = check_report_status(email_in, code_in)
                
                if status == "NOT_FOUND":
                    st.error("❌ لم نجد سجلات تطابق هذه البيانات. تأكد من البريد والكود.")
                elif status == "ERROR":
                    st.warning(f"⚠️ خطأ في النظام: {data}")
                else:
                    st.success("✅ تم العثور على سجلّك بنجاح في نظام شفق.")
                    st.session_state.user_email = email_in
                    st.session_state.user_code = code_in
                    st.session_state.can_analyze = True
        else:
            st.warning("يرجى تعبئة جميع الحقول.")

    if st.session_state.get("can_analyze"):
        st.write("")
        if st.button("إصدار ومعالجة التقرير 🚀"):
            st.session_state.page = "waiting"
            st.rerun()
    
    if st.button("↩️ العودة"):
        st.session_state.page = "main"
        st.rerun()

# --- المرحلة 3: صفحة الانتظار ---
elif st.session_state.page == "waiting":
    st.markdown("<h3 style='text-align:center;'>الذكاء الاصطناعي يحلل بياناتك...</h3>", unsafe_allow_html=True)
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for p in range(1, 101):
        if p % 20 == 0:
            status, data = check_report_status(st.session_state.user_email, st.session_state.user_code)
            if status == "READY":
                st.session_state.final_report = data
                st.session_state.page = "result"
                st.rerun()
        progress_bar.progress(p)
        status_text.markdown(f"<p style='text-align:center;'>جاري المعالجة... {p}%</p>", unsafe_allow_html=True)
        time.sleep(0.3)
    
    st.info("التقرير يستغرق وقتاً إضافياً للمعالجة.")
    if st.button("تحديث الحالة 🔄"): st.rerun()

# --- المرحلة 4: عرض النتائج ---
elif st.session_state.page == "result":
    st.markdown("<h3 style='text-align:center;'>✅ تقريرك جاهز الآن</h3>", unsafe_allow_html=True)
    st.write("---")
    st.markdown(st.session_state.final_report)
    st.write("---")
    if st.button("استعلام جديد 🔄"):
        st.session_state.can_analyze = False
        st.session_state.page = "query_page"
        st.rerun()

# التذييل
st.markdown("<br><p style='text-align:center; opacity:0.6; font-size:0.8rem;'>جميع الحقوق محفوظة لـ شفق © 2026</p>", unsafe_allow_html=True)
