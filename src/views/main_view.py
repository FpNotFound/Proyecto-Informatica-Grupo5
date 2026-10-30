"""MainView — capa VISTA. Pantalla principal tras el inicio de sesión (RF-04).

Da la bienvenida al usuario autenticado y muestra su rol. Los paneles
(dashboards) específicos de cada rol con los datos de sensores se desarrollarán
en el Sprint 3; aquí se presentan como adelanto no funcional para dejar
preparada la navegación y la estructura responsive.
"""
from __future__ import annotations

import flet as ft

from src.models.usuario import Rol, Usuario

# Descripción orientativa de lo que verá cada rol en próximos sprints.
_DESCRIPCION_ROL = {
    Rol.VECINO: "Consultarás el nivel de ruido y el aforo de tu calle.",
    Rol.PROPIETARIO: "Verás los datos ambientales asociados a tu local.",
    Rol.AUTORIDAD: "Supervisarás los sensores de la zona (ruido, aforo y más).",
}

_PROXIMOS_PANELES = [
    (ft.Icons.VOLUME_UP, "Nivel de ruido", "Sensor de ruido ambiental"),
    (ft.Icons.GROUPS, "Aforo", "Ocupación estimada de la zona"),
    (ft.Icons.INSIGHTS, "Histórico", "Evolución y estadísticas"),
]


class MainView:
    def __init__(self, app, usuario: Usuario) -> None:
        self.app = app
        self.usuario = usuario

    def _tarjeta_panel(self, icono, titulo, subtitulo) -> ft.Control:
        return ft.Card(
            col={"xs": 12, "sm": 6, "md": 4},
            content=ft.Container(
                padding=20,
                content=ft.Column(
                    spacing=8,
                    controls=[
                        ft.Icon(icono, size=36, color=ft.Colors.BLUE),
                        ft.Text(titulo, size=16, weight=ft.FontWeight.BOLD),
                        ft.Text(subtitulo, size=12, color=ft.Colors.BLUE_GREY),
                        ft.Container(
                            padding=ft.Padding(left=10, top=4, right=10, bottom=4),
                            bgcolor=ft.Colors.AMBER_100,
                            border_radius=12,
                            content=ft.Text("Próximamente · Sprint 3", size=11),
                        ),
                    ],
                ),
            ),
        )

    def construir(self) -> ft.Control:
        cabecera = ft.Container(
            bgcolor=ft.Colors.BLUE,
            padding=ft.Padding(left=24, top=16, right=24, bottom=16),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Row(
                        spacing=10,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Icon(ft.Icons.SENSORS, color=ft.Colors.WHITE),
                            ft.Text(
                                "Bajos de Argüelles",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.WHITE,
                            ),
                        ],
                    ),
                    ft.OutlinedButton(
                        "Cerrar sesión",
                        icon=ft.Icons.LOGOUT,
                        on_click=self.app.cerrar_sesion,
                    ),
                ],
            ),
        )

        bienvenida = ft.Container(
            padding=24,
            content=ft.Column(
                spacing=6,
                controls=[
                    ft.Text(
                        f"¡Hola, {self.usuario.nombre}!",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Row(
                        spacing=8,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Icon(ft.Icons.BADGE, size=18, color=ft.Colors.BLUE_GREY),
                            ft.Text(f"Rol: {self.usuario.rol.value}", size=14),
                        ],
                    ),
                    ft.Text(
                        _DESCRIPCION_ROL.get(self.usuario.rol, ""),
                        size=13,
                        color=ft.Colors.BLUE_GREY,
                    ),
                ],
            ),
        )

        paneles = ft.Container(
            padding=ft.Padding(left=24, top=0, right=24, bottom=24),
            content=ft.ResponsiveRow(
                controls=[
                    self._tarjeta_panel(ic, t, s) for ic, t, s in _PROXIMOS_PANELES
                ],
            ),
        )

        return ft.Column(
            expand=True,
            spacing=0,
            scroll=ft.ScrollMode.AUTO,
            controls=[cabecera, bienvenida, paneles],
        )
