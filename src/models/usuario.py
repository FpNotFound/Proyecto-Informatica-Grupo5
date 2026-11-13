"""MODELO: define qué es un usuario y cómo se guarda en usuarios.json."""
# Traemos las dos funciones que leen y escriben archivos JSON (ver archivo_json.py).
from src.models.archivo_json import escribir_json, leer_json

# Los tres tipos de usuario (roles) que existen. Están explicados en docs/ROLES.md.
ROLES = ["Vecino", "Propietario", "Autoridad"]

# Nombre del archivo donde se guardan los usuarios.
ARCHIVO_USUARIOS = "usuarios.json"

# Nombre del archivo con la lista de IDs policiales que se aceptan al registrarse.
ARCHIVO_IDS_POLICIALES = "ids_policiales.json"


# Una "clase" es un molde: describe qué datos tiene cada usuario.
class Usuario:
    # __init__ se ejecuta al crear un usuario nuevo y guarda sus datos.
    # codigo_negocio e id_policial valen "" (vacío) si no se indican.
    def __init__(self, nombre, email, rol, password_hash, codigo_negocio="", id_policial=""):
        # Nombre que se muestra en pantalla.
        self.nombre = nombre
        # Correo electrónico; sirve para iniciar sesión y no se puede repetir.
        self.email = email
        # Rol del usuario: "Vecino", "Propietario" o "Autoridad".
        self.rol = rol
        # Contraseña ya transformada (hash). Nunca guardamos la contraseña real.
        self.password_hash = password_hash
        # Solo Propietarios: código del local que les pertenece (ejemplo "NEG-001").
        self.codigo_negocio = codigo_negocio
        # Solo Autoridad: su ID de identificación policial (ejemplo "POL-0001").
        self.id_policial = id_policial

    def a_diccionario(self):
        """Convierte el usuario en el formato que se guarda en el JSON."""
        # Un diccionario guarda parejas "nombre del dato": valor.
        return {
            "nombre": self.nombre,
            "email": self.email,
            "rol": self.rol,
            "password_hash": self.password_hash,
            "codigo_negocio": self.codigo_negocio,
            "id_policial": self.id_policial,
        }


def cargar_usuarios():
    """Lee usuarios.json y devuelve la lista de usuarios (vacía si aún no existe)."""
    # Empezamos con una lista vacía que iremos llenando.
    usuarios = []
    # Recorremos cada usuario guardado en el archivo (cada "d" es un diccionario).
    for d in leer_json(ARCHIVO_USUARIOS):
        # Creamos un objeto Usuario con los datos y lo añadimos a la lista.
        # d.get(..., "") devuelve "" si ese dato no está (usuarios antiguos del Sprint 1).
        usuarios.append(
            Usuario(
                d["nombre"],
                d["email"],
                d["rol"],
                d["password_hash"],
                d.get("codigo_negocio", ""),
                d.get("id_policial", ""),
            )
        )
    # Devolvemos la lista completa.
    return usuarios


def guardar_usuarios(usuarios):
    """Escribe la lista completa de usuarios en usuarios.json."""
    # Lista vacía donde pondremos cada usuario convertido en diccionario.
    datos = []
    # Recorremos los usuarios uno a uno.
    for usuario in usuarios:
        # Lo convertimos a diccionario y lo añadimos.
        datos.append(usuario.a_diccionario())
    # Guardamos todo en el archivo.
    escribir_json(ARCHIVO_USUARIOS, datos)


def cargar_ids_policiales():
    """Devuelve la lista de IDs policiales válidos (ids_policiales.json)."""
    # El archivo ya es una lista de textos, así que la devolvemos tal cual.
    return leer_json(ARCHIVO_IDS_POLICIALES)
