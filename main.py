"""Punto de entrada de la aplicación. Para ejecutarla: python main.py"""
import flet as ft

# AppSensores es la App de siempre más los sensores, las alertas y los cierres
# (ver src/app_sensores.py).
from src.app_sensores import AppSensores


def main(page):
    AppSensores(page).ir_a_login()


ft.run(main)
