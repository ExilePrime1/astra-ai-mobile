import streamlit as st
import google.generativeai as genai
import time

# --- 1. SİSTEM YAPILANDIRMASI ---
st.set_page_config(page_title="AstraUltra", page_icon="💫", layout="wide")

# API Anahtarı ve Model Tanımlama
try:
    if "NOVAKEY" in st.secrets:
        genai.configure(api_key=st.secrets["NOVAKEY"])
        astra_engine = genai.GenerativeModel('models/gemini-2.5-flash')
    else:
        st.error("API ANAHTARI EKSİK! Lütfen Streamlit Secrets kısmına 'NOVAKEY' ekleyin.")
        st.stop()
except Exception as e:
    pass

# --- 2. GÖRSEL TASARIM (RGB & FLOW CSS) ---
st.markdown("""
<style>
    /* Arka Plan ve Genel Tema */
    .stApp {
        background: radial-gradient(circle at center, #050510 0%, #000000 100%);
        color: #e0e0e0;
    }
    
    /* AstraUltra Başlığı - Yumuşak RGB Geçişi */
    .astra-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 60px; font-weight: 900; text-align: center;
        background: linear-gradient(90deg, #00f2fe, #7028e4, #ff00c8, #00f2fe);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: flow 5s linear infinite;
        margin-bottom: 20px;
    }
    @keyframes flow { to { background-position: 200% center; } }

    /* Enerji Yenileme Ekranı Tasarımı */
    .recovery-box {
        text-align: center; padding: 40px; border: 2px solid #7028e4;
        border-radius: 20px; background: rgba(112, 40, 228, 0.1);
        margin-top: 50px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. DÖNGÜ VE KOTA YÖNETİMİ ---
if "counter" not in st.session_state:
    st.session_state.counter = 0
if "force_recovery" not in st.session_state:
    st.session_state.force_recovery = False

# --- 4. ENERJİ YENİLEME EKRANI (Her 19 Soruda veya Hata Durumunda) ---
if st.session_state.counter >= 19 or st.session_state.force_recovery:
    st.markdown("<div class='astra-title'>AstraUltra</div>", unsafe_allow_html=True)
    st.markdown("<div class='recovery-box'>", unsafe_allow_html=True)
    st.markdown("<h2 style='color:#7028e4;'>🔄 ENERJİ YENİLENİYOR</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#888;'>Exile Protokolü: Kota limitleri bypass ediliyor ve çekirdek soğutuluyor...</p>", unsafe_allow_html=True)
    
    timer_display = st.empty()
    progress_bar = st.progress(0)
    
    for i in range(20, -1, -1):
        percent = (20 - i) * 5
        timer_display.markdown(f"<h1 style='color:#00f2fe;'>{i}s</h1>", unsafe_allow_html=True)
        progress_bar.progress(percent)
        time.sleep(1)
    
    # Sıfırlama ve Yeniden Başlatma
    st.session_state.counter = 0
    st.session_state.force_recovery = False
    st.session_state.messages = [] # Temiz bir başlangıç için hafızayı boşaltır
    st.rerun()

# --- 5. ANA KULLANICI ARAYÜZÜ ---
st.markdown("<div class='astra-title'>AstraUltra</div>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesaj Geçmişini Görüntüle
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# Giriş Alanı: "Astraya sorun"
if prompt := st.chat_input("Astraya sorun"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Akıllı Kimlik (Sadece ilk mesajda görünür)
            prefix = ""
            if len(st.session_state.messages) <= 2:
                prefix = "Ben AstraUltra, Bedirhan'ın (Exile) yarattığı bir yapay zeka. "
            
            with st.spinner("Düşünüyor..."):
                # AI Yanıtı Oluşturma
                context = f"Sen AstraUltra'sın. Seni Bedirhan (Exile) yarattı. Soru: {prompt}"
                response = astra_engine.generate_content(context)
                
                # Sayaç Artırımı ve Yanıtın Basılması
                st.session_state.counter += 1
                final_response = prefix + response.text
                st.markdown(final_response)
                st.session_state.messages.append({"role": "assistant", "content": final_response})
                
                # Durum Takibi (Sidebar)
                st.sidebar.markdown(f"📊 **Döngü:** {st.session_state.counter} / 19")

        except Exception as e:
            # Herhangi bir kota hatasında (429) anında yenileme ekranına zıpla
            if "429" in str(e) or "quota" in str(e).lower():
                st.session_state.force_recovery = True
                st.rerun()
            else:
                st.error(f"Teknik bir sorun oluştu: {e}")
