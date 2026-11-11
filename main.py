"""Punto de entrada de la aplicación. Para ejecutarla: python main.py"""
import flet as ft

from src.app import App


def main(page):
    App(page).ir_a_login()


ft.run(main)
