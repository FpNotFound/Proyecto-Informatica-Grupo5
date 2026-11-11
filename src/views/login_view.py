"""VISTA: pantalla de inicio de sesión."""
import flet as ft


class LoginView:
    def __init__(self, app):
        self.app = app
        self.email = ft.TextField(label="Correo electrónico", width=320, autofocus=True)
        self.password = ft.TextField(
            label="Contraseña",
            width=320,
            password=True,
            can_reveal_password=True,
            on_submit=self.entrar,
        )
        self.mensaje = ft.Text("", color=ft.Colors.RED)

    def entrar(self, evento):
        usuario, mensaje = self.app.login_controller.autenticar(
            self.email.value, self.password.value
        )
        if usuario:
            self.app.ir_a_principal(usuario)
        else:
            self.mensaje.value = mensaje
            self.app.page.update()

    def construir(self):
        formulario = ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text("Bajos de Argüelles", size=24, weight=ft.FontWeight.BOLD),
                ft.Text("Sistema de monitorización ambiental"),
                self.email,
                self.password,
                self.mensaje,
                ft.FilledButton("Iniciar sesión", width=320, on_click=self.entrar),
                ft.TextButton("¿No tienes cuenta? Regístrate", on_click=self.app.ir_a_registro),
            ],
        )
        # El contenedor ocupa toda la ventana y deja el formulario en el centro.
        return ft.Container(expand=True, alignment=ft.Alignment.CENTER, content=formulario)
