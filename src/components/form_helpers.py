# src/components/form_helpers.py
import flet as ft
from core.config import APP_COLORS


def form_text_value(initial: str = "-") -> ft.Text:
    """สร้าง Text widget สำหรับแสดงค่าในฟอร์ม"""
    return ft.Text(initial, size=14, color=APP_COLORS["text_dark"])


def create_form_row(label: str, value_control: ft.Control, label_width: int = 140):
    """สร้างแถวข้อมูลแบบ label-value สำหรับ Form Detail Screen"""
    return ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.START,
        controls=[
            ft.Container(
                width=label_width,
                content=ft.Text(label, size=14, color=APP_COLORS["text_muted"]),
            ),
            ft.Container(expand=True, content=value_control),
        ],
    )


def FormDetailCard(content: ft.Control):
    """การ์ดมาตรฐานสำหรับ Form Detail Screen — ใช้แทน inline Container ที่ซ้ำกัน"""
    return ft.Container(
        bgcolor=APP_COLORS["white"],
        border_radius=20,
        padding=25,
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=15,
            color=APP_COLORS["card_shadow"],
            offset=ft.Offset(0, 4),
        ),
        content=content,
    )


def FormDetailAppBar(page: ft.Page, user_role: str):
    """AppBar มาตรฐานสำหรับ Form Detail Screen — ปุ่มย้อนกลับตาม Role"""
    return ft.AppBar(
        leading=ft.IconButton(
            icon=ft.Icons.ARROW_BACK,
            icon_color=APP_COLORS["black"],
            on_click=lambda _: page.go(
                "/advisor_home" if user_role == "advisor" else "/student_home"
            ),
        ),
        title=ft.Text("KMITL", color=APP_COLORS["black"], weight="bold"),
        center_title=True,
        bgcolor=APP_COLORS["form_background"],
        elevation=0,
    )
