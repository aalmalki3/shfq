import streamlit as st
import streamlit.components.v1 as components
from notion_client import Client
import time

# --- المرحلة 1: الصفحة الرئيسية (الاستبيان) ---
if st.session_state.page == "main":
    st.markdown("<h1 class='stTitle'>مرحباً بك في شفق</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#2C4251; font-size:1.2rem;'>نورٌ هادئ، لمستقبلٍ مهنيٍ واضح. يرجى إكمال النموذج أدناه لبدء التحليل.</p>", unsafe_allow_html=True)
    st.write("---")

    # كود تضمين تالي المحسن
    tally_embed_html = """
    <iframe data-tally-src="https://tally.so/embed/lb7DVN?alignLeft=1&hideTitle=1&transparentBackground=1&dynamicHeight=1" 
    loading="lazy" width="100%" height="1100" frameborder="0" marginheight="0" marginwidth="0" 
    title="بنك السير الذاتية | CV Bank"></iframe>
    <script src="https://tally.so/widgets/embed.js"></script>
    """
    
    # عرض النموذج
    components.html(tally_embed_html, height=1100, scrolling=True)

    # --- إضافة زر الانتقال لصفحة البحث بشكل واضح في الأسفل ---
    st.write("---")
    st.markdown("<p style='text-align:center;'>هل قمت بتعبئة النموذج مسبقاً وتريد استخراج تقريرك؟</p>", unsafe_allow_html=True)
    
    # زر الانتقال اليدوي
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        if st.button("🔍 انتقل لصفحة البحث والاستخراج", use_container_width=True):
            st.session_state.page = "query_page"
            st.rerun()

    st.markdown("<p style='text-align:center; opacity:0.5; font-size:0.8rem;'>أو يمكنك استخدام الرابط المباشر: <a href='?action=query' target='_self'>shfq-app.streamlit.app/?action=query</a></p>", unsafe_allow_html=True)

# 2. التنسيق المحسن (CSS) كما هو
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

# الشعار
col1, col2, col3 = st.columns([1, 1.5, 1])
with col2:
    try: st.image("assets/shfq.jpg", use_container_width=True)
    except: st.markdown("<h2 style='text-align:center;'>🌅 شفق</h2>", unsafe_allow_html=True)

# 4. إدارة حالات الصفحة
if "page" not in st.session_state:
    params = st.query_params
    st.session_state.page = "query_page" if params.get("action") == "query" else "main"

# --- المرحلة 1: الرئيسية ---
if st.session_state.page == "main":
    st.markdown("<h1 class='stTitle'>مرحباً بك في شفق</h1>")
    tally_embed_html = '<iframe data-tally-src="https://tally.so/embed/lb7DVN?alignLeft=1&hideTitle=1&transparentBackground=1&dynamicHeight=1" loading="lazy" width="100%" height="1000" frameborder="0" title="بنك السير الذاتية"></iframe><script src="https://tally.so/widgets/embed.js"></script>'
    components.html(tally_embed_html, height=1000, scrolling=True)
    st.markdown("<p style='text-align:center; opacity:0.7;'>لديك كود استعلام مسبق؟ <a href='?action=query' target='_self'>اضغط هنا</a></p>", unsafe_allow_html=True)

# --- المرحلة 2: صفحة الاستعلام ---
elif st.session_state.page == "query_page":
    st.markdown("<h2 class='stTitle'>🛡️ استعلام آمن عن التقرير</h2>")
    col_a, col_b = st.columns(2)
    with col_a: email_input = st.text_input("البريد الإلكتروني:")
    with col_b: code_input = st.text_input("كود الاستعلام (4 أرقام):", type="password")
    if st.button("التحقق والاستخراج 🚀"):
        if email_input and code_input:
            st.session_state.user_email = email_input
            st.session_state.user_code = code_input
            st.session_state.page = "waiting"
            st.rerun()

# --- المرحلة 3: صفحة الانتظار (الفحص الفوري قبل العداد) ---
elif st.session_state.page == "waiting":
    # التحقق الفوري قبل عرض أي شيء
    status, data = check_report_status(st.session_state.user_email, st.session_state.user_code)
    
    if status == "NOT_FOUND":
        st.error(f"❌ لم نجد أي سجل للبريد: {st.session_state.user_email}")
        st.info("تأكد من كتابة البريد بشكل صحيح، وأنك أرسلت النموذج بنجاح.")
        if st.button("العودة للتصحيح ↩️"):
            st.session_state.page = "query_page"
            st.rerun()
        st.stop() # هنا يتم القتل الفوري للعملية

    # إذا مر الفحص بنجاح، اعرض العداد
    header_p = st.empty()
    progress_p = st.empty()
    status_p = st.empty()
    
    header_p.markdown("<h2 style='text-align:center;'>ذكاء شفق يحلل بياناتك الآن...</h2>", unsafe_allow_html=True)
    
    for percent in range(1, 101):
        if percent % 10 == 0: # فحص دوري للجاهزية فقط
            status, data = check_report_status(st.session_state.user_email, st.session_state.user_code)
            if status == "READY":
                st.session_state.final_report = data
                st.session_state.page = "result"
                st.rerun()
        
        progress_p.progress(percent)
        status_p.text(f"جاري استخراج وتحليل البيانات... {percent}%")
        time.sleep(0.4)

# --- المرحلة 4: النتائج ---
elif st.session_state.page == "result":
    st.markdown(f"### 📄 التقرير الاستراتيجي لـ {st.session_state.user_email}")
    st.markdown(st.session_state.final_report)
    if st.button("استعلام جديد 🔄"):
        st.session_state.page = "main"
        st.rerun()
