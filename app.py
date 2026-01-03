import streamlit as st
import google.generativeai as genai

# --- 1. SİSTEM YAPILANDIRMASI ---
st.set_page_config(page_title="AstraUltra", page_icon="🔱", layout="wide")

# Tek anahtar çekme (Secrets'taki ilk anahtarı alır)
if "NOVAKEY" in st.secrets:
    # Virgülle ayrılmışsa ilkini, değilse direkt kendisini temizleyerek al
    raw_keys = st.secrets["NOVAKEY"].split(",")
    master_key = raw_keys[0].strip()
    genai.configure(api_key=master_key)
else:
    st.error("⚠️ Bedirhan, Secrets kısmında anahtar bulunamadı.")
    st.stop()

# --- 2. GÖRSEL TASARIM ---
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

# --- 3. TEK ÇEKİRDEK MOTOR ---
def get_astra_response(user_input):
    try:
        # En stabil model olan 2.0-flash-lite (Hızlı ve kotalara takılmaz)
        model = genai.GenerativeModel("models/gemini-2.0-flash-lite")
        
        # İlk mesaj kimliği
        prefix = ""
        if len(st.session_state.messages) <= 1:
            prefix = "Ben AstraUltra, Bedirhan'ın (Exile) yarattığı bir yapay zeka. "
            
        response = model.generate_content(user_input)
        return prefix + response.text
    except Exception as e:
        return f"🚨 Enerji Çekirdeği Hatası: {str(e)}"

# --- 4. ARAYÜZ ---
st.markdown("<div class='astra-header'>AstraUltra</div>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Bir komut ver Bedirhan..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("İşleniyor..."):
            res = get_astra_response(prompt)
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})
