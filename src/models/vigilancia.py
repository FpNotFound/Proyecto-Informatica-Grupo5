"""MODELO: datos de VIGILANCIA (incidencias, cierres y notificaciones).

Son tres archivos JSON en src/models. Cada elemento es un diccionario:

incidencias.json  -> el LOG (registro) de incidencias de cada bar
    {"local": "NEG-001", "fecha": "2026-11-13 21:30", "tipo": "Cierre temporal",
     "autor": "Ayuntamiento Demo", "descripcion": "Texto que explica lo ocurrido"}

cierres.json  -> los cierres temporales que ha hecho la policía
    {"local": "NEG-001", "fecha": "2026-11-13 21:30", "policia": "Ayuntamiento Demo (POL-0001)",
     "motivo": "Texto obligatorio que escribe la policía",
     "activo": True,                    # True mientras el local siga cerrado
     "reclamacion": "",                 # texto que escribe el propietario si reclama
     "estado_reclamacion": "",          # "", "Pendiente", "Justificado" o "No justificado"
     "respuesta": ""}                   # lo que contesta la policía a la reclamación

notificaciones.json  -> avisos que ve cada usuario en su panel
    {"para": "Autoridad", "fecha": "...", "titulo": "...", "mensaje": "...", "leida": False}
    "para" vale "Autoridad" (lo ven todos los policías) o un código de local como
    "NEG-001" (lo ve el propietario de ese local).
"""
# Las mismas funciones de leer/escribir JSON que usa el resto del proyecto.
from src.models.archivo_json import escribir_json, leer_json

ARCHIVO_INCIDENCIAS = "incidencias.json"
ARCHIVO_CIERRES = "cierres.json"
ARCHIVO_NOTIFICACIONES = "notificaciones.json"


def cargar_incidencias():
    return leer_json(ARCHIVO_INCIDENCIAS)


def guardar_incidencias(incidencias):
    escribir_json(ARCHIVO_INCIDENCIAS, incidencias)


def cargar_cierres():
    return leer_json(ARCHIVO_CIERRES)


def guardar_cierres(cierres):
    escribir_json(ARCHIVO_CIERRES, cierres)


def cargar_notificaciones():
    return leer_json(ARCHIVO_NOTIFICACIONES)


def guardar_notificaciones(notificaciones):
    escribir_json(ARCHIVO_NOTIFICACIONES, notificaciones)
