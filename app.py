import streamlit as st
import google.generativeai as genai

# --- 1. ASTRA ÇEKİRDEK ---
try:
    # Secrets panelindeki NOVAKEY'i kullanır
    ASTRA_CORE_KEY = st.secrets["NOVAKEY"] 
    genai.configure(api_key=ASTRA_CORE_KEY)
    # Model ismini 'models/' ön eki ve '-latest' son ekiyle tam tanımladık
    astra_engine = genai.GenerativeModel('models/gemini-1.5-flash-latest')
except Exception as e:
    st.error(f"⚠️ BAĞLANTI HATASI: {str(e)}")
    st.stop()

# --- 2. NOVA UI ---
st.set_page_config(page_title="Astra 3.0 Nova", page_icon="☄️")
st.markdown("<style>.stApp { background-color: #050508; color: #ffffff; }</style>", unsafe_allow_html=True)

# --- 3. ERİŞİM SİSTEMİ ---
if "nova_access" not in st.session_state:
    st.session_state.nova_access = False

if not st.session_state.nova_access:
    st.title("ASTRA 3.0")
    password = st.text_input("Giriş:", type="password")
    if st.button("SİSTEMİ ATEŞLE"):
        if password == "1234":
            st.session_state.nova_access = True
            st.rerun()
    st.stop()

# --- 4. SOHBET MOTORU ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for msg in st.session_state.chat_history[-10:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if user_input := st.chat_input("Komut ver, Exile..."):
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        try:
            response = astra_engine.generate_content(f"Sen Astra'sın, yaratıcın Exile. Soru: {user_input}")
            st.markdown(response.text)
            st.session_state.chat_history.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"⚠️ SİNYAL KESİLDİ: {str(e)}")
