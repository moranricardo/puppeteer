import json
import os
from datetime import datetime
from filters.maat_filter import MaatFilter

def generate_manifest():
    mf = MaatFilter()
    root_dir = os.path.expanduser("~/bot-factory")
    manifest_data = {
        "node_id": "root_01",
        "timestamp": datetime.now().isoformat(),
        "verified_files": []
    }
    
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            path = os.path.join(root, file)
            # Creamos un objeto de datos para Maat
            data_to_validate = {"content": path, "timestamp": datetime.now().isoformat()}
            
            # Aplicamos el filtro
            if mf.validate(data_to_validate):
                manifest_data["verified_files"].append(path)
                
    with open(os.path.expanduser("~/bot-factory/knowledge_graph/system_manifest.json"), "w") as f:
        json.dump(manifest_data, f, indent=4)
    print(f"Manifestación purificada: {len(manifest_data['verified_files'])} archivos validados.")

if __name__ == "__main__":
    generate_manifest()
