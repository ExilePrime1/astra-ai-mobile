import streamlit as st
import google.generativeai as genai
import time

# --- 1. SİSTEM YAPILANDIRMASI (V3.7) ---
st.set_page_config(page_title="ASTRA LIVE v3.7", page_icon="🛸", layout="wide")

if "NOVAKEY" in st.secrets:
    genai.configure(api_key=st.secrets["NOVAKEY"])
    # Senin belirlediğin güçlü motor
    astra_engine = genai.GenerativeModel('models/gemini-2.5-flash')
else:
    st.error("⚠️ SİSTEM DURDURULDU: API ANAHTARI EKSİK!")
    st.stop()

# --- 2. ZORLAMALI CANLI TASARIM (CSS) ---
# Tarayıcının 'fotoğraf' gibi algılamasını engellemek için animasyon ekliyoruz
st.markdown("""
<style>
    /* Arka Planı Zorla Karart */
    .stApp {
        background-color: #050508 !important;
        background-image: radial-gradient(circle at center, #101020 0%, #050508 100%) !important;
        color: #00f2fe !important;
    }

    /* RGB BAŞLIK - SÜREKLİ HAREKETLİ */
    .astra-live-header {
        font-family: 'Courier New', monospace;
        font-size: 60px;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(90deg, #ff0000, #00ff00, #0000ff, #ff0000);
        background-size: 300% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: astra-flow 5s linear infinite;
        filter: drop-shadow(0 0 10px rgba(0, 242, 254, 0.3));
    }

    @keyframes astra-flow {
        0% { background-position: 0% center; }
        100% { background-position: 300% center; }
    }

    /* Mesaj Kutularına Cam Efekti Ver */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(0, 242, 254, 0.2) !important;
        border-radius: 20px !important;
        backdrop-filter: blur(10px);
    }
</style>
<div class="astra-live-header">ASTRA 3.0 NOVA</div>
<p style="text-align:center; color:#555; letter-spacing:8px; font-size:10px;">OPERATÖR: EXILE</p>
""", unsafe_allow_html=True)

# --- 3. ERİŞİM PANELİ ---
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    # Mobilde şık duran giriş alanı
    pw = st.text_input("ERİŞİM KODUNU GİR:", type="password")
    if st.button("SİSTEMİ UYANDIR"):
        if pw == "1234":
            st.session_state.auth = True
            st.rerun()
    st.stop()

# --- 4. SOHBET DİNAMİĞİ ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Emret Exile..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Bedirhan (Exile) kimliğini sisteme hatırlat
            full_prompt = f"Sen Astra 3.0 Nova'sın. Seni Bedirhan (Exile) yarattı. Cevapların zeki olsun. Soru: {prompt}"
            
            # Yazma animasyonu hissi vermek için
            response = astra_engine.generate_content(full_prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"⚠️ SİNYAL KESİLDİ: {str(e)}")
