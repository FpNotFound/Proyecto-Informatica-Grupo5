"""Punto de entrada de la aplicación "Bajos de Argüelles".

Sistema de Monitorización Ambiental — Sprint 1 (estructura base y
autenticación). Arranca la interfaz gráfica construida con Flet siguiendo el
patrón Modelo-Vista-Controlador.

Ejecución:
    python main.py
"""
from __future__ import annotations

import flet as ft

from src.app import App


def main(page: ft.Page) -> None:
    App(page).iniciar()


if __name__ == "__main__":
    ft.run(main)
