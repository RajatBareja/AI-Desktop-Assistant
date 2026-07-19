import google.generativeai as genai
genai.configure(api_key="TERI_GEMINI_KEY")

for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name) # Ye tujhe sahi model name bata dega