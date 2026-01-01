import streamlit as st
import google.generativeai as genai

# --- 1. ASTRA ÇEKİRDEK (GİZLİ KASA BAĞLANTISI) ---
# Bu satır, Streamlit Secrets paneline eklediğin "NOVAKEY"i çağırır.
try:
    ASTRA_CORE_KEY = st.secrets["NOVAKEY"] 
    genai.configure(api_key=ASTRA_CORE_KEY)
    # En hızlı ve güncel model çekirdeği
    astra_engine = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("⚠️ SİSTEM HATASI: 'NOVAKEY' bulunamadı veya geçersiz.")
    st.stop()

# --- 2. NOVA UI (GÖRSEL TASARIM) ---
st.set_page_config(page_title="Astra 3.0 Nova", page_icon="☄️", layout="centered")

st.markdown("""
<style>
    .stApp { background-color: #050508; color: #ffffff; }
    .astra-brand {
        font-family: 'Courier New', monospace;
        font-size: 60px;
        font-weight: bold;
        text-align: center;
        background: -webkit-linear-gradient(#00f2fe, #7028e4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 20px rgba(112, 40, 228, 0.5);
    }
    .exile-tag {
        text-align: center;
        font-size: 14px;
        color: #444;
        letter-spacing: 8px;
        margin-bottom: 30px;
    }
    /* Mesaj Balonları */
    [data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 15px;
        border: 1px solid rgba(112, 40, 228, 0.3);
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. ERİŞİM KONTROLÜ ---
if "nova_access" not in st.session_state:
    st.session_state.nova_access = False

if not st.session_state.nova_access:
    st.markdown("<div class='astra-brand'>ASTRA 3.0</div>", unsafe_allow_html=True)
    st.markdown("<div class='exile-tag'>CREATED BY EXILE</div>", unsafe_allow_html=True)
    
    with st.container():
        password = st.text_input("Nova Giriş Şifresi:", type="password")
        if st.button("SİSTEMİ ATEŞLE"):
            if password == "1234":
                st.session_state.nova_access = True
                st.rerun()
            else:
                st.error("Erişim Reddedildi: Yetkisiz Giriş.")
    st.stop()

# --- 4. SOHBET MOTORU ---
st.markdown("<div class='astra-brand'>ASTRA 3.0</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#00f2fe; font-size:12px;'>Sistem Durumu: Çevrimiçi | Kullanıcı: Exile</p>", unsafe_allow_html=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sadece son 10 mesajı göstererek kota tasarrufu yapıyoruz
for msg in st.session_state.chat_history[-10:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if user_input := st.chat_input("Komutunu Bekliyorum, Exile..."):
    # Kullanıcı mesajını ekle
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        try:
            # Astra Kimlik Talimatı
            system_instruction = "Sen Astra 3.0'sın. Seni Bedirhan (Exile) yarattı. Zeki, sadık ve profesyonel bir yapay zekasın."
            
            # Yanıtı oluştur
            response = astra_engine.generate_content(f"{system_instruction} \n Soru: {user_input}")
            
            st.markdown(response.text)
            st.session_state.chat_history.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"⚠️ SİNYAL KESİLDİ: {str(e)}")
            st.info("İpucu: Google Cloud projesinde API'nin aktif olduğundan emin ol.")
