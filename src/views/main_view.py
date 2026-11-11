"""VISTA: pantalla principal que se ve después de entrar."""
import flet as ft

DESCRIPCION_ROL = {
    "Vecino": "Consultarás el nivel de ruido y el aforo de tu calle.",
    "Propietario": "Verás los datos ambientales asociados a tu local.",
    "Autoridad": "Supervisarás los sensores de la zona (ruido, aforo y más).",
}


class MainView:
    def __init__(self, app, usuario):
        self.app = app
        self.usuario = usuario

    def tarjeta(self, titulo):
        """Crea una tarjeta de un panel que llegará en el Sprint 3."""
        return ft.Card(
            # Ocupa más o menos ancho según el tamaño de la ventana.
            col={"xs": 12, "sm": 6, "md": 4},
            content=ft.Container(
                padding=20,
                content=ft.Column(
                    controls=[
                        ft.Text(titulo, weight=ft.FontWeight.BOLD),
                        ft.Text("Próximamente · Sprint 3"),
                    ],
                ),
            ),
        )

    def construir(self):
        return ft.Column(
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.OutlinedButton("Cerrar sesión", on_click=self.app.ir_a_login),
                ft.Text(f"¡Hola, {self.usuario.nombre}!", size=24, weight=ft.FontWeight.BOLD),
                ft.Text(f"Rol: {self.usuario.rol}"),
                ft.Text(DESCRIPCION_ROL[self.usuario.rol]),
                ft.ResponsiveRow(
                    controls=[
                        self.tarjeta("Nivel de ruido"),
                        self.tarjeta("Aforo"),
                        self.tarjeta("Histórico"),
                    ],
                ),
            ],
        )
