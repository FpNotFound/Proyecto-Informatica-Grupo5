"""VISTA: pantalla de registro de usuarios."""
# Flet es la librería que dibuja la interfaz gráfica.
import flet as ft

# Lista de roles ("Vecino", "Propietario", "Autoridad") para el desplegable.
from src.models.usuario import ROLES


class RegisterView:
    def __init__(self, app):
        # Guardamos la aplicación para cambiar de pantalla y usar los controladores.
        self.app = app
        # Cajas de texto del formulario.
        self.nombre = ft.TextField(label="Nombre", width=320)
        self.email = ft.TextField(label="Correo electrónico", width=320)
        self.password = ft.TextField(
            label="Contraseña", width=320, password=True, can_reveal_password=True
        )
        self.confirmar = ft.TextField(
            label="Repetir contraseña", width=320, password=True, can_reveal_password=True
        )

        # Construimos las opciones del desplegable de roles, una por cada rol.
        opciones = []
        for rol in ROLES:
            opciones.append(ft.DropdownOption(key=rol, text=rol))
        # Desplegable de rol. on_select llama a cambiar_rol cada vez que se elige uno.
        self.rol = ft.Dropdown(
            label="Rol", width=320, options=opciones, on_select=self.cambiar_rol
        )

        # Caja para el código especial del rol. Empieza oculta (visible=False)
        # y solo aparece para Propietario (código de negocio) o Autoridad (ID policial).
        self.codigo = ft.TextField(width=320, visible=False)

        # Texto rojo para los errores.
        self.mensaje = ft.Text("", color=ft.Colors.RED)

    def cambiar_rol(self, evento):
        """Muestra u oculta la caja del código según el rol elegido."""
        # Propietario: debe escribir el código de negocio de su local.
        if self.rol.value == "Propietario":
            self.codigo.label = "Código de negocio (ej. NEG-001)"
            self.codigo.visible = True
        # Autoridad: debe escribir su ID de identificación policial.
        elif self.rol.value == "Autoridad":
            self.codigo.label = "ID de identificación policial (ej. POL-0001)"
            self.codigo.visible = True
        # Vecino: no necesita código; ocultamos la caja y la vaciamos.
        else:
            self.codigo.visible = False
            self.codigo.value = ""
        # Refrescamos la pantalla para que se vea el cambio.
        self.app.page.update()

    def registrar(self, evento):
        """Se ejecuta al pulsar "Registrarme"."""
        # Pasamos todos los datos al controlador para que los compruebe y guarde.
        usuario, mensaje = self.app.login_controller.registrar(
            self.nombre.value,
            self.email.value,
            self.password.value,
            self.confirmar.value,
            self.rol.value,
            self.codigo.value,
        )
        # Si todo ha ido bien, entramos directamente en la aplicación.
        if usuario:
            self.app.entrar(usuario)
        # Si no, mostramos el error.
        else:
            self.mensaje.value = mensaje
            self.app.page.update()

    def construir(self):
        """Monta y devuelve la pantalla completa."""
        formulario = ft.Column(
            # Si la ventana es pequeña, permite desplazarse hacia abajo.
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
                self.codigo,
                self.mensaje,
                ft.FilledButton("Registrarme", width=320, on_click=self.registrar),
                ft.TextButton("¿Ya tienes cuenta? Inicia sesión", on_click=self.app.ir_a_login),
            ],
        )
        # El contenedor ocupa toda la ventana y deja el formulario en el centro.
        return ft.Container(expand=True, alignment=ft.Alignment.CENTER, content=formulario)
