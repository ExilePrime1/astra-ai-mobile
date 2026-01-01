import streamlit as st
import google.generativeai as genai

# --- 1. CORE CONFIG (SİSTEM AYARLARI) ---
GOOGLE_API_KEY = "AIzaSyA34SS1f-QgCMzeuuoXSyjvtkQpjGhvgBI"
genai.configure(api_key=GOOGLE_API_KEY)

# Hata vermemesi için en kararlı modeli seçiyoruz
model = genai.GenerativeModel('gemini-1.5-flash-latest')

st.set_page_config(page_title="Astra Ultra AI", page_icon="🚀", layout="wide")

# --- 2. GEMINI STYLE CSS (ARAYÜZ TASARIMI) ---
st.markdown("""
    <style>
    /* Ana Arkaplan */
    .stApp { background-color: #131314; color: #e3e3e3; }
    
    /* Mesaj Balonları Tasarımı */
    .stChatMessage {
        background-color: #1e1f20;
        border-radius: 20px;
        padding: 15px;
        margin-bottom: 15px;
        border: 1px solid #333;
    }
    
    /* Kullanıcı Mesajı Farklı Renk */
    [data-testid="stChatMessageUser"] {
        background-color: #2b2c2f;
        border: 1px solid #444;
    }

    /* Giriş Alanı */
    .stChatInputContainer {
        background-color: #1e1f20 !important;
        border-radius: 30px !important;
    }

    /* Başlık ve Sidebar */
    h1 { font-family: 'Google Sans', sans-serif; font-weight: 500; color: #ffffff; }
    .stSidebar { background-color: #1e1f20 !important; border-right: 1px solid #333; }
    
    /* Buton Tasarımı */
    .stButton>button {
        background-color: #444746;
        color: white;
        border-radius: 20px;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #6c5ce7; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. GÜVENLİK (EXILE SİSTEMİ) ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def login():
    if st.session_state.password_input == "1234":
        st.session_state.authenticated = True
    else:
        st.error("❌ Şifre hatalı, Exile erişim izni vermedi.")

if not st.session_state.authenticated:
    st.markdown("<h1 style='text-align: center;'>Astra Ultra 2.0 Pro</h1>", unsafe_allow_html=True)
    with st.container():
        st.text_input("Sistem Şifresi", type="password", key="password_input")
        st.button("Sistemi Başlat", on_click=login)
    st.stop()

# --- 4. SOHBET MANTIĞI ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Üst Bilgi
st.markdown("<h2 style='color: #8ab4f8;'>Astra</h2>", unsafe_allow_html=True)
st.caption("AstraUltra 2.0 Pro | Powered by Exile")

# Mesajları Ekrana Yazdır
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcı Girişi
if prompt := st.chat_input("Buraya bir şeyler yazın..."):
    # Kullanıcı mesajını göster ve kaydet
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Astra'nın Yanıtı
    with st.chat_message("assistant"):
        with st.spinner("Astra yanıtlıyor..."):
            try:
                # Benim (Gemini) sistem talimatlarımı Astra'ya yüklüyoruz
                full_context = f"Senin adın Astra. Seni Exile (Bedirhan) yarattı. Sen zeki, profesyonel ve modern bir yapay zekasın. Yanıtların akıcı ve anlaşılır olsun. Soru: {prompt}"
                response = model.generate_content(full_context)
                
                if response.text:
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"⚠️ Sistem Hatası: {str(e)}")

# --- 5. SIDEBAR (AYARLAR) ---
with st.sidebar:
    st.markdown("<h2 style='color: #8ab4f8;'>Sistem Paneli</h2>", unsafe_allow_html=True)
    st.write("🤖 **Model:** AstraUltra 2.0 Pro")
    st.write("👤 **Sahip:** Exile")
    st.write("🟢 **Durum:** Bağlantı Kuruldu")
    st.divider()
    if st.button("Sohbeti Temizle"):
        st.session_state.messages = []
        st.rerun()
