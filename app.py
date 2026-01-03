import streamlit as st
import google.generativeai as genai
import random
import time

# --- 1. SİSTEM YAPILANDIRMASI ---
st.set_page_config(
    page_title="AstraUltra", 
    page_icon="🔱", 
    layout="wide"
)

# Secrets'tan anahtarları çekme
if "NOVAKEY" in st.secrets:
    # Virgülle ayrılmış birden fazla anahtarı temizleyerek listeye al
    keys = [k.strip() for k in st.secrets["NOVAKEY"].split(",") if k.strip()]
else:
    st.error("⚠️ Bedirhan, Secrets kısmında NOVAKEY bulunamadı!")
    st.stop()

# --- 2. GÖRSEL TASARIM ---
st.markdown("""
<style>
    .stApp { background-color: #000000; color: #e0e0e0; }
    .astra-header {
        font-family: 'Orbitron', sans-serif;
        font-size: 50px; font-weight: 900; text-align: center;
        background: linear-gradient(90deg, #00f2fe, #7028e4, #ff00c8);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 20px;
    }
    .stChatMessage { border-radius: 15px; border: 1px solid #262626; background-color: #0e0e0e; }
</style>
""", unsafe_allow_html=True)

# --- 3. AKILLI VE HAFİF MOTOR ---
def get_astra_response(user_input):
    # Anahtarları her seferinde karıştır ki yük dağılsın
    shuffled_keys = random.sample(keys, len(keys))
    
    for i, key in enumerate(shuffled_keys):
        try:
            genai.configure(api_key=key)
            # '8b' sürümü kota dostudur ve daha az 429 hatası verir
            model = genai.GenerativeModel("models/gemini-1.5-flash-8b")
            
            # İlk mesaj kimliği
            prefix = ""
            if len(st.session_state.messages) <= 1:
                prefix = "Ben AstraUltra, Bedirhan'ın (Exile) yarattığı bir yapay zeka. "
            
            response = model.generate_content(user_input)
            
            if response and response.text:
                return prefix + response.text
                
        except Exception as e:
            error_str = str(e)
            # Gerçek hatayı sidebar'da gizlice göster
            st.sidebar.warning(f"Çekirdek {i+1} Denendi: {error_str[:50]}...")
            # Eğer kota hatasıysa bir saniye bekle ve diğer anahtara geç
            time.sleep(1)
            continue
            
    return "🚫 Bedirhan, tüm anahtarlar şu an kilitli. Lütfen 10 dakika sonra tekrar dene veya yeni bir anahtar ekle."

# --- 4. ANA ARAYÜZ ---
st.markdown("<div class='astra-header'>AstraUltra</div>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesaj geçmişini görüntüle
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcı girişi
if prompt := st.chat_input("Komutunu buraya bırak..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Enerji dengeleniyor..."):
            full_response = get_astra_response(prompt)
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

# --- 5. YAN PANEL (KONTROL) ---
with st.sidebar:
    st.title("🔱 Kontrol Ünitesi")
    st.write(f"Sistem: **Exile v2.0**")
    st.write(f"Aktif Çekirdek: {len(keys)}")
    st.divider()
    if st.button("Hafızayı Sıfırla"):
        st.session_state.messages = []
        st.rerun()
