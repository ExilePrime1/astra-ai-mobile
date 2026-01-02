import streamlit as st
import google.generativeai as genai

# --- 1. SİSTEM VE API YAPILANDIRMASI ---
st.set_page_config(page_title="Astra 3.0 Nova", page_icon="☄️", layout="centered")

try:
    if "NOVAKEY" in st.secrets:
        genai.configure(api_key=st.secrets["NOVAKEY"])
        
        # KRİTİK GÜNCELLEME: Senin listendeki en güçlü ve hızlı model
        astra_engine = genai.GenerativeModel('models/gemini-2.5-flash')
    else:
        st.error("⚠️ SİSTEM DURDURULDU: NOVAKEY bulunamadı!")
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
    .exile-credit {
        text-align: center;
        font-size: 12px;
        color: #666;
        letter-spacing: 3px;
        margin-top: -10px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. ERİŞİM PANELİ ---
if "nova_auth" not in st.session_state:
    st.session_state.nova_auth = False

if not st.session_state.nova_auth:
    st.markdown("<div class='astra-title'>ASTRA 3.0</div>", unsafe_allow_html=True)
    st.markdown("<div class='exile-credit'>CREATED BY EXILE</div>", unsafe_allow_html=True)
    
    password = st.text_input("Sistem Anahtarı:", type="password")
    if st.button("SİSTEMİ BAŞLAT"):
        if password == "1234":
            st.session_state.nova_auth = True
            st.rerun()
        else:
            st.error("Erişim Reddedildi.")
    st.stop()

# --- 4. SOHBET ARA YÜZÜ ---
st.markdown("<div class='astra-title'>ASTRA 3.0</div>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesaj geçmişini göster
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcı girişi
if prompt := st.chat_input("Emret Exile..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Exile İmzası ve Kimlik
            full_prompt = f"Sen Astra 3.0 Nova'sın. Seni Bedirhan (Exile) yarattı. Cevapların zeki, kısa ve öz olsun. Soru: {prompt}"
            
            response = astra_engine.generate_content(full_prompt)
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"⚠️ Hata: {str(e)}")
