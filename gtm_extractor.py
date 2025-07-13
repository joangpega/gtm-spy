from urllib.request import urlopen, Request
from urllib.error import URLError
import re
import json
import ssl

def obtener_codigo_fuente(url):
    """Obtiene el código fuente de una URL usando urllib"""
    try:
        # Configuración para evitar errores SSL
        context = ssl._create_unverified_context()
        headers = {'User-Agent': 'Mozilla/5.0'}
        req = Request(url, headers=headers)
        with urlopen(req, context=context) as response:
            return response.read().decode('utf-8')
    except URLError as e:
        raise Exception(f"❌ Error al descargar el código fuente: {str(e)}")

def buscar_ids_gtm(codigo_fuente):
    """Busca todos los IDs de GTM en el código fuente"""
    patron_gtm = r'GTM-[A-Z0-9]{4,7}'
    ids_encontrados = list(set(re.findall(patron_gtm, codigo_fuente)))
    return ids_encontrados

def fetch_gtm_script(container_id):
    """Descarga el script GTM usando urllib"""
    url = f"https://www.googletagmanager.com/gtm.js?id={container_id}"
    try:
        context = ssl._create_unverified_context()
        headers = {'User-Agent': 'Mozilla/5.0'}
        req = Request(url, headers=headers)
        with urlopen(req, context=context) as response:
            return response.read().decode('utf-8')
    except URLError as e:
        raise Exception(f"❌ Error al descargar GTM {container_id} ({str(e)})")

def extraer_objetos_posibles(js_code):
    """Extrae posibles objetos JSON del código JS"""
    objetos = []
    # Patrón mejorado para capturar objetos
    matches = re.findall(r'\{.*?\}', js_code, re.DOTALL)
    
    for match in matches:
        try:
            # Limpieza básica del texto
            clean_match = re.sub(r'/\*.*?\*/', '', match)  # Remueve comentarios
            clean_match = clean_match.replace('\n', '').replace('\r', '')
            obj = json.loads(clean_match)
            objetos.append(obj)
        except json.JSONDecodeError:
            continue

    return objetos

def guardar_como_json(data, container_id):
    """Guarda los datos en un archivo JSON"""
    filename = f"gtm_{container_id}_extracted.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"📁 Archivo guardado como {filename}")

def analizar_gtm(container_id):
    """Función principal de análisis para un contenedor GTM"""
    print(f"\n🔎 Iniciando análisis para: {container_id}")
    try:
        js_code = fetch_gtm_script(container_id)
        objetos = extraer_objetos_posibles(js_code)
        
        if objetos:
            print(f"✅ Se extrajeron {len(objetos)} objetos de configuración")
            guardar_como_json(objetos, container_id)
        else:
            print("⚠️ No se encontraron objetos JSON válidos")
    except Exception as e:
        print(f"❌ Error durante el análisis: {str(e)}")

def main():
    print("\n" + "="*50)
    print("🛠️ GTM ANALYZER (Sin dependencias externas)".center(50))
    print("="*50 + "\n")
    
    # Paso 1: Obtener URL
    url = input("Introduce la URL a analizar (ej: ejemplo.com): ").strip()
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    try:
        # Paso 2: Buscar contenedores GTM
        print("\n🔍 Buscando contenedores GTM...")
        codigo = obtener_codigo_fuente(url)
        gtm_ids = buscar_ids_gtm(codigo)
        
        if not gtm_ids:
            print("⚠️ No se encontraron contenedores GTM")
            return
        
        print(f"🔍 Contenedores encontrados: {', '.join(gtm_ids)}")
        
        # Paso 3: Analizar cada contenedor
        for gtm_id in gtm_ids:
            analizar_gtm(gtm_id)
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
    finally:
        print("\n" + "="*50)
        print("🏁 Proceso completado".center(50))
        print("="*50)

if __name__ == "__main__":
    main()