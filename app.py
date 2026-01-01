import streamlit as st
import google.generativeai as genai

# --- 1. YAPILANDIRMA (YENİ API ANAHTARIN) ---
GOOGLE_API_KEY = "AIzaSyA34SS1f-QgCMzeuuoXSyjvtkQpjGhvgBI"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

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

# --- 3. AKILLI SOHBET EKRANI ---
st.title("🚀 Astra Ultra")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesaj geçmişini göster
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcı sorusu
if prompt := st.chat_input("Astra'ya her şeyi sor..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gemini'den cevap al
    with st.chat_message("assistant"):
        try:
            # Astra'ya kimlik kazandırıyoruz
            full_prompt = f"Senin adın Astra. Seni Exile (Bedirhan) yarattı. Zeki ve yardımsever ol. Soru: {prompt}"
            response = model.generate_content(full_prompt)
            astra_reply = response.text
            st.markdown(astra_reply)
            st.session_state.messages.append({"role": "assistant", "content": astra_reply})
        except Exception as e:
            st.error(f"Bağlantı hatası: {str(e)}")
