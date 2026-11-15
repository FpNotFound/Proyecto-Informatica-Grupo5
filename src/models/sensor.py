"""MODELO: datos de los SENSORES y su HISTORIAL.

Cada local (bar) tiene 3 sensores. Cada sensor se guarda en sensores.json
como un diccionario así:

    {"local": "NEG-001", "tipo": "temperatura", "valor": 23.4, "fecha": "2026-11-13 21:30"}

Y cada medida antigua se guarda en historial_sensores.json igual:

    {"local": "NEG-001", "tipo": "temperatura", "valor": 22.9, "fecha": "2026-11-13 20:30"}

Los dos archivos se guardan en src/models, junto a usuarios.json y locales.json.
"""
# Usamos las MISMAS funciones de leer/escribir JSON que el resto del proyecto.
from src.models.archivo_json import escribir_json, leer_json

# Nombres de los archivos.
ARCHIVO_SENSORES = "sensores.json"
ARCHIVO_HISTORIAL = "historial_sensores.json"

# Los tres tipos de sensor.
TIPOS_SENSOR = ["temperatura", "humedad", "calidad_aire"]

# Nombre que se ve en pantalla para cada tipo.
NOMBRE_SENSOR = {
    "temperatura": "Sensor de temperatura",
    "humedad": "Sensor de humedad",
    "calidad_aire": "Sensor de calidad del aire",
}

# Unidad de medida de cada tipo.
UNIDAD_SENSOR = {
    "temperatura": "°C",
    "humedad": "%",
    "calidad_aire": "ppm CO2",
}

# Color del diodo LED que enciende cada tipo cuando hay alerta.
LED_SENSOR = {
    "temperatura": "rojo",
    "humedad": "azul",
    "calidad_aire": "verde",
}

# ----------------------------------------------------------------------
# UMBRALES: a partir de qué valor hay PRECAUCIÓN (amarillo) o PELIGRO (rojo).
# Si hay que cambiar algún número, solo se cambia aquí.
# ----------------------------------------------------------------------
# Temperatura (°C): peligro si pasa de 30; precaución si pasa de 27.
TEMPERATURA_PELIGRO = 30
TEMPERATURA_PRECAUCION = 27
# Humedad (%): peligro por debajo de 30 o por encima de 70.
HUMEDAD_PELIGRO_MINIMA = 30
HUMEDAD_PELIGRO_MAXIMA = 70
# Humedad (%): precaución por debajo de 35 o por encima de 65.
HUMEDAD_PRECAUCION_MINIMA = 35
HUMEDAD_PRECAUCION_MAXIMA = 65
# Calidad del aire (ppm de CO2): desde 800 es "Moderada" y desde 1200 es "Mala" (peligro).
CO2_MODERADO = 800
CO2_MALO = 1200

# Cuántas medidas antiguas se guardan como máximo en el historial (para que no crezca sin fin).
MAXIMO_HISTORIAL = 1500


def cargar_sensores():
    """Devuelve la lista de sensores de todos los locales."""
    return leer_json(ARCHIVO_SENSORES)


def guardar_sensores(sensores):
    """Guarda la lista de sensores."""
    escribir_json(ARCHIVO_SENSORES, sensores)


def cargar_historial():
    """Devuelve todas las medidas antiguas (de la más antigua a la más nueva)."""
    return leer_json(ARCHIVO_HISTORIAL)


def guardar_historial(historial):
    """Guarda el historial. Si es muy largo, borra las medidas más antiguas."""
    # historial[-MAXIMO_HISTORIAL:] se queda solo con las últimas 1500 medidas.
    escribir_json(ARCHIVO_HISTORIAL, historial[-MAXIMO_HISTORIAL:])
