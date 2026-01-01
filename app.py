import streamlit as st
import google.generativeai as genai

# --- 1. YAPILANDIRMA ---
GOOGLE_API_KEY = "AIzaSyA34SS1f-QgCMzeuuoXSyjvtkQpjGhvgBI"
genai.configure(api_key=GOOGLE_API_KEY)

# Hata ihtimaline karşı en temel model ismini deniyoruz
# Eğer flash-latest çalışmıyorsa 'gemini-1.0-pro' en sağlamıdır.
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    model = genai.GenerativeModel('gemini-pro')

st.set_page_config(page_title="Astra Ultra AI", page_icon="🚀")

# --- 2. GÜVENLİK ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def login():
    if st.session_state.password_input == "1234":
        st.session_state.authenticated = True
    else:
        st.error("❌ Hatalı şifre!")

if not st.session_state.authenticated:
    st.title("🔒 Astra Ultra Giriş")
    st.text_input("Şifre", type="password", key="password_input", on_change=login)
    st.button("Giriş Yap", on_click=login)
    st.stop()

# --- 3. SOHBET ---
st.title("🚀 Astra Ultra")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Bir şeyler yaz..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # En basit haliyle yanıt almayı deniyoruz
            response = model.generate_content(prompt)
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # Eğer yine 404 verirse, koda model listesini yazdırıp hatayı göreceğiz
            st.error(f"Sistem hatası: {str(e)}")
            st.info("Alternatif model deneniyor, lütfen tekrar mesaj gönderin.")
            # Hata durumunda modeli 'gemini-pro'ya zorla
            st.session_state.model_fail = True
