import streamlit as st
import google.generativeai as genai
import time

# --- 1. SİSTEM TETİKLEYİCİ (V3.6) ---
# Bu başlık değiştikçe tarayıcı sayfayı yenilemek zorunda kalır.
st.set_page_config(page_title="ASTRA CORE v3.0", page_icon="⚡", layout="wide")

if "NOVAKEY" in st.secrets:
    genai.configure(api_key=st.secrets["NOVAKEY"])
    astra_engine = genai.GenerativeModel('models/gemini-2.5-flash')
else:
    st.error("⚠️ SİSTEM DURDURULDU: API ANAHTARI YOK!")
    st.stop()

# --- 2. ZORLAMALI (INLINE) TASARIM ---
# !important komutları tarayıcının eski ayarlarını geçersiz kılar.
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&display=swap');

    .stApp {
        background: #050508 !important;
        color: #00f2fe !important;
    }

    /* RGB BAŞLIK - CANLI ANİMASYON */
    .astra-header {
        font-family: 'Orbitron', sans-serif;
        font-size: clamp(40px, 8vw, 80px);
        font-weight: 900;
        text-align: center;
        background: linear-gradient(to right, #ff0000, #00ff00, #0000ff, #ff0000);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradient-flow 4s linear infinite;
    }

    @keyframes gradient-flow {
        0% { background-position: 0% center; }
        100% { background-position: 200% center; }
    }

    /* CANLI MESAJ KUTULARI */
    .stChatMessage {
        background: rgba(0, 242, 254, 0.05) !important;
        border: 1px solid #7028e4 !important;
        border-radius: 15px !important;
        box-shadow: 0 0 15px rgba(112, 40, 228, 0.2);
    }
</style>
<div class="astra-header">ASTRA 3.0</div>
<p style="text-align:center; color:#666; letter-spacing:5px;">OPERATÖR: EXILE</p>
""", unsafe_allow_html=True)

# --- 3. ERİŞİM VE SOHBET ---
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    pw = st.text_input("SİSTEM ŞİFRESİ:", type="password")
    if st.button("SİSTEME GİRİŞ YAP"):
        if pw == "1234":
            st.session_state.auth = True
            st.rerun()
    st.stop()

# Sohbet Alanı
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("sorularını bana sor..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Exile bilgisi sisteme gömülü
            context = f"Sen Astra'sın. Seni Bedirhan (Exile) yarattı. Soru: {prompt}"
            resp = astra_engine.generate_content(context)
            st.markdown(resp.text)
            st.session_state.messages.append({"role": "assistant", "content": resp.text})
        except Exception as e:
            st.error(f"Sinyal Hatası: {e}")
