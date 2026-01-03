import streamlit as st
import google.generativeai as genai
import time
import random

# --- 1. SİSTEM YAPILANDIRMASI ---
st.set_page_config(page_title="AstraUltra", page_icon="🔱", layout="wide")

if "NOVAKEY" in st.secrets:
    keys = [k.strip() for k in st.secrets["NOVAKEY"].split(",") if k.strip()]
else:
    st.error("⚠️ NOVAKEY bulunamadı Bedirhan.")
    st.stop()

# --- 2. MOTOR (KOTA SAVAR) ---
def get_astra_response(user_input):
    shuffled_keys = random.sample(keys, len(keys))
    
    for key in shuffled_keys:
        try:
            genai.configure(api_key=key)
            # En az kota harcayan ve en hızlı model
            model = genai.GenerativeModel("models/gemini-2.0-flash-lite")
            
            response = model.generate_content(user_input)
            
            if response and response.text:
                return response.text
                
        except Exception as e:
            if "429" in str(e):
                # Kota dolmuşsa diğer anahtara geçmeden önce kısa bir mola
                time.sleep(1)
                continue
            else:
                return f"🚨 Teknik Hata: {str(e)[:50]}"
                
    return "🚫 Bedirhan, eklediğin TÜM anahtarların kotası dolmuş. Yeni anahtarlar eklemelisin."

# --- 3. ARAYÜZ ---
st.markdown("<h1 style='text-align: center; color: #7028e4;'>🔱 AstraUltra</h1>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Bir komut ver..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        res = get_astra_response(prompt)
        st.markdown(res)
        st.session_state.messages.append({"role": "assistant", "content": res})
