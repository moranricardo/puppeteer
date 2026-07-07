import os
import json
import google.generativeai as genai

# Configuración del puente
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-pro')

def consultar_ra(prompt_contexto):
    response = model.generate_content(f"Eres el núcleo cognitivo de Ra Pulse. Analiza el siguiente estado del sistema y responde con una recomendación estructurada: {prompt_contexto}")
    return response.text

if __name__ == "__main__":
    # Aquí cargaremos el estado extraído de status.log y memory.py
    print("Puente cognitivo inicializado.")
