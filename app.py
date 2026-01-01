import streamlit as st
import google.generativeai as genai

# --- 1. ÇEKİRDEK BAĞLANTISI ---
# Streamlit Secrets panelindeki "NOVAKEY" ismini kullanır.
try:
    if "NOVAKEY" in st.secrets:
        ASTRA_CORE_KEY = st.secrets["NOVAKEY"]
        genai.configure(api_key=ASTRA_CORE_KEY)
        # 404 hatasını önlemek için en güncel flash modelini seçiyoruz
        astra_engine = genai.GenerativeModel('gemini-1.5-flash')
    else:
        st.error("⚠️ SİSTEM HATASI: Streamlit Secrets panelinde 'NOVAKEY' bulunamadı.")
        st.stop()
except Exception as e:
    st.error(f"⚠️ BAĞLANTI HATASI: {str(e)}")
    st.stop()

# --- 2. GÖRSEL TASARIM (UI) ---
st.set_page_config(page_title="Astra 3.0 Nova", page_icon="☄️", layout="centered")

st.markdown("""
<style>
    .stApp { background-color: #050508; color: #ffffff; }
    .astra-title {
        font-family: 'Courier New', monospace;
        font-size: 50px;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(45deg, #00f2fe, #7028e4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    .exile-credit {
        text-align: center;
        font-size: 12px;
        color: #555;
        letter-spacing: 5px;
        margin-bottom: 30px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. ERİŞİM KONTROLÜ ---
if "nova_authenticated" not in st.session_state:
    st.session_state.nova_authenticated = False

if not st.session_state.nova_authenticated:
    st.markdown("<div class='astra-title'>ASTRA 3.0</div>", unsafe_allow_html=True)
    st.markdown("<div class='exile-credit'>CREATED BY EXILE</div>", unsafe_allow_html=True)
    
    password = st.text_input("Giriş Anahtarı:", type="password")
    if st.button("SİSTEMİ UYANDIR"):
        if password == "1234":
            st.session_state.nova_authenticated = True
            st.rerun()
        else:
            st.error("Hatalı Giriş.")
    st.stop()

# --- 4. SOHBET ARA YÜZÜ ---
st.markdown("<div class='astra-title'>ASTRA 3.0</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#00f2fe;'>Sinyal Gücü: Maksimum | Operatör: Exile</p>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesaj geçmişini ekrana bas
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcı girişi
if prompt := st.chat_input("Bir komut ver, Exile..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Astra'ya karakterini hatırlatıyoruz
            full_prompt = f"Sen Astra 3.0 Nova'sın. Seni Bedirhan (Exile) yarattı. Cevapların kısa, öz ve zekice olsun. Kullanıcı: {prompt}"
            response = astra_engine.generate_content(full_prompt)
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"⚠️ SİNYAL KESİLDİ: {str(e)}")
            st.info("İpucu: Google Cloud'da API'nin 'Enabled' olduğunu ve anahtarın doğru projeye bağlı olduğunu kontrol et.")
