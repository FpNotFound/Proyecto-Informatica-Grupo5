"""CONTROLADOR de la aplicación CON SENSORES.

"class AppSensores(App)" HEREDA todo lo que hace App (login, registro,
formularios de locales...) y solo cambia o añade estas pantallas:

    ir_a_principal()  -> panel de sensores de todos los bares (en vez de MainView)
    ir_a_locales()    -> lista de locales con su semáforo (en vez de LocalesView)
    ir_a_bar(local)   -> NUEVA: detalle de un bar (sensores, LEDs, incidencias)

Así no hace falta tocar ningún archivo que ya existía.
"""
# La aplicación original.
from src.app import App

# Controladores nuevos.
from src.controllers.sensor_controller import SensorController
from src.controllers.vigilancia_controller import VigilanciaController

# Pantallas nuevas.
from src.views.bar_sensores_view import BarSensoresView
from src.views.locales_estado_view import LocalesEstadoView
from src.views.panel_sensores_view import PanelSensoresView


class AppSensores(App):
    def __init__(self, page):
        # super().__init__(page) hace todo lo que hacía App al empezar.
        super().__init__(page)
        self.sensor_controller = SensorController()
        self.vigilancia_controller = VigilanciaController()
        # Función que vuelve a dibujar la pantalla que se está viendo (ver recargar()).
        self.pantalla_actual = self.ir_a_principal

    def actualizar_medidas(self):
        """Toma medidas nuevas en todos los bares y revisa si hay que avisar a la policía."""
        self.sensor_controller.medir_todos()
        self.vigilancia_controller.revisar_alertas(self.sensor_controller)

    def recargar(self):
        """Vuelve a dibujar la pantalla actual (después de un cambio)."""
        self.pantalla_actual()

    def entrar(self, usuario):
        """Al iniciar sesión se toman medidas nuevas antes de enseñar el panel."""
        self.actualizar_medidas()
        super().entrar(usuario)

    def ir_a_principal(self, evento=None):
        self.pantalla_actual = self.ir_a_principal
        self.mostrar(PanelSensoresView(self).construir())

    def ir_a_locales(self, evento=None):
        self.pantalla_actual = self.ir_a_locales
        self.mostrar(LocalesEstadoView(self).construir())

    def ir_a_bar(self, local):
        # "lambda: self.ir_a_bar(local)" guarda cómo volver a ESTE mismo bar.
        self.pantalla_actual = lambda: self.ir_a_bar(local)
        self.mostrar(BarSensoresView(self, local).construir())
