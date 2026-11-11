"""MODELO: define al usuario y guarda los usuarios en usuarios.json."""
import json

ROLES = ["Vecino", "Propietario", "Autoridad"]

# usuarios.json está en la misma carpeta que este archivo.
RUTA_JSON = __file__.replace("usuario.py", "usuarios.json")


class Usuario:
    def __init__(self, nombre, email, rol, password_hash):
        self.nombre = nombre
        self.email = email
        self.rol = rol
        self.password_hash = password_hash

    def a_diccionario(self):
        """Convierte el usuario en el formato que se guarda en el JSON."""
        return {
            "nombre": self.nombre,
            "email": self.email,
            "rol": self.rol,
            "password_hash": self.password_hash,
        }


def cargar_usuarios():
    """Lee el JSON y devuelve la lista de usuarios (vacía si aún no existe)."""
    try:
        with open(RUTA_JSON, encoding="utf-8") as archivo:
            datos = json.load(archivo)
    except FileNotFoundError:
        return []

    usuarios = []
    for d in datos:
        usuarios.append(Usuario(d["nombre"], d["email"], d["rol"], d["password_hash"]))
    return usuarios


def guardar_usuarios(usuarios):
    """Escribe la lista completa de usuarios en el JSON."""
    datos = []
    for usuario in usuarios:
        datos.append(usuario.a_diccionario())

    with open(RUTA_JSON, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=2, ensure_ascii=False)
