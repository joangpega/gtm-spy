from urllib.request import urlopen, Request
from urllib.error import URLError
import re
import json
import ssl

def obtener_codigo_fuente(url):
    """Obtiene el código fuente de una URL"""
    try:
        # Configuración para evitar errores SSL y simular navegador
        context = ssl._create_unverified_context()
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        
        req = Request(url, headers=headers)
        with urlopen(req, context=context) as response:
            return response.read().decode('utf-8')
    except URLError as e:
        raise Exception(f"❌ Error al descargar el código fuente: {str(e)}")

def buscar_ids_gtm(codigo_fuente):
    """Busca todos los IDs de GTM en el código fuente"""
    patron_gtm = r'GTM-[A-Z0-9]{4,7}'
    ids_encontrados = list(set(re.findall(patron_gtm, codigo_fuente)))
    
    if not ids_encontrados:
        print("⚠️ No se encontraron IDs de GTM en la página")
    else:
        print(f"🔍 IDs de GTM encontrados: {', '.join(ids_encontrados)}")
    
    return ids_encontrados

def fetch_gtm_script(container_id):
    """Descarga el script GTM para un ID específico"""
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
    """Intenta extraer objetos JSON del código JS"""
    objetos = []
    # Patrón mejorado para capturar objetos JSON
    matches = re.findall(r'(?:(?<=\=)|(?<:\s))\{.*?\}(?=\s*;|\s*\)|\s*\}|\s*$)', js_code, re.DOTALL)
    
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

def guardar_como_json(data, filename="gtm_extracted.json"):
    """Guarda los datos en un archivo JSON"""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"📁 Archivo guardado como {filename}")

def main():
    """Función principal"""
    print("\n" + "="*50)
    print("🛠️ GTM EXTRACTOR - Herramienta de análisis".center(50))
    print("="*50 + "\n")
    
    # Solicitar URL al usuario
    url = input("Introduce la URL de la web a analizar (ej: https://ejemplo.com): ").strip()
    
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url  # Asumir HTTPS si no se especifica
    
    try:
        # Paso 1: Obtener código fuente y buscar IDs GTM
        print("\n🔎 Analizando la página...")
        codigo_fuente = obtener_codigo_fuente(url)
        ids_gtm = buscar_ids_gtm(codigo_fuente)
        
        if not ids_gtm:
            return
        
        # Paso 2: Analizar cada contenedor GTM encontrado
        for container_id in ids_gtm:
            print(f"\n{'='*30}")
            print(f"🔧 Procesando contenedor: {container_id}")
            print("="*30)
            
            try:
                js_code = fetch_gtm_script(container_id)
                objetos = extraer_objetos_posibles(js_code)
                
                if objetos:
                    print(f"✅ Se extrajeron {len(objetos)} objetos de configuración")
                    guardar_como_json(objetos, f"gtm_{container_id}_extracted.json")
                else:
                    print("⚠️ No se encontraron objetos JSON válidos")
                    
            except Exception as e:
                print(f"❌ Error al procesar {container_id}: {str(e)}")
                
    except Exception as e:
        print(f"\n❌ Error crítico: {str(e)}")
    finally:
        print("\n" + "="*50)
        print("🏁 Análisis completado".center(50))
        print("="*50)

if __name__ == "__main__":
    main()