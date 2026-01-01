import streamlit as st
import google.generativeai as genai

# --- 1. BEYİN YAPILANDIRMASI ---
GOOGLE_API_KEY = "AIzaSyA34SS1f-QgCMzeuuoXSyjvtkQpjGhvgBI"
genai.configure(api_key=GOOGLE_API_KEY)

# En güvenli ve hızlı model
@st.cache_resource
def astra_brain():
    return genai.GenerativeModel('gemini-1.5-flash')

model = astra_brain()

st.set_page_config(page_title="AstraUltra", page_icon="✨", layout="wide")

# --- 2. ASTRAULTRA ÖZEL TASARIM (UZAY TEMASI) ---
st.markdown("""
<style>
    /* Ana Ekran: Derin Uzay Siyahı */
    .stApp {
        background: radial-gradient(circle at top, #1a1a2e 0%, #0f0f1b 100%);
        color: #e0e0e0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Başlık: Yıldız ve Galaksi Renkleri (İsmin Anlamına Göre) */
    .astra-title {
        font-size: 50px;
        font-weight: 800;
        background: linear-gradient(45deg, #4facfe 0%, #00f2fe 25%, #7028e4 50%, #e5b2ca 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        letter-spacing: 5px;
        margin-top: 20px;
        filter: drop-shadow(0 0 15px rgba(79, 172, 254, 0.5));
    }

    /* Mesaj Kutuları: Şeffaf ve Cam Efekti (Glassmorphism) */
    [data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        margin-bottom: 15px;
        backdrop-filter: blur(10px);
    }

    /* Gelişmiş Giriş Alanı */
    .stChatInputContainer {
        border-radius: 30px !important;
        border: 1px solid #4facfe !important;
        background: rgba(15, 15, 27, 0.9) !important;
        box-shadow: 0 0 20px rgba(79, 172, 254, 0.2);
    }

    /* Sidebar ve Header Temizliği */
    header {visibility: hidden;}
    [data-testid="stSidebar"] {
        background-color: rgba(15, 15, 27, 0.8);
        border-right: 1px solid #7028e4;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. ERİŞİM KONTROLÜ ---
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.markdown("<div class='astra-title'>ASTRAULTRA</div>", unsafe_allow_html=True)
    with st.container():
        key = st.text_input("Sistemi Uyandır (Şifre)", type="password")
        if st.button("Başlat"):
            if key == "1234":
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("Erişim reddedildi.")
    st.stop()

# --- 4. ANA ARAYÜZ ---
st.markdown("<div class='astra-title'>ASTRAULTRA</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>Exile'ın Yıldızlar Arası Asistanı</p>", unsafe_allow_html=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Mesaj Geçmişini Göster
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.markdown(chat["content"])

# Yeni Mesaj Girişi
if user_input := st.chat_input("Yıldızlara bir mesaj gönder..."):
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        try:
            # Bedirhan (Exile) kimliğini koruyan sistem talimatı
            prompt = f"Senin adın AstraUltra. Seni Bedirhan (Exile) yarattı. Sen bir yıldız kadar parlak ve zeki bir asistansın. Cevapların kısa, öz ve etkileyici olsun. Soru: {user_input}"
            response = model.generate_content(prompt)
            if response.text:
                st.markdown(response.text)
                st.session_state.chat_history.append({"role": "assistant", "content": response.text})
        except Exception:
            st.error("🚀 Galaksiler arası bağlantıda kısa bir kopukluk oldu. Lütfen tekrar dene.")

# --- 5. YAN PANEL (SIDEBAR) ---
with st.sidebar:
    st.markdown("<h3 style='color: #4facfe;'>Sistem Paneli</h3>", unsafe_allow_html=True)
    st.write("✨ **Durum:** Aktif")
    st.write("🛸 **Sürüm:** 3.0 Nova")
    st.write("👤 **Sahip:** Exile")
    st.divider()
    if st.button("Hafızayı Sıfırla"):
        st.session_state.chat_history = []
        st.rerun()
