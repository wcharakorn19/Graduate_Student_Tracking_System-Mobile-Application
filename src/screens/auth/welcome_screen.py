import flet as ft

from components.buttons import PrimaryButton

def WelcomeScreen(page: ft.Page):
    # SIET KMITL LOGO
    text_logo = ft.Image(src="kmitl_logo.png")
    # WELCOME button
    welcome_btn = ft.Container(
        content=PrimaryButton(
            text="WELCOME", 
            on_click=lambda _: page.go("/login"), 
            weight=ft.FontWeight.BOLD,
            padding=ft.padding.symmetric(horizontal=30, vertical=30) # ปรับระยะตัวอักษรกับขอบปุ่ม
        ),
        margin=ft.margin.only(top=70, bottom=120) # ปรับระยะปุ่ม WELCOME
    )

    welcome_txt = ft.Container(
        content=ft.Text("Graduate Student Tracking System", color="#EF3961", size=18),
        margin=ft.margin.only(bottom=50) # ปรับระยะข้อความ Graduate
    )

    return ft.View(
        route="/",
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.END,
        bgcolor="#FFFFFF",
        controls=[
            text_logo,
            welcome_btn,
            welcome_txt
        ]
    )
