import streamlit as st
import google.generativeai as genai
import time
import random

# --- 1. SİSTEM YAPILANDIRMASI ---
st.set_page_config(page_title="AstraUltra", page_icon="🔱", layout="wide")

if "NOVAKEY" in st.secrets:
    keys = [k.strip() for k in st.secrets["NOVAKEY"].split(",") if k.strip()]
else:
    st.error("⚠️ Bedirhan, Secrets kısmında anahtar yok.")
    st.stop()

# --- 2. TASARIM ---
st.markdown("<h1 style='text-align: center; color: #00f2fe;'>🔱 AstraUltra</h1>", unsafe_allow_html=True)

# --- 3. KOTA DOSTU MOTOR ---
def get_astra_response(user_input):
    # Anahtarları karıştır ama birini seç
    shuffled_keys = random.sample(keys, len(keys))
    
    for key in shuffled_keys:
        try:
            genai.configure(api_key=key)
            # En hafif ve en yüksek limitli model
            model = genai.GenerativeModel("models/gemini-1.5-flash")
            
            # Kimlik Tanımı
            prefix = ""
            if len(st.session_state.messages) <= 1:
                prefix = "Ben AstraUltra, Bedirhan'ın (Exile) yarattığı bir yapay zeka. "
            
            # Google sunucusuna nazikçe sor
            response = model.generate_content(user_input)
            
            if response and response.text:
                return prefix + response.text
                
        except Exception as e:
            # Hatanın detayını sadece sidebar'da gör (Kullanıcıyı yorma)
            st.sidebar.warning(f"Bir çekirdek hata verdi: {str(e)[:30]}")
            time.sleep(1) # Diğer anahtara geçmeden önce nefes al
            continue
            
    return "⚠️ Bedirhan, Google tüm anahtarlarını kilitledi. Lütfen 10-15 dakika sisteme dokunma, sonra uyanacağım."

# --- 4. ARAYÜZ ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Bir şeyler yaz..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Sistem yanıt bekliyor..."):
            res = get_astra_response(prompt)
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})
