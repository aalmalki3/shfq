import streamlit as st
import streamlit.components.v1 as components
import requests
import time

# 1. إعداد الصفحة
st.set_page_config(page_title="شفق | SHFQ", page_icon="🌅", layout="centered")

# --- 2. دالة جلب البيانات (Direct API Request) ---
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
                    {"property": "Access Code", "number": {"equals": int(access_code)}}
                ]
            }
        }
        
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        
        if response.status_code != 200:
            return "ERROR", data.get("message", "خطأ في الاتصال بنوشن")

        results = data.get("results", [])
        if not results:
            return "NOT_FOUND", None
            
        for res in results:
            props = res.get("properties", {})
            n_name_list = props.get("Full Name", {}).get("title", [])
            
            if n_name_list:
                page_id = res["id"]
                # جلب محتوى التقرير (Blocks) عبر API مباشر
                blocks_url = f"https://api.notion.com/v1/blocks/{page_id}/children"
                blocks_resp = requests.get(blocks_url, headers=headers)
                blocks_data = blocks_resp.json()
                
                report_text = ""
                for block in blocks_data.get("results", []):
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

# --- 3. التصميم (Modern UI) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    html, body, [data-testid="stAppViewContainer"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
    .block-container { background-color: rgba(255, 255, 255, 0.95); border-radius: 24px; padding: 3rem 2rem !important; box-shadow: 0 20px 40px rgba(0,0,0,0.05); margin-top: 2rem; }
    .stButton>button { width: 100%; border-radius: 12px; height: 3.5rem; background-color: #2c4251 !important; color: white !important; font-weight: 600; transition: all 0.3s ease; }
    .stButton>button:hover { background-color: #0b1622 !important; transform: translateY(-2px); }
    #MainMenu, footer, header { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

# 4. منطق إدارة الصفحات
if "page" not in st.session_state:
    st.session_state.page = "main"

if st.session_state.page == "main":
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        try: st.image("assets/shfq.jpg", use_container_width=True)
        except: st.markdown("<h1 style='text-align:center;'>🌅 شفق</h1>", unsafe_allow_html=True)
    
    tally_embed = '<iframe data-tally-src="https://tally.so/embed/lb7DVN?alignLeft=1&hideTitle=1&transparentBackground=1&dynamicHeight=1" loading="lazy" width="100%" height="800" frameborder="0"></iframe><script src="https://tally.so/widgets/embed.js"></script>'
    components.html(tally_embed, height=800, scrolling=True)
    
    if st.button("🔍 استخراج تقريري الآن"):
        st.session_state.page = "query_page"
        st.rerun()

elif st.session_state.page == "query_page":
    st.markdown("<h3 style='text-align:center;'>🛡️ مركز الاستعلام الآمن</h3>", unsafe_allow_html=True)
    email_in = st.text_input("البريد الإلكتروني المعتمد:")
    code_in = st.text_input("كود الاستعلام الخاص بك:", type="password")
    
    if st.button("التحقق من البيانات ⚡"):
        if email_in and code_in:
            with st.spinner("جاري الاتصال بقاعدة البيانات..."):
                status, data = check_report_status(email_in, code_in)
                if status == "NOT_FOUND":
                    st.error("❌ لم نجد سجلات تطابق هذه البيانات.")
                elif status == "ERROR":
                    st.warning(f"⚠️ خطأ: {data}")
                else:
                    st.success("✅ تم العثور على سجلّك بنجاح.")
                    st.session_state.user_email = email_in
                    st.session_state.user_code = code_in
                    st.session_state.can_analyze = True
        else: st.warning("يرجى تعبئة جميع الحقول.")

    if st.session_state.get("can_analyze"):
        if st.button("إصدار ومعالجة التقرير 🚀"):
            st.session_state.page = "waiting"
            st.rerun()
    
    if st.button("↩️ العودة"):
        st.session_state.page = "main"
        st.rerun()

elif st.session_state.page == "waiting":
    st.markdown("<h3 style='text-align:center;'>الذكاء الاصطناعي يحلل بياناتك...</h3>", unsafe_allow_html=True)
    progress_bar = st.progress(0)
    for p in range(1, 101):
        if p % 20 == 0:
            status, data = check_report_status(st.session_state.user_email, st.session_state.user_code)
            if status == "READY":
                st.session_state.final_report = data
                st.session_state.page = "result"
                st.rerun()
        progress_bar.progress(p)
        time.sleep(0.3)
    st.info("التقرير لم يجهز بعد.")
    if st.button("تحديث الحالة 🔄"): st.rerun()

elif st.session_state.page == "result":
    st.success("✅ تقريرك جاهز الآن")
    st.markdown(st.session_state.final_report)
    if st.button("استعلام جديد 🔄"):
        st.session_state.can_analyze = False
        st.session_state.page = "query_page"
        st.rerun()
