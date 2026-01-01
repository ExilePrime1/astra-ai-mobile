import streamlit as st
import google.generativeai as genai

# --- 1. YAPILANDIRMA ---
GOOGLE_API_KEY = "AIzaSyA34SS1f-QgCMzeuuoXSyjvtkQpjGhvgBI"
genai.configure(api_key=GOOGLE_API_KEY)

# Mevcut modelleri kontrol et ve en iyisini seç
def get_model():
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    # Tercih sıramız
    if 'models/gemini-1.5-flash' in available_models:
        return genai.GenerativeModel('gemini-1.5-flash')
    elif 'models/gemini-pro' in available_models:
        return genai.GenerativeModel('gemini-pro')
    else:
        # Eğer hiçbiri yoksa listedeki ilk uygun olanı seç
        return genai.GenerativeModel(available_models[0].replace('models/', ''))

model = get_model()

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
            # Astra kimliğini koruyarak yanıt al
            full_prompt = f"Senin adın Astra. Seni Exile (Bedirhan) yarattı. Soru: {prompt}"
            response = model.generate_content(full_prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Hata: {str(e)}")
