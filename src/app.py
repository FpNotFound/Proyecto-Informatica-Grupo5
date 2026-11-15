"""CONTROLADOR de la aplicación: decide qué pantalla se ve en cada momento."""
# Flet es la librería que dibuja la interfaz gráfica (ventanas, botones, textos...).
import flet as ft

# Controladores: contienen la lógica (comprobar datos, guardar, permisos...).
from src.controllers.local_controller import LocalController
from src.controllers.login_controller import LoginController

# Vistas: cada una dibuja una pantalla.
from src.views.local_form_view import LocalFormView
from src.views.locales_view import LocalesView
from src.views.login_view import LoginView
from src.views.main_view import MainView
from src.views.register_view import RegisterView


class App:
    def __init__(self, page):
        # "page" es la ventana de la aplicación; la guardamos para usarla después.
        self.page = page
        # Texto que aparece en la barra de título de la ventana.
        self.page.title = "Bajos de Argüelles · Monitorización ambiental"
        # Tema claro (fondo blanco).
        self.page.theme_mode = ft.ThemeMode.LIGHT
        # Creamos los controladores una sola vez y los compartimos con las vistas.
        self.login_controller = LoginController()
        self.local_controller = LocalController()
        # Usuario que ha iniciado sesión. None significa "nadie".
        self.usuario = None

    def mostrar(self, pantalla):
        """Quita lo que hay en la ventana y pone la pantalla indicada."""
        # Borra todo lo que se ve ahora.
        self.page.clean()
        # Añade la pantalla nueva.
        self.page.add(pantalla)

    # "evento=None" permite llamar a estas funciones desde un botón (que manda
    # un evento) o directamente desde el código (sin mandar nada).

    def ir_a_login(self, evento=None):
        # Al volver al login se cierra la sesión.
        self.usuario = None
        self.mostrar(LoginView(self).construir())

    def ir_a_registro(self, evento=None):
        self.mostrar(RegisterView(self).construir())

    def entrar(self, usuario):
        """Se llama cuando el login o el registro han ido bien."""
        # Recordamos quién ha entrado.
        self.usuario = usuario
        # Y lo llevamos a la pantalla principal.
        self.ir_a_principal()

    def ir_a_principal(self, evento=None):
        self.mostrar(MainView(self).construir())

    def ir_a_locales(self, evento=None):
        self.mostrar(LocalesView(self).construir())

    def ir_a_nuevo_local(self, evento=None):
        # Sin local: el formulario sale vacío para crear uno nuevo.
        self.mostrar(LocalFormView(self).construir())

    def ir_a_editar_local(self, local):
        # Con local: el formulario sale relleno con sus datos para editarlos.
        self.mostrar(LocalFormView(self, local).construir())
