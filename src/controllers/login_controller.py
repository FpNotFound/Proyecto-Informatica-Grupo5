"""CONTROLADOR de acceso: comprueba los datos del registro y del login.

Sus dos funciones devuelven dos cosas: el usuario (None si algo ha fallado)
y un mensaje de error para mostrar en pantalla.
"""
from src.controllers.user_controller import UserController


class LoginController:
    def __init__(self):
        self.users = UserController()

    def registrar(self, nombre, email, password, confirmar, rol):
        nombre = nombre.strip()
        email = email.strip().lower()

        if not nombre or not email or not password:
            return None, "Todos los campos son obligatorios."
        if "@" not in email or "." not in email:
            return None, "El correo electrónico no tiene un formato válido."
        if len(password) < 4:
            return None, "La contraseña debe tener al menos 4 caracteres."
        if password != confirmar:
            return None, "Las contraseñas no coinciden."
        if not rol:
            return None, "Debes seleccionar un rol."
        if self.users.buscar_por_email(email):
            return None, "Ya existe un usuario registrado con ese correo."

        return self.users.crear_usuario(nombre, email, password, rol), ""

    def autenticar(self, email, password):
        email = email.strip().lower()
        if not email or not password:
            return None, "Introduce tu correo y tu contraseña."

        usuario = self.users.buscar_por_email(email)
        if usuario is None or not self.users.password_correcta(usuario, password):
            return None, "Correo o contraseña incorrectos."

        return usuario, ""
