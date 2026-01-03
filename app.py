 import streamlit as st
import google.generativeai as genai
import random
import time

# ... (Tasarım kısımları aynı kalsın) ...

def get_astra_response(user_input):
    shuffled_keys = random.sample(keys, len(keys))
    
    # 2026'nın en stabil ve geniş kotalı modelleri
    model_pool = [
        "models/gemini-2.0-flash", # En dengeli olan
        "models/gemini-1.5-flash", # En yüksek kotalı olan
        "models/gemini-2.5-flash-lite" # En hafif olan
    ]
    
    for key in shuffled_keys:
        try:
            genai.configure(api_key=key)
            for model_name in model_pool:
                try:
                    model = genai.GenerativeModel(model_name)
                    # Google'ı yormamak için mikro bekleme
                    time.sleep(0.2) 
                    
                    response = model.generate_content(user_input)
                    if response and response.text:
                        return response.text
                except Exception as e:
                    if "429" in str(e): # Kota hatasıysa beklemeden diğer anahtara geç
                        break 
                    continue
        except:
            continue
            
    return "⚠️ Bedirhan, Google tüm projelerine kota sınırı koymuş. AI Studio'dan 'New Project' ile yeni anahtarlar alman lazım."
