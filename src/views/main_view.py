"""VISTA: pantalla principal que se ve después de entrar."""
# Flet es la librería que dibuja la interfaz gráfica.
import flet as ft

# Frase que explica a cada rol qué puede hacer.
DESCRIPCION_ROL = {
    "Vecino": "Puedes consultar los locales de la zona y, más adelante, el ruido y el aforo de tu calle.",
    "Propietario": "Puedes consultar los locales y mantener actualizados los datos de tu local.",
    "Autoridad": "Puedes dar de alta, modificar y eliminar locales, y supervisar la zona.",
}

# Texto del botón que lleva a la pantalla de locales, distinto para cada rol.
TEXTO_BOTON_LOCALES = {
    "Vecino": "Ver locales de la zona",
    "Propietario": "Ver locales y editar el mío",
    "Autoridad": "Gestionar locales",
}


class MainView:
    def __init__(self, app):
        # Guardamos la aplicación y el usuario que ha iniciado sesión.
        self.app = app
        self.usuario = app.usuario

    def tarjeta(self, titulo):
        """Crea una tarjeta de un panel que llegará en el Sprint 3."""
        return ft.Card(
            # Ocupa más o menos ancho según el tamaño de la ventana
            # (12 = toda la fila, 6 = media fila, 4 = un tercio).
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

    def identificacion(self):
        """Devuelve el texto con el código especial del usuario según su rol."""
        # El propietario ve su código de negocio.
        if self.usuario.rol == "Propietario":
            return f"Código de negocio: {self.usuario.codigo_negocio}"
        # La autoridad ve su ID policial.
        if self.usuario.rol == "Autoridad":
            return f"ID policial: {self.usuario.id_policial}"
        # El vecino no tiene código.
        return ""

    def construir(self):
        """Monta y devuelve la pantalla completa."""
        # Rol del usuario, para no repetir "self.usuario.rol" muchas veces.
        rol = self.usuario.rol
        return ft.Column(
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.OutlinedButton("Cerrar sesión", on_click=self.app.ir_a_login),
                # f"...{x}..." mete el valor de x dentro del texto.
                ft.Text(f"¡Hola, {self.usuario.nombre}!", size=24, weight=ft.FontWeight.BOLD),
                ft.Text(f"Rol: {rol}"),
                ft.Text(self.identificacion()),
                ft.Text(DESCRIPCION_ROL[rol]),
                # Botón hacia la pantalla de locales (gestión CRUD).
                ft.FilledButton(
                    TEXTO_BOTON_LOCALES[rol], icon=ft.Icons.STOREFRONT, on_click=self.app.ir_a_locales
                ),
                # Fila de tarjetas que se recolocan según el ancho de la ventana.
                ft.ResponsiveRow(
                    controls=[
                        self.tarjeta("Nivel de ruido"),
                        self.tarjeta("Aforo"),
                        self.tarjeta("Histórico"),
                    ],
                ),
            ],
        )
