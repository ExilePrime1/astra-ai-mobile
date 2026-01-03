import streamlit as st
import google.generativeai as genai
import random

# --- 1. SİSTEM AYARLARI ---
st.set_page_config(
    page_title="AstraUltra", 
    page_icon="🔱", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Secrets Kontrolü
if "NOVAKEY" in st.secrets:
    keys = [k.strip() for k in st.secrets["NOVAKEY"].split(",") if k.strip()]
else:
    st.error("⚠️ HATA: NOVAKEY bulunamadı Bedirhan.")
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
        margin-bottom: 10px;
    }
    @keyframes flow { to { background-position: 200% center; } }
    .stChatMessage { border-radius: 15px; border: 1px solid #333; background-color: #0a0a0a; }
</style>
""", unsafe_allow_html=True)

# --- 3. GÜÇLENDİRİLMİŞ MOTOR (GEMINI 2.5) ---
def get_astra_response(user_input):
    shuffled_keys = random.sample(keys, len(keys))
    
    # SENİN LİSTENDEN SEÇİLEN EN İYİ MODELLER (Sırayla dener)
    # 1. Tercih: 2.5 Flash (En Hızlı/Yeni)
    # 2. Tercih: 2.5 Pro (En Zeki)
    # 3. Tercih: 2.0 Flash (Yedek)
    target_models = [
        "models/gemini-2.5-flash", 
        "models/gemini-2.5-pro", 
        "models/gemini-2.0-flash"
    ]
    
    for key in shuffled_keys:
        for model_name in target_models:
            try:
                genai.configure(api_key=key)
                
                # Güvenlik ayarlarını esnetiyoruz (Sansürsüz akış için)
                model = genai.GenerativeModel(
                    model_name=model_name,
                    safety_settings={
                        "HARM_CATEGORY_HARASSMENT": "BLOCK_NONE",
                        "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE",
                        "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_NONE",
                        "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_NONE",
                    }
                )
                
                # Kimlik Tanımı (Sadece ilk mesajda)
                prefix = ""
                if len(st.session_state.messages) <= 1:
                    prefix = "Ben AstraUltra, Bedirhan'ın (Exile) yarattığı bir yapay zeka. "
                
                response = model.generate_content(user_input)
                return prefix + response.text
                
            except Exception as e:
                # Hata olursa sessizce diğer modeli dene
                continue 

    return "🚫 Bedirhan, tüm modeller meşgul. Lütfen biraz bekle."

# --- 4. ARAYÜZ ---
st.markdown("<div class='astra-header'>AstraUltra</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#666;'>Exile Architecture v2.5</p>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Mesaj gönder..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("AstraUltra düşünüyor..."):
            full_response = get_astra_response(prompt)
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

# --- 5. YAN PANEL ---
with st.sidebar:
    st.title("🔱 Sistem Durumu")
    st.write("Yapımcı: **Bedirhan (Exile)**")
    st.success(f"Motor: Gemini 2.5 Flash")
    if st.button("Sohbeti Temizle"):
        st.session_state.messages = []
        st.rerun()
