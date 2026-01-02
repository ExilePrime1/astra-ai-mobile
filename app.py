import streamlit as st
import google.generativeai as genai

# --- 1. SİSTEM VE API YAPILANDIRMASI ---
st.set_page_config(page_title="Astra 3.0 Nova", page_icon="☄️", layout="centered")

try:
    if "NOVAKEY" in st.secrets:
        genai.configure(api_key=st.secrets["NOVAKEY"])
        
        # KRİTİK DEĞİŞİKLİK: 'models/' ön ekini kaldırıp sadece isim deniyoruz
        # Bazı API anahtarları 'gemini-1.5-flash' ismini bu şekilde kabul eder
        astra_engine = genai.GenerativeModel('gemini-1.5-flash')
    else:
        st.error("⚠️ SİSTEM DURDURULDU: şifre bulunamadı!")
        st.stop()
except Exception as e:
    st.error(f"⚠️ BAĞLANTI HATASI: {str(e)}")
    st.stop()

# --- 2. GÖRSEL TASARIM (CSS) ---
st.markdown("""
<style>
    .stApp { background-color: #050508; color: #ffffff; }
    .astra-title {
        font-family: 'Courier New', monospace;
        font-size: 55px;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(45deg, #00f2fe, #7028e4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. ERİŞİM PANELİ ---
if "nova_auth" not in st.session_state:
    st.session_state.nova_auth = False

if not st.session_state.nova_auth:
    st.markdown("<div class='astra-title'>ASTRA 3.0</div>", unsafe_allow_html=True)
    password = st.text_input("Sistem Anahtarı:", type="password")
    if st.button("Astra ile iletişime geç"):
        if password == "9900":
            st.session_state.nova_auth = True
            st.rerun()
    st.stop()

# --- 4. SOHBET ARA YÜZÜ ---
st.markdown("<div class='astra-title'>ASTRA 3.0</div>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Astra 3'e birşeyler sorun"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Bedirhan (Exile) tarafından yaratıldığı bilgisini modele veriyoruz
            full_prompt = f"Sen Astra 3.0 Nova'sın. Seni Bedirhan (Exile) yarattı. Soru: {prompt}"
            response = astra_engine.generate_content(full_prompt)
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # Hata mesajını daha detaylı gösteriyoruz ki nerede takıldığını görelim
            st.error(f"⚠️ Hata: {str(e)}")
            st.info("Eğer hala 404 ise, lütfen Google Cloud Console'dan 'Generative Language API' durumunu tekrar kontrol et.")
