import streamlit as st
import google.generativeai as genai
import random
import time

# --- 1. AYARLAR (BOŞLUKSUZ BAŞLA) ---
st.set_page_config(page_title="AstraUltra", page_icon="🔱", layout="wide")

# Secrets kontrolü
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
        font-size: 50px; font-weight: 900; text-align: center;
        background: linear-gradient(90deg, #00f2fe, #7028e4, #ff00c8);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. MOTOR ---
def get_astra_response(user_input):
    shuffled_keys = random.sample(keys, len(keys))
    model_pool = ["models/gemini-2.0-flash", "models/gemini-1.5-flash"]
    
    for key in shuffled_keys:
        try:
            genai.configure(api_key=key)
            for model_name in model_pool:
                try:
                    model = genai.GenerativeModel(model_name)
                    response = model.generate_content(user_input)
                    if response and response.text:
                        return response.text
                except:
                    continue
        except:
            continue
    return "🚫 Tüm hatlar meşgul Bedirhan, lütfen biraz bekle."

# --- 4. ARAYÜZ ---
st.markdown("<div class='astra-header'>AstraUltra</div>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Komut ver..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    with st.chat_message("assistant"):
        res = get_astra_response(prompt)
        st.markdown(res)
        st.session_state.messages.append({"role": "assistant", "content": res})
