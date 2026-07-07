import json
import os

manifest_path = os.path.expanduser('~/bot-factory/knowledge_graph/system_manifest.json')

def ask_ra(query):
    if not os.path.exists(manifest_path):
        return "Error: Manifiesto no encontrado."
    with open(manifest_path, 'r') as f:
        data = json.load(f)
    query = query.lower()
    results = [f for f in data['verified_files'] if query in f.lower()]
    return f"Ra Pulse localizó:\n" + "\n".join(results[:5]) if results else "Ra Pulse: Sin coincidencias."

if __name__ == "__main__":
    import sys
    print(ask_ra(" ".join(sys.argv[1:])))
