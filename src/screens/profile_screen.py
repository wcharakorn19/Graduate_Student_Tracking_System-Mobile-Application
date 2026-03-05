import flet as ft

def ProfileScreen(page: ft.Page):


    return ft.View(
        route="/profile",
        controls=[
            ft.Text("Hello Profile")
        ]
    )