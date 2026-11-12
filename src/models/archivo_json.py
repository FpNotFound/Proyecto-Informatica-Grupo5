"""MODELO: funciones para LEER y ESCRIBIR archivos JSON.

Todos los datos de la aplicación (usuarios, locales e IDs policiales) se
guardan en archivos .json dentro de esta misma carpeta (src/models).
Este es el ÚNICO archivo del proyecto que abre y cierra esos archivos;
el resto del código siempre pasa por estas dos funciones.
"""
# "json" es una herramienta que ya viene con Python para trabajar con archivos .json.
import json

# "os" es otra herramienta de Python; aquí la usamos para construir rutas de archivos.
import os

# Guardamos en CARPETA la ruta de la carpeta donde está este archivo (src/models).
# "__file__" es la ruta de este mismo archivo y "dirname" le quita el nombre del archivo.
CARPETA = os.path.dirname(__file__)


def leer_json(nombre_archivo):
    """Lee el archivo indicado y devuelve su contenido (una lista).

    Si el archivo todavía no existe, devuelve una lista vacía.
    """
    # Unimos la carpeta y el nombre. Ejemplo: ".../src/models/locales.json".
    ruta = os.path.join(CARPETA, nombre_archivo)
    # "try" significa "intenta hacer esto"; si algo falla, salta al "except".
    try:
        # Abrimos el archivo para leerlo. encoding="utf-8" permite tildes y la letra ñ.
        # "with" se encarga de cerrar el archivo solo cuando terminamos.
        with open(ruta, encoding="utf-8") as archivo:
            # json.load convierte el texto del archivo en datos de Python y los devolvemos.
            return json.load(archivo)
    # FileNotFoundError es el error que aparece si el archivo no existe (la primera vez).
    except FileNotFoundError:
        # En ese caso devolvemos una lista vacía, que significa "aún no hay datos".
        return []


def escribir_json(nombre_archivo, datos):
    """Guarda los datos indicados en el archivo, sustituyendo lo que hubiera."""
    # Construimos la ruta completa igual que en leer_json.
    ruta = os.path.join(CARPETA, nombre_archivo)
    # Abrimos el archivo en modo "w" (write = escribir). Si no existe, se crea.
    with open(ruta, "w", encoding="utf-8") as archivo:
        # json.dump convierte los datos de Python en texto JSON y los escribe.
        # indent=2 deja el archivo ordenado con sangría para que se lea fácil.
        # ensure_ascii=False guarda las tildes tal cual (sin códigos raros).
        json.dump(datos, archivo, indent=2, ensure_ascii=False)
