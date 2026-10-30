"""Controlador de aplicación / enrutador de vistas.

Coordina la navegación entre las vistas (Login, Registro y Principal) y
mantiene el estado de la sesión actual. Pertenece a la capa CONTROLADOR y es
el punto de unión entre la VISTA (Flet) y la lógica de autenticación
(``LoginController``). Implementa la navegación básica entre pantallas (RF-04).
"""
from __future__ import annotations

import flet as ft

from src.controllers.login_controller import LoginController
from src.models.usuario import Usuario
from src.views.login_view import LoginView
from src.views.main_view import MainView
from src.views.register_view import RegisterView


class App:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.login_controller = LoginController()
        self.usuario_actual: Usuario | None = None
        self._configurar_pagina()

    def _configurar_pagina(self) -> None:
        self.page.title = "Bajos de Argüelles · Monitorización ambiental"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 0
        self.page.bgcolor = ft.Colors.BLUE_GREY_50

    def _render(self, contenido: ft.Control) -> None:
        """Sustituye el contenido de la página por la vista indicada."""
        self.page.clean()
        self.page.add(contenido)

    # ------------------------------------------------------------------ #
    # Navegación entre pantallas (RF-04)
    # ------------------------------------------------------------------ #
    def ir_a_login(self, *_event) -> None:
        self._render(LoginView(self).construir())

    def ir_a_registro(self, *_event) -> None:
        self._render(RegisterView(self).construir())

    def ir_a_principal(self, usuario: Usuario) -> None:
        self.usuario_actual = usuario
        self._render(MainView(self, usuario).construir())

    def cerrar_sesion(self, *_event) -> None:
        self.usuario_actual = None
        self.ir_a_login()

    def iniciar(self) -> None:
        """Arranca la aplicación mostrando la pantalla de inicio de sesión."""
        self.ir_a_login()
