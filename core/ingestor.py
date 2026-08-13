import json
import urllib.request
import urllib.error

def obtener_cambios_gerrit(limite=5):
    """Obtiene los parches abiertos recientes desde la API de Gerrit."""
    url = f"https://gerrit.wikimedia.org/r/changes/?q=status:open&n={limite}"
    req = urllib.request.Request(
        url, 
        headers={"User-Agent": "RaPulse-Ingestor/1.2.0"}
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            raw_data = response.read().decode('utf-8')
            # Limpieza del prefijo de seguridad de Gerrit ()]}')
            json_str = raw_data.split('\n', 1)[1] if '\n' in raw_data else raw_data
            return json.loads(json_str)
    except urllib.error.URLError as e:
        print(f"[-] ERROR: Fallo de red en la ingesta -> {e}")
        return []
    except Exception as e:
        print(f"[-] ERROR: Fallo general en la ingesta -> {e}")
        return []

if __name__ == "__main__":
    print("📡 Iniciando ingesta de telemetría externa (Gerrit)...")
    cambios = obtener_cambios_gerrit()
    
    if cambios:
        print(f"[+] Se recuperaron {len(cambios)} registros:")
        for cambio in cambios:
            print(f"    • ID: {cambio.get('_number')} | Asunto: {cambio.get('subject')}")
    else:
        print("ℹ️ No se obtuvieron cambios o hubo un error en la conexión.")
