"""VISTA: pantalla de registro de usuarios."""
import flet as ft

from src.models.usuario import ROLES


class RegisterView:
    def __init__(self, app):
        self.app = app
        self.nombre = ft.TextField(label="Nombre", width=320)
        self.email = ft.TextField(label="Correo electrónico", width=320)
        self.password = ft.TextField(
            label="Contraseña", width=320, password=True, can_reveal_password=True
        )
        self.confirmar = ft.TextField(
            label="Repetir contraseña", width=320, password=True, can_reveal_password=True
        )

        opciones = []
        for rol in ROLES:
            opciones.append(ft.DropdownOption(key=rol, text=rol))
        self.rol = ft.Dropdown(label="Rol", width=320, options=opciones)

        self.mensaje = ft.Text("", color=ft.Colors.RED)

    def registrar(self, evento):
        usuario, mensaje = self.app.login_controller.registrar(
            self.nombre.value,
            self.email.value,
            self.password.value,
            self.confirmar.value,
            self.rol.value,
        )
        if usuario:
            self.app.ir_a_principal(usuario)
        else:
            self.mensaje.value = mensaje
            self.app.page.update()

    def construir(self):
        formulario = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text("Crear cuenta", size=24, weight=ft.FontWeight.BOLD),
                self.nombre,
                self.email,
                self.password,
                self.confirmar,
                self.rol,
                self.mensaje,
                ft.FilledButton("Registrarme", width=320, on_click=self.registrar),
                ft.TextButton("¿Ya tienes cuenta? Inicia sesión", on_click=self.app.ir_a_login),
            ],
        )
        # El contenedor ocupa toda la ventana y deja el formulario en el centro.
        return ft.Container(expand=True, alignment=ft.Alignment.CENTER, content=formulario)
