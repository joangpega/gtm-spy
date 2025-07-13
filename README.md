# Google Tag Manager Spy

made with 💛 by Jose Angel Perez


![image](https://github.com/user-attachments/assets/5707ec64-30b1-4bad-9996-6c5fd79f7c0a)


GTM content downloader without direct access to GTM. Download, process and show all GTM content powered by python

Ejecutar el script:

Abres una terminal y ejecutas el comando:

    python gtm_extractor.py

Ingresar la URL del sitio:

El script te pedirá que introduzcas la URL del sitio web del que deseas extraer el GTM ID.

Extracción automática:

El script analiza el HTML de la página para localizar cualquier ID de Google Tag Manager (ej. GTM-XXXXXXX). Si encuentra uno o más IDs, los extrae.

Generación del JSON:

El script guarda los datos extraídos en un archivo .json local. Este archivo será necesario para el paso 2, donde puedes subirlo a al viewer_plus.html.

