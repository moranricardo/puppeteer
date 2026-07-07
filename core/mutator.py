import os
import shutil
import sys
from memory import recordar

BASE_DIR = "/data/data/com.termux/files/home/bot-factory"

def transmutar(nombre_archivo, nuevo_codigo_path):
    ruta_destino = f"{BASE_DIR}/core/{nombre_archivo}"
    ruta_bak = f"{ruta_destino}.bak"
    
    msg = f"Iniciando transmutación de {nombre_archivo}"
    recordar(msg, tipo="mutacion")
    
    shutil.copy(ruta_destino, ruta_bak)
    shutil.move(nuevo_codigo_path, ruta_destino)
    
    from health import calcular_salud
    salud_valor, _ = calcular_salud()
    
    if salud_valor < 90.0:
        recordar(f"Fallo en transmutación de {nombre_archivo}. Revertiendo.", tipo="mutacion")
        shutil.move(ruta_bak, ruta_destino)
        return False
    
    recordar(f"Transmutación exitosa: {nombre_archivo}", tipo="mutacion")
    os.remove(ruta_bak)
    return True
