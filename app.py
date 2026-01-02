import streamlit as st
import google.generativeai as genai

# --- 1. SİSTEM YAPILANDIRMASI ---
st.set_page_config(page_title="AstraUltra", page_icon="💫", layout="wide")

# API Anahtarı ve Model Tanımlama
if "NOVAKEY" in st.secrets:
    genai.configure(api_key=st.secrets["NOVAKEY"])
    astra_engine = genai.GenerativeModel('models/gemini-2.5-flash')
else:
    st.error("API ANAHTARI EKSİK!")
    st.stop()

# --- 2. GÖRSEL TASARIM (RGB FLOW CSS) ---
st.markdown("""
<style>
    .stApp { background: #000; color: #e0e0e0; }
    .astra-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 60px; font-weight: 900; text-align: center;
        background: linear-gradient(90deg, #00f2fe, #7028e4, #ff00c8, #00f2fe);
        background-size: 200% auto;
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        animation: flow 5s linear infinite;
        margin-bottom: 20px;
    }
    @keyframes flow { to { background-position: 200% center; } }
</style>
""", unsafe_allow_html=True)

# --- 3. ANA ARAYÜZ ---
st.markdown("<div class='astra-title'>AstraUltra</div>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesajları Görüntüle
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# Giriş Alanı: "Astraya sorun"
if prompt := st.chat_input("Astraya sorun"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Akıllı Kimlik: Sadece ilk soruda görünür
            prefix = ""
            if len(st.session_state.messages) <= 2:
                prefix = "Ben AstraUltra, Bedirhan'ın (Exile) yarattığı bir yapay zeka. "
            
            with st.spinner("Düşünüyor..."):
                context = f"Sen AstraUltra'sın. Seni Bedirhan (Exile) yarattı. Soru: {prompt}"
                response = astra_engine.generate_content(context)
                
                final_response = prefix + response.text
                st.markdown(final_response)
                st.session_state.messages.append({"role": "assistant", "content": final_response})

        except Exception as e:
            if "429" in str(e):
                st.warning("⚠️ Google kotası doldu. Lütfen bir süre sonra tekrar dene Bedirhan.")
            else:
                st.error(f"Teknik bir sorun oluştu: {e}")
