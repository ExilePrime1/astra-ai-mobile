import streamlit as st
import google.generativeai as genai
import time

# --- 1. SİSTEM YAPILANDIRMASI ---
st.set_page_config(page_title="Astra 3.0 Nova - Ultra", page_icon="☄️", layout="wide")

# API Bağlantısı
if "NOVAKEY" in st.secrets:
    genai.configure(api_key=st.secrets["NOVAKEY"])
    # 2.5 Flash motoru ile yüksek performans
    model = genai.GenerativeModel('models/gemini-2.5-flash')
else:
    st.error("⚠️ NOVAKEY Eksik!")
    st.stop()

# --- 2. GÖRSEL TASARIM (CSS) ---
st.markdown("""
<style>
    .stApp { background-color: #050508; color: #e0e0e0; }
    .main-title { font-family: 'Courier New', monospace; font-size: 60px; font-weight: bold; text-align: center;
        background: linear-gradient(90deg, #00f2fe, #7028e4, #00f2fe); background-size: 200% auto;
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; animation: shine 3s linear infinite; }
    @keyframes shine { to { background-position: 200% center; } }
    .stChatMessage { border-radius: 15px; border: 1px solid #1a1a2e; margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR (AYARLAR VE ÖZELLİKLER) ---
with st.sidebar:
    st.markdown("### 🛠️ ASTRA KONTROL")
    st.info(f"Yaratıcı: **Exile**") #
    if st.button("🗑️ Sohbeti Temizle"):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    uploaded_file = st.file_uploader("🖼️ Resim veya Dosya Analizi", type=['png', 'jpg', 'jpeg', 'pdf', 'txt'])
    st.markdown("---")
    st.write("🛰️ **Sinyal:** Maksimum")

# --- 4. ERİŞİM KONTROLÜ ---
if "nova_auth" not in st.session_state:
    st.session_state.nova_auth = False

if not st.session_state.nova_auth:
    st.markdown("<h1 class='main-title'>ASTRA 3.0</h1>", unsafe_allow_html=True)
    pw = st.text_input("Sistem Şifresi:", type="password")
    if st.button("ERİŞİM SAĞLA"):
        if pw == "1234":
            st.session_state.nova_auth = True
            st.rerun()
    st.stop()

# --- 5. ANA EKRAN & SOHBET ---
st.markdown("<h1 class='main-title'>ASTRA 3.0 NOVA</h1>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# Giriş Alanı
if prompt := st.chat_input("Emret Exile..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        start_time = time.time()
        try:
            # Sistem Talimatı
            context_prompt = f"Sen Astra 3.0 Nova'sın. Bedirhan (Exile) seni yarattı. Çok zekice ve Exile'a sadık cevaplar ver. Soru: {prompt}"
            
            # Eğer dosya yüklendiyse onu da işleme kat
            if uploaded_file:
                # Dosya işleme mantığı buraya eklenebilir
                response = model.generate_content([context_prompt, uploaded_file])
            else:
                response = model.generate_content(context_prompt)
            
            end_time = time.time()
            st.markdown(response.text)
            st.caption(f"⏱️ İşlem Süresi: {round(end_time - start_time, 2)} saniye")
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            st.error(f"Sinyal Kaybı: {e}")
