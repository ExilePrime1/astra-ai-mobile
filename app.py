import streamlit as st
import google.generativeai as genai

# --- 1. YAPILANDIRMA ---
GOOGLE_API_KEY = "AIzaSyA34SS1f-QgCMzeuuoXSyjvtkQpjGhvgBI"
genai.configure(api_key=GOOGLE_API_KEY)

# AKILLI MODEL SEÇİCİ (404 HATASINI BİTİRİR)
@st.cache_resource
def load_astra_engine():
    try:
        # Önce en güncel modelleri listele
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        # Tercih sırasına göre model seç
        for target in ['models/gemini-1.5-flash-latest', 'models/gemini-1.5-flash', 'models/gemini-pro']:
            if target in models:
                return genai.GenerativeModel(target.replace('models/', ''))
        # Hiçbiri yoksa bulduğun ilk modeli al
        return genai.GenerativeModel(models[0].replace('models/', ''))
    except:
        return genai.GenerativeModel('gemini-1.5-flash')

model = load_astra_engine()

st.set_page_config(page_title="Astra Ultra AI", page_icon="🚀", layout="centered")

# --- 2. TASARIM ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    h1 { color: #a29bfe; text-align: center; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #6c5ce7; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. GÜVENLİK ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def login():
    if st.session_state.get("password_input") == "1234":
        st.session_state.authenticated = True
    else:
        st.error("❌ Şifre yanlış!")

if not st.session_state.authenticated:
    st.markdown("<h1>🔒 ASTRA ULTRA GİRİŞ</h1>", unsafe_allow_html=True)
    st.text_input("Şifre", type="password", key="password_input")
    st.button("Giriş", on_click=login)
    st.stop()

# --- 4. SOHBET ---
st.markdown("<h1>🚀 ASTRA ULTRA</h1>", unsafe_allow_html=True)
st.caption(f"Aktif Model: {model.model_name} | Geliştirici: Exile")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Merhaba Bedirhan! Astra hazır."}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Sorunuzu yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            full_prompt = f"Senin adın Astra. Seni Bedirhan (Exile) yarattı. Soru: {prompt}"
            response = model.generate_content(full_prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"⚠️ Kritik Hata: {str(e)}")

# --- 5. AYARLAR ---
with st.sidebar:
    st.title("⚙️ Ayarlar")
    st.write("🤖 **Sistem:** AstraUltra 2.0 Pro")
    st.write("👤 **Sahip:** Exile")
    if st.button("Geçmişi Sil"):
        st.session_state.messages = []
        st.rerun()
