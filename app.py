import streamlit as st
import google.generativeai as genai
import time

# --- 1. SİSTEM BAŞLATMA ---
st.set_page_config(page_title="AstraUltra", page_icon="💫", layout="wide")

# API Anahtarı Yönetimi
if "api_key" not in st.session_state:
    st.session_state.api_key = st.secrets.get("NOVAKEY", "")

def configure_astra():
    if st.session_state.api_key:
        genai.configure(api_key=st.session_state.api_key)
        return genai.GenerativeModel('models/gemini-2.5-flash')
    return None

astra_engine = configure_astra()

# --- 2. CSS ---
st.markdown("""
<style>
    .stApp { background: #000; color: #00f2fe; }
    .astra-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 50px; text-align: center;
        background: linear-gradient(90deg, #00f2fe, #7028e4, #ff00c8);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        animation: flow 5s linear infinite;
    }
    @keyframes flow { to { background-position: 200% center; } }
</style>
""", unsafe_allow_html=True)

# --- 3. DÖNGÜ VE KOTA TAKİBİ ---
if "counter" not in st.session_state: st.session_state.counter = 0
if "error_loop" not in st.session_state: st.session_state.error_loop = False

# --- 4. KRİTİK YENİLEME EKRANI ---
if st.session_state.counter >= 19 or st.session_state.error_loop:
    st.markdown("<div class='astra-title'>AstraUltra</div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center; padding:30px; border:2px solid #7028e4; border-radius:15px; background:rgba(112,40,228,0.1);'>", unsafe_allow_html=True)
    
    if st.session_state.error_loop:
        st.error("🚫 GOOGLE GÜNLÜK KOTASI TAMAMEN DOLDU!")
        new_key = st.text_input("Devam etmek için yeni bir API Key gir (Veya yarını bekle):", type="password")
        if st.button("Enerji Çekirdeğini Yenile"):
            st.session_state.api_key = new_key
            st.session_state.error_loop = False
            st.session_state.counter = 0
            st.rerun()
    else:
        st.markdown("<h2 style='color:#7028e4;'>🔄 ENERJİ YENİLENİYOR (20s)</h2>", unsafe_allow_html=True)
        p_bar = st.progress(0)
        for i in range(20, -1, -1):
            p_bar.progress((20-i)*5)
            time.sleep(1)
        st.session_state.counter = 0
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- 5. ANA PANEL ---
st.markdown("<div class='astra-title'>AstraUltra</div>", unsafe_allow_html=True)

if "messages" not in st.session_state: st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if prompt := st.chat_input("Astraya sorun"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Sadece ilk mesajda kimlik
            prefix = "Ben AstraUltra, Bedirhan'ın (Exile) yarattığı bir yapay zeka. " if len(st.session_state.messages) <= 2 else ""
            
            with st.spinner("İşleniyor..."):
                response = astra_engine.generate_content(f"Sen AstraUltra'sın. Soru: {prompt}")
                st.session_state.counter += 1
                st.markdown(prefix + response.text)
                st.session_state.messages.append({"role": "assistant", "content": prefix + response.text})
        except Exception as e:
            if "429" in str(e):
                st.session_state.error_loop = True
                st.rerun()
            else:
                st.error(f"Hata: {e}")
