import streamlit as st

# Sayfa Ayarları
st.set_page_config(page_title="Astra Ultra", page_icon="🚀")

# 1. Şifre Kontrolü İçin Hafıza Fonksiyonu
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Şifre Onaylama Fonksiyonu
def check_password():
    if st.session_state["password_input"] == "1234": # Şifreni buradan değiştirebilirsin
        st.session_state.authenticated = True
    else:
        st.error("❌ Hatalı şifre, Astra erişimi reddetti!")

# 2. Giriş Ekranı (Sadece giriş yapılmadıysa görünür)
if not st.session_state.authenticated:
    st.title("🔒 Astra Ultra Güvenli Giriş")
    st.write("Lütfen erişim anahtarını girin.")
    
    # Şifre kutusu
    st.text_input("Şifre", type="password", key="password_input", on_change=check_password)
    st.button("Giriş Yap", on_click=check_password)
    
    st.info("Created by **Exile**")
    st.stop()

# 3. ANA UYGULAMA (Şifre girildikten sonra burası açılır)
# Buradan sonrası uygulama açık kaldığı sürece görünür kalır.
st.title("🚀 Astra Ultra")
st.success("Erişim Onaylandı. Hoş geldiniz!")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesajları göster
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Sohbet Girişi
if prompt := st.chat_input("Astra'ya bir şeyler sor..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = f"Astra: '{prompt}' hakkında ne bilmek istersin? Senin için buradayım."
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
