import streamlit as st
import google.generativeai as genai
import time

# --- 1. SİSTEM YAPILANDIRMASI ---
st.set_page_config(page_title="AstraUltra", page_icon="💫", layout="wide")

if "NOVAKEY" in st.secrets:
    genai.configure(api_key=st.secrets["NOVAKEY"])
    astra_engine = genai.GenerativeModel('models/gemini-2.5-flash')
else:
    st.error("API ANAHTARI BULUNAMADI!")
    st.stop()

# --- 2. GÖRSEL EFEKTLER (CSS) ---
st.markdown("""
<style>
    .stApp { background: #000; color: #00f2fe; }
    .astra-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 55px; font-weight: 900; text-align: center;
        background: linear-gradient(90deg, #00f2fe, #7028e4, #ff00c8);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        animation: flow 6s linear infinite;
    }
    @keyframes flow { to { background-position: 200% center; } }
    
    /* Enerji Barı Tasarımı */
    .recovery-container {
        border: 2px solid #7028e4; border-radius: 15px;
        padding: 30px; text-align: center; background: rgba(112, 40, 228, 0.1);
    }
    .recovery-bar-bg {
        width: 100%; background: #111; border-radius: 20px;
        height: 25px; margin-top: 20px; overflow: hidden;
    }
    .recovery-bar-fill {
        height: 100%; background: linear-gradient(90deg, #00f2fe, #7028e4);
        width: 0%; transition: width 1s linear;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. DÖNGÜSEL KOTA TAKİBİ ---
if "counter" not in st.session_state:
    st.session_state.counter = 0

# --- 4. ENERJİ YENİLEME EKRANI (Her 19 Soruda Bir) ---
if st.session_state.counter >= 19:
    st.markdown("<div class='astra-title'>AstraUltra</div>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("<div class='recovery-container'>", unsafe_allow_html=True)
        st.markdown("<h2 style='color:#7028e4;'>🔄 ENERJİ DÖNGÜSÜ BAŞLATILDI</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color:#888;'>Exile Protokolü: Kotanız 20 saniye içinde optimize ediliyor...</p>", unsafe_allow_html=True)
        
        timer_text = st.empty()
        bar_fill = st.empty()
        
        for i in range(20, -1, -1):
            percent = (20 - i) * 5
            timer_text.markdown(f"<h1 style='color:#00f2fe;'>{i}s</h1>", unsafe_allow_html=True)
            bar_fill.markdown(f"""
                <div class='recovery-bar-bg'>
                    <div class='recovery-bar-fill' style='width: {percent}%;'></div>
                </div>
            """, unsafe_allow_html=True)
            time.sleep(1)
            
        st.markdown("</div>", unsafe_allow_html=True)
        
        # SIFIRLAMA VE YENİDEN BAŞLATMA
        st.session_state.counter = 0 
        st.success("✨ Enerji %100! Yeni bir 19 soruluk döngü hazır.")
        time.sleep(1.5)
        st.rerun()

# --- 5. ANA SOHBET EKRANI ---
st.markdown("<div class='astra-title'>AstraUltra</div>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# Giriş Alanı
if prompt := st.chat_input("Astraya sorun"):
    st.session_state.counter += 1 # Sayacı 1 artır
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Akıllı Kimlik (Sohbetin en başında)
            prefix = "Ben AstraUltra, Bedirhan'ın (Exile) yarattığı bir yapay zeka. " if len(st.session_state.messages) <= 2 else ""
            
            with st.spinner("Düşünüyor..."):
                context = f"Sen AstraUltra'sın. Seni Bedirhan (Exile) yarattı. Soru: {prompt}"
                response = astra_engine.generate_content(context)
            
            answer = prefix + response.text
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
            
            # Sağ alt bilgi
            st.sidebar.markdown(f"📊 **Döngü Durumu:** {st.session_state.counter} / 19")
            
        except Exception as e:
            if "429" in str(e):
                st.session_state.counter = 19 # Eğer Google erken kota verirse zorla döngüye sok
                st.rerun()
            else:
                st.error(f"Sistem Hatası: {e}")
