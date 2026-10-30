"""UserController — capa CONTROLADOR (gestión de datos de usuario).

Responsable de:
  * La persistencia de los usuarios en ``usuarios.json`` (RF-03).
  * El tratamiento seguro de las contraseñas mediante hash SHA-256 + salt
    aleatorio por usuario (RNF-05: seguridad básica en autenticación).

Actúa de puente entre el modelo :class:`Usuario` y el almacenamiento en disco.
"""
from __future__ import annotations

import hashlib
import json
import secrets
from pathlib import Path

from src.models.usuario import Rol, Usuario


class UserController:
    def __init__(self, ruta_json: Path | None = None) -> None:
        # usuarios.json vive junto al modelo (capa MODELO del MVC).
        self.ruta_json = ruta_json or (
            Path(__file__).resolve().parent.parent / "models" / "usuarios.json"
        )
        self._asegurar_almacen()

    # ------------------------------------------------------------------ #
    # Seguridad (RNF-05)
    # ------------------------------------------------------------------ #
    @staticmethod
    def hash_password(password: str, salt: str) -> str:
        """Calcula el hash SHA-256 de ``salt + password``."""
        return hashlib.sha256((salt + password).encode("utf-8")).hexdigest()

    def verificar_password(self, usuario: Usuario, password: str) -> bool:
        """Comprueba, de forma segura, si la contraseña coincide."""
        return secrets.compare_digest(
            usuario.password_hash, self.hash_password(password, usuario.salt)
        )

    # ------------------------------------------------------------------ #
    # Persistencia JSON (RF-03)
    # ------------------------------------------------------------------ #
    def _asegurar_almacen(self) -> None:
        """Crea el almacén con usuarios de demostración si no existe."""
        if not self.ruta_json.exists():
            self.ruta_json.parent.mkdir(parents=True, exist_ok=True)
            self._sembrar_demo()

    def cargar_usuarios(self) -> list[Usuario]:
        """Lee y deserializa todos los usuarios del fichero JSON."""
        try:
            datos = json.loads(self.ruta_json.read_text(encoding="utf-8"))
        except (FileNotFoundError, json.JSONDecodeError):
            return []
        return [Usuario.from_dict(d) for d in datos]

    def guardar_usuarios(self, usuarios: list[Usuario]) -> None:
        """Serializa y escribe la lista completa de usuarios en el JSON."""
        self.ruta_json.write_text(
            json.dumps(
                [u.to_dict() for u in usuarios], indent=2, ensure_ascii=False
            ),
            encoding="utf-8",
        )

    def buscar_por_email(self, email: str) -> Usuario | None:
        """Devuelve el usuario con ese correo, o ``None`` si no existe."""
        objetivo = (email or "").strip().lower()
        for usuario in self.cargar_usuarios():
            if usuario.email.lower() == objetivo:
                return usuario
        return None

    def crear_usuario(
        self, nombre: str, email: str, password: str, rol: Rol
    ) -> Usuario:
        """Crea y persiste un nuevo usuario con la contraseña ya protegida."""
        salt = secrets.token_hex(16)
        usuario = Usuario(
            nombre=nombre.strip(),
            email=email.strip().lower(),
            rol=rol,
            salt=salt,
            password_hash=self.hash_password(password, salt),
        )
        usuarios = self.cargar_usuarios()
        usuarios.append(usuario)
        self.guardar_usuarios(usuarios)
        return usuario

    # ------------------------------------------------------------------ #
    # Datos de demostración
    # ------------------------------------------------------------------ #
    def _sembrar_demo(self) -> None:
        """Crea un usuario de demostración por cada rol (contraseña: 1234)."""
        demo = [
            ("Vecino Demo", "vecino@arguelles.es", "1234", Rol.VECINO),
            ("Bar Demo", "bar@arguelles.es", "1234", Rol.PROPIETARIO),
            ("Ayuntamiento Demo", "ayto@arguelles.es", "1234", Rol.AUTORIDAD),
        ]
        usuarios: list[Usuario] = []
        for nombre, email, password, rol in demo:
            salt = secrets.token_hex(16)
            usuarios.append(
                Usuario(nombre, email, rol, salt, self.hash_password(password, salt))
            )
        self.guardar_usuarios(usuarios)
