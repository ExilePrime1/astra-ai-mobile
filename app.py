import streamlit as st
import google.generativeai as genai

# --- 1. ASTRA ÇEKİRDEK YAPILANDIRMASI ---
# Buraya Google AI Studio'dan aldığın anahtarı yapıştır
ASTRA_CORE_KEY = "BURAYA_API_KEYINI_YAPISTIR" 

genai.configure(api_key=ASTRA_CORE_KEY)
# Motoru arka planda çalıştırıyoruz ama adını Astra koyuyoruz
astra_engine = genai.GenerativeModel('gemini-1.5-flash')

# --- 2. ÖZEL TASARIM (DARK SPACE UI) ---
st.set_page_config(page_title="Astra 3.0 Nova", page_icon="☄️")

st.markdown("""
<style>
    .stApp { background-color: #050508; color: #ffffff; }
    
    /* Astra 3.0 Parlayan Başlık */
    .astra-brand {
        font-family: 'Courier New', monospace;
        font-size: 55px;
        font-weight: bold;
        text-align: center;
        color: #fff;
        text-shadow: 0 0 10px #7028e4, 0 0 20px #7028e4, 0 0 40px #00f2fe;
        margin-bottom: 0px;
    }
    
    .exile-signature {
        text-align: center;
        font-size: 14px;
        color: #444;
        letter-spacing: 10px;
        text-transform: uppercase;
        margin-bottom: 50px;
    }

    /* Mesaj Balonları - Astra Stili */
    [data-testid="stChatMessage"] {
        background: rgba(15, 15, 25, 0.8);
        border-left: 5px solid #7028e4;
        border-radius: 0px 15px 15px 0px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. NOVA ERİŞİM KONTROLÜ ---
if "nova_access" not in st.session_state:
    st.session_state.nova_access = False

if not st.session_state.nova_access:
    st.markdown("<div class='astra-brand'>ASTRA 3.0</div>", unsafe_allow_html=True)
    st.markdown("<div class='exile-signature'>Exile OS v3</div>", unsafe_allow_html=True)
    
    password = st.text_input("Sistem Şifresi:", type="password")
    if st.button("ASTRA'YI BAŞLAT"):
        if password == "1234":
            st.session_state.nova_access = True
            st.rerun()
        else:
            st.error("Erişim Reddedildi.")
    st.stop()

# --- 4. ASTRA 3.0 SOHBET ARAYÜZÜ ---
st.markdown("<div class='astra-brand'>ASTRA 3.0</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#00f2fe; font-size:12px;'>Nova Sürümü Aktif | Kullanıcı: Exile</p>", unsafe_allow_html=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if user_input := st.chat_input("Astra'ya komut ver..."):
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        try:
            # SİSTEM TALİMATI: Burada ona Gemini olduğunu unutturuyoruz!
            system_instruction = (
                "Senin adın Astra 3.0. Sen Bedirhan (Exile) tarafından geliştirilen özel bir yapay zekasın. "
                "Gemini veya Google kelimelerini asla kullanma. Sorulduğunda 'Ben Astra 3.0'ım ve yaratıcım Exile' de. "
                "Ciddi, zeki ve tamamen Bedirhan'a odaklı cevaplar ver."
            )
            
            response = astra_engine.generate_content(f"{system_instruction} \n\n Kullanıcı: {user_input}")
            
            st.markdown(response.text)
            st.session_state.chat_history.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error("⚠️ Astra 3.0 Çekirdek Hatası: Sinyal zayıf.")
