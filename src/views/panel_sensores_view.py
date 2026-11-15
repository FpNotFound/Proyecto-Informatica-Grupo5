"""VISTA: panel principal (dashboard) con los sensores de TODOS los bares.

Sustituye a la pantalla principal (MainView) cuando se usa AppSensores.
Lo que se ve depende del rol:

    Todos          -> notificaciones (si tienen) y la lista de bares con su
                      semáforo, sus valores, sus LEDs y el ventilador.
    Autoridad      -> además: alertas de niveles peligrosos (con el botón para
                      cerrar el bar), reclamaciones pendientes y bares cerrados.
    Propietario    -> además: el estado de SU bar y, si está cerrado, el motivo
                      y el botón para presentar una reclamación.
"""
# Flet es la librería que dibuja la interfaz gráfica.
import flet as ft

# Textos de la pantalla principal original (para no repetirlos).
from src.views.main_view import DESCRIPCION_ROL, TEXTO_BOTON_LOCALES

# Piezas que se repiten en varias pantallas.
from src.views.piezas_sensores import etiqueta_cerrado, icono_semaforo, led, ventana_texto


class PanelSensoresView:
    def __init__(self, app):
        self.app = app
        self.usuario = app.usuario
        # Atajos para no escribir "self.app." todo el rato.
        self.sensores = app.sensor_controller
        self.vigilancia = app.vigilancia_controller

    # ------------------------------------------------------------------
    # PIEZAS
    # ------------------------------------------------------------------
    def seccion(self, titulo, controles, icono=None):
        """Tarjeta con un título y lo que se le pase dentro."""
        cabecera = [ft.Text(titulo, size=18, weight=ft.FontWeight.BOLD)]
        if icono:
            cabecera.insert(0, ft.Icon(icono))
        return ft.Card(
            content=ft.Container(
                padding=20,
                content=ft.Column(controls=[ft.Row(controls=cabecera)] + controles),
            )
        )

    def tarjeta_bar(self, local):
        """Tarjeta pequeña de un bar con su estado y sus medidas actuales."""
        codigo = local.codigo
        leds = self.sensores.leds(codigo)
        # Texto del ventilador.
        if self.sensores.ventilador(codigo):
            ventilador = ft.Text("Ventilador ENCENDIDO", color=ft.Colors.CYAN_700, weight=ft.FontWeight.BOLD)
        else:
            ventilador = ft.Text("Ventilador apagado", color=ft.Colors.GREY)

        controles = [
            ft.Row(
                controls=[
                    icono_semaforo(self.sensores.color_bar(codigo)),
                    ft.Text(local.nombre, size=18, weight=ft.FontWeight.BOLD),
                ]
            ),
            ft.Text(f"{codigo} · {local.direccion}", size=12),
        ]
        # Si la policía lo ha cerrado, se pone el cartel.
        if self.vigilancia.cierre_activo(codigo):
            controles.append(etiqueta_cerrado())
        controles = controles + [
            ft.Text(f"Temperatura: {self.sensores.valor(codigo, 'temperatura')} °C"),
            ft.Text(f"Humedad: {self.sensores.valor(codigo, 'humedad')} %"),
            ft.Text(
                f"Aire: {self.sensores.valor(codigo, 'calidad_aire')} ppm "
                f"({self.sensores.calidad_aire(self.sensores.valor(codigo, 'calidad_aire'))})"
            ),
            ft.Row(
                controls=[
                    led("rojo", leds["rojo"], 18),
                    led("azul", leds["azul"], 18),
                    led("verde", leds["verde"], 18),
                    ventilador,
                ]
            ),
            ft.TextButton(
                "Ver sensores e incidencias",
                icon=ft.Icons.SENSORS,
                # Al pulsar se abre la pantalla de detalle de ESTE bar.
                on_click=lambda evento: self.app.ir_a_bar(local),
            ),
        ]
        return ft.Card(
            # 1 tarjeta por fila en móvil, 2 en tablet, 3 en pantalla grande.
            col={"xs": 12, "sm": 6, "lg": 4},
            content=ft.Container(padding=16, content=ft.Column(controls=controles)),
        )

    def nombre_local(self, codigo):
        """Nombre del local a partir de su código (o el código si ya no existe)."""
        local = self.app.local_controller.buscar(codigo)
        if local:
            return local.nombre
        return codigo

    # ------------------------------------------------------------------
    # SECCIONES
    # ------------------------------------------------------------------
    def seccion_notificaciones(self):
        """Avisos del usuario (los no leídos salen en negrita)."""
        avisos = self.vigilancia.notificaciones_de(self.usuario)
        controles = []
        if not avisos:
            controles.append(ft.Text("No tienes notificaciones."))
        # avisos[:8] son los 8 primeros (los más nuevos).
        for aviso in avisos[:8]:
            if aviso["leida"]:
                grosor = ft.FontWeight.NORMAL
            else:
                grosor = ft.FontWeight.BOLD
            controles.append(
                ft.Column(
                    spacing=2,
                    controls=[
                        ft.Text(f"{aviso['fecha']} · {aviso['titulo']}", weight=grosor),
                        ft.Text(aviso["mensaje"], size=13),
                    ],
                )
            )
        if self.vigilancia.sin_leer(self.usuario) > 0:
            controles.append(ft.TextButton("Marcar como leídas", icon=ft.Icons.DONE_ALL, on_click=self.marcar_leidas))
        titulo = f"Notificaciones ({self.vigilancia.sin_leer(self.usuario)} sin leer)"
        return self.seccion(titulo, controles, ft.Icons.NOTIFICATIONS)

    def fila_alerta(self, local):
        """(Autoridad) Una línea de alerta: bar en rojo + botón para cerrarlo."""
        codigo = local.codigo
        return ft.Row(
            wrap=True,
            controls=[
                icono_semaforo("rojo"),
                ft.Text(f"{local.nombre} ({codigo})", weight=ft.FontWeight.BOLD),
                ft.Text(
                    f"{self.sensores.valor(codigo, 'temperatura')} °C · "
                    f"{self.sensores.valor(codigo, 'humedad')} % · "
                    f"{self.sensores.valor(codigo, 'calidad_aire')} ppm"
                ),
                ft.FilledButton(
                    "Cerrar temporalmente",
                    icon=ft.Icons.LOCK,
                    on_click=lambda evento: self.pedir_cierre(local),
                ),
            ],
        )

    def seccion_alertas_policia(self):
        """(Autoridad) Bares abiertos que están ahora mismo en ROJO."""
        controles = []
        for local in self.app.local_controller.listar():
            en_peligro = self.sensores.color_bar(local.codigo) == "rojo"
            abierto = not self.vigilancia.cierre_activo(local.codigo)
            if en_peligro and abierto:
                controles.append(self.fila_alerta(local))
        if not controles:
            controles.append(ft.Text("Ningún bar abierto tiene niveles peligrosos ahora mismo."))
        return self.seccion("Alertas de niveles peligrosos", controles, ft.Icons.WARNING)

    def fila_reclamacion(self, cierre):
        """(Autoridad) Una reclamación con los dos botones para valorarla."""
        codigo = cierre["local"]
        return ft.Column(
            controls=[
                ft.Text(f"{self.nombre_local(codigo)} ({codigo})", weight=ft.FontWeight.BOLD),
                ft.Text(f"Motivo del cierre ({cierre['policia']}): {cierre['motivo']}", size=13),
                ft.Text(f"Reclamación del propietario: {cierre['reclamacion']}", size=13),
                ft.Row(
                    controls=[
                        ft.OutlinedButton(
                            "Justificado (sigue cerrado)",
                            on_click=lambda evento: self.pedir_resolucion(codigo, True),
                        ),
                        ft.FilledButton(
                            "No justificado (reabrir)",
                            on_click=lambda evento: self.pedir_resolucion(codigo, False),
                        ),
                    ]
                ),
            ]
        )

    def seccion_reclamaciones(self):
        """(Autoridad) Reclamaciones de propietarios que hay que valorar."""
        controles = []
        for cierre in self.vigilancia.reclamaciones_pendientes():
            controles.append(self.fila_reclamacion(cierre))
        if not controles:
            controles.append(ft.Text("No hay reclamaciones pendientes."))
        return self.seccion("Reclamaciones pendientes", controles, ft.Icons.GAVEL)

    def fila_cerrado(self, cierre):
        """(Autoridad) Un bar cerrado con el botón para reabrirlo."""
        codigo = cierre["local"]
        return ft.Row(
            wrap=True,
            controls=[
                ft.Icon(ft.Icons.LOCK),
                ft.Text(f"{self.nombre_local(codigo)} ({codigo}) · desde {cierre['fecha']}"),
                ft.TextButton(
                    "Reabrir",
                    icon=ft.Icons.LOCK_OPEN,
                    on_click=lambda evento: self.pedir_reapertura(codigo),
                ),
            ],
        )

    def seccion_cerrados(self):
        """(Autoridad) Bares cerrados ahora mismo, con el botón para reabrirlos."""
        controles = []
        for cierre in self.vigilancia.cerrados():
            controles.append(self.fila_cerrado(cierre))
        if not controles:
            controles.append(ft.Text("No hay bares cerrados."))
        return self.seccion("Bares cerrados temporalmente", controles, ft.Icons.LOCK)

    def seccion_mi_local(self):
        """(Propietario) Estado de su bar y, si está cerrado, la opción de reclamar."""
        codigo = self.usuario.codigo_negocio
        controles = [
            ft.Row(
                controls=[
                    icono_semaforo(self.sensores.color_bar(codigo)),
                    ft.Text(f"{self.nombre_local(codigo)} ({codigo})", weight=ft.FontWeight.BOLD),
                ]
            )
        ]
        cierre = self.vigilancia.cierre_activo(codigo)
        if not cierre:
            controles.append(ft.Text("Tu local está abierto."))
        else:
            controles.append(etiqueta_cerrado())
            controles.append(ft.Text(f"Cerrado el {cierre['fecha']} por {cierre['policia']}."))
            controles.append(ft.Text(f"Incidencia escrita por la policía: {cierre['motivo']}"))
            if cierre["estado_reclamacion"] == "":
                # Aún no ha reclamado: le damos la opción.
                controles.append(
                    ft.FilledButton(
                        "Presentar reclamación",
                        icon=ft.Icons.REPORT,
                        on_click=lambda evento: self.pedir_reclamacion(codigo),
                    )
                )
            else:
                controles.append(ft.Text(f"Tu reclamación: {cierre['reclamacion']}"))
                controles.append(ft.Text(f"Estado: {cierre['estado_reclamacion']}", weight=ft.FontWeight.BOLD))
                if cierre["respuesta"]:
                    controles.append(ft.Text(f"Respuesta de la policía: {cierre['respuesta']}"))
        # Si la última reclamación se resolvió a su favor, también se lo enseñamos.
        ultimo = self.vigilancia.ultimo_cierre(codigo)
        if not cierre and ultimo and ultimo["estado_reclamacion"] == "No justificado":
            controles.append(ft.Text(f"Tu última reclamación fue aceptada: {ultimo['respuesta']}"))
        return self.seccion("Mi local", controles, ft.Icons.STOREFRONT)

    def seccion_bares(self):
        """Todos los bares de la zona con su semáforo (lo ven todos los roles)."""
        tarjetas = []
        for local in self.app.local_controller.listar():
            tarjetas.append(self.tarjeta_bar(local))
        if not tarjetas:
            return ft.Text("Todavía no hay locales registrados.")
        return ft.ResponsiveRow(controls=tarjetas)

    # ------------------------------------------------------------------
    # ACCIONES DE LOS BOTONES
    # ------------------------------------------------------------------
    def actualizar_medidas(self, evento):
        """Toma medidas nuevas de todos los sensores y vuelve a dibujar el panel."""
        self.app.actualizar_medidas()
        self.app.recargar()

    def marcar_leidas(self, evento):
        self.vigilancia.marcar_leidas(self.usuario)
        self.app.recargar()

    def pedir_cierre(self, local):
        """(Autoridad) Pide el motivo y cierra el bar."""

        # Esta función recibe el texto escrito en la ventanita.
        def al_aceptar(motivo):
            error = self.vigilancia.cerrar_local(self.usuario, local.codigo, motivo)
            if not error:
                # Al cerrar, el bar se vacía: sus sensores vuelven a valores normales.
                self.sensores.volver_normal(local.codigo)
            return error

        ventana_texto(
            self.app,
            f"Cerrar temporalmente {local.nombre}",
            "Escribe la incidencia que justifica el cierre. El propietario la recibirá.",
            "Cerrar local",
            al_aceptar,
        )

    def pedir_reapertura(self, codigo):
        """(Autoridad) Reabre un bar, con una nota opcional."""

        def al_aceptar(nota):
            return self.vigilancia.reabrir_local(self.usuario, codigo, nota)

        ventana_texto(
            self.app,
            f"Reabrir {self.nombre_local(codigo)}",
            "Puedes escribir una nota para el propietario (opcional).",
            "Reabrir",
            al_aceptar,
        )

    def pedir_resolucion(self, codigo, justificado):
        """(Autoridad) Valora una reclamación con una respuesta para el propietario."""

        def al_aceptar(respuesta):
            return self.vigilancia.resolver_reclamacion(self.usuario, codigo, justificado, respuesta)

        if justificado:
            titulo = "El cierre está justificado"
        else:
            titulo = "El cierre NO está justificado (se reabrirá el local)"
        ventana_texto(self.app, titulo, "Escribe la respuesta para el propietario.", "Enviar", al_aceptar)

    def pedir_reclamacion(self, codigo):
        """(Propietario) Escribe una reclamación contra el cierre de su bar."""

        def al_aceptar(texto):
            return self.vigilancia.reclamar(self.usuario, codigo, texto)

        ventana_texto(
            self.app,
            "Presentar reclamación",
            "Explica por qué crees que el cierre no está justificado. La policía la valorará.",
            "Enviar reclamación",
            al_aceptar,
        )

    # ------------------------------------------------------------------
    # PANTALLA COMPLETA
    # ------------------------------------------------------------------
    def construir(self):
        rol = self.usuario.rol
        controles = [
            ft.Row(
                wrap=True,
                controls=[
                    ft.OutlinedButton("Cerrar sesión", on_click=self.app.ir_a_login),
                    ft.FilledButton(TEXTO_BOTON_LOCALES[rol], icon=ft.Icons.STOREFRONT, on_click=self.app.ir_a_locales),
                    ft.FilledButton("Actualizar medidas", icon=ft.Icons.REFRESH, on_click=self.actualizar_medidas),
                ],
            ),
            ft.Text(f"¡Hola, {self.usuario.nombre}!", size=24, weight=ft.FontWeight.BOLD),
            ft.Text(f"Rol: {rol}. {DESCRIPCION_ROL[rol]}"),
        ]
        # Los vecinos no reciben notificaciones; los demás sí.
        if rol == "Autoridad":
            controles.append(self.seccion_notificaciones())
            controles.append(self.seccion_alertas_policia())
            controles.append(self.seccion_reclamaciones())
            controles.append(self.seccion_cerrados())
        if rol == "Propietario":
            controles.append(self.seccion_notificaciones())
            controles.append(self.seccion_mi_local())
        controles.append(ft.Text("Bares de la zona", size=20, weight=ft.FontWeight.BOLD))
        controles.append(
            ft.Row(
                wrap=True,
                controls=[
                    icono_semaforo("verde", 16), ft.Text("Todo correcto"),
                    icono_semaforo("amarillo", 16), ft.Text("Precaución"),
                    icono_semaforo("rojo", 16), ft.Text("Nivel peligroso"),
                ],
            )
        )
        controles.append(self.seccion_bares())
        return ft.Column(expand=True, scroll=ft.ScrollMode.AUTO, controls=controles)
