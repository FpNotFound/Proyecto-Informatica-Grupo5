"""CONTROLADOR de usuarios: los crea, los busca y protege sus contraseñas."""
import hashlib

from src.models.usuario import Usuario, cargar_usuarios, guardar_usuarios


class UserController:
    def __init__(self):
        # La primera vez que se abre la aplicación crea un usuario por rol.
        if not cargar_usuarios():
            self.crear_usuario("Vecino Demo", "vecino@arguelles.es", "1234", "Vecino")
            self.crear_usuario("Bar Demo", "bar@arguelles.es", "1234", "Propietario")
            self.crear_usuario("Ayuntamiento Demo", "ayto@arguelles.es", "1234", "Autoridad")

    def calcular_hash(self, password):
        """Transforma la contraseña para no guardarla tal cual."""
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def password_correcta(self, usuario, password):
        return usuario.password_hash == self.calcular_hash(password)

    def buscar_por_email(self, email):
        """Devuelve el usuario con ese correo, o None si no existe."""
        for usuario in cargar_usuarios():
            if usuario.email == email:
                return usuario
        return None

    def crear_usuario(self, nombre, email, password, rol):
        usuario = Usuario(nombre, email, rol, self.calcular_hash(password))
        usuarios = cargar_usuarios()
        usuarios.append(usuario)
        guardar_usuarios(usuarios)
        return usuario
