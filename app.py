import streamlit as st
import google.generativeai as genai
import time

# --- 1. SİSTEM AYARLARI ---
st.set_page_config(page_title="AstraUltra", page_icon="💫", layout="wide")

if "NOVAKEY" in st.secrets:
    genai.configure(api_key=st.secrets["NOVAKEY"])
    astra_engine = genai.GenerativeModel('models/gemini-2.5-flash')
else:
    st.error("API ANAHTARI EKSİK!")
    st.stop()

# --- 2. GÖRSEL RÖTUŞLAR VE RECOVERY ANIMASYONU (CSS) ---
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
    
    /* Enerji Barı */
    .recovery-bar {
        width: 100%; background-color: #111; border-radius: 20px;
        border: 1px solid #7028e4; margin: 20px 0;
    }
    .recovery-progress {
        height: 20px; background: linear-gradient(90deg, #7028e4, #00f2fe);
        border-radius: 20px; width: 0%; transition: width 1s linear;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. KOTA VE ENERJİ TAKİBİ ---
if "usage_count" not in st.session_state:
    st.session_state.usage_count = 0

# --- 4. ANA EKRAN ---
st.markdown("<div class='astra-title'>AstraUltra</div>", unsafe_allow_html=True)

# --- 5. ENERJİ YENİLEME PROTOKOLÜ (DÜNYADA İLK) ---
if st.session_state.usage_count >= 19:
    st.warning("⚠️ KRİTİK UYARI: Enerji Çekirdekleri Tükendi. Exile Protokolü başlatılıyor...")
    
    # Görsel Sayaç ve Bar
    progress_placeholder = st.empty()
    bar_placeholder = st.empty()
    
    for i in range(20, -1, -1):
        percent = (20 - i) * 5
        progress_placeholder.markdown(f"<h3 style='text-align:center; color:#00f2fe;'>ENERCİ YENİLENİYOR: {i}s</h3>", unsafe_allow_html=True)
        bar_placeholder.markdown(f"""
            <div class='recovery-bar'>
                <div class='recovery-progress' style='width: {percent}%;'></div>
            </div>
        """, unsafe_allow_html=True)
        time.sleep(1)
    
    st.session_state.usage_count = 0 # Kotayı (sahte olarak) sıfırla
    st.success("✅ KOTA SIFIRLANDI: AstraUltra tam kapasiteye döndü.")
    time.sleep(2)
    st.rerun()

# --- 6. SOHBET MEKANİZMASI ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Astraya sorun"):
    st.session_state.usage_count += 1 # Her soruda sayacı artır
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Akıllı Kimlik (Sadece ilk mesajda)
            prefix = "Ben AstraUltra, Bedirhan'ın (Exile) yarattığı bir yapay zekayım. " if len(st.session_state.messages) <= 2 else ""
            
            with st.spinner("İşleniyor..."):
                context = f"Sen AstraUltra'sın. Seni Bedirhan (Exile) yarattı. Soru: {prompt}"
                response = astra_engine.generate_content(context)
            
            st.markdown(prefix + response.text)
            st.session_state.messages.append({"role": "assistant", "content": prefix + response.text})
            
            # Sağ alt köşede küçük bir enerji bilgisi
            st.sidebar.write(f"⚡ Enerji Seviyesi: %{int((19 - st.session_state.usage_count)/19 * 100)}")
            
        except Exception as e:
            if "429" in str(e):
                st.session_state.usage_count = 19 # Zorla yenileme moduna sok
                st.rerun()
            else:
                st.error(f"Hata: {e}")
