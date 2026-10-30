"""LoginController — capa CONTROLADOR (autenticación y registro).

Contiene la lógica de negocio del registro (RF-01) y del inicio de sesión
(RF-02): validación de los datos del formulario y comunicación con
``UserController`` para persistir y recuperar usuarios.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

from src.controllers.user_controller import UserController
from src.models.usuario import Rol, Usuario

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
LONGITUD_MIN_PASSWORD = 4


@dataclass
class ResultadoAuth:
    """Resultado de una operación de autenticación o registro."""

    ok: bool
    mensaje: str
    usuario: Usuario | None = None


class LoginController:
    def __init__(self, user_controller: UserController | None = None) -> None:
        self.users = user_controller or UserController()

    def registrar(
        self, nombre: str, email: str, password: str, confirmar: str, rol: Rol | None
    ) -> ResultadoAuth:
        """Valida los datos y da de alta un nuevo usuario (RF-01)."""
        nombre = (nombre or "").strip()
        email = (email or "").strip().lower()

        if not nombre or not email or not password:
            return ResultadoAuth(False, "Todos los campos son obligatorios.")
        if not _EMAIL_RE.match(email):
            return ResultadoAuth(
                False, "El correo electrónico no tiene un formato válido."
            )
        if len(password) < LONGITUD_MIN_PASSWORD:
            return ResultadoAuth(
                False,
                f"La contraseña debe tener al menos {LONGITUD_MIN_PASSWORD} caracteres.",
            )
        if password != confirmar:
            return ResultadoAuth(False, "Las contraseñas no coinciden.")
        if not isinstance(rol, Rol):
            return ResultadoAuth(False, "Debes seleccionar un rol.")
        if self.users.buscar_por_email(email):
            return ResultadoAuth(
                False, "Ya existe un usuario registrado con ese correo."
            )

        usuario = self.users.crear_usuario(nombre, email, password, rol)
        return ResultadoAuth(True, "Registro completado correctamente.", usuario)

    def autenticar(self, email: str, password: str) -> ResultadoAuth:
        """Verifica las credenciales e inicia sesión (RF-02)."""
        email = (email or "").strip().lower()
        if not email or not password:
            return ResultadoAuth(False, "Introduce tu correo y tu contraseña.")

        usuario = self.users.buscar_por_email(email)
        if usuario is None or not self.users.verificar_password(usuario, password):
            return ResultadoAuth(False, "Correo o contraseña incorrectos.")

        return ResultadoAuth(True, f"Bienvenido/a, {usuario.nombre}.", usuario)
