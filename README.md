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

El script guarda los datos extraídos en un archivo .json local. 

<img width="516" height="179" alt="Code 2025-07-13 19 15 02" src="https://github.com/user-attachments/assets/68792d40-cc23-444e-86d6-bb4f43508fd1" />

Este archivo será necesario para el paso 2, donde puedes subirlo a al viewer_plus.html.

Ya en el viewer_plus.html, subimos el JSON: 

<img width="1170" height="538" alt="image" src="https://github.com/user-attachments/assets/b01b115f-c31e-4f33-8723-796d802e9486" />

Clicamos en Analizar JSON, y tendremos el resultado. 

<img width="1180" height="725" alt="image" src="https://github.com/user-attachments/assets/99012536-99e0-4b43-bdf2-c367009f5ce9" />





