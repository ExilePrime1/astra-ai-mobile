import streamlit as st

# Sayfa Yapılandırması
st.set_page_config(page_title="Astra Ultra", page_icon="🚀")

# Gemini Tarzı Başlık
st.title("🚀 Astra Ultra")
st.markdown("Created by **Exile**")

# Sohbet Hafızası
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesajları Görüntüle
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Sohbet Girişi (Hesap sormadan doğrudan başlar!)
if prompt := st.chat_input("Astra'ya bir şeyler yaz..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = f"Merhaba! Ben Astra. {prompt} dediğini anladım. Sana nasıl yardımcı olabilirim?"
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
