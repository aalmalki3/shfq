import streamlit as st
import streamlit.components.v1 as components

# 1. إعداد الصفحة
st.set_page_config(page_title="شفق | SHFQ", page_icon="🌅", layout="centered")

# 2. التنسيق المحسن (CSS) لدمج الهوية مع الاستبيان
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

    /* إخفاء شعار ستريملت الزائد للتركيز على المحتوى */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# 3. عرض الشعار في المنتصف
col1, col2, col3 = st.columns([1, 1.5, 1])
with col2:
    try:
        st.image("assets/shfq.jpg", use_container_width=True)
    except:
        st.markdown("<h2 style='text-align:center;'>🌅 شفق</h2>", unsafe_allow_html=True)

# 4. النصوص التعريفية
st.markdown("<h1 class='stTitle'>مرحباً بك في شفق</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#2C4251; font-size:1.2rem;'>نورٌ هادئ، لمستقبلٍ مهنيٍ واضح. يرجى إكمال النموذج أدناه لرفع سيرتك الذاتية وبدء التحليل الاستراتيجي.</p>", unsafe_allow_html=True)
st.write("---")

# 5. تضمين استبيان تالي (Tally Embed)
# تم استخدام كود التضمين الخاص بك مع ميزة الطول الديناميكي
tally_embed_html = """
<iframe data-tally-src="https://tally.so/embed/lb7DVN?alignLeft=1&hideTitle=1&transparentBackground=1&dynamicHeight=1" 
loading="lazy" width="100%" height="1245" frameborder="0" marginheight="0" marginwidth="0" 
title="بنك السير الذاتية | CV Bank"></iframe>
<script>
var d=document,w="https://tally.so/widgets/embed.js",v=function(){"undefined"!=typeof Tally?Tally.loadEmbeds():d.querySelectorAll("iframe[data-tally-src]:not([src])").forEach((function(e){e.src=e.dataset.tallySrc}))};if("undefined"!=typeof Tally)v();else if(d.querySelector('script[src="'+w+'"]')==null){var s=d.createElement("script");s.src=w,s.onload=v,s.onerror=v,d.body.appendChild(s);}
</script>
"""

# عرض الاستبيان داخل حاوية ستريملت
components.html(tally_embed_html, height=1300, scrolling=True)

# 6. التذييل
st.write("---")
st.markdown("<p style='text-align:center; opacity:0.5; color:#0B1622;'>جميع الحقوق محفوظة - شفق 2026</p>", unsafe_allow_html=True)
