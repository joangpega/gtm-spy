import requests
import re
import json
from urllib.parse import urlparse

def get_gtm_ids_from_website(url):
    """Scrapea una página web para encontrar IDs de contenedores GTM"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        raise Exception(f"❌ Error al acceder a la URL: {str(e)}")

    # Buscar el formato estándar de GTM (GTM-XXXXXX)
    gtm_ids = set(re.findall(r'GTM-[A-Z0-9]{4,7}', response.text))
    
    # Buscar en el dataLayer (común en implementaciones GTM)
    data_layer_matches = re.findall(r'dataLayer\s*\.\s*push\s*\(\s*{[^}]*\'gtm\.start\'[^}]*\'gtm\.id\'\s*:\s*\'([^\']+)\'', response.text)
    for match in data_layer_matches:
        if match.startswith('GTM-'):
            gtm_ids.add(match)

    # Buscar en scripts de GTM
    script_matches = re.findall(r'googletagmanager\.com/gtm\.js\?id=(GTM-[A-Z0-9]{4,7})', response.text)
    gtm_ids.update(script_matches)

    # Buscar en iframes
    iframe_matches = re.findall(r'www\.googletagmanager\.com/ns\.html\?id=(GTM-[A-Z0-9]{4,7})', response.text)
    gtm_ids.update(iframe_matches)

    if not gtm_ids:
        raise Exception("⚠️ No se encontraron contenedores GTM en la página")

    return list(gtm_ids)

def fetch_gtm_script(container_id):
    """Descarga el código JavaScript del contenedor GTM"""
    url = f"https://www.googletagmanager.com/gtm.js?id={container_id}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        print(f"✔️ Código GTM descargado para {container_id}")
        return response.text
    except requests.RequestException as e:
        raise Exception(f"❌ Error al descargar GTM {container_id}: {str(e)}")

def extraer_objetos_posibles(js_code):
    """Busca bloques con estructuras JSON dentro del código JS"""
    objetos = []
    
    # Mejoramos la expresión regular para capturar objetos más complejos
    matches = re.finditer(r'({(?:[^{}]|(?R))*})', js_code, re.DOTALL)
    
    for match in matches:
        try:
            # Limpieza básica del texto antes de parsear
            json_str = match.group(1)
            json_str = re.sub(r'/\*.*?\*/', '', json_str)  # Eliminar comentarios
            json_str = re.sub(r'//.*?\n', '', json_str)    # Eliminar comentarios de línea
            json_str = json_str.replace("'", '"')           # Normalizar comillas
            json_str = re.sub(r',\s*}', '}', json_str)      # Eliminar comas finales
            
            obj = json.loads(json_str)
            objetos.append(obj)
        except json.JSONDecodeError:
            continue
    
    return objetos

def guardar_como_json(data, filename_prefix="gtm_extracted"):
    """Guarda los datos en un archivo JSON con nombre único"""
    filename = f"{filename_prefix}_{len(data)}_objects.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"📁 Archivo guardado como {filename}")

def main():
    try:
        # Solicitar URL al usuario
        website_url = input("Introduce la URL de la web a analizar: ").strip()
        
        # Validar URL básica
        if not website_url.startswith(('http://', 'https://')):
            website_url = 'https://' + website_url
        
        print(f"\n🔍 Analizando {website_url} en busca de contenedores GTM...")
        gtm_ids = get_gtm_ids_from_website(website_url)
        
        print(f"\n✅ Contenedores GTM encontrados:")
        for i, gtm_id in enumerate(gtm_ids, 1):
            print(f"{i}. {gtm_id}")
        
        # Procesar cada contenedor GTM encontrado
        all_objects = []
        for gtm_id in gtm_ids:
            print(f"\n🔄 Procesando {gtm_id}...")
            try:
                js_code = fetch_gtm_script(gtm_id)
                objetos = extraer_objetos_posibles(js_code)
                print(f"   → Encontrados {len(objetos)} objetos JSON")
                all_objects.extend(objetos)
            except Exception as e:
                print(f"   ⚠️ Error procesando {gtm_id}: {str(e)}")
        
        if all_objects:
            domain = urlparse(website_url).netloc.replace('.', '_')
            guardar_como_json(all_objects, f"gtm_data_{domain}")
        else:
            print("\n⚠️ No se encontraron objetos JSON válidos en ningún contenedor GTM")
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    print("=== GTM Scraper & Analyzer ===")
    main()