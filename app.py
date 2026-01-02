import streamlit as st
import google.generativeai as genai
import time

# --- 1. SİSTEM YAPILANDIRMASI ---
st.set_page_config(page_title="AstraUltra", page_icon="💫", layout="wide")

if "NOVAKEY" in st.secrets:
    genai.configure(api_key=st.secrets["NOVAKEY"])
    astra_engine = genai.GenerativeModel('models/gemini-2.5-flash')
else:
    st.error("SİSTEM HATASI: API ANAHTARI EKSİK!")
    st.stop()

# --- 2. GÖRSEL TASARIM (RGB FLOW) ---
st.markdown("""
<style>
    .stApp { background: #000; color: #00f2fe; }
    .astra-title {
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

# --- 3. DURUM YÖNETİMİ ---
if "counter" not in st.session_state: st.session_state.counter = 0
if "is_locked" not in st.session_state: st.session_state.is_locked = False

# --- 4. 20 SANİYELİK ENERJİ YENİLEME EKRANI (Her 19 Soruda Bir) ---
if st.session_state.counter >= 19:
    st.markdown("<div class='astra-title'>AstraUltra</div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center; padding:40px; border:2px solid #7028e4; border-radius:15px; background:rgba(112,40,228,0.1);'>", unsafe_allow_html=True)
    st.markdown("<h2 style='color:#7028e4;'>🔄 ENERJİ YENİLENİYOR</h2>", unsafe_allow_html=True)
    
    t_place = st.empty()
    p_bar = st.progress(0)
    for i in range(20, -1, -1):
        t_place.markdown(f"<h1 style='color:#00f2fe;'>{i}s</h1>", unsafe_allow_html=True)
        p_bar.progress((20 - i) * 5)
        time.sleep(1)
    
    st.session_state.counter = 0 # Sayacı sıfırla
    st.session_state.is_locked = False # Kilidi aç
    st.rerun()

# --- 5. ANA PANEL ---
st.markdown("<div class='astra-title'>AstraUltra</div>", unsafe_allow_html=True)

if "messages" not in st.session_state: st.session_state.messages = []

# Mesajları Görüntüle
for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

# Giriş Alanı
if prompt := st.chat_input("Astraya sorun"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Sadece ilk soruda kimlik belirt
            prefix = "Ben AstraUltra, Bedirhan'ın (Exile) yarattığı bir yapay zeka. " if len(st.session_state.messages) <= 2 else ""
            
            with st.spinner("Düşünüyor..."):
                resp = astra_engine.generate_content(f"Sen AstraUltra'sın. Soru: {prompt}")
                st.session_state.counter += 1 # Her başarılı soruda artır
                
                full_text = prefix + resp.text
                st.markdown(full_text)
                st.session_state.messages.append({"role": "assistant", "content": full_text})
        
        except Exception as e:
            if "429" in str(e):
                # Günlük kota dolduysa zorla 19'a set et ve ekranı yenile
                st.session_state.counter = 19
                st.rerun()
            else:
                st.error(f"Sinyal Hatası: {e}")
