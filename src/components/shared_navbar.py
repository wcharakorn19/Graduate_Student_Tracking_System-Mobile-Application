# src/components/shared_navbar.py
import logging
import flet as ft
from core.config import APP_COLORS

logger = logging.getLogger(__name__)


def SharedNavBar(page: ft.Page, current_route: str):
    # 🌟 1. ดึง Role เพื่อกำหนดเส้นทางที่ถูกต้อง
    user_role = page.session.get("user_role")

    if user_role == "advisor":
        home_route = "/advisor_home"
        left_route = "/advisor_activities"
    else:
        home_route = "/student_home"
        left_route = "/profile"

    is_home = current_route == home_route
    is_left_active = current_route == left_route

    # 🌟 2. กำหนด icon ซ้ายตาม Role
    if user_role == "advisor":
        # Advisor: ใช้ folder icon
        left_icon = ft.Icons.FOLDER if is_left_active else ft.Icons.FOLDER_OUTLINED
    else:
        # Student: ใช้ person icon
        left_icon = ft.Icons.PERSON if is_left_active else ft.Icons.PERSON_OUTLINE

    chat_route = "/contact_staff"
    is_chat_active = current_route == chat_route

    return ft.BottomAppBar(
        bgcolor=APP_COLORS["background"],
        content=ft.Row(
            controls=[
                ft.IconButton(
                    icon=left_icon,
                    icon_color=APP_COLORS["primary"],
                    icon_size=30,
                    on_click=lambda _: page.go(left_route),
                ),
                ft.IconButton(
                    icon=ft.Icons.HOME if is_home else ft.Icons.HOME_OUTLINED,
                    icon_color=APP_COLORS["primary"],
                    icon_size=30,
                    on_click=lambda _: page.go(home_route),
                ),
                ft.IconButton(
                    icon=ft.Icons.CHAT_BUBBLE if is_chat_active else ft.Icons.CHAT_BUBBLE_OUTLINE,
                    icon_color=APP_COLORS["primary"],
                    icon_size=30,
                    on_click=lambda _: page.go(chat_route),
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
        ),
    )
