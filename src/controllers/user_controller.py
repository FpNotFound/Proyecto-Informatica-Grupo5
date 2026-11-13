"""CONTROLADOR de usuarios: los crea, los busca y protege sus contraseñas."""
# hashlib es una herramienta de Python para transformar textos de forma irreversible.
import hashlib

# Traemos del modelo el molde Usuario y las funciones que leen/escriben los JSON.
from src.models.usuario import (
    Usuario,
    cargar_ids_policiales,
    cargar_usuarios,
    guardar_usuarios,
)


class UserController:
    def __init__(self):
        # La primera vez que se abre la aplicación (no hay usuarios) crea uno por rol.
        if not cargar_usuarios():
            # Vecino: no necesita ningún código.
            self.crear_usuario("Vecino Demo", "vecino@arguelles.es", "1234", "Vecino")
            # Propietario: va unido al local de prueba "NEG-001".
            self.crear_usuario(
                "Bar Demo", "bar@arguelles.es", "1234", "Propietario", codigo_negocio="NEG-001"
            )
            # Autoridad: usa el ID policial de prueba "POL-0001".
            self.crear_usuario(
                "Ayuntamiento Demo", "ayto@arguelles.es", "1234", "Autoridad", id_policial="POL-0001"
            )

    def calcular_hash(self, password):
        """Transforma la contraseña para no guardarla tal cual."""
        # encode convierte el texto en bytes; sha256 lo transforma;
        # hexdigest lo devuelve como un texto de 64 letras y números.
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def password_correcta(self, usuario, password):
        """Devuelve True si la contraseña escrita coincide con la guardada."""
        # Transformamos la contraseña escrita y la comparamos con la guardada.
        return usuario.password_hash == self.calcular_hash(password)

    def buscar_por_email(self, email):
        """Devuelve el usuario con ese correo, o None si no existe."""
        # Recorremos todos los usuarios guardados.
        for usuario in cargar_usuarios():
            # Si el correo coincide, lo devolvemos y la función termina aquí.
            if usuario.email == email:
                return usuario
        # Si acabamos el recorrido sin encontrarlo, devolvemos None (= "nada").
        return None

    def buscar_por_codigo_negocio(self, codigo):
        """Devuelve el propietario que tiene ese código de negocio, o None."""
        # Igual que buscar_por_email, pero mirando el código de negocio.
        for usuario in cargar_usuarios():
            if usuario.codigo_negocio == codigo:
                return usuario
        return None

    def buscar_por_id_policial(self, id_policial):
        """Devuelve la autoridad que tiene ese ID policial, o None."""
        # Igual que buscar_por_email, pero mirando el ID policial.
        for usuario in cargar_usuarios():
            if usuario.id_policial == id_policial:
                return usuario
        return None

    def id_policial_valido(self, id_policial):
        """Devuelve True si el ID está en la lista oficial (ids_policiales.json)."""
        # "in" comprueba si un valor está dentro de una lista.
        return id_policial in cargar_ids_policiales()

    def crear_usuario(self, nombre, email, password, rol, codigo_negocio="", id_policial=""):
        """Crea un usuario, lo guarda en usuarios.json y lo devuelve."""
        # Creamos el usuario guardando la contraseña ya transformada.
        usuario = Usuario(
            nombre, email, rol, self.calcular_hash(password), codigo_negocio, id_policial
        )
        # Leemos los usuarios que ya existen.
        usuarios = cargar_usuarios()
        # Añadimos el nuevo al final de la lista.
        usuarios.append(usuario)
        # Guardamos la lista completa otra vez en el archivo.
        guardar_usuarios(usuarios)
        # Devolvemos el usuario recién creado.
        return usuario
