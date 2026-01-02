import streamlit as st
import google.generativeai as genai
import time

# --- 1. CORE CONFIG ---
st.set_page_config(page_title="AstraUltra", page_icon="💫", layout="wide")

if "NOVAKEY" in st.secrets:
    genai.configure(api_key=st.secrets["NOVAKEY"])
else:
    st.error("API ANAHTARI EKSİK!")
    st.stop()

# --- 2. INFINITE RGB FLOW (CSS) ---
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(125deg, #000000, #050510, #0a0015, #000000);
        background-size: 400% 400%;
        animation: flowBG 15s ease infinite;
    }
    @keyframes flowBG { 0% {background-position:0% 50%} 50% {background-position:100% 50%} 100% {background-position:0% 50%} }
    
    .ultra-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 60px; font-weight: 900; text-align: center;
        background: linear-gradient(90deg, #00f2fe, #7028e4, #ff00c8, #00f2fe);
        background-size: 200% auto;
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        animation: ultra-glow 5s linear infinite;
    }
    @keyframes ultra-glow { to { background-position: 200% center; } }

    /* Seçenek Butonlarını Şıklaştır */
    div[data-testid="stHorizontalBlock"] {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 5px;
        margin-bottom: -10px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='ultra-title'>AstraUltra</div>", unsafe_allow_html=True)

# --- 3. SOHBET MEKANİZMASI ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# --- 4. MOD SEÇENEKLERİ (Yazı Yerinin Hemen Üstünde) ---
# st.columns kullanarak butonları yazı alanına yaklaştırıyoruz
col1, col2, col3 = st.columns([1,1,1])
with col1:
    mode = st.radio("🧠 Mod Seç:", ["Hızlı", "Dengeli", "Pro"], horizontal=True, label_visibility="collapsed")

# Giriş Alanı
if prompt := st.chat_input("Astraya sorun"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Seçilen moda göre motoru belirle
            if mode == "Hızlı":
                model_name = 'models/gemini-2.5-flash'
                mode_note = "🚀 Hızlı Mod"
            elif mode == "Pro":
                model_name = 'models/gemini-2.5-pro'
                mode_note = "💎 Pro Mod (Derin Düşünme)"
            else:
                model_name = 'models/gemini-2.5-flash' # Dengeli için de flash kullanabiliriz
                mode_note = "⚖️ Dengeli Mod"

            astra_engine = genai.GenerativeModel(model_name)

            # Kimlik tanımı (Sadece ilk mesajda)
            prefix = ""
            if len(st.session_state.messages) <= 2:
                prefix = "Sen AstraUltra, Bedirhan'ın (Exile) yarattığı bir yapay zeka. "

            with st.spinner(f"AstraUltra {mode} çekirdeği ile düşünüyor..."):
                context = f"Sen AstraUltra'sın. Bedirhan (Exile) seni yarattı. Soru: {prompt}"
                response = astra_engine.generate_content(context)
            
            final_text = prefix + response.text
            st.markdown(final_text)
            st.caption(f"Aktif Çekirdek: {mode_note}")
            st.session_state.messages.append({"role": "assistant", "content": final_text})
        except Exception as e:
            st.error(f"Sinyal Hatası: {e}")
