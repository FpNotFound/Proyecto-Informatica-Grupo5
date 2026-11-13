"""VISTA: la lista de locales de siempre (LocalesView), pero con el semáforo
de cada local y el cartel de "CERRADO TEMPORALMENTE".

"class LocalesEstadoView(LocalesView)" significa que esta pantalla HEREDA
todo lo de LocalesView (botones Editar, Eliminar, Nuevo local...). Solo
cambiamos la tarjeta de cada local para añadirle el estado arriba.
"""
# Flet es la librería que dibuja la interfaz gráfica.
import flet as ft

# La pantalla original de locales.
from src.views.locales_view import LocalesView

# Piezas que se repiten en varias pantallas.
from src.views.piezas_sensores import SIGNIFICADO, etiqueta_cerrado, icono_semaforo


class LocalesEstadoView(LocalesView):
    def tarjeta(self, local):
        """Tarjeta original del local + una fila con su estado."""
        # super().tarjeta(local) crea la tarjeta tal y como la hacía LocalesView.
        tarjeta = super().tarjeta(local)

        color = self.app.sensor_controller.color_bar(local.codigo)
        fila_estado = ft.Row(
            wrap=True,
            controls=[
                icono_semaforo(color),
                ft.Text(SIGNIFICADO[color]),
                ft.TextButton("Ver sensores", icon=ft.Icons.SENSORS, on_click=lambda evento: self.app.ir_a_bar(local)),
            ],
        )
        if self.app.vigilancia_controller.cierre_activo(local.codigo):
            fila_estado.controls.append(etiqueta_cerrado())

        # La tarjeta es: Card -> Container -> Column. Ponemos la fila al principio de la Column.
        tarjeta.content.content.controls.insert(0, fila_estado)
        return tarjeta
