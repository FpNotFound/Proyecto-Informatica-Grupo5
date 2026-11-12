"""VISTA: lista de locales con los botones que permite cada rol.

- Vecino:      solo ve la lista.
- Propietario: ve la lista y tiene el botón "Editar" en SU local.
- Autoridad:   ve la lista, puede crear ("Nuevo local"), editar y eliminar.
"""
# Flet es la librería que dibuja la interfaz gráfica.
import flet as ft


class LocalesView:
    def __init__(self, app):
        # Guardamos la aplicación, el usuario conectado y el controlador de locales.
        self.app = app
        self.usuario = app.usuario
        self.controller = app.local_controller

    def tarjeta(self, local):
        """Crea la tarjeta que muestra un local y sus botones."""
        # Lista de botones; se llena según los permisos del usuario.
        botones = []
        # Botón "Editar" si el usuario puede editar este local.
        # "lambda evento: ..." es una función de una línea: al pulsar el botón
        # se ejecuta lo que hay detrás de los dos puntos.
        if self.controller.puede_editar(self.usuario, local):
            botones.append(
                ft.TextButton(
                    "Editar",
                    icon=ft.Icons.EDIT,
                    on_click=lambda evento: self.app.ir_a_editar_local(local),
                )
            )
        # Botón "Eliminar" si el usuario puede eliminar locales.
        if self.controller.puede_eliminar(self.usuario):
            botones.append(
                ft.TextButton(
                    "Eliminar",
                    icon=ft.Icons.DELETE,
                    on_click=lambda evento: self.confirmar_eliminar(local),
                )
            )

        return ft.Card(
            # Ancho adaptable: 1 tarjeta por fila en móvil, 2 en tablet, 3 en pantalla grande.
            col={"xs": 12, "sm": 6, "md": 4},
            content=ft.Container(
                padding=20,
                content=ft.Column(
                    controls=[
                        ft.Text(local.nombre, size=18, weight=ft.FontWeight.BOLD),
                        ft.Text(f"Código: {local.codigo}"),
                        ft.Text(f"Tipo: {local.tipo}"),
                        ft.Text(f"Dirección: {local.direccion}"),
                        ft.Text(f"Aforo máximo: {local.aforo} personas"),
                        # Row coloca los botones uno al lado del otro.
                        ft.Row(controls=botones),
                    ],
                ),
            ),
        )

    def confirmar_eliminar(self, local):
        """Abre una ventanita que pregunta antes de borrar."""
        dialogo = ft.AlertDialog(
            title=ft.Text("Eliminar local"),
            content=ft.Text(f"¿Seguro que quieres eliminar «{local.nombre}»?"),
            actions=[
                # "Cancelar" solo cierra la ventanita.
                ft.TextButton("Cancelar", on_click=lambda evento: self.app.page.pop_dialog()),
                # "Eliminar" borra de verdad.
                ft.FilledButton("Eliminar", on_click=lambda evento: self.eliminar(local)),
            ],
        )
        # Mostramos la ventanita encima de la pantalla.
        self.app.page.show_dialog(dialogo)

    def eliminar(self, local):
        """Borra el local y vuelve a dibujar la lista."""
        # Cerramos la ventanita de confirmación.
        self.app.page.pop_dialog()
        # Pedimos al controlador que lo borre (él comprueba el permiso).
        self.controller.eliminar(self.usuario, local.codigo)
        # Volvemos a cargar esta pantalla para que desaparezca de la lista.
        self.app.ir_a_locales()

    def construir(self):
        """Monta y devuelve la pantalla completa."""
        # Botones de arriba: "Volver" siempre; "Nuevo local" solo si tiene permiso.
        barra = [ft.OutlinedButton("Volver", icon=ft.Icons.ARROW_BACK, on_click=self.app.ir_a_principal)]
        if self.controller.puede_crear(self.usuario):
            barra.append(
                ft.FilledButton("Nuevo local", icon=ft.Icons.ADD, on_click=self.app.ir_a_nuevo_local)
            )

        # Creamos una tarjeta por cada local guardado.
        tarjetas = []
        for local in self.controller.listar():
            tarjetas.append(self.tarjeta(local))

        # Si no hay ninguno, lo decimos con un texto.
        if not tarjetas:
            contenido = ft.Text("Todavía no hay locales registrados.")
        # Si hay, los colocamos en una fila adaptable.
        else:
            contenido = ft.ResponsiveRow(controls=tarjetas)

        return ft.Column(
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Row(controls=barra),
                ft.Text("Locales de la zona", size=24, weight=ft.FontWeight.BOLD),
                contenido,
            ],
        )
