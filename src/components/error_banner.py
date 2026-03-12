# src/components/error_banner.py
import flet as ft


class ErrorBanner(ft.Container):
    def __init__(self, message: str):
        super().__init__()
        self.bgcolor = ft.Colors.RED_50
        self.padding = 15
        self.border_radius = 10
        self.border = ft.border.all(1, ft.Colors.RED_200)
        self.margin = ft.margin.only(bottom=15)

        self.content = ft.Row(
            controls=[
                ft.Icon(ft.Icons.ERROR_OUTLINE, color=ft.Colors.RED_700, size=24),
                ft.Text(
                    message,
                    color=ft.Colors.RED_900,
                    weight=ft.FontWeight.W_500,
                    size=14,
                    expand=True,
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
