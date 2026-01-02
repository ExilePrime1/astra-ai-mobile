import streamlit as st
import google.generativeai as genai
import time

# --- 1. SİSTEM BAŞLATMA ---
st.set_page_config(page_title="AstraUltra", page_icon="💫", layout="wide")

if "NOVAKEY" in st.secrets:
    genai.configure(api_key=st.secrets["NOVAKEY"])
    astra_engine = genai.GenerativeModel('models/gemini-2.5-flash')
else:
    st.error("API ANAHTARI BULUNAMADI!")
    st.stop()

# --- 2. GÖRSEL DÜZENLEMELER ---
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
    .recovery-screen {
        text-align: center; padding: 50px; border: 2px solid #7028e4;
        border-radius: 20px; background: rgba(112, 40, 228, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# --- 3. SAYAÇ VE DURUM KONTROLÜ ---
if "counter" not in st.session_state:
    st.session_state.counter = 0
if "is_recovering" not in st.session_state:
    st.session_state.is_recovering = False

# --- 4. ENERJİ YENİLEME EKRANI (Tetiklendiğinde Çalışır) ---
if st.session_state.is_recovering or st.session_state.counter >= 19:
    st.markdown("<div class='astra-title'>AstraUltra</div>", unsafe_allow_html=True)
    st.markdown("<div class='recovery-screen'>", unsafe_allow_html=True)
    st.markdown("<h2 style='color:#7028e4;'>🔄 EXİLE ENERJİ SİSTEMİ DEVREDE</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#888;'>Günlük kota veya kullanım sınırı aşıldı. 20 saniye içinde sistem bypass ediliyor...</p>", unsafe_allow_html=True)
    
    t_placeholder = st.empty()
    p_bar = st.progress(0)
    
    for i in range(20, -1, -1):
        t_placeholder.markdown(f"<h1 style='color:#00f2fe;'>{i}s</h1>", unsafe_allow_html=True)
        p_bar.progress((20 - i) * 5)
        time.sleep(1)
    
    st.session_state.counter = 0 
    st.session_state.is_recovering = False
    st.success("✅ SİSTEM YENİLENDİ. Devam edebilirsin Exile.")
    time.sleep(1.5)
    st.rerun()

# --- 5. ANA EKRAN ---
st.markdown("<div class='astra-title'>AstraUltra</div>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Astraya sorun"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Sadece ilk mesajda kimlik belirt
            prefix = ""
            if len(st.session_state.messages) <= 2:
                prefix = "Sen AstraUltra, Bedirhan'ın (Exile) yarattığı bir yapay zeka. "

            with st.spinner("İşleniyor..."):
                context = f"Sen AstraUltra'sın. Bedirhan (Exile) seni yarattı. Soru: {prompt}"
                response = astra_engine.generate_content(context)
            
            st.session_state.counter += 1
            st.markdown(prefix + response.text)
            st.session_state.messages.append({"role": "assistant", "content": prefix + response.text})
            
        except Exception as e:
            # HATA GELDİĞİ AN (429 veya herhangi bir kota hatası)
            if "429" in str(e) or "quota" in str(e).lower():
                st.session_state.is_recovering = True # Hemen yenileme modunu tetikle
                st.rerun()
            else:
                st.error(f"Teknik Hata: {e}")
