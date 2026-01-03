import streamlit as st
import google.generativeai as genai
import random

# --- 1. SİSTEM YAPILANDIRMASI ---
st.set_page_config(
    page_title="AstraUltra", 
    page_icon="🔱", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Anahtarlarını Secrets'tan Çekme
if "NOVAKEY" in st.secrets:
    keys = [k.strip() for k in st.secrets["NOVAKEY"].split(",") if k.strip()]
else:
    st.error("⚠️ KRİTİK HATA: NOVAKEY Secrets kısmında bulunamadı Bedirhan.")
    st.stop()

# --- 2. GÖRSEL TASARIM ---
st.markdown("""
<style>
    .stApp { background-color: #000000; color: #e0e0e0; }
    .astra-header {
        font-family: 'Orbitron', sans-serif;
        font-size: 60px; font-weight: 900; text-align: center;
        background: linear-gradient(90deg, #00f2fe, #7028e4, #ff00c8, #00f2fe);
        background-size: 200% auto;
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        animation: flow 5s linear infinite;
        margin-bottom: 5px;
    }
    @keyframes flow { to { background-position: 200% center; } }
    .stChatMessage { border-radius: 15px; border: 1px solid #222; background-color: #0a0a0a; }
</style>
""", unsafe_allow_html=True)

# --- 3. AKILLI CEVAP MOTORU (UNAVAILABLE KORUMALI) ---
def get_astra_response(user_input):
    shuffled_keys = random.sample(keys, len(keys))
    # Unavailable hatasını aşmak için denenecek model listesi
    model_variants = ['gemini-1.5-flash', 'gemini-1.5-pro']
    
    for key in shuffled_keys:
        for model_name in model_variants:
            try:
                genai.configure(api_key=key)
                
                # Güvenlik ayarlarını esnetiyoruz (Hata payını azaltır)
                safety = [
                    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
                ]
                
                model = genai.GenerativeModel(model_name=model_name, safety_settings=safety)
                
                # Kimlik tanımı
                prefix = ""
                if len(st.session_state.messages) <= 1:
                    prefix = "Ben AstraUltra, Bedirhan'ın (Exile) yarattığı bir yapay zeka. "
                
                response = model.generate_content(user_input)
                
                if response and response.text:
                    return prefix + response.text
                    
            except Exception as e:
                # "Unavailable" veya "404" gibi hataları yan panelde sessizce logla
                st.sidebar.write(f"⚠️ {model_name} Denendi: Hata alındı.")
                continue # Bir sonraki modele veya anahtara geç
                
    return "🚫 Bedirhan, tüm modeller şu an 'Unavailable' yanıtı veriyor. Lütfen anahtarları veya VPN durumunu kontrol et."

# --- 4. ANA ARAYÜZ ---
st.markdown("<div class='astra-header'>AstraUltra</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#555;'>Exile Yapay Zeka Sistemleri</p>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Bir komut ver..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Enerji çekirdekleri optimize ediliyor..."):
            full_response = get_astra_response(prompt)
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

# --- 5. YAN PANEL ---
with st.sidebar:
    st.title("🔱 Kontrol Ünitesi")
    st.write(f"**Yapımcı:** Bedirhan (Exile)")
    st.divider()
    st.info(f"🛰️ Aktif Çekirdek: {len(keys)}")
    if st.button("Hafızayı Temizle"):
        st.session_state.messages = []
        st.rerun()
