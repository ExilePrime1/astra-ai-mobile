import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Astra Tanı Modu", page_icon="🛠️")

st.title("🛠️ Sistem Tarama Modu")

try:
    if "NOVAKEY" in st.secrets:
        # API Bağlantısı
        genai.configure(api_key=st.secrets["NOVAKEY"])
        
        st.info("📡 Google Sunucularına Bağlanılıyor...")
        
        # Mevcut modelleri çek ve listele
        found_models = []
        for m in genai.list_models():
            # Sadece sohbet edebilen modelleri filtrele
            if 'generateContent' in m.supported_generation_methods:
                found_models.append(m.name)
        
        if found_models:
            st.success("✅ BAĞLANTI BAŞARILI! Senin API Anahtarının izinli olduğu modeller şunlar:")
            st.code(found_models)
            st.warning("Lütfen bu listedeki isimlerden birini (örneğin 'models/gemini-pro') kopyalayıp bana söyle.")
        else:
            st.error("❌ Bağlantı var ama hiç model bulunamadı. API Key yetkilerinde sorun olabilir.")
            
    else:
        st.error("⚠️ Secrets içinde NOVAKEY bulunamadı.")

except Exception as e:
    st.error(f"⚠️ KRİTİK HATA: {str(e)}")
