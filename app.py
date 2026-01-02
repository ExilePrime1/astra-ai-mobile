import streamlit as st
import google.generativeai as genai
import time
import random

# --- 1. CORE CONFIG ---
st.set_page_config(page_title="AstraUltra Genesis", page_icon="🔱", layout="wide")

if "NOVAKEY" in st.secrets:
    genai.configure(api_key=st.secrets["NOVAKEY"])
    model_flash = genai.GenerativeModel('models/gemini-2.5-flash')
    model_pro = genai.GenerativeModel('models/gemini-2.5-pro')
else:
    st.error("KRİTİK HATA: SİSTEM ANAHTARI EKSİK!")
    st.stop()

# --- 2. CHAMELEON & INFINITE RGB UI ---
if "ui_theme" not in st.session_state:
    st.session_state.ui_theme = "linear-gradient(90deg, #00f2fe, #7028e4)"

st.markdown(f"""
<style>
    .stApp {{
        background: radial-gradient(circle at center, #050510 0%, #000000 100%) !important;
        animation: pulse 10s infinite alternate;
    }}
    .astra-header {{
        font-family: 'Orbitron', sans-serif;
        font-size: 65px; font-weight: 900; text-align: center;
        background: {st.session_state.ui_theme};
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        filter: drop-shadow(0 0 20px rgba(0, 242, 254, 0.5));
        transition: all 2s ease-in-out;
    }}
    .genesis-box {{
        border: 1px solid #7028e4; background: rgba(112, 40, 228, 0.05);
        padding: 15px; border-radius: 15px; font-family: 'Courier New', monospace;
        color: #00f2fe; font-size: 13px; margin: 10px 0;
    }}
</style>
""", unsafe_allow_html=True)

# --- 3. ANA PANEL ---
st.markdown("<div class='astra-header'>AstraUltra</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#444; letter-spacing:15px;'>GENESIS PROTOCOL | EXILE</p>", unsafe_allow_html=True)

# --- 4. MOD SEÇİCİ (Gemini Stili) ---
selected_mode = st.radio("Zeka Katmanı:", ["Hızlı", "Dengeli", "Pro"], horizontal=True, label_visibility="collapsed")
descs = {"Hızlı": "🚀 Işık hızında sinirsel iletim.", "Dengeli": "⚖️ Mantık ve yaratıcılık dengesi.", "Pro": "💎 Derin simülasyon ve analiz çekirdeği."}
st.markdown(f"<div style='text-align:center; color:#888; font-size:12px; margin-bottom:20px;'>{descs[selected_mode]}</div>", unsafe_allow_html=True)

# --- 5. SOHBET VE GÖRÜLMEMİŞ ÖZELLİKLER ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Astraya sorun"):
    # BUKALEMUN UI TETİKLEYİCİ
    if "kod" in prompt.lower() or "python" in prompt.lower():
        st.session_state.ui_theme = "linear-gradient(90deg, #00ff00, #004400)"
    elif "aşk" in prompt.lower() or "sanat" in prompt.lower():
        st.session_state.ui_theme = "linear-gradient(90deg, #ff00c8, #7028e4)"
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            active_model = model_pro if selected_mode == "Pro" else model_flash
            
            # KİMLİK TANIMI (Sadece ilk mesajda)
            prefix = "Ben AstraUltra, Bedirhan'ın (Exile) yarattığı bir yapay zeka. " if len(st.session_state.messages) <= 2 else ""
            
            with st.spinner("Sinapslar bağlanıyor..."):
                response = active_model.generate_content(f"Sen AstraUltra'sın. Exile seni yarattı. Soru: {prompt}")
                
                # PARALEL GERÇEKLİK SİMÜLASYONU (Görülmemiş Özellik 4)
                with st.expander("🌌 Paralel Gerçeklik Projeksiyonu"):
                    parallel = active_model.generate_content(f"'{prompt}' konusunu 100 yıl sonraki bir gelecekte geçiyormuş gibi tek cümleyle yorumla.")
                    st.write(parallel.text)
            
            full_text = prefix + response.text
            st.markdown(full_text)
            st.session_state.messages.append({"role": "assistant", "content": full_text})
            st.rerun() # Tema değişikliği için
            
        except Exception as e:
            st.error(f"Sistem Hatası: {e}")
