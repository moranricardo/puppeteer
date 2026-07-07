import os
import json

def verify_env():
    key = os.environ.get('GEMINI_API_KEY')
    if key:
        print("Estado: API KEY detectada correctamente.")
    else:
        print("Error: API KEY no encontrada.")

if __name__ == "__main__":
    verify_env()

