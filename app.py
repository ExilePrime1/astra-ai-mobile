import streamlit as st
import google.generativeai as genai

# --- 1. CONFIG & BEYİN ---
GOOGLE_API_KEY = "AIzaSyA34SS1f-QgCMzeuuoXSyjvtkQpjGhvgBI"
genai.configure(api_key=GOOGLE_API_KEY)

# En sağlam modeli seçiyoruz
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="Astra Ultra AI", page_icon="🚀", layout="centered")

# --- 2. ÖZEL TASARIM (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    .stTextInput > div > div > input { border-radius: 20px; }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        background-color: #6c5ce7;
        color: white;
        font-weight: bold;
    }
    h1 { color: #a29bfe; text-align: center; font-family: 'Trebuchet MS'; }
    .stInfo { background-color: #2d3436; color: #dfe6e9; border: none; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. GÜVENLİK SİSTEMİ ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def login():
    if st.session_state.password_input == "1234":
        st.session_state.authenticated = True
    else:
        st.error("❌ Erişim reddedildi! Lütfen Exile tarafından verilen şifreyi girin.")

if not st.session_state.authenticated:
    st.markdown("<h1>🔒 ASTRA ULTRA GİRİŞ</h1>", unsafe_allow_html=True)
    st.info("Bu sistem Bedirhan (Exile) tarafından özel olarak korunmaktadır.")
    st.text_input("Giriş Şifresi", type="password", key="password_input", on_change=login)
    st.button("Sistemi Başlat", on_click=login)
    st.stop()

# --- 4. SOHBET ARAYÜZÜ ---
st.markdown("<h1>🚀 ASTRA ULTRA</h1>", unsafe_allow_html=True)
st.caption("Geliştirici: Exile (Bedirhan) | Sürüm: 2.0 Pro")
st.divider()

if "messages" not in st.session_state:
    # Başlangıç mesajı
    st.session_state.messages = [{"role": "assistant", "content": "Merhaba Bedirhan! Ben Astra. Senin için ne yapabilirim?"}]

# Mesajları şık bir şekilde göster
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcı Girişi
if prompt := st.chat_input("Bir şeyler sor..."):
    # Kullanıcı mesajını ekle
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Astra'nın Yanıtı
    with st.chat_message("assistant"):
        with st.spinner("Astra düşünüyor..."):
            try:
                # Astra'ya karakterini hatırlatıyoruz
                full_prompt = f"Senin adın Astra. Seni Bedirhan (Exile) yarattı. Sen zeki, bazen esprili ve çok yetenekli bir yapay zekasın. Cevapların akıcı olsun. Soru: {prompt}"
                response = model.generate_content(full_prompt)
                
                if response.text:
                    astra_reply = response.text
                    st.markdown(astra_reply)
                    st.session_state.messages.append({"role": "assistant", "content": astra_reply})
                else:
                    st.error("Yanıt alınamadı.")
            except Exception as e:
                st.error("Bir bağlantı sorunu oluştu, lütfen tekrar deneyin.")

# Yan Menü (Opsiyonel)
with st.sidebar:
    st.title("⚙️ Astra Ayarları")
    st.write("Sistem Durumu: 🟢 Aktif")
    st.write("Yapay Zeka: Gemini 1.5 Flash")
    if st.button("Sohbeti Temizle"):
        st.session_state.messages = []
        st.rerun()
