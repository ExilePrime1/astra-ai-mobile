import streamlit as st
import google.generativeai as genai
import random

# --- 1. SİSTEM YAPILANDIRMASI ---
st.set_page_config(
    page_title="AstraUltra", 
    page_icon="🔱", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# API Anahtarlarını Secrets'tan Çekme
if "NOVAKEY" in st.secrets:
    keys = [k.strip() for k in st.secrets["NOVAKEY"].split(",")]
else:
    st.error("⚠️ HATA: NOVAKEY Secrets kısmında bulunamadı Bedirhan.")
    st.stop()

# --- 2. GÖRSEL TASARIM (RGB FLOW) ---
st.markdown("""
<style>
    .stApp { background-color: #000000; color: #e0e0e0; }
    .astra-header {
        font-family: 'Orbitron', sans-serif;
        font-size: 60px; font-weight: 900; text-align: center;
        background: linear-gradient(90deg, #00f2fe, #7028e4, #ff00c8, #00f2fe);
        background-size: 200% auto;
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        animation: flow 5s linear infinite;
        margin-bottom: 30px;
    }
    @keyframes flow { to { background-position: 200% center; } }
</style>
""", unsafe_allow_html=True)

# --- 3. AKILLI MOTOR ---
def get_astra_response(user_input):
    shuffled_keys = random.sample(keys, len(keys))
    
    for key in shuffled_keys:
        try:
            genai.configure(api_key=key)
            model = genai.GenerativeModel('gemini-2.0-flash')
            
            # Sadece ilk mesajda kimlik tanımı
            prefix = ""
            if len(st.session_state.messages) <= 1:
                prefix = "Ben AstraUltra, Bedirhan'ın (Exile) yarattığı bir yapay zeka. "
            
            response = model.generate_content(user_input)
            return prefix + response.text
        except Exception as e:
            if "429" in str(e):
                continue
            else:
                return f"Teknik bir hata: {str(e)}"
    
    return "🚫 Enerji çekirdekleri şu an meşgul Bedirhan."

# --- 4. ANA ARAYÜZ ---
st.markdown("<div class='astra-header'>AstraUltra</div>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Astraya bir mesaj gönder..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("İşleniyor..."):
            full_response = get_astra_response(prompt)
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

# Yan Panel
st.sidebar.title("🔱 AstraUltra")
st.sidebar.write("Yapımcı: **Bedirhan (Exile)**")
st.sidebar.write(f"Sistem Durumu: {len(keys)} Çekirdek Aktif")
