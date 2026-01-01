import streamlit as st
import google.generativeai as genai

# --- 1. YAPILANDIRMA ---
GOOGLE_API_KEY = "AIzaSyA34SS1f-QgCMzeuuoXSyjvtkQpjGhvgBI"
genai.configure(api_key=GOOGLE_API_KEY)

# Hata ihtimaline karşı en güncel model ismini kullanıyoruz
MODEL_NAME = 'gemini-1.5-flash-latest' 
model = genai.GenerativeModel(MODEL_NAME)

st.set_page_config(page_title="Astra Ultra AI", page_icon="🚀")

# --- 2. GÜVENLİK (ŞİFRE) ---
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

# --- 3. SOHBET EKRANI ---
st.title("🚀 Astra Ultra")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Mesajınızı yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Sistem talimatını buraya ekliyoruz
            full_prompt = f"Senin adın Astra. Seni Exile (Bedirhan) yarattı. Zeki ol. Soru: {prompt}"
            response = model.generate_content(full_prompt)
            
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.error("Astra şu an cevap üretemedi.")
        except Exception as e:
            st.error(f"Bağlantı Hatası: {str(e)}")
            st.info("İpucu: Eğer 404 hatası devam ediyorsa, API anahtarının Google AI Studio'da aktif olduğundan emin olun.")
