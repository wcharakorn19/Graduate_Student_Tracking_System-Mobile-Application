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
        profile_route = "/profile"
    else:
        home_route = "/student_home"
        profile_route = "/profile"

    is_home = current_route == home_route
    is_profile = current_route == profile_route

    return ft.BottomAppBar(
        bgcolor=APP_COLORS["background"],
        content=ft.Row(
            controls=[
                ft.IconButton(
                    icon=ft.Icons.PERSON if is_profile else ft.Icons.PERSON_OUTLINE,
                    icon_color=APP_COLORS["primary"],
                    icon_size=30,
                    on_click=lambda _: page.go(profile_route),
                ),
                ft.IconButton(
                    icon=ft.Icons.HOME if is_home else ft.Icons.HOME_OUTLINED,
                    icon_color=APP_COLORS["primary"],
                    icon_size=30,
                    on_click=lambda _: page.go(home_route),
                ),
                ft.IconButton(
                    icon=ft.Icons.CHAT_BUBBLE_OUTLINE,
                    icon_color=APP_COLORS["primary"],
                    icon_size=30,
                    on_click=lambda _: logger.info("Chat feature coming soon!"),
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
        ),
    )
