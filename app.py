import streamlit as st
import google.generativeai as genai

# --- 1. SİSTEM AYARLARI ---
# API Key sabitlendi
GOOGLE_API_KEY = "AIzaSyA34SS1f-QgCMzeuuoXSyjvtkQpjGhvgBI"
genai.configure(api_key=GOOGLE_API_KEY)

# 404 ve bağlantı hataları için en güvenli modelleme
@st.cache_resource
def load_astra():
    return genai.GenerativeModel('gemini-1.5-flash')

model = load_astra()

st.set_page_config(page_title="AstraUltra", page_icon="✨")

# --- 2. GALAXY ARAYÜZ (GÜVENLİ CSS) ---
st.markdown("""
<style>
    .stApp {
        background: radial-gradient(circle at top, #1a1a2e 0%, #080810 100%);
        color: #e0e0e0;
    }
    .astra-title {
        font-size: 45px;
        font-weight: 800;
        background: linear-gradient(45deg, #4facfe, #7028e4, #e5b2ca);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-top: 10px;
    }
    /* Tarayıcı hatalarını önlemek için sadeleştirilmiş giriş */
    .stChatInputContainer { border-radius: 25px !important; }
</style>
<div class='astra-title'>ASTRAULTRA</div>
""", unsafe_allow_html=True)

# --- 3. GİRİŞ KONTROLÜ ---
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    pwd = st.text_input("Sistem Anahtarı", type="password")
    if st.button("Sistemi Aç"):
        if pwd == "1234":
            st.session_state.auth = True
            st.rerun()
    st.stop()

# --- 4. SOHBET MANTIĞI ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Yıldızlara yaz..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Exile sistem talimatı
            full_prompt = f"Senin adın AstraUltra. Seni Exile (Bedirhan) yarattı. Zeki bir uzay asistanısın. Soru: {prompt}"
            response = model.generate_content(full_prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Bağlantı Hatası: Lütfen API anahtarını kontrol et veya 10 saniye bekle.")
