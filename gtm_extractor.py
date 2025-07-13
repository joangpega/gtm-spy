import requests
import re
import json

def fetch_gtm_script(container_id):
    url = f"https://www.googletagmanager.com/gtm.js?id={container_id}"
    response = requests.get(url)
    
    if response.status_code == 200:
        print("✔️ Código GTM descargado")
        return response.text
    else:
        raise Exception(f"❌ Error al descargar GTM ({response.status_code})")

def extraer_objetos_posibles(js_code):
    """
    Busca bloques con estructuras JSON dentro del código JS, heurísticamente.
    GTM no expone todo como JSON, pero algunas etiquetas o configs sí aparecen como objetos.
    """
    objetos = []

    # Buscar bloques que parecen objetos JSON o inicializaciones
    matches = re.findall(r'{.*?}', js_code, re.DOTALL)
    
    for match in matches:
        try:
            # Prueba a convertirlo en JSON
            obj = json.loads(match)
            objetos.append(obj)
        except Exception:
            continue  # ignora los que no son JSON válidos

    return objetos

def guardar_como_json(data, filename="gtm_extracted.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"📁 Archivo guardado como {filename}")

def main():
    container_id = "GTM-XXXXXX"  # reemplázalo por un contenedor real
    js_code = fetch_gtm_script(container_id)
    
    print("🔍 Buscando objetos tipo JSON...")
    objetos = extraer_objetos_posibles(js_code)

    if objetos:
        print(f"✅ Se extrajeron {len(objetos)} objetos")
        guardar_como_json(objetos)
    else:
        print("⚠️ No se encontraron objetos JSON válidos")

if __name__ == "__main__":
    main()