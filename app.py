def get_astra_response(user_input):
    shuffled_keys = random.sample(keys, len(keys))
    
    # Sırayla en garantiden en yeniye modeller
    model_list = ['gemini-1.5-flash', 'gemini-1.5-pro']
    
    for key in shuffled_keys:
        for model_name in model_list:
            try:
                genai.configure(api_key=key)
                # Güvenlik ayarlarını gevşeterek engelleri kaldırıyoruz
                model = genai.GenerativeModel(
                    model_name=model_name,
                    safety_settings={
                        "HARM_CATEGORY_HARASSMENT": "BLOCK_NONE",
                        "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE",
                        "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_NONE",
                        "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_NONE",
                    }
                )
                
                prefix = "Ben AstraUltra, Bedirhan'ın (Exile) yarattığı bir yapay zeka. " if len(st.session_state.messages) <= 1 else ""
                
                response = model.generate_content(user_input)
                if response.text:
                    return prefix + response.text
            except Exception as e:
                # "Unavailable" hatasını burada yakalayıp bir sonrakine geçer
                continue
                
    return "🚫 Bedirhan, Google servisleri şu an bölgen için 'Unavailable' diyor. Lütfen 5 dakika sonra tekrar dene."
