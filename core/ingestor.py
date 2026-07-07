import json
import urllib.request

def obtener_cambios_gerrit():
    # Endpoint de cambios abiertos (n=5 para mantener la ligereza)
    url = "https://gerrit.wikimedia.org/r/changes/?q=status:open&n=5"
    
    try:
        with urllib.request.urlopen(url) as response:
            raw_data = response.read().decode('utf-8')
            # Limpieza del prefijo de seguridad de Gerrit
            json_data = raw_data.split('\n', 1)[1]
            return json.loads(json_data)
    except Exception as e:
        print(f"ERROR: Fallo en la ingesta -> {e}")
        return []

if __name__ == "__main__":
    cambios = obtener_cambios_gerrit()
    for cambio in cambios:
        print(f"ID: {cambio.get('_number')} | Asunto: {cambio.get('subject')}")
