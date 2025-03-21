import re
import os

def convertir_obsidian_a_md(archivo_md, carpeta_imagenes="https://github.com/MartinLopezDeIpina/TFG_apuntes/blob/master/Imagenes"):
    with open(archivo_md, "r", encoding="utf-8") as f:
        contenido = f.read()
    
    # Función para reemplazar espacios con %20 en el nombre de la imagen
    def reemplazar_espacios(nombre_imagen):
        return nombre_imagen.replace(" ", "%20")
    
    # Buscar enlaces de imágenes en formato Obsidian ![[imagen.png]]
    nuevo_contenido = re.sub(r'!\[\[(.*?)\]\]', 
                             lambda match: f'![{match.group(1)}]({carpeta_imagenes}/{reemplazar_espacios(match.group(1))})', 
                             contenido)

    with open(archivo_md, "w", encoding="utf-8") as f:
        f.write(nuevo_contenido)

# Aplicar a todos los archivos en un directorio
directorio_md = "/home/martin/TFG_apuntes/cursos_juanan"
for archivo in os.listdir(directorio_md):
    if archivo.endswith(".md"):
        convertir_obsidian_a_md(os.path.join(directorio_md, archivo))
