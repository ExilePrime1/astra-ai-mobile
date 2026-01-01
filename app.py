import streamlit as st
import google.generativeai as genai

# --- 1. ÇEKİRDEK BAĞLANTISI ---
try:
    if "NOVAKEY" in st.secrets:
        # API Anahtarını Tanımla
        genai.configure(api_key=st.secrets["NOVAKEY"])
        
        # 404 HATASINI BİTİREN MODEL TANIMI
        # Eğer gemini-pro ve gemini-1.5-flash hata veriyorsa, 
        # sistemin en güncel 'flash' sürümünü açıkça belirtiyoruz.
        model_name = 'gemini-1.5-flash-latest' 
        astra_engine = genai.GenerativeModel(model_name)
    else:
        st.error("⚠️ SİSTEM HATASI: Secrets panelinde 'NOVAKEY' eksik.")
        st.stop()
except Exception as e:
    st.error(f"⚠️ KRİTİK BAĞLANTI HATASI: {str(e)}")
    st.stop()

# --- 2. GÖRSEL TASARIM ---
st.set_page_config(page_title="Astra 3.0 Nova", page_icon="☄️")
st.markdown("<style>.stApp { background-color: #050508; color: white; }</style>", unsafe_allow_html=True)

# --- 3. ERİŞİM SİSTEMİ ---
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("ASTRA 3.0")
    pw = st.text_input("Giriş:", type="password")
    if st.button("SİSTEMİ AÇ"):
        if pw == "1234":
            st.session_state.auth = True
            st.rerun()
    st.stop()

# --- 4. SOHBET ---
st.subheader("Astra 3.0 Nova | Operatör: Exile")

if "msgs" not in st.session_state:
    st.session_state.msgs = []

for m in st.session_state.msgs:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Komut ver..."):
    st.session_state.msgs.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # SİSTEM TALİMATI İLE BİRLİKTE GÖNDER
            full_text = f"Sen Astra'sın, yaratıcın Bedirhan (Exile). Cevap ver: {prompt}"
            response = astra_engine.generate_content(full_text)
            st.markdown(response.text)
            st.session_state.msgs.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # Hatanın tam nedenini görmek için detaylı mesaj
            st.error(f"⚠️ SİNYAL KESİLDİ: {str(e)}")
            st.info("Eğer hata 404 ise: AI Studio'da 'AstraNova Project'i seçip YENİ bir key almalısın.")
