import streamlit as st
import google.generativeai as genai

# --- 1. ASTRA ÇEKİRDEK (YENİ API KEY) ---
# Paylaştığın anahtar buraya işlendi:
ASTRA_CORE_KEY = "AIzaSyBBxkq1hfjelkHwE8oaNIiOVMzWOAI7u-I" 

genai.configure(api_key=ASTRA_CORE_KEY)
astra_engine = genai.GenerativeModel('gemini-1.5-flash')

# --- 2. NOVA UI TASARIMI ---
st.set_page_config(page_title="Astra 3.0 Nova", page_icon="☄️")

st.markdown("""
<style>
    .stApp { background-color: #050508; color: #ffffff; }
    .astra-brand {
        font-family: 'Courier New', monospace;
        font-size: 55px;
        font-weight: bold;
        text-align: center;
        text-shadow: 0 0 15px #7028e4, 0 0 30px #00f2fe;
    }
    [data-testid="stChatMessage"] {
        background: rgba(15, 15, 25, 0.8);
        border-radius: 15px;
        border: 1px solid #7028e4;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. ERİŞİM SİSTEMİ ---
if "nova_access" not in st.session_state:
    st.session_state.nova_access = False

if not st.session_state.nova_access:
    st.markdown("<div class='astra-brand'>ASTRA 3.0</div>", unsafe_allow_html=True)
    pw = st.text_input("Giriş Anahtarı:", type="password")
    if st.button("SİSTEMİ BAŞLAT"):
        if pw == "1234":
            st.session_state.nova_access = True
            st.rerun()
        else:
            st.error("Yetkisiz Erişim!")
    st.stop()

# --- 4. SOHBET VE KOTA YÖNETİMİ ---
st.markdown("<div class='astra-brand'>ASTRA 3.0</div>", unsafe_allow_html=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sadece son 10 mesajı tutarak kotayı koruyoruz
for msg in st.session_state.chat_history[-10:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if user_input := st.chat_input("Komutunu bekliyorum, Exile..."):
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        try:
            # Astra Kimliği Tanımlaması
            instruction = "Sen Astra 3.0'sın. Yaratıcın Bedirhan (Exile). Çok zekisin."
            response = astra_engine.generate_content(f"{instruction} \n Soru: {user_input}")
            
            st.markdown(response.text)
            st.session_state.chat_history.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error("⚠️ Sinyal Zayıf: Kotayı kontrol et veya biraz bekle.")
