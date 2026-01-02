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

# --- 2. ADVANCED UI (CSS) ---
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
        font-size: 55px; font-weight: 900; text-align: center;
        background: linear-gradient(90deg, #00f2fe, #7028e4, #ff00c8, #00f2fe);
        background-size: 200% auto;
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        animation: ultra-glow 5s linear infinite;
    }
    @keyframes ultra-glow { to { background-position: 200% center; } }

    /* Mod Açıklama Kutusu */
    .mode-desc {
        background: rgba(112, 40, 228, 0.1);
        border: 1px solid rgba(112, 40, 228, 0.3);
        padding: 10px 15px;
        border-radius: 12px;
        font-size: 13px;
        color: #b0b0b0;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='ultra-title'>AstraUltra</div>", unsafe_allow_html=True)

# --- 3. SOHBET GEÇMİŞİ ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# --- 4. AKILLI MOD SEÇİCİ (Gemini Stili) ---
# Yazı alanının hemen üstünde yer alır
selected_mode = st.radio(
    "Zeka Modu:",
    ["🚀 Hızlı", "⚖️ Dengeli", "💎 Pro"],
    horizontal=True,
    label_visibility="collapsed"
)

# Seçilen moda göre dinamik açıklama
descriptions = {
    "🚀 Hızlı": "Işık hızında yanıtlar için optimize edilmiş çevik mod.",
    "⚖️ Dengeli": "Yaratıcılık ve hız arasında mükemmel denge kuran standart mod.",
    "💎 Pro": "Karmaşık problemler ve derin analizler için Exile'ın en güçlü çekirdeği."
}

st.markdown(f"<div class='mode-desc'>{descriptions[selected_mode]}</div>", unsafe_allow_html=True)

# --- 5. GİRİŞ VE YANIT ---
if prompt := st.chat_input("Astraya sorun"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Model Belirleme
            m_id = 'models/gemini-2.5-pro' if "Pro" in selected_mode else 'models/gemini-2.5-flash'
            model = genai.GenerativeModel(m_id)

            # Akıllı Kimlik (Sadece ilk mesajda)
            prefix = ""
            if len(st.session_state.messages) <= 2:
                prefix = "Sen AstraUltra, Bedirhan'ın (Exile) yarattığı bir yapay zeka. "

            with st.spinner(f"AstraUltra {selected_mode} modunda çalışıyor..."):
                context = f"Sen AstraUltra'sın. Seni Bedirhan (Exile) yarattı. Soru: {prompt}"
                response = model.generate_content(context)
            
            final_ans = prefix + response.text
            st.markdown(final_ans)
            st.session_state.messages.append({"role": "assistant", "content": final_ans})
        except Exception as e:
            if "429" in str(e):
                st.warning("⚠️ Kota Doldu! Lütfen 'Hızlı' moda geç Bedirhan.")
            else:
                st.error(f"Sinyal Hatası: {e}")
