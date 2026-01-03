import streamlit as st
import google.generativeai as genai
import random

# --- 1. AYARLAR ---
st.set_page_config(page_title="AstraUltra", page_icon="🔱", layout="wide")

if "NOVAKEY" in st.secrets:
    keys = [k.strip() for k in st.secrets["NOVAKEY"].split(",") if k.strip()]
else:
    st.error("⚠️ Secrets hatası: NOVAKEY yok.")
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
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. MOTOR (HEM YENİ HEM ESKİ MODEL DENER) ---
def get_astra_response(user_input):
    shuffled_keys = random.sample(keys, len(keys))
    
    # 1.5 çalışmazsa 1.0-pro devreye girer
    model_list = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-1.0-pro']
    
    for key in shuffled_keys:
        for model_name in model_list:
            try:
                genai.configure(api_key=key)
                model = genai.GenerativeModel(model_name)
                
                # Kimlik
                prefix = ""
                if len(st.session_state.messages) <= 1:
                    prefix = "Ben AstraUltra, Bedirhan'ın (Exile) yarattığı bir yapay zeka. "
                
                response = model.generate_content(user_input)
                return prefix + response.text
                
            except Exception as e:
                # Hatayı sidebar'a DETAYLI yaz (Debug için şart)
                st.sidebar.error(f"⚠️ {model_name} / {key[:5]}... -> HATA: {str(e)}")
                continue 
                
    return "🚫 Bedirhan, bağlantı kurulamadı. Sidebar'daki kırmızı hataları oku."

# --- 4. ARAYÜZ ---
st.markdown("<div class='astra-header'>AstraUltra</div>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Processing..."):
            full_response = get_astra_response(prompt)
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

with st.sidebar:
    st.write(f"🔑 Key Sayısı: {len(keys)}")
    if st.button("Reset"):
        st.session_state.messages = []
        st.rerun()
