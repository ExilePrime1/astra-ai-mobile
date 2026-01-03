import streamlit as st
import google.generativeai as genai
import random

# --- 1. YAPILANDIRMA ---
st.set_page_config(page_title="AstraUltra", page_icon="🔱", layout="wide")

if "NOVAKEY" in st.secrets:
    keys = [k.strip() for k in st.secrets["NOVAKEY"].split(",") if k.strip()]
else:
    st.error("⚠️ NOVAKEY bulunamadı Bedirhan.")
    st.stop()

# --- 2. TASARIM ---
st.markdown("""
<style>
    .stApp { background-color: #000000; color: #e0e0e0; }
    .astra-header {
        font-family: 'Orbitron', sans-serif;
        font-size: 55px; font-weight: 900; text-align: center;
        background: linear-gradient(90deg, #00f2fe, #7028e4, #ff00c8);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. HİBRİT MOTOR (HER ŞEYİ DENER) ---
def get_astra_response(user_input):
    shuffled_keys = random.sample(keys, len(keys))
    
    # Senin listendeki en mantıklı modellerden bir havuz oluşturduk
    # En yeniden en kararlıya doğru sıralı:
    model_pool = [
        "models/gemini-2.5-flash",
        "models/gemini-2.0-flash",
        "models/gemini-flash-latest",
        "models/gemini-2.0-flash-lite",
        "models/gemini-pro-latest"
    ]
    
    for key in shuffled_keys:
        genai.configure(api_key=key)
        for model_name in model_pool:
            try:
                model = genai.GenerativeModel(model_name)
                
                # Kimlik tanımı
                prefix = ""
                if len(st.session_state.messages) <= 1:
                    prefix = "Ben AstraUltra, Bedirhan'ın (Exile) yarattığı bir yapay zeka. "
                
                response = model.generate_content(user_input)
                if response and response.text:
                    return prefix + response.text
            except Exception:
                continue # Bu model veya anahtar hata verirse vakit kaybetmeden sonrakine geç
                
    return "🚫 Bedirhan, tüm hatlar (2.5, 2.0 ve Flash) şu an aşırı yoğun. 10 saniye sonra tekrar dene."

# --- 4. ARAYÜZ ---
st.markdown("<div class='astra-header'>AstraUltra</div>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Sisteme komut ver..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Enerji seviyesi ayarlanıyor..."):
            full_response = get_astra_response(prompt)
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
