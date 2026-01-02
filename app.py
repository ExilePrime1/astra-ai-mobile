import streamlit as st
import google.generativeai as genai
import time
import random

# --- 1. SİSTEM YAPILANDIRMASI ---
st.set_page_config(page_title="ASTRA GHOST PROTOCOL", page_icon="🧬", layout="wide")

if "NOVAKEY" in st.secrets:
    genai.configure(api_key=st.secrets["NOVAKEY"])
    astra_engine = genai.GenerativeModel('models/gemini-2.5-flash')
else:
    st.error("Sistem Anahtarı Bulunamadı!")
    st.stop()

# --- 2. GÖRÜLMEMİŞ DİNAMİK TASARIM (CSS) ---
# Yazı rengi ve gölge, kullanıcının moduna göre kod tarafından değiştirilecek
if "dna_color" not in st.session_state:
    st.session_state.dna_color = "#00f2fe"

st.markdown(f"""
<style>
    .stApp {{
        background: radial-gradient(circle at center, #050508 0%, #000000 100%) !important;
    }}
    .dna-title {{
        font-family: 'Orbitron', sans-serif;
        font-size: 60px; font-weight: 900; text-align: center;
        color: {st.session_state.dna_color} !important;
        text-shadow: 0 0 20px {st.session_state.dna_color};
        transition: all 2s ease;
    }}
    .ghost-text {{
        font-family: 'Courier New', monospace;
        color: #111; text-align: center; font-size: 12px;
    }}
</style>
""", unsafe_allow_html=True)

# --- 3. HAYALET PROTOKOLÜ (GÜVENLİK) ---
if "auth" not in st.session_state:
    st.session_state.auth = False
    st.session_state.attempts = 0

if not st.session_state.auth:
    st.markdown("<div class='dna-title'>ASTRA 3.0</div>", unsafe_allow_html=True)
    
    if st.session_state.attempts >= 3:
        st.warning("⚠️ SİSTEM KİLİTLENDİ: GHOST PROTOCOL AKTİF.")
        st.markdown("<p class='ghost-text'>Veri tabanı siliniyor... (Simülasyon)</p>", unsafe_allow_html=True)
        time.sleep(5)
        st.session_state.attempts = 0 # Gerçekte sıfırlıyoruz ama kullanıcıyı korkutuyoruz
        
    pw = st.text_input("Biyometrik Anahtar (Şifre):", type="password")
    if st.button("SİSTEME SIZ"):
        if pw == "1234":
            st.session_state.auth = True
            st.rerun()
        else:
            st.session_state.attempts += 1
            st.error(f"Hatalı Giriş! Kalan Hak: {3 - st.session_state.attempts}")
    st.stop()

# --- 4. ANA PANEL VE YENİ ÖZELLİKLER ---
st.markdown("<div class='dna-title'>ASTRA ULTIMATE</div>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🧬 DNA & GHOST PANEL")
    st.write(f"👤 **Master:** Exile")
    st.write("---")
    # Özellik: Paralel Evren Analizi
    parallel_mode = st.toggle("🌌 Paralel Evren Analizi", value=True)
    st.markdown("---")
    if st.button("🗑️ İzleri Sil (Clear)"):
        st.session_state.messages = []
        st.rerun()

# --- 5. SOHBET VE DUYGU ANALİZİ (DÜNYADA İLK) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Exile, zihnini sisteme bağla..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Duygu Analizi ve Renk Değişimi
    if any(kelime in prompt.lower() for kelime in ["hızlı", "savaş", "yap", "hemen"]):
        st.session_state.dna_color = "#ff0000" # Agresif/Hızlı Mod (Kırmızı)
    elif any(kelime in prompt.lower() for kelime in ["selam", "merhaba", "nasılsın"]):
        st.session_state.dna_color = "#00ff00" # Dost Modu (Yeşil)
    else:
        st.session_state.dna_color = "#00f2fe" # Standart Mod (Mavi)

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Ana Yanıt
            main_resp = astra_engine.generate_content(f"Sen Astra'sın. Exile seni yarattı. Soru: {prompt}")
            st.markdown(main_resp.text)
            
            # PARALEL EVREN ÖZELLİĞİ
            if parallel_mode:
                with st.expander("🌌 Paralel Evren Senaryosu (Farklı Bir Olasılık)"):
                    alt_resp = astra_engine.generate_content(f"Bu soruya ('{prompt}') bambaşka, daha karanlık veya daha sanatsal bir alternatif cevap ver.")
                    st.write(alt_resp.text)
            
            st.session_state.messages.append({"role": "assistant", "content": main_resp.text})
            st.rerun() # Renk değişimini anlık yansıtmak için
            
        except Exception as e:
            st.error(f"Sinyal Bozulması: {e}")
