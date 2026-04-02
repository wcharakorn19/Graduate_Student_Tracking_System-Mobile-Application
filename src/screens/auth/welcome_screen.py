# ==============================================================================
# src/screens/auth/welcome_screen.py — หน้าจอต้อนรับ (Welcome Screen)
# ==============================================================================
# หน้าจอแรกที่ผู้ใช้จะเห็นเมื่อเปิดแอป
# แสดงโลโก้ KMITL + ปุ่ม "WELCOME" + ชื่อระบบ
# เมื่อกดปุ่ม WELCOME จะนำทางไปหน้า Login
#
# Route: "/"
# ==============================================================================
import flet as ft

from components.buttons import PrimaryButton    # ใช้ปุ่มหลักของแอป


def WelcomeScreen(page: ft.Page):
    """
    สร้างหน้าจอ Welcome Screen
    ประกอบด้วย 3 ส่วน: โลโก้, ปุ่ม WELCOME, ข้อความชื่อระบบ
    """
    # ── ส่วนที่ 1: โลโก้ SIET KMITL ──
    text_logo = ft.Image(src="/kmitl_logo.png")

    # ── ส่วนที่ 2: ปุ่ม WELCOME ──
    # เมื่อกด → นำทางไปหน้า Login (/login)
    welcome_btn = ft.Container(
        content=PrimaryButton(
            text="WELCOME",
            on_click=lambda _: page.go("/login"),
            weight=ft.FontWeight.BOLD,
            padding=ft.padding.symmetric(
                horizontal=30, vertical=30
            ),  # ปรับระยะตัวอักษรกับขอบปุ่ม
        ),
        margin=ft.margin.only(top=70, bottom=120),  # ปรับระยะปุ่ม WELCOME
    )

    # ── ส่วนที่ 3: ข้อความชื่อระบบ ──
    welcome_txt = ft.Container(
        content=ft.Text("Graduate Student Tracking System", color="#EF3961", size=18),
        margin=ft.margin.only(bottom=50),  # ปรับระยะข้อความ
    )

    # ── คืนค่า View — จัดตำแหน่ง: ชิดด้านล่าง, กลางแนวนอน ──
    return ft.View(
        route="/",
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.END,
        bgcolor="#FFFFFF",
        controls=[text_logo, welcome_btn, welcome_txt],
    )
