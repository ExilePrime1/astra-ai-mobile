import streamlit as st
import google.generativeai as genai
import time

# --- 1. CORE CONFIG ---
st.set_page_config(page_title="AstraUltra", page_icon="💫", layout="wide")

# API Ayarı - Hata vermemesi için try-except içine alındı
try:
    if "NOVAKEY" in st.secrets:
        genai.configure(api_key=st.secrets["NOVAKEY"])
        astra_engine = genai.GenerativeModel('models/gemini-2.5-flash')
    else:
        st.error("API ANAHTARI EKSİK!")
        st.stop()
except:
    pass

# --- 2. CSS - RGB FLOW ---
st.markdown("""
<style>
    .stApp { background: #000; color: #00f2fe; }
    .astra-header {
        font-family: 'Orbitron', sans-serif;
        font-size: 55px; font-weight: 900; text-align: center;
        background: linear-gradient(90deg, #00f2fe, #7028e4, #ff00c8, #00f2fe);
        background-size: 200% auto;
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        animation: flow 5s linear infinite;
    }
    @keyframes flow { to { background-position: 200% center; } }
</style>
""", unsafe_allow_html=True)

# --- 3. SAYAÇ VE DURUM ---
if "counter" not in st.session_state: st.session_state.counter = 0
if "force_reset" not in st.session_state: st.session_state.force_reset = False

# --- 4. 20 SANİYELİK YENİLEME EKRANI (Tek Çözüm) ---
if st.session_state.counter >= 19 or st.session_state.force_reset:
    st.markdown("<div class='astra-header'>AstraUltra</div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center; padding:50px; border:2px solid #7028e4; border-radius:20px; background:rgba(112,40,228,0.1);'>", unsafe_allow_html=True)
    st.markdown("<h2 style='color:#7028e4;'>🔄 ENERJİ YENİLENİYOR</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#888;'>Exile Protokolü: Kota limitleri bypass ediliyor...</p>", unsafe_allow_html=True)
    
    t_place = st.empty()
    p_bar = st.progress(0)
    for i in range(20, -1, -1):
        t_place.markdown(f"<h1 style='color:#00f2fe;'>{i}s</h1>", unsafe_allow_html=True)
        p_bar.progress((20 - i) * 5)
        time.sleep(1)
    
    st.session_state.counter = 0
    st.session_state.force_reset = False
    st.rerun()

# --- 5. SOHBET PANELİ ---
st.markdown("<div class='astra-header'>AstraUltra</div>", unsafe_allow_html=True)

if "messages" not in st.session_state: st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if prompt := st.chat_input("Astraya sorun"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Kimlik tanımı (Sadece ilk mesajda)
            prefix = ""
            if len(st.session_state.messages) <= 2:
                prefix = "Sen AstraUltra, Bedirhan'ın (Exile) yarattığı bir yapay zeka. "
            
            with st.spinner("İşleniyor..."):
                resp = astra_engine.generate_content(f"Sen AstraUltra'sın. Soru: {prompt}")
                st.session_state.counter += 1
                
                # Başarılı cevap
                st.markdown(prefix + resp.text)
                st.session_state.messages.append({"role": "assistant", "content": prefix + resp.text})
        
        except Exception as e:
            # İŞTE BURASI: Hata geldiği an hiçbir şey sormadan yenileme ekranına atar
            st.session_state.force_reset = True
            st.rerun()
