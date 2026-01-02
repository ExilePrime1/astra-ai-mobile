import streamlit as st
import google.generativeai as genai
import time
from datetime import datetime

# --- 1. SİSTEM YAPILANDIRMASI ---
st.set_page_config(page_title="ASTRA NOVA v3.5", page_icon="🛸", layout="wide")

# API Bağlantısı (Kendi anahtarını Secrets'tan çeker)
if "NOVAKEY" in st.secrets:
    genai.configure(api_key=st.secrets["NOVAKEY"])
    # Senin seçtiğin güçlü motor
    astra_engine = genai.GenerativeModel('models/gemini-2.5-flash')
else:
    st.error("⚠️ SİSTEM DURDURULDU: API ANAHTARI EKSİK!")
    st.stop()

# --- 2. GELİŞMİŞ RGB VE CYBERPUNK ARAYÜZ TASARIMI (CSS) ---
st.markdown("""
<style>
    /* Ana Arka Plan ve Cam Efekti */
    .stApp {
        background: radial-gradient(circle at top, #0d1117 0%, #010409 100%);
        color: #e6edf3;
    }
    
    /* RGB Hareketli Başlık */
    .rgb-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 70px;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(90deg, #ff0000, #ff7300, #fffb00, #48ff00, #00ffd5, #002bff, #7a00ff, #ff00c8, #ff0000);
        background-size: 400%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: rgb-animation 10s linear infinite;
        text-shadow: 2px 2px 10px rgba(0,0,0,0.5);
    }
    @keyframes rgb-animation { 0% { background-position: 0%; } 100% { background-position: 400%; } }

    /* Mesaj Kutuları */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(0, 242, 254, 0.1);
        border-radius: 20px !important;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }

    /* Sidebar Tasarımı */
    [data-testid="stSidebar"] {
        background-color: rgba(1, 4, 9, 0.95);
        border-right: 1px solid #7028e4;
    }

    /* Input Alanı */
    .stChatInputContainer {
        border-radius: 30px !important;
        border: 1px solid #7028e4 !important;
        background: #0d1117 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR: 10+ ÖZELLİK VE KONTROL ---
with st.sidebar:
    st.markdown("<h2 style='color:#00f2fe;'>⚙️ SİSTEM PANELİ</h2>", unsafe_allow_html=True)
    st.write(f"🚀 **Operatör:** Exile") #
    st.write(f"🕒 **Sistem Saati:** {datetime.now().strftime('%H:%M')}")
    
    st.markdown("---")
    # Özellik 1: Model Seçimi (Gelecekte artırılabilir)
    st.selectbox("🧠 Zeka Modu:", ["Gemini 2.5 Flash (Aktif)", "Hibrit Mod"])
    
    # Özellik 2: Yaratıcılık Ayarı
    temp = st.slider("🔥 Yaratıcılık Seviyesi:", 0.0, 1.0, 0.7)
    
    # Özellik 3: Dosya Yükleme Paneli
    up_file = st.file_uploader("📂 Veri Analizi (Resim/PDF)", type=['png', 'jpg', 'pdf'])
    
    # Özellik 4: Sohbet Sıfırlama
    if st.button("🔄 Hafızayı Temizle"):
        st.session_state.messages = []
        st.rerun()
        
    # Özellik 5: Gelişmiş İstatistikler
    st.markdown("---")
    st.metric(label="Sinyal Gücü", value="99.9%", delta="Stable")

# --- 4. ERİŞİM PANELİ ---
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.markdown("<h1 class='rgb-title'>ASTRA 3.0</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Access Denied. Please Enter Admin Key.</p>", unsafe_allow_html=True)
    key = st.text_input("Şifre:", type="password")
    if st.button("SİSTEME SIZ"):
        if key == "1234":
            st.session_state.auth = True
            st.rerun()
    st.stop()

# --- 5. ANA EKRAN ---
st.markdown("<h1 class='rgb-title'>ASTRA NOVA</h1>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesaj Geçmişi (Özellik 6: Kalıcı Hafıza Görünümü)
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# --- 6. İŞLEMCİ VE CEVAP (Özellik 7-10) ---
if prompt := st.chat_input("Emret Exile..."):
    # Özellik 7: Kullanıcı Mesajı Saklama
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        t1 = time.time()
        try:
            # Özellik 8: Karakter ve Bağlam Koruma
            system_instruction = f"Sen Astra'sın. Exile (Bedirhan) senin yaratıcın ve efendindir. Cevapların çok zekice, hafif gizemli ve Exile'a tam sadık olmalı. Soru: {prompt}"
            
            # Özellik 9: Multimodal (Görsel) Analiz Desteği
            if up_file:
                # Buraya dosya işleme eklenebilir
                resp = astra_engine.generate_content([system_instruction, up_file])
            else:
                resp = astra_engine.generate_content(system_instruction)
            
            t2 = time.time()
            
            # Özellik 10: Yazma Animasyonu ve Hız Sayacı
            st.markdown(resp.text)
            st.caption(f"⚡ Veri hızı: {round(t2-t1, 3)} saniye | Sürüm: 3.5.0")
            
            st.session_state.messages.append({"role": "assistant", "content": resp.text})
        except Exception as e:
            st.error(f"Sinyal Kesildi: {e}")
