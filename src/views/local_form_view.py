"""VISTA: formulario para CREAR un local nuevo o EDITAR uno que ya existe.

- Si se abre sin local  -> modo "crear"  (cajas vacías).
- Si se abre con local  -> modo "editar" (cajas rellenas; el código no se puede cambiar).
"""
# Flet es la librería que dibuja la interfaz gráfica.
import flet as ft

# Lista de tipos de local para el desplegable.
from src.models.local import TIPOS_LOCAL


class LocalFormView:
    # local=None significa que, si no se pasa ningún local, estamos creando uno nuevo.
    def __init__(self, app, local=None):
        # Guardamos la aplicación, el usuario conectado, el controlador y el local.
        self.app = app
        self.usuario = app.usuario
        self.controller = app.local_controller
        self.local = local

        # Cajas de texto del formulario.
        self.codigo = ft.TextField(label="Código de negocio (ej. NEG-002)", width=320)
        self.nombre = ft.TextField(label="Nombre del local", width=320)
        self.direccion = ft.TextField(label="Dirección", width=320)
        # keyboard_type=NUMBER muestra el teclado numérico en el móvil.
        self.aforo = ft.TextField(
            label="Aforo máximo (personas)", width=320, keyboard_type=ft.KeyboardType.NUMBER
        )

        # Desplegable con los tipos de local.
        opciones = []
        for tipo in TIPOS_LOCAL:
            opciones.append(ft.DropdownOption(key=tipo, text=tipo))
        self.tipo = ft.Dropdown(label="Tipo de local", width=320, options=opciones)

        # Texto rojo para los errores.
        self.mensaje = ft.Text("", color=ft.Colors.RED)

        # Modo editar: rellenamos las cajas con los datos actuales del local.
        if local is not None:
            self.codigo.value = local.codigo
            # read_only=True: se ve pero no se puede cambiar (el código identifica al local).
            self.codigo.read_only = True
            self.nombre.value = local.nombre
            self.direccion.value = local.direccion
            self.tipo.value = local.tipo
            # str() convierte el número 80 en el texto "80" para poder mostrarlo.
            self.aforo.value = str(local.aforo)

    def guardar(self, evento):
        """Se ejecuta al pulsar "Guardar"."""
        # Modo crear: pedimos al controlador que cree el local.
        if self.local is None:
            local, mensaje = self.controller.crear(
                self.usuario,
                self.codigo.value,
                self.nombre.value,
                self.direccion.value,
                self.tipo.value,
                self.aforo.value,
            )
        # Modo editar: pedimos al controlador que lo modifique.
        else:
            local, mensaje = self.controller.modificar(
                self.usuario,
                self.local.codigo,
                self.nombre.value,
                self.direccion.value,
                self.tipo.value,
                self.aforo.value,
            )
        # Si ha ido bien, volvemos a la lista de locales.
        if local:
            self.app.ir_a_locales()
        # Si no, mostramos el error.
        else:
            self.mensaje.value = mensaje
            self.app.page.update()

    def construir(self):
        """Monta y devuelve la pantalla completa."""
        # El título cambia según el modo.
        if self.local is None:
            titulo = "Nuevo local"
        else:
            titulo = "Editar local"

        formulario = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(titulo, size=24, weight=ft.FontWeight.BOLD),
                self.codigo,
                self.nombre,
                self.direccion,
                self.tipo,
                self.aforo,
                self.mensaje,
                ft.FilledButton("Guardar", width=320, on_click=self.guardar),
                ft.TextButton("Cancelar", on_click=self.app.ir_a_locales),
            ],
        )
        # El contenedor ocupa toda la ventana y deja el formulario en el centro.
        return ft.Container(expand=True, alignment=ft.Alignment.CENTER, content=formulario)
