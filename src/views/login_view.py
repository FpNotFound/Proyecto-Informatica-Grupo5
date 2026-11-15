"""VISTA: pantalla de inicio de sesión."""
# Flet es la librería que dibuja la interfaz gráfica.
import flet as ft


class LoginView:
    def __init__(self, app):
        # Guardamos la aplicación para poder cambiar de pantalla y usar los controladores.
        self.app = app
        # Caja de texto para el correo. autofocus=True pone el cursor aquí al abrir.
        self.email = ft.TextField(label="Correo electrónico", width=320, autofocus=True)
        # Caja de texto para la contraseña.
        self.password = ft.TextField(
            label="Contraseña",
            width=320,
            # password=True oculta lo que se escribe con puntos.
            password=True,
            # Muestra un icono de "ojo" para ver la contraseña si se quiere.
            can_reveal_password=True,
            # Al pulsar Intro en esta caja se intenta entrar.
            on_submit=self.entrar,
        )
        # Texto rojo donde aparecerán los errores (empieza vacío).
        self.mensaje = ft.Text("", color=ft.Colors.RED)

    def entrar(self, evento):
        """Se ejecuta al pulsar "Iniciar sesión" (o Intro)."""
        # Pedimos al controlador que compruebe el correo y la contraseña.
        usuario, mensaje = self.app.login_controller.autenticar(
            self.email.value, self.password.value
        )
        # Si ha devuelto un usuario, todo ha ido bien: entramos.
        if usuario:
            self.app.entrar(usuario)
        # Si no, mostramos el error y refrescamos la pantalla para que se vea.
        else:
            self.mensaje.value = mensaje
            self.app.page.update()

    def construir(self):
        """Monta y devuelve la pantalla completa."""
        # Column coloca los elementos uno debajo de otro.
        formulario = ft.Column(
            # Centrado vertical y horizontal.
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            # Elementos de la pantalla, en orden de arriba a abajo.
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
