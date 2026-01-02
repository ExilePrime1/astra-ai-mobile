import streamlit as st
import google.generativeai as genai
import time

# --- 1. SİSTEM YAPILANDIRMASI ---
st.set_page_config(page_title="ASTRA NOVA PRO", page_icon="💠", layout="wide")

if "NOVAKEY" in st.secrets:
    genai.configure(api_key=st.secrets["NOVAKEY"])
else:
    st.error("⚠️ API ANAHTARI EKSİK!")
    st.stop()

# --- 2. GELİŞMİŞ CYBER ARAYÜZ (CSS) ---
st.markdown("""
<style>
    .stApp { background: #050508 !important; color: #00f2fe !important; }
    
    /* RGB Başlık */
    .astra-logo {
        font-family: 'Courier New', monospace;
        font-size: 50px; font-weight: 900; text-align: center;
        background: linear-gradient(90deg, #ff0000, #00ff00, #0000ff, #ff0000);
        background-size: 200% auto; -webkit-background-clip: text;
        -webkit-text-fill-color: transparent; animation: glow 3s linear infinite;
    }
    @keyframes glow { to { background-position: 200% center; } }

    /* Mesaj Kutuları */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid #7028e4 !important;
        border-radius: 15px !important;
    }
</style>
<div class="astra-logo">ASTRA 3.0</div>
<p style="text-align:center; color:#444; font-size:10px; letter-spacing:5px;">DESIGNED BY EXILE</p>
""", unsafe_allow_html=True)

# --- 3. ÜÇ NOKTA (SIDEBAR) ÖZELLİKLERİ ---
with st.sidebar:
    st.markdown("### 💠 ASTRA KONTROL MERKEZİ")
    st.write(f"🛡️ **Operatör:** Bedirhan (Exile)")
    
    st.markdown("---")
    # Özellik 1: Kişilik Seçimi
    mood = st.selectbox("🎭 Astra Kişiliği:", ["Ciddi & Profesyonel", "Esprili & Arkadaş Canlısı", "Kısa & Öz"])
    
    # Özellik 2: Dosya Analizi
    uploaded_file = st.file_uploader("📂 Veri Yükle (Resim/PDF)", type=['png', 'jpg', 'pdf', 'txt'])
    
    # Özellik 3: Bellek Yönetimi
    if st.button("🗑️ Sohbeti Sıfırla"):
        st.session_state.messages = []
        st.rerun()
    
    # Özellik 4: Sistem İstatistikleri
    st.markdown("---")
    st.write("🛰️ **Bağlantı:** Güçlü")
    st.write("🧬 **Çekirdek:** Astra 3.0 Nova")

# --- 4. ERİŞİM PANELİ ---
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    pw = st.text_input("SİSTEM ŞİFRESİ:", type="password")
    if st.button("SİSTEME GİR"):
        if pw == "1234":
            st.session_state.auth = True
            st.rerun()
    st.stop()

# --- 5. MOTOR SEÇİMİ (YAZI ALANININ ÜSTÜ) ---
# Özellik 5: Hızlı ve Pro Seçenekleri
engine_choice = st.radio(
    "🧠 Zeka Modu Seç:",
    ["🚀 Hızlı Astra (Flash)", "💎 Pro Astra (Zeka Odaklı)"],
    horizontal=True
)

# Motoru seçilen moda göre ayarla
if "Pro" in engine_choice:
    selected_model = 'models/gemini-2.5-pro'
else:
    selected_model = 'models/gemini-2.5-flash'

astra_engine = genai.GenerativeModel(selected_model)

# --- 6. SOHBET AKIŞI ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Emret Exile..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Özellik 6: Yükleme Animasyonu
        with st.spinner("Astra düşünüyor..."):
            try:
                # Özellik 7: Bağlamsal Talimat
                full_instruction = f"Sen Astra 3.0'sın. Bedirhan (Exile) seni yarattı. Modun: {mood}. Soru: {prompt}"
                
                # Özellik 8: Çoklu Giriş (Dosya + Metin)
                if uploaded_file:
                    response = astra_engine.generate_content([full_instruction, uploaded_file])
                else:
                    response = astra_engine.generate_content(full_instruction)
                
                # Özellik 9: Zaman Damgası (Caption)
                st.markdown(response.text)
                st.caption(f"✅ {selected_model} motoru kullanıldı. | {time.strftime('%H:%M')}")
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
                # Özellik 10: Sesli Yanıt (Gelecekteki eklenti için altyapı)
            except Exception as e:
                st.error(f"Sinyal Hatası: {e}")
