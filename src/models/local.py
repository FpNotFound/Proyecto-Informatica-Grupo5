"""MODELO: define qué es un local (bar, restaurante...) y cómo se guarda en locales.json."""
# Traemos las dos funciones que leen y escriben archivos JSON (ver archivo_json.py).
from src.models.archivo_json import escribir_json, leer_json

# Tipos de local que se pueden elegir en el formulario.
TIPOS_LOCAL = ["Bar", "Restaurante", "Discoteca", "Otro"]

# Nombre del archivo donde se guardan los locales.
ARCHIVO_LOCALES = "locales.json"


# Molde que describe los datos de cada local.
class Local:
    # Se ejecuta al crear un local nuevo y guarda sus datos.
    def __init__(self, codigo, nombre, direccion, tipo, aforo):
        # Código de negocio: identifica al local y no se repite (ejemplo "NEG-001").
        # El propietario lo necesita para registrarse.
        self.codigo = codigo
        # Nombre comercial del local.
        self.nombre = nombre
        # Calle y número.
        self.direccion = direccion
        # Uno de los TIPOS_LOCAL de arriba.
        self.tipo = tipo
        # Número máximo de personas permitidas dentro (un número entero).
        self.aforo = aforo

    def a_diccionario(self):
        """Convierte el local en el formato que se guarda en el JSON."""
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "direccion": self.direccion,
            "tipo": self.tipo,
            "aforo": self.aforo,
        }


def cargar_locales():
    """Lee locales.json y devuelve la lista de locales (vacía si aún no existe)."""
    # Lista vacía que iremos llenando.
    locales = []
    # Recorremos cada local guardado (cada "d" es un diccionario).
    for d in leer_json(ARCHIVO_LOCALES):
        # Creamos un objeto Local con sus datos y lo añadimos a la lista.
        locales.append(Local(d["codigo"], d["nombre"], d["direccion"], d["tipo"], d["aforo"]))
    # Devolvemos la lista completa.
    return locales


def guardar_locales(locales):
    """Escribe la lista completa de locales en locales.json."""
    # Lista vacía para los locales convertidos en diccionario.
    datos = []
    # Recorremos los locales uno a uno.
    for local in locales:
        # Lo convertimos a diccionario y lo añadimos.
        datos.append(local.a_diccionario())
    # Guardamos todo en el archivo.
    escribir_json(ARCHIVO_LOCALES, datos)
