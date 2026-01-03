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

# Secrets'tan anahtarları güvenli çekme
if "NOVAKEY" in st.secrets:
    # Boşlukları ve gizli karakterleri temizle
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
    .stChatMessage { border-radius: 15px; border: 1px solid #222; }
</style>
""", unsafe_allow_html=True)

# --- 3. AKILLI CEVAP MOTORU (404 VE 429 KORUMALI) ---
def get_astra_response(user_input):
    shuffled_keys = random.sample(keys, len(keys))
    
    for i, key in enumerate(shuffled_keys):
        try:
            # Yapılandırma
            genai.configure(api_key=key)
            
            # 404 HATASINI ÖNLEYEN KRİTİK SATIR:
            # Model ismini tam yol (full path) olmadan yazıyoruz
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Kimlik tanımı
            prefix = ""
            if len(st.session_state.messages) <= 1:
                prefix = "Ben AstraUltra, Bedirhan'ın (Exile) yarattığı bir yapay zeka. "
            
            # İçerik üretimi
            response = model.generate_content(user_input)
            
            if response and response.text:
                return prefix + response.text
            else:
                continue
                
        except Exception as e:
            # Hatayı yan panelde göster (Sadece debug için)
            error_msg = str(e)
            st.sidebar.warning(f"⚠️ Çekirdek {i+1} Denendi: {error_msg[:50]}...")
            continue # Hata ne olursa olsun bir sonraki anahtara geç
            
    return "🚫 Bedirhan, tüm enerji çekirdekleri (API Keys) reddedildi. Lütfen anahtarları ve model iznini kontrol et."

# --- 4. ANA ARAYÜZ ---
st.markdown("<div class='astra-header'>AstraUltra</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#555;'>Exile Yapay Zeka Sistemleri</p>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Mesajınızı buraya bırakın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Enerji çekirdekleri sorgulanıyor..."):
            full_response = get_astra_response(prompt)
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

# --- 5. YAN PANEL ---
with st.sidebar:
    st.title("🔱 Kontrol Ünitesi")
    st.write(f"**Yapımcı:** Bedirhan (Exile)")
    st.divider()
    st.info(f"🛰️ Çekirdek Sayısı: {len(keys)}")
    if st.button("Hafızayı Sıfırla"):
        st.session_state.messages = []
        st.rerun()
