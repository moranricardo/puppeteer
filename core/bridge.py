import os
import json
from pathlib import Path
import google.generativeai as genai

def inicializar_modelo():
    """Configura y retorna la instancia del modelo de Gemini."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("⚠️ ALERTA: GEMINI_API_KEY no encontrada en el entorno.")
        return None
        
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(
        model_name='gemini-3.5-flash',
        system_instruction="Eres el núcleo cognitivo de Ra Pulse. Analizas el estado del sistema y respondes con recomendaciones estructuradas y accionables."
    )

def consultar_ra(prompt_contexto):
    """Envía una consulta al núcleo cognitivo."""
    model = inicializar_modelo()
    if not model:
        return "ERROR: No se pudo conectar con Gemini API (Falta API Key)."

    try:
        response = model.generate_content(f"Estado del sistema / Contexto:\n{prompt_contexto}")
        return response.text
    except Exception as e:
        return f"ERROR durante la inferencia cognitiva: {str(e)}"

if __name__ == "__main__":
    print("🧠 Puente cognitivo de Ra Pulse inicializado (Gemini 3.5 Flash).")
    
    # Cargar estado actual de config/state.json si existe
    base_dir = Path(__file__).resolve().parent.parent
    state_file = base_dir / "config" / "state.json"
    
    if state_file.exists():
        with open(state_file, "r", encoding="utf-8") as f:
            estado_actual = f.read()
        print("\n📊 Estado detectado en config/state.json:")
        print(estado_actual)
    else:
        print("\nℹ️ No se encontró config/state.json para la prueba local.")
