import streamlit as st
import google.generativeai as genai

# --- 1. ÇEKİRDEK AYARLARI ---
try:
    if "NOVAKEY" in st.secrets:
        genai.configure(api_key=st.secrets["NOVAKEY"])
        # En stabil model ismi
        astra_engine = genai.GenerativeModel('gemini-1.5-flash')
    else:
        st.error("⚠️ Secrets panelinde NOVAKEY eksik!")
        st.stop()
except Exception as e:
    st.error(f"⚠️ Hata: {str(e)}")
    st.stop()

# --- 2. ASTRA ARAYÜZÜ ---
st.set_page_config(page_title="Astra 3.0 Nova", page_icon="☄️")
st.markdown("<style>.stApp { background-color: #050508; color: white; }</style>", unsafe_allow_html=True)

if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("ASTRA 3.0")
    pw = st.text_input("Şifre:", type="password")
    if st.button("SİSTEMİ ATEŞLE"):
        if pw == "1234":
            st.session_state.auth = True
            st.rerun()
    st.stop()

# --- 3. SOHBET ---
st.subheader("Astra 3.0 Nova | Operatör: Exile")

if "msgs" not in st.session_state:
    st.session_state.msgs = []

for m in st.session_state.msgs:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Emret Exile..."):
    st.session_state.msgs.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = astra_engine.generate_content(f"Sen Astra'sın, yaratıcın Exile. Cevap ver: {prompt}")
            st.markdown(response.text)
            st.session_state.msgs.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"⚠️ Sinyal Hatası: {str(e)}")
