"""RegisterView — capa VISTA. Pantalla de registro de usuarios (RF-01).

Permite dar de alta un usuario indicando nombre, correo, contraseña y rol
(Vecino, Propietario o Autoridad). La validación y el alta se delegan en
``LoginController``.
"""
from __future__ import annotations

import flet as ft

from src.models.usuario import Rol


class RegisterView:
    def __init__(self, app) -> None:
        self.app = app
        self.nombre = ft.TextField(label="Nombre", prefix_icon=ft.Icons.PERSON, width=320)
        self.email = ft.TextField(
            label="Correo electrónico", prefix_icon=ft.Icons.EMAIL, width=320
        )
        self.password = ft.TextField(
            label="Contraseña",
            prefix_icon=ft.Icons.LOCK,
            password=True,
            can_reveal_password=True,
            width=320,
        )
        self.confirmar = ft.TextField(
            label="Repetir contraseña",
            prefix_icon=ft.Icons.LOCK_OUTLINE,
            password=True,
            can_reveal_password=True,
            width=320,
            on_submit=self._registrar,
        )
        self.rol = ft.Dropdown(
            label="Rol",
            width=320,
            options=[ft.DropdownOption(key=r.value, text=r.value) for r in Rol],
        )
        self.mensaje = ft.Text("", size=13)

    def _registrar(self, _evento) -> None:
        rol = None
        if self.rol.value:
            try:
                rol = Rol.desde_texto(self.rol.value)
            except ValueError:
                rol = None

        resultado = self.app.login_controller.registrar(
            self.nombre.value,
            self.email.value,
            self.password.value,
            self.confirmar.value,
            rol,
        )
        if resultado.ok:
            # Tras registrarse, el usuario entra directamente a su panel.
            self.app.ir_a_principal(resultado.usuario)
        else:
            self.mensaje.value = resultado.mensaje
            self.mensaje.color = ft.Colors.RED
            self.app.page.update()

    def construir(self) -> ft.Control:
        tarjeta = ft.Card(
            width=420,
            content=ft.Container(
                padding=30,
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=14,
                    controls=[
                        ft.Icon(ft.Icons.PERSON_ADD, size=48, color=ft.Colors.BLUE),
                        ft.Text("Crear cuenta", size=22, weight=ft.FontWeight.BOLD),
                        self.nombre,
                        self.email,
                        self.password,
                        self.confirmar,
                        self.rol,
                        self.mensaje,
                        ft.FilledButton(
                            "Registrarme",
                            icon=ft.Icons.CHECK,
                            width=320,
                            on_click=self._registrar,
                        ),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=2,
                            controls=[
                                ft.Text("¿Ya tienes cuenta?", size=13),
                                ft.TextButton(
                                    "Inicia sesión", on_click=self.app.ir_a_login
                                ),
                            ],
                        ),
                    ],
                ),
            ),
        )
        return ft.Container(
            expand=True,
            alignment=ft.Alignment.CENTER,
            padding=20,
            content=ft.Column(
                scroll=ft.ScrollMode.AUTO,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[tarjeta],
            ),
        )
