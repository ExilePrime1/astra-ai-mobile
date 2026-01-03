import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="AstraUltra Diagnostik", page_icon="🔱")

st.title("🔱 AstraUltra: Model Tarayıcı")

# Secrets kontrolü
if "NOVAKEY" in st.secrets:
    # İlk anahtarı alıp deneyeceğiz
    key = st.secrets["NOVAKEY"].split(",")[0].strip()
    genai.configure(api_key=key)
else:
    st.error("Anahtar bulunamadı!")
    st.stop()

if st.button("Hangi Modeller Açık? (TARA)"):
    try:
        st.write("Google sunucularına bağlanılıyor...")
        # Mevcut modelleri listele
        available_models = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                available_models.append(m.name)
        
        if available_models:
            st.success("✅ BAĞLANTI BAŞARILI! Erişilebilir Modeller:")
            st.json(available_models)
            st.info("Bedirhan, yukarıdaki listede 'models/gemini-...' ile başlayan isimleri koda yazmalıyız.")
        else:
            st.error("Bağlantı kuruldu ama hiç model bulunamadı. (Bölgesel kısıtlama olabilir)")
            
    except Exception as e:
        st.error(f"Sistem Hatası: {e}")
        st.warning("Eğer hata 'AttributeError' ise, requirements.txt dosyan çalışmamış demektir.")
