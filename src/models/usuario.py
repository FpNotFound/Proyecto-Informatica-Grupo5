"""Modelo de datos de Usuario.

Forma parte de la capa MODELO dentro de la arquitectura MVC del proyecto
"Bajos de Argüelles". Define la entidad :class:`Usuario` y la enumeración de
roles :class:`Rol`. La persistencia en ``usuarios.json`` la gestiona
``UserController`` (capa controlador).
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Rol(str, Enum):
    """Roles de usuario contemplados en el sistema.

    En el Sprint 1 el rol se registra, se almacena y se muestra tras el login.
    Los paneles (dashboards) diferenciados por rol se desarrollarán en el
    Sprint 3 (Vecino, Propietario y Autoridad).
    """

    VECINO = "Vecino"
    PROPIETARIO = "Propietario"
    AUTORIDAD = "Autoridad"

    @classmethod
    def desde_texto(cls, texto: str) -> "Rol":
        """Devuelve el rol correspondiente a un texto, ignorando mayúsculas."""
        objetivo = str(texto).strip().lower()
        for rol in cls:
            if rol.value.lower() == objetivo:
                return rol
        raise ValueError(f"Rol no válido: {texto!r}")


@dataclass
class Usuario:
    """Entidad que representa a un usuario registrado en el sistema."""

    nombre: str
    email: str
    rol: Rol
    salt: str
    password_hash: str

    def to_dict(self) -> dict:
        """Serializa el usuario a un diccionario apto para JSON."""
        return {
            "nombre": self.nombre,
            "email": self.email,
            "rol": self.rol.value,
            "salt": self.salt,
            "password_hash": self.password_hash,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Usuario":
        """Reconstruye un usuario a partir de un diccionario leído del JSON."""
        return cls(
            nombre=data["nombre"],
            email=data["email"],
            rol=Rol.desde_texto(data["rol"]),
            salt=data["salt"],
            password_hash=data["password_hash"],
        )
