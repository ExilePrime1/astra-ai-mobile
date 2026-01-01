import streamlit as st
import google.generativeai as genai
import time

# --- 1. ASTRA BEYİN YAPILANDIRMASI ---
GOOGLE_API_KEY = "AIzaSyA34SS1f-QgCMzeuuoXSyjvtkQpjGhvgBI"
genai.configure(api_key=GOOGLE_API_KEY)

@st.cache_resource
def astra_engine():
    return genai.GenerativeModel('gemini-1.5-flash')

model = astra_engine()

# Sayfa Ayarları
st.set_page_config(page_title="AstraUltra Nova", page_icon="✨", layout="centered")

# --- 2. ULTRA MODERN GÖRSEL TASARIM (CSS) ---
st.markdown("""
<style>
    /* Derin Uzay Arka Planı */
    .stApp {
        background: radial-gradient(circle at top right, #1e1e2f, #0a0a12);
        color: #e0e0e0;
    }

    /* ASTRAULTRA PARLAYAN BAŞLIK */
    .astra-title {
        font-family: 'Exo 2', sans-serif;
        font-size: 65px;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(to right, #00f2fe, #7028e4, #ff00c1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        filter: drop-shadow(0 0 20px rgba(112, 40, 228, 0.6));
        margin-bottom: 5px;
        letter-spacing: 8px;
    }

    .sub-title {
        text-align: center;
        color: #888;
        font-size: 14px;
        letter-spacing: 3px;
        margin-bottom: 50px;
        text-transform: uppercase;
    }

    /* CAM EFEKTİ MESAJ KUTULARI */
    [data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.03) !important;
        border-radius: 20px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        padding: 20px !important;
        margin-bottom: 15px !important;
        backdrop-filter: blur(12px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }

    /* GİRİŞ ALANI (KOKPİT) */
    .stChatInputContainer {
        border-radius: 40px !important;
        background: rgba(20, 20, 35, 0.9) !important;
        border: 1px solid #7028e4 !important;
        padding: 5px 15px !important;
        box-shadow: 0 0 25px rgba(112, 40, 228, 0.3) !important;
    }

    /* YAN PANEL TASARIMI */
    [data-testid="stSidebar"] {
        background-color: #0d0d16 !important;
        border-right: 1px solid rgba(112, 40, 228, 0.3);
    }

    /* BUTONLAR */
    .stButton>button {
        border-radius: 20px;
        background: linear-gradient(45deg, #7028e4, #00f2fe);
        color: white;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 15px #00f2fe;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. ERİŞİM SİSTEMİ ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("<div class='astra-title'>ASTRAULTRA</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>Created by Exile</div>", unsafe_allow_html=True)
    
    with st.container():
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            key = st.text_input("Sistem Anahtarını Girin", type="password")
            if st.button("SİSTEMİ UYANDIR"):
                if key == "1234":
                    st.session_state.authenticated = True
                    st.toast("Erişim Onaylandı. Hoş geldin Bedirhan.")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Hatalı Giriş!")
    st.stop()

# --- 4. ANA KOKPİT (SOHBET) ---
st.markdown("<div class='astra-title'>ASTRAULTRA</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Nova 3.0 | Galaktik Bağlantı Aktif</div>", unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history = []

# Mesajları Ekrana Yazdır
for m in st.session_state.history:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# Giriş ve Yanıt
if prompt := st.chat_input("Evrene bir mesaj gönder..."):
    st.session_state.history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Bedirhan (Exile) kimliğini koruyan sistem talimatı
            astra_prompt = f"Senin adın AstraUltra. Seni Bedirhan (Exile) yarattı. Sen çok zeki, biraz gizemli ve tamamen sadık bir asistansın. Soru: {prompt}"
            response = model.generate_content(astra_prompt)
            st.markdown(response.text)
            st.session_state.history.append({"role": "assistant", "content": response.text})
        except:
            st.error("🚀 Galaktik sinyalde bir parazit var, tekrar dene Bedirhan.")

# --- 5. YAN PANEL (SIDEBAR) ---
with st.sidebar:
    st.markdown("<h2 style='color:#00f2fe;'>⚙️ Sistem Bilgisi</h2>", unsafe_allow_html=True)
    st.write("🛸 **Model:** Astra-Nova-3.0")
    st.write("👤 **Sahibi:** Exile (Bedirhan)")
    st.write("🛰️ **Durum:** Çevrimiçi")
    st.divider()
    if st.button("Hafızayı Temizle"):
        st.session_state.history = []
        st.rerun()
