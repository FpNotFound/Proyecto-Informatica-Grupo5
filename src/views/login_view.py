"""LoginView — capa VISTA. Pantalla de inicio de sesión (RF-02).

Interfaz con la que el usuario introduce sus credenciales. Delega la lógica de
autenticación en ``LoginController`` a través del controlador de aplicación.
"""
from __future__ import annotations

import flet as ft


class LoginView:
    def __init__(self, app) -> None:
        self.app = app
        self.email = ft.TextField(
            label="Correo electrónico",
            prefix_icon=ft.Icons.EMAIL,
            autofocus=True,
            width=320,
        )
        self.password = ft.TextField(
            label="Contraseña",
            prefix_icon=ft.Icons.LOCK,
            password=True,
            can_reveal_password=True,
            width=320,
            on_submit=self._entrar,
        )
        self.mensaje = ft.Text("", color=ft.Colors.RED, size=13)

    def _entrar(self, _evento) -> None:
        resultado = self.app.login_controller.autenticar(
            self.email.value, self.password.value
        )
        if resultado.ok:
            self.app.ir_a_principal(resultado.usuario)
        else:
            self.mensaje.value = resultado.mensaje
            self.app.page.update()

    def construir(self) -> ft.Control:
        tarjeta = ft.Card(
            width=400,
            content=ft.Container(
                padding=30,
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=16,
                    controls=[
                        ft.Icon(ft.Icons.SENSORS, size=52, color=ft.Colors.BLUE),
                        ft.Text("Bajos de Argüelles", size=24, weight=ft.FontWeight.BOLD),
                        ft.Text(
                            "Sistema de monitorización ambiental",
                            size=13,
                            color=ft.Colors.BLUE_GREY,
                        ),
                        self.email,
                        self.password,
                        self.mensaje,
                        ft.FilledButton(
                            "Iniciar sesión",
                            icon=ft.Icons.LOGIN,
                            width=320,
                            on_click=self._entrar,
                        ),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=2,
                            controls=[
                                ft.Text("¿No tienes cuenta?", size=13),
                                ft.TextButton(
                                    "Regístrate", on_click=self.app.ir_a_registro
                                ),
                            ],
                        ),
                    ],
                ),
            ),
        )
        return ft.Container(
            expand=True, alignment=ft.Alignment.CENTER, padding=20, content=tarjeta
        )
