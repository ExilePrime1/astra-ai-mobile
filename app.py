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

# API Anahtarlarını Secrets'tan Çekme (Hata korumalı)
if "NOVAKEY" in st.secrets:
    # Anahtarları listeye al, temizle ve boş olanları ele
    keys = [k.strip() for k in st.secrets["NOVAKEY"].split(",") if k.strip()]
else:
    st.error("⚠️ KRİTİK HATA: Streamlit Secrets kısmında 'NOVAKEY' bulunamadı Bedirhan.")
    st.stop()

# --- 2. GÖRSEL TASARIM (EXILE STYLE) ---
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

# --- 3. AKILLI CEVAP MOTORU (DİNAMİK ÇEKİRDEK YÖNETİMİ) ---
def get_astra_response(user_input):
    # Anahtarları her seferinde karıştır (Yük dengeleme)
    shuffled_keys = random.sample(keys, len(keys))
    
    for i, key in enumerate(shuffled_keys):
        try:
            genai.configure(api_key=key)
            # En stabil model: gemini-1.5-flash
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # İlk mesajda kimlik tanımı
            prefix = ""
            if len(st.session_state.messages) <= 1:
                prefix = "Ben AstraUltra, Bedirhan'ın (Exile) yarattığı bir yapay zeka. "
            
            response = model.generate_content(user_input)
            return prefix + response.text
            
        except Exception as e:
            # Hataları gizlice sidebar'a yaz (Hata ayıklama için)
            st.sidebar.warning(f"⚠️ Çekirdek {i+1} atlandı: {str(e)[:40]}...")
            continue # Bir sonraki anahtarı dene
            
    return "🚫 Tüm enerji çekirdekleri reddedildi Bedirhan. Lütfen Secrets panelindeki anahtarlarını kontrol et."

# --- 4. ARAYÜZ ---
st.markdown("<div class='astra-header'>AstraUltra</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#555;'>Exile Yapay Zeka Sistemleri</p>", unsafe_allow_html=True)

# Sohbet Geçmişi
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Giriş ve İşleme
if prompt := st.chat_input("Bir mesaj gönder..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("İşleniyor..."):
            full_response = get_astra_response(prompt)
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

# --- 5. YAN PANEL (DURUM) ---
with st.sidebar:
    st.title("🔱 Kontrol Ünitesi")
    st.write(f"**Yapımcı:** Bedirhan (Exile)")
    st.divider()
    st.info(f"🛰️ Aktif Çekirdek Sayısı: {len(keys)}")
    if st.button("Hafızayı Temizle"):
        st.session_state.messages = []
        st.rerun()
