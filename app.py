import streamlit as st
import google.generativeai as genai

# --- 1. YAPILANDIRMA (GÜNCEL MODEL) ---
GOOGLE_API_KEY = "AIzaSyA34SS1f-QgCMzeuuoXSyjvtkQpjGhvgBI"
genai.configure(api_key=GOOGLE_API_KEY)

# Burayı 'gemini-1.5-flash' olarak güncelledik (Hata veren yer burasıydı)
model = genai.GenerativeModel('gemini-1.5-flash')

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

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Astra'ya her şeyi sor..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Astra'ya senin kimliğini öğretiyoruz
            full_prompt = f"Senin adın Astra. Seni Exile (Bedirhan) yarattı. Zeki, kısa ve öz cevaplar ver. Soru: {prompt}"
            response = model.generate_content(full_prompt)
            astra_reply = response.text
            st.markdown(astra_reply)
            st.session_state.messages.append({"role": "assistant", "content": astra_reply})
        except Exception as e:
            st.error(f"Hala bir sorun var: {str(e)}")
