import streamlit as st
import google.generativeai as genai
import time

# --- 1. CORE CONFIG ---
st.set_page_config(page_title="AstraUltra", page_icon="💫", layout="wide")

if "NOVAKEY" in st.secrets:
    genai.configure(api_key=st.secrets["NOVAKEY"])
    astra_engine = genai.GenerativeModel('models/gemini-2.5-flash')
else:
    st.error("API ANAHTARI EKSİK!")
    st.stop()

# --- 2. INFINITE RGB FLOW (CSS) ---
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(125deg, #000000, #050510, #0a0015, #000000);
        background-size: 400% 400%;
        animation: flowBG 15s ease infinite;
    }
    @keyframes flowBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .ultra-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 60px; font-weight: 900; text-align: center;
        background: linear-gradient(90deg, #00f2fe, #7028e4, #ff00c8, #00f2fe);
        background-size: 200% auto;
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        animation: ultra-glow 6s linear infinite;
    }
    @keyframes ultra-glow { to { background-position: 200% center; } }
    
    /* Zihin Yansıtma Kutusu */
    .thought-process {
        background: rgba(0, 242, 254, 0.05);
        border-left: 2px solid #7028e4;
        padding: 10px;
        font-family: 'Courier New', monospace;
        font-size: 13px;
        color: #00f2fe;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='ultra-title'>AstraUltra</div>", unsafe_allow_html=True)

# --- 3. SOHBET VE ZİHİN YANSITMA ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Astraya sorun"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # YENİ ÖZELLİK: ZİHİN YANSITMA (THOUGHT REFLECTION)
        thought_placeholder = st.empty()
        with thought_placeholder.container():
            st.markdown("<div class='thought-process'>🧬 <i>Zihin Yansıtma Aktif: Veri paketleri çözümleniyor...</i></div>", unsafe_allow_html=True)
            time.sleep(0.5)
            st.markdown("<div class='thought-process'>🧠 <i>Exile protokolü doğrulandı. Mantık çerçevesi kuruluyor...</i></div>", unsafe_allow_html=True)
            time.sleep(0.8)
        
        try:
            context = f"Sen AstraUltra'sın. Seni Bedirhan (Exile) yarattı. Soru: {prompt}"
            response = astra_engine.generate_content(context)
            
            thought_placeholder.empty() # Düşünme yazısını kaldır ve cevabı bas
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Bağlantı Hatası: {e}")
