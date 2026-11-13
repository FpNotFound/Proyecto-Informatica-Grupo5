"""VISTA: detalle de UN bar: sus sensores, LEDs, ventilador, historial y log de incidencias.

Todos los roles pueden verla. La policía además tiene aquí los botones de
cerrar o reabrir el bar. Abajo hay un pequeño "simulador" para pruebas que
permite forzar valores peligrosos en este bar.
"""
# Flet es la librería que dibuja la interfaz gráfica.
import flet as ft

# Nombres y unidades de cada tipo de sensor.
from src.models.sensor import NOMBRE_SENSOR, TIPOS_SENSOR, UNIDAD_SENSOR

# Piezas que se repiten en varias pantallas.
from src.views.piezas_sensores import COLOR_FLET, etiqueta_cerrado, icono_semaforo, led, ventana_texto

# Cuántas medidas antiguas se enseñan en la tabla de cada sensor.
MEDIDAS_EN_TABLA = 8

# Icono de cada tipo de sensor.
ICONO_SENSOR = {
    "temperatura": ft.Icons.THERMOSTAT,
    "humedad": ft.Icons.WATER_DROP,
    "calidad_aire": ft.Icons.AIR,
}


class BarSensoresView:
    def __init__(self, app, local):
        self.app = app
        self.usuario = app.usuario
        # El bar que estamos viendo.
        self.local = local
        self.codigo = local.codigo
        self.sensores = app.sensor_controller
        self.vigilancia = app.vigilancia_controller

    # ------------------------------------------------------------------
    # PIEZAS
    # ------------------------------------------------------------------
    def panel_leds(self):
        """Los 3 LEDs y el ventilador del bar."""
        leds = self.sensores.leds(self.codigo)
        if self.sensores.ventilador(self.codigo):
            icono_ventilador = ft.Icon(ft.Icons.WIND_POWER, size=40, color=ft.Colors.CYAN_700)
            texto_ventilador = ft.Text("Ventilador ENCENDIDO", color=ft.Colors.CYAN_700, weight=ft.FontWeight.BOLD)
        else:
            icono_ventilador = ft.Icon(ft.Icons.MODE_FAN_OFF, size=40, color=ft.Colors.GREY)
            texto_ventilador = ft.Text("Ventilador apagado", color=ft.Colors.GREY)
        return ft.Card(
            content=ft.Container(
                padding=20,
                content=ft.Column(
                    controls=[
                        ft.Text("Alertas (LEDs) y ventilador", size=18, weight=ft.FontWeight.BOLD),
                        ft.Row(
                            wrap=True,
                            spacing=30,
                            controls=[
                                ft.Column(controls=[led("rojo", leds["rojo"]), ft.Text("Temperatura")]),
                                ft.Column(controls=[led("azul", leds["azul"]), ft.Text("Humedad")]),
                                ft.Column(controls=[led("verde", leds["verde"]), ft.Text("Calidad del aire")]),
                                ft.Column(controls=[icono_ventilador, texto_ventilador]),
                            ],
                        ),
                        ft.Text(
                            "LED rojo: más de 30 °C · LED azul: humedad menor de 30 % o mayor de 70 % · "
                            "LED verde: aire Malo (1200 ppm o más). "
                            "El ventilador se enciende con más de 30 °C y aire Malo a la vez.",
                            size=12,
                        ),
                    ]
                ),
            )
        )

    def tarjeta_sensor(self, tipo):
        """Tarjeta de un sensor: valor actual y tabla con sus últimas medidas."""
        valor = self.sensores.valor(self.codigo, tipo)
        unidad = UNIDAD_SENSOR[tipo]
        color = self.sensores.color_sensor(tipo, valor)

        # Filas de la tabla del historial.
        filas = []
        for medida in self.sensores.historial_de(self.codigo, tipo, MEDIDAS_EN_TABLA):
            color_medida = self.sensores.color_sensor(tipo, medida["valor"])
            filas.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(medida["fecha"])),
                        ft.DataCell(ft.Text(f"{medida['valor']} {unidad}")),
                        ft.DataCell(icono_semaforo(color_medida, 16)),
                    ]
                )
            )

        controles = [
            ft.Row(controls=[ft.Icon(ICONO_SENSOR[tipo]), ft.Text(NOMBRE_SENSOR[tipo], weight=ft.FontWeight.BOLD)]),
            ft.Row(
                controls=[
                    icono_semaforo(color),
                    ft.Text(f"{valor} {unidad}", size=28, weight=ft.FontWeight.BOLD, color=COLOR_FLET[color]),
                ]
            ),
        ]
        # El sensor de aire también dice si la calidad es Buena, Moderada o Mala.
        if tipo == "calidad_aire":
            controles.append(ft.Text(f"Calidad del aire: {self.sensores.calidad_aire(valor)}"))
        controles.append(ft.Text("Historial (lo más nuevo arriba)", size=12))
        controles.append(
            ft.DataTable(
                column_spacing=16,
                heading_row_height=30,
                data_row_min_height=26,
                data_row_max_height=26,
                columns=[ft.DataColumn("Fecha"), ft.DataColumn("Valor"), ft.DataColumn("Estado")],
                rows=filas,
            )
        )
        return ft.Card(
            col={"xs": 12, "md": 6, "lg": 4},
            content=ft.Container(padding=16, content=ft.Column(controls=controles)),
        )

    def log_incidencias(self):
        """Tabla con el log de incidencias del bar."""
        filas = []
        for incidencia in self.vigilancia.incidencias_de(self.codigo):
            filas.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(incidencia["fecha"])),
                        ft.DataCell(ft.Text(incidencia["tipo"], weight=ft.FontWeight.BOLD)),
                        ft.DataCell(ft.Text(incidencia["autor"])),
                        # width limita el ancho para que los textos largos bajen de línea.
                        ft.DataCell(ft.Text(incidencia["descripcion"], width=380)),
                    ]
                )
            )
        if not filas:
            contenido = ft.Text("Este bar no tiene incidencias.")
        else:
            contenido = ft.DataTable(
                data_row_max_height=80,
                columns=[
                    ft.DataColumn("Fecha"),
                    ft.DataColumn("Tipo"),
                    ft.DataColumn("Autor"),
                    ft.DataColumn("Descripción"),
                ],
                rows=filas,
            )
        return ft.Card(
            content=ft.Container(
                padding=20,
                content=ft.Column(
                    controls=[
                        ft.Row(controls=[ft.Icon(ft.Icons.HISTORY), ft.Text("Log de incidencias", size=18, weight=ft.FontWeight.BOLD)]),
                        # Row con scroll por si la tabla no cabe a lo ancho (móvil).
                        ft.Row(scroll=ft.ScrollMode.AUTO, controls=[contenido]),
                    ]
                ),
            )
        )

    def botones_policia(self):
        """(Autoridad) Botón para cerrar o reabrir este bar."""
        if self.vigilancia.cierre_activo(self.codigo):
            return ft.OutlinedButton("Reabrir local", icon=ft.Icons.LOCK_OPEN, on_click=self.pedir_reapertura)
        return ft.FilledButton("Cerrar temporalmente", icon=ft.Icons.LOCK, on_click=self.pedir_cierre)

    def simulador(self):
        """Botones de prueba para cambiar las medidas de este bar."""
        if self.sensores.escenario(self.codigo) == "alerta":
            situacion = "Ahora se simula: situación de ALERTA (calor, humedad y aire cargado)."
        else:
            situacion = "Ahora se simula: situación normal."
        return ft.Card(
            content=ft.Container(
                padding=20,
                content=ft.Column(
                    controls=[
                        ft.Text("Simulador (solo para pruebas)", size=16, weight=ft.FontWeight.BOLD),
                        ft.Text(situacion, italic=True),
                        ft.Row(
                            wrap=True,
                            controls=[
                                ft.OutlinedButton("Forzar alerta", icon=ft.Icons.WARNING, on_click=self.forzar_alerta),
                                ft.OutlinedButton("Volver a normal", icon=ft.Icons.CHECK_CIRCLE, on_click=self.volver_normal),
                            ],
                        ),
                        ft.Text(
                            "Los valores cambian poco a poco: pulsa \"Actualizar medidas\" "
                            "varias veces para ver cómo suben o bajan.",
                            size=12,
                        ),
                    ]
                ),
            )
        )

    # ------------------------------------------------------------------
    # ACCIONES DE LOS BOTONES
    # ------------------------------------------------------------------
    def actualizar_medidas(self, evento):
        self.app.actualizar_medidas()
        self.app.recargar()

    def forzar_alerta(self, evento):
        self.sensores.forzar_alerta(self.codigo)
        self.app.actualizar_medidas()
        self.app.recargar()

    def volver_normal(self, evento):
        self.sensores.volver_normal(self.codigo)
        self.app.actualizar_medidas()
        self.app.recargar()

    def pedir_cierre(self, evento):
        """(Autoridad) Pide el motivo y cierra el bar."""

        def al_aceptar(motivo):
            error = self.vigilancia.cerrar_local(self.usuario, self.codigo, motivo)
            if not error:
                # Al cerrar, el bar se vacía: sus sensores vuelven a valores normales.
                self.sensores.volver_normal(self.codigo)
            return error

        ventana_texto(
            self.app,
            f"Cerrar temporalmente {self.local.nombre}",
            "Escribe la incidencia que justifica el cierre. El propietario la recibirá.",
            "Cerrar local",
            al_aceptar,
        )

    def pedir_reapertura(self, evento):
        """(Autoridad) Reabre el bar, con una nota opcional."""

        def al_aceptar(nota):
            return self.vigilancia.reabrir_local(self.usuario, self.codigo, nota)

        ventana_texto(
            self.app,
            f"Reabrir {self.local.nombre}",
            "Puedes escribir una nota para el propietario (opcional).",
            "Reabrir",
            al_aceptar,
        )

    # ------------------------------------------------------------------
    # PANTALLA COMPLETA
    # ------------------------------------------------------------------
    def construir(self):
        barra = [
            ft.OutlinedButton("Volver", icon=ft.Icons.ARROW_BACK, on_click=self.app.ir_a_principal),
            ft.FilledButton("Actualizar medidas", icon=ft.Icons.REFRESH, on_click=self.actualizar_medidas),
        ]
        if self.usuario.rol == "Autoridad":
            barra.append(self.botones_policia())

        cabecera = [
            icono_semaforo(self.sensores.color_bar(self.codigo), 36),
            ft.Text(self.local.nombre, size=24, weight=ft.FontWeight.BOLD),
        ]
        if self.vigilancia.cierre_activo(self.codigo):
            cabecera.append(etiqueta_cerrado())

        tarjetas = []
        for tipo in TIPOS_SENSOR:
            tarjetas.append(self.tarjeta_sensor(tipo))

        return ft.Column(
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Row(wrap=True, controls=barra),
                ft.Row(wrap=True, controls=cabecera),
                ft.Text(f"{self.codigo} · {self.local.tipo} · {self.local.direccion}"),
                self.panel_leds(),
                ft.ResponsiveRow(controls=tarjetas),
                self.log_incidencias(),
                self.simulador(),
            ],
        )
