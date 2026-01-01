import streamlit as st
import google.generativeai as genai

# --- 1. SİSTEM YAPILANDIRMASI ---
GOOGLE_API_KEY = "AIzaSyA34SS1f-QgCMzeuuoXSyjvtkQpjGhvgBI"
genai.configure(api_key=GOOGLE_API_KEY)

# 404 Hatasını Önlemek İçin Model Seçici
@st.cache_resource
def get_model():
    # En güvenli model ismini kullanıyoruz
    return genai.GenerativeModel('gemini-1.5-flash')

model = get_model()

st.set_page_config(page_title="Astra Ultra", page_icon="🚀", layout="wide")

# --- 2. GERÇEK GEMINI CSS TASARIMI ---
st.markdown("""
<style>
    .stApp { background-color: #131314; color: #e3e3e3; font-family: 'Google Sans', sans-serif; }
    header {visibility: hidden;}
    .main .block-container {padding-top: 1rem; max-width: 850px;}
    
    /* Mesajlar */
    [data-testid="stChatMessage"] { background-color: transparent; padding: 1rem 0; border: none; }
    
    /* OVAL ALT GİRİŞ BARI */
    .stChatInputContainer {
        position: fixed;
        bottom: 30px;
        background-color: #1e1f20 !important;
        border: 1px solid #3c4043 !important;
        border-radius: 35px !important;
        padding: 5px 20px !important;
    }
    .stChatInputContainer textarea { color: #e3e3e3 !important; }

    /* Logo ve Başlık */
    .astra-logo {
        font-size: 38px;
        font-weight: 600;
        background: linear-gradient(to right, #4285f4, #9b72cb, #d96570);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 40px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. GÜVENLİK ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("<div class='astra-logo'>ASTRA ULTRA</div>", unsafe_allow_html=True)
    pwd = st.text_input("Giriş Şifresi", type="password")
    if st.button("Sistemi Başlat"):
        if pwd == "1234":
            st.session_state.authenticated = True
            st.rerun()
        else: st.error("Hatalı!")
    st.stop()

# --- 4. SOHBET ---
st.markdown("<div class='astra-logo'>Astra</div>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Astra'ya bir şeyler sor..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Astra'nın kimliğini hatırlatıyoruz
            full_context = f"Senin adın Astra. Seni Bedirhan (Exile) yarattı. Soru: {prompt}"
            response = model.generate_content(full_context)
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # Eğer yine model hatası verirse daha basit bir hata mesajı göster
            st.error("🚀 Astra uyanıyor, lütfen 5 saniye bekleyip tekrar yaz.")

# --- 5. SIDEBAR ---
with st.sidebar:
    st.title("⚙️ Ayarlar")
    st.write("🤖 **Model:** AstraUltra 2.0 Pro")
    st.write("👤 **Sahip:** Exile")
    if st.button("Sohbeti Temizle"):
        st.session_state.messages = []
        st.rerun()
