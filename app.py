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

# API Anahtarlarını Güvenli Şekilde Çekme
if "NOVAKEY" in st.secrets:
    # Anahtarları listeye al ve boşlukları temizle
    keys = [k.strip() for k in st.secrets["NOVAKEY"].split(",")]
else:
    st.error("⚠️ KRİTİK HATA: NOVAKEY Secrets kısmında bulunamadı Bedirhan. Lütfen anahtarları ekle.")
    st.stop()

# --- 2. GÖRSEL TASARIM (RGB FLOW & MODERN UI) ---
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
    .stChatMessage { border-radius: 20px; border: 1px solid #333; }
</style>
""", unsafe_allow_html=True)

# --- 3. AKILLI MOTOR (LOAD BALANCER & AUTO-RECOVERY) ---
def get_astra_response(user_input):
    """Bozuk veya kotası dolmuş anahtarları otomatik atlar."""
    # Her seferinde anahtarları karıştır ki yük dağılsın
    shuffled_keys = random.sample(keys, len(keys))
    
    for i, key in enumerate(shuffled_keys):
        try:
            genai.configure(api_key=key)
            model = genai.GenerativeModel('gemini-2.0-flash')
            
            # Kimlik tanımı (Sadece ilk mesajda)
            prefix = ""
            if len(st.session_state.messages) <= 1:
                prefix = "Ben AstraUltra, Bedirhan'ın (Exile) yarattığı bir yapay zeka. "
            
            response = model.generate_content(user_input)
            return prefix + response.text
            
        except Exception as e:
            error_msg = str(e).lower()
            # Eğer anahtarın süresi dolmuşsa veya kota bittiyse bir sonrakini dene
            if "api_key_invalid" in error_msg or "expired" in error_msg or "429" in error_msg:
                continue 
            else:
                return f"Beklenmedik teknik bir arıza: {str(e)}"
    
    return "🚫 Sistem uyarısı: Tüm enerji çekirdekleri (API Anahtarları) geçersiz veya kotaları dolmuş Bedirhan. Lütfen anahtarları yenile."

# --- 4. ANA ARAYÜZ ---
st.markdown("<div class='astra-header'>AstraUltra</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#7028e4;'>Exile Savunma Sistemleri Aktif</p>", unsafe_allow_html=True)

# Sohbet Geçmişi Yönetimi
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcı Girişi
if prompt := st.chat_input("Mesajınızı yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Enerji çekirdekleri taranıyor..."):
            full_response = get_astra_response(prompt)
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

# --- 5. YAN PANEL (DURUM MONİTÖRÜ) ---
with st.sidebar:
    st.title("🔱 Kontrol Paneli")
    st.write(f"**Yapımcı:** Bedirhan (Exile)")
    st.divider()
    st.write(f"🛰️ **Toplam Çekirdek:** {len(keys)}")
    st.success("Sistem Çevrimiçi")
    if st.button("Sohbeti Temizle"):
        st.session_state.messages = []
        st.rerun()
