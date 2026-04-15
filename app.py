import streamlit as st
import streamlit.components.v1 as components
import requests
import time

# 1. إعداد الصفحة
st.set_page_config(page_title="شفق | SHFQ", page_icon="🌅", layout="centered")

# --- 2. دالة جلب البيانات المحدثة (البحث السريع ودعم العربية) ---
def check_report_status(email, access_code):
    try:
        token = st.secrets["NOTION_TOKEN"]
        database_id = st.secrets["NOTION_DATABASE_ID"]
        url = f"https://api.notion.com/v1/databases/{database_id}/query"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        
        payload = {
            "filter": {
                "and": [
                    {"property": "Email", "email": {"equals": email.strip().lower()}},
                    {"property": "Access Code", "rich_text": {"equals": str(access_code).strip()}}
                ]
            },
            "page_size": 1 
        }
        
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        
        if response.status_code != 200:
            return "ERROR", "خطأ في الاتصال السريع بقاعدة البيانات"

        results = data.get("results", [])
        if not results:
            return "NOT_FOUND", None
            
        res = results[0]
        page_id = res["id"]
        
        blocks_url = f"https://api.notion.com/v1/blocks/{page_id}/children?page_size=100"
        blocks_resp = requests.get(blocks_url, headers=headers)
        blocks_data = blocks_resp.json()
        
        all_text_parts = []
        for block in blocks_data.get("results", []):
            block_type = block["type"]
            supported = ["paragraph", "heading_1", "heading_2", "heading_3", "bulleted_list_item", "numbered_list_item"]
            
            if block_type in supported:
                rich_text = block[block_type].get("rich_text", [])
                if rich_text:
                    block_text = "".join([t["plain_text"] for t in rich_text])
                    all_text_parts.append(block_text)
        
        report_text = "\n\n".join(all_text_parts)
        
        if not report_text.strip():
            return "PROCESSING", None
            
        return "READY", report_text

    except Exception as e:
        return "ERROR", f"حدث خطأ غير متوقع: {str(e)}"

# --- 3. التصميم البصري (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    html, body, [data-testid="stAppViewContainer"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background: linear-gradient(-45deg, #E8D9C0, #F4D3C5, #F4C7A5, #A9CAD7, #2C4251, #0B1622); background-size: 400% 400%; animation: gradient 15s ease infinite; }
    @keyframes gradient { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
    .block-container { background-color: rgba(255, 255, 255, 0.95); border-radius: 24px; padding: 3rem 2rem !important; box-shadow: 0 20px 40px rgba(0,0,0,0.2); margin-top: 2rem; }
    .stButton>button { width: 100%; border-radius: 12px; height: 3.5rem; background-color: #2c4251 !important; color: white !important; font-weight: 600; transition: all 0.3s ease; border: none; }
    .stButton>button:hover { background-color: #0b1622 !important; transform: translateY(-2px); }
    #MainMenu, footer, header { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

# 4. منطق الصفحات
if "page" not in st.session_state:
    st.session_state.page = "main"

if st.session_state.page == "main":
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        try: st.image("assets/shfq.jpg", use_container_width=True)
        except: st.markdown("<h1 style='text-align:center;'>🌅 شفق</h1>", unsafe_allow_html=True)
    
    tally_embed = '<iframe data-tally-src="https://tally.so/embed/lb7DVN?alignLeft=1&hideTitle=1&transparentBackground=1&dynamicHeight=1" loading="lazy" width="100%" height="800" frameborder="0"></iframe><script src="https://tally.so/widgets/embed.js"></script>'
    components.html(tally_embed, height=800, scrolling=True)
    
    if st.button("🔍 استخراج التقرير"):
        st.session_state.page = "query_page"
        st.rerun()

elif st.session_state.page == "query_page":
    st.markdown("<h3 style='text-align:center;'>🛡️ مركز الاستعلام الآمن</h3>", unsafe_allow_html=True)
    email_in = st.text_input("البريد الإلكتروني المعتمد:")
    code_in = st.text_input("كود الاستعلام الخاص بك (4 أرقام):", type="password")
    
    if st.button("التحقق من البيانات ⚡"):
        if email_in and code_in:
            with st.spinner("جاري فحص السجلات..."):
                status, data = check_report_status(email_in, code_in)
                if status == "NOT_FOUND":
                    st.error("❌ لم نجد سجلات تطابق هذه البيانات.")
                elif status == "ERROR":
                    st.warning(f"⚠️ {data}")
                else:
                    st.success("✅ تم العثور على سجلّك بنجاح.")
                    st.session_state.user_email = email_in
                    st.session_state.user_code = code_in
                    st.session_state.can_analyze = True
        else: st.warning("يرجى إكمال جميع البيانات.")

    if st.session_state.get("can_analyze"):
        if st.button("إصدار ومعالجة التقرير 🚀"):
            st.session_state.page = "waiting"
            st.rerun()
    
    if st.button("↩️ العودة"):
        st.session_state.page = "main"
        st.rerun()

elif st.session_state.page == "waiting":
    st.markdown("<h3 style='text-align:center;'>الذكاء الاصطناعي يحلل بياناتك الآن...</h3>", unsafe_allow_html=True)
    
    # رسائل إشغال العميل لرفع القيمة المتصورة للخدمة
    loading_messages = [
        "جاري فحص ملف السيرة الذاتية بدقة...",
        "جاري مطابقة الخبرات مع معايير الـ ATS العالمية...",
        "الذكاء الاصطناعي يصيغ التوصيات الاستراتيجية بالعربية...",
        "جاري تنسيق التقرير النهائي ورفعه للنظام...",
        "لحظات ويصبح تقريرك المهني جاهزاً للعرض..."
    ]
    
    progress_bar = st.progress(0)
    status_placeholder = st.empty()

    # حلقة انتظار أطول قليلاً (حوالي 25 ثانية إجمالاً) لضمان مزامنة نوشن تماماً
    for i in range(100):
        # تحديث الرسالة كل 20% من التقدم
        msg_idx = min(i // 20, len(loading_messages) - 1)
        status_placeholder.markdown(f"<p style='text-align:center; color:#2c4251;'>{loading_messages[msg_idx]}</p>", unsafe_allow_html=True)
        
        # محاولات فحص عند نقاط استراتيجية
        if i in [30, 60, 90, 99]:
            status, data = check_report_status(st.session_state.user_email, st.session_state.user_code)
            if status == "READY":
                st.session_state.final_report = data
                st.session_state.page = "result"
                st.rerun()
        
        progress_bar.progress(i + 1)
        time.sleep(0.25) # زيادة طفيفة لزيادة الصبر الممنوح لنوشن
    
    st.info("التقرير يستغرق وقتاً أطول قليلاً من المعتاد لضمان الدقة.")
    if st.button("تحديث الحالة يدوياً 🔄"): st.rerun()

elif st.session_state.page == "result":
    st.success("✅ تم استخراج التقرير الاستراتيجي")
    st.write("---")
    st.markdown(st.session_state.final_report)
    st.write("---")
    if st.button("استعلام جديد 🔄"):
        st.session_state.can_analyze = False
        st.session_state.page = "query_page"
        st.rerun()

st.markdown("<p style='text-align:center; opacity:0.6; font-size:0.8rem; margin-top:2rem;'>جميع الحقوق محفوظة لـ شفق © 2026</p>", unsafe_allow_html=True)
