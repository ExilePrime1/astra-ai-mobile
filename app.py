import streamlit as st
import google.generativeai as genai
import time

# --- 1. CONFIG ---
st.set_page_config(page_title="AstraUltra", page_icon="💫", layout="wide")

if "NOVAKEY" in st.secrets:
    genai.configure(api_key=st.secrets["NOVAKEY"])
    astra_engine = genai.GenerativeModel('models/gemini-2.5-flash')
else:
    st.error("API ANAHTARI EKSİK!")
    st.stop()

# --- 2. CSS & RGB ---
st.markdown("""
<style>
    .stApp { background: #000; color: #00f2fe; }
    .astra-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 55px; font-weight: 900; text-align: center;
        background: linear-gradient(90deg, #00f2fe, #7028e4, #ff00c8, #00f2fe);
        background-size: 200% auto;
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        animation: ultra-glow 5s linear infinite;
    }
    @keyframes ultra-glow { to { background-position: 200% center; } }
    
    .recovery-box {
        border: 2px solid #7028e4; border-radius: 20px;
        padding: 40px; text-align: center; background: rgba(112, 40, 228, 0.1);
        margin: 50px auto; max-width: 700px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. DÖNGÜ KONTROLÜ ---
if "counter" not in st.session_state:
    st.session_state.counter = 0

# --- 4. ENERJİ YENİLEME EKRANI (Sadece Sayaç 19'a Ulaştığında) ---
if st.session_state.counter >= 19:
    st.markdown("<div class='astra-title'>AstraUltra</div>", unsafe_allow_html=True)
    st.markdown("<div class='recovery-box'>", unsafe_allow_html=True)
    st.markdown("<h2 style='color:#7028e4;'>🔄 KOTA OPTİMİZASYONU</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#888;'>Exile Protokolü: Enerji çekirdekleri 20 saniye içinde soğutuluyor...</p>", unsafe_allow_html=True)
    
    t_placeholder = st.empty()
    p_bar = st.progress(0)
    
    for i in range(20, -1, -1):
        t_placeholder.markdown(f"<h1 style='color:#00f2fe;'>{i}s</h1>", unsafe_allow_html=True)
        p_bar.progress((20 - i) * 5)
        time.sleep(1)
    
    st.session_state.counter = 0 # SIFIRLAMA
    st.success("⚡ Enerji Yenilendi! Sisteme geri dönülüyor...")
    time.sleep(1.5)
    st.rerun()

# --- 5. ANA ARAYÜZ ---
st.markdown("<div class='astra-title'>AstraUltra</div>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# Giriş Alanı
if prompt := st.chat_input("Astraya sorun"):
    # Mesajı ekle ve sayacı artır
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.counter += 1
    
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Akıllı Kimlik (Sadece ilk mesajda)
            prefix = ""
            if len(st.session_state.messages) <= 2:
                prefix = "Ben AstraUltra, Bedirhan'ın (Exile) yarattığı bir yapay zekayım. "
            
            with st.spinner("İşleniyor..."):
                context = f"Sen AstraUltra'sın. Seni Bedirhan (Exile) yarattı. Soru: {prompt}"
                response = astra_engine.generate_content(context)
            
            full_ans = prefix + response.text
            st.markdown(full_ans)
            st.session_state.messages.append({"role": "assistant", "content": full_ans})
            
            # Sağ alt bilgi ekranı
            st.sidebar.markdown(f"📊 **Kota Durumu:** {st.session_state.counter} / 19")

        except Exception as e:
            if "429" in str(e):
                st.session_state.counter = 19 # Hata gelirse zorla yenileme moduna sok
                st.rerun()
            else:
                st.error(f"Sistem Hatası: {e}")
