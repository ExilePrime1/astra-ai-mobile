import streamlit as st
import google.generativeai as genai
import time
import random

# --- 1. SİSTEM YAPILANDIRMASI ---
st.set_page_config(page_title="AstraUltra", page_icon="🔱", layout="wide")

if "NOVAKEY" in st.secrets:
    # Birden fazla anahtarın varsa hepsini kullanır
    keys = [k.strip() for k in st.secrets["NOVAKEY"].split(",") if k.strip()]
else:
    st.error("⚠️ Bedirhan, NOVAKEY bulunamadı.")
    st.stop()

# --- 2. GÖRSEL TASARIM ---
st.markdown("""
<style>
    .stApp { background-color: #000000; color: #e0e0e0; }
    .astra-header {
        font-family: 'Orbitron', sans-serif;
        font-size: 50px; text-align: center;
        background: linear-gradient(90deg, #00f2fe, #7028e4, #ff00c8);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. AKILLI RETRY MOTORU ---
def get_astra_response(user_input):
    shuffled_keys = random.sample(keys, len(keys))
    
    for key in shuffled_keys:
        genai.configure(api_key=key)
        # Kota dostu model
        model = genai.GenerativeModel("models/gemini-1.5-flash")
        
        # 3 kez deneme hakkı
        for attempt in range(3):
            try:
                # Kimlik Tanımı
                prefix = ""
                if len(st.session_state.messages) <= 1:
                    prefix = "Ben AstraUltra, Bedirhan'ın (Exile) yarattığı bir yapay zeka. "
                
                response = model.generate_content(user_input)
                return prefix + response.text
                
            except Exception as e:
                if "429" in str(e):
                    # Kota hatasıysa 2 saniye uyu ve tekrar dene
                    time.sleep(2)
                    continue
                else:
                    break # Başka bir hataysa bu anahtarı terk et
                    
    return "🚫 Bedirhan, Google'ın ücretsiz kotası şu an çok daraldı. 30 saniye sonra tekrar dene."

# --- 4. ARAYÜZ ---
st.markdown("<div class='astra-header'>AstraUltra</div>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Mesajını bırak..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Kota limiti kontrol ediliyor..."):
            res = get_astra_response(prompt)
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})
