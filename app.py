import streamlit as st
import google.generativeai as genai

# --- 1. ASTRA ÇEKİRDEK (404 SAVAR) ---
try:
    if "NOVAKEY" in st.secrets:
        genai.configure(api_key=st.secrets["NOVAKEY"])
        
        # Kökten çözüm: Model ismini en güncel ve tam yoluyla tanımlıyoruz.
        # Bu yazım şekli v1beta hatalarını genellikle tamamen bitirir.
        astra_engine = genai.GenerativeModel('models/gemini-1.5-flash-latest')
    else:
        st.error("⚠️ SİSTEM HATASI: NOVAKEY tanımlanmamış.")
        st.stop()
except Exception as e:
    st.error(f"⚠️ KRİTİK BAĞLANTI HATASI: {str(e)}")
    st.stop()

# --- 2. NOVA TASARIM ---
st.set_page_config(page_title="Astra 3.0 Nova", page_icon="☄️")
st.markdown("<style>.stApp { background-color: #050508; color: white; }</style>", unsafe_allow_html=True)

# --- 3. ERİŞİM SİSTEMİ ---
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("ASTRA 3.0")
    pw = st.text_input("Giriş:", type="password")
    if st.button("SİSTEMİ ATEŞLE"):
        if pw == "1234":
            st.session_state.auth = True
            st.rerun()
    st.stop()

# --- 4. SOHBET SİSTEMİ ---
st.subheader("Astra 3.0 Nova | Operatör: Exile")

if "msgs" not in st.session_state:
    st.session_state.msgs = []

for m in st.session_state.msgs:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Komut ver, Exile..."):
    st.session_state.msgs.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Sinyali güçlendirmek için açık talimat
            response = astra_engine.generate_content(f"Sen Astra'sın. Yaratıcın Exile (Bedirhan). Soru: {prompt}")
            st.markdown(response.text)
            st.session_state.msgs.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # Hata devam ederse model ismini otomatik değiştirmeyi dene:
            st.error(f"⚠️ SİNYAL KESİLDİ: {str(e)}")
            st.info("Eğer hala 404 ise, Google Cloud'da API'yi kapatıp açman gerekebilir.")
