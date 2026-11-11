"""CONTROLADOR de la aplicación: decide qué pantalla se ve en cada momento."""
import flet as ft

from src.controllers.login_controller import LoginController
from src.views.login_view import LoginView
from src.views.main_view import MainView
from src.views.register_view import RegisterView


class App:
    def __init__(self, page):
        self.page = page
        self.page.title = "Bajos de Argüelles · Monitorización ambiental"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.login_controller = LoginController()

    def mostrar(self, pantalla):
        """Quita lo que hay en la ventana y pone la pantalla indicada."""
        self.page.clean()
        self.page.add(pantalla)

    def ir_a_login(self, evento=None):
        self.mostrar(LoginView(self).construir())

    def ir_a_registro(self, evento=None):
        self.mostrar(RegisterView(self).construir())

    def ir_a_principal(self, usuario):
        self.mostrar(MainView(self, usuario).construir())
