import streamlit as st
import google.generativeai as genai

# --- 1. ASTRA ÇEKİRDEK (STABİL MODEL) ---
try:
    # Secrets panelindeki NOVAKEY'i çağırır
    ASTRA_CORE_KEY = st.secrets["NOVAKEY"] 
    genai.configure(api_key=ASTRA_CORE_KEY)
    
    # EN STABİL MODEL: 'gemini-pro'
    # Bu model 404 hatasını aşmak için en güvenli limandır.
    astra_engine = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error(f"⚠️ BAĞLANTI HATASI: {str(e)}")
    st.stop()

# --- 2. NOVA UI ---
st.set_page_config(page_title="Astra 3.0 Nova", page_icon="☄️")
st.markdown("""
<style>
    .stApp { background-color: #050508; color: #ffffff; }
    .astra-brand {
        font-family: 'Courier New', monospace;
        font-size: 50px;
        font-weight: bold;
        text-align: center;
        color: #00f2fe;
        text-shadow: 0 0 15px #7028e4;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. ERİŞİM SİSTEMİ ---
if "nova_access" not in st.session_state:
    st.session_state.nova_access = False

if not st.session_state.nova_access:
    st.markdown("<div class='astra-brand'>ASTRA 3.0</div>", unsafe_allow_html=True)
    password = st.text_input("Giriş Anahtarı:", type="password")
    if st.button("SİSTEMİ AÇ"):
        if password == "1234":
            st.session_state.nova_access = True
            st.rerun()
    st.stop()

# --- 4. SOHBET ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for msg in st.session_state.chat_history[-10:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if user_input := st.chat_input("Emret Exile..."):
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        try:
            # Yanıt oluşturma
            response = astra_engine.generate_content(f"Sen Astra'sın, seni Exile yarattı. Soru: {user_input}")
            st.markdown(response.text)
            st.session_state.chat_history.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"⚠️ KRİTİK HATA: {str(e)}")
