"""VISTA: piezas pequeñas que se repiten en varias pantallas de sensores.

    icono_semaforo(color)   -> circulito verde, amarillo o rojo con el estado del bar
    etiqueta_cerrado()      -> cartel negro "CERRADO TEMPORALMENTE"
    led(color, encendido)   -> un diodo LED (encendido = color vivo; apagado = gris)
    ventana_texto(...)      -> ventanita con una caja para escribir (motivo, reclamación...)
"""
# Flet es la librería que dibuja la interfaz gráfica.
import flet as ft

# Color de Flet para cada color del semáforo.
COLOR_FLET = {"verde": ft.Colors.GREEN, "amarillo": ft.Colors.AMBER, "rojo": ft.Colors.RED}

# Qué significa cada color del semáforo.
SIGNIFICADO = {"verde": "Todo correcto", "amarillo": "Precaución", "rojo": "Nivel peligroso"}

# Color de Flet para cada LED.
COLOR_LED = {"rojo": ft.Colors.RED, "azul": ft.Colors.BLUE, "verde": ft.Colors.GREEN}


def icono_semaforo(color, tamano=28):
    """Circulito del color del estado del bar. Al pasar el ratón explica qué significa."""
    return ft.Icon(ft.Icons.CIRCLE, color=COLOR_FLET[color], size=tamano, tooltip=SIGNIFICADO[color])


def etiqueta_cerrado():
    """Cartel que se pone en los bares cerrados por la policía."""
    return ft.Container(
        bgcolor=ft.Colors.BLACK,
        padding=6,
        border_radius=6,
        content=ft.Row(
            tight=True,
            controls=[
                ft.Icon(ft.Icons.LOCK, color=ft.Colors.WHITE, size=16),
                ft.Text("CERRADO TEMPORALMENTE", color=ft.Colors.WHITE, size=12, weight=ft.FontWeight.BOLD),
            ],
        ),
    )


def led(color, encendido, tamano=30):
    """Un diodo LED redondo."""
    if encendido:
        relleno = COLOR_LED[color]
        # La sombra del mismo color hace que parezca que brilla.
        brillo = ft.BoxShadow(blur_radius=14, spread_radius=1, color=COLOR_LED[color])
    else:
        relleno = ft.Colors.GREY_300
        brillo = None
    return ft.Container(
        width=tamano,
        height=tamano,
        border_radius=tamano / 2,
        bgcolor=relleno,
        shadow=brillo,
        border=ft.Border.all(2, COLOR_LED[color]),
    )


def ventana_texto(app, titulo, explicacion, texto_boton, al_aceptar):
    """Abre una ventanita para escribir un texto (motivo de cierre, reclamación...).

    "al_aceptar" es una función que recibe lo escrito y devuelve "" si todo ha
    ido bien, o un mensaje de error. Si hay error, se muestra y la ventana sigue abierta.
    Si va bien, la ventana se cierra y la pantalla se vuelve a dibujar.
    """
    caja = ft.TextField(label="Escribe aquí", multiline=True, min_lines=3, max_lines=6)
    texto_error = ft.Text(color=ft.Colors.RED)

    # Esta función se ejecuta al pulsar el botón principal de la ventana.
    def aceptar(evento):
        error = al_aceptar(caja.value or "")
        if error:
            texto_error.value = error
            app.page.update()
        else:
            app.page.pop_dialog()
            app.recargar()

    dialogo = ft.AlertDialog(
        title=ft.Text(titulo),
        content=ft.Column(tight=True, width=420, controls=[ft.Text(explicacion), caja, texto_error]),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda evento: app.page.pop_dialog()),
            ft.FilledButton(texto_boton, on_click=aceptar),
        ],
    )
    app.page.show_dialog(dialogo)
