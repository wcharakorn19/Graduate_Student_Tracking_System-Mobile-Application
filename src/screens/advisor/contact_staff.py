# src/screens/advisor/contact_staff.py
import logging
import flet as ft
from components.shared_navbar import SharedNavBar
from core.auth_guard import require_auth
from core.config import APP_COLORS

logger = logging.getLogger(__name__)

# ข้อมูลเจ้าหน้าที่ (Mock Data — สามารถเปลี่ยนเป็นเรียก API ภายหลัง)
STAFF_LIST = [
    {
        "name": "นางสาว อรปรียา",
        "position": "เจ้าหน้าห้องภาควิชาการ",
        "phone": "0812345678",
        "email": "orapreya@example.ac.th",
        "line": "https://line.me/ti/p/orapreya_line",
    },
    {
        "name": "นางสาว อรปรียา",
        "position": "เจ้าหน้าห้องภาควิชาการ",
        "phone": "0812345679",
        "email": "orapreya2@example.ac.th",
        "line": "https://line.me/ti/p/orapreya2_line",
    },
    {
        "name": "นางสาว อรปรียา",
        "position": "เจ้าหน้าห้องภาควิชาการ",
        "phone": "0812345680",
        "email": "orapreya3@example.ac.th",
        "line": "https://line.me/ti/p/orapreya3_line",
    },
]


def _action_button(icon, label, bgcolor, text_color="white"):
    """สร้างปุ่ม action พร้อมไอคอน (phone / email / Line)"""
    return ft.Container(
        content=ft.Row(
            [
                ft.Icon(icon, size=16, color=text_color),
                ft.Text(label, size=12, color=text_color, weight=ft.FontWeight.W_500),
            ],
            spacing=4,
            tight=True,
        ),
        bgcolor=bgcolor,
        padding=ft.padding.symmetric(horizontal=14, vertical=8),
        border_radius=20,
    )


def _staff_card(staff, page):
    """สร้างการ์ดเจ้าหน้าที่แต่ละคน"""
    return ft.Container(
        content=ft.Column(
            [
                # ชื่อ + ไอคอนโปรไฟล์
                ft.Row(
                    [
                        ft.Icon(
                            ft.Icons.ACCOUNT_CIRCLE_OUTLINED,
                            color=APP_COLORS["primary"],
                            size=40,
                        ),
                        ft.Column(
                            [
                                ft.Text(
                                    staff["name"],
                                    size=14,
                                    weight=ft.FontWeight.BOLD,
                                    color="black",
                                ),
                                ft.Text(
                                    staff["position"],
                                    size=12,
                                    color="black54",
                                ),
                            ],
                            spacing=2,
                            expand=True,
                        ),
                    ],
                    spacing=10,
                ),
                ft.Container(height=6),
                # ปุ่ม phone / email / Line
                ft.Row(
                    [
                        ft.GestureDetector(
                            content=_action_button(
                                ft.Icons.MAIL_OUTLINE, "email", "#9E9E9E", "black87"
                            ),
                            on_tap=lambda e, em=staff["email"]: page.launch_url(
                                f"mailto:{em}"
                            ),
                        ),
                        ft.GestureDetector(
                            content=_action_button(
                                ft.Icons.PLAY_ARROW, "Line", "#4CAF50"
                            ),
                            on_tap=lambda e, ln=staff["line"]: page.launch_url(ln),
                        ),
                    ],
                    spacing=10,
                ),
            ],
            spacing=2,
        ),
        bgcolor="white",
        padding=ft.padding.symmetric(horizontal=20, vertical=16),
        border_radius=12,
        shadow=ft.BoxShadow(
            blur_radius=8,
            color="black08",
            offset=ft.Offset(0, 2),
        ),
    )


def ContactStaffScreen(page: ft.Page):
    # Auth guard
    user_id = require_auth(page)
    if not user_id:
        return ft.View(
            route="/contact_staff",
            controls=[ft.Text("Redirecting to login...")],
        )

    staff_count = len(STAFF_LIST)

    # Header: icon + title + count
    header = ft.Row(
        [
            ft.Icon(
                ft.Icons.ACCOUNT_CIRCLE_OUTLINED,
                color=APP_COLORS["primary"],
                size=45,
            ),
            ft.Column(
                [
                    ft.Text(
                        "ติดต่อเจ้าหน้าที่",
                        size=22,
                        weight=ft.FontWeight.BOLD,
                        color="black",
                    ),
                    ft.Text(
                        f"{staff_count} คน",
                        size=14,
                        color="black54",
                    ),
                ],
                spacing=0,
            ),
        ],
        spacing=12,
    )

    # Staff list
    staff_cards = ft.Column(
        [_staff_card(s, page) for s in STAFF_LIST],
        spacing=15,
        scroll=ft.ScrollMode.AUTO,
    )

    return ft.View(
        route="/contact_staff",
        bgcolor=APP_COLORS["background"],
        padding=0,
        controls=[
            ft.Container(
                content=ft.Column(
                    [
                        header,
                        ft.Container(height=10),
                        staff_cards,
                    ],
                    expand=True,
                ),
                padding=ft.padding.only(left=20, right=20, top=60),
                expand=True,
            )
        ],
        bottom_appbar=SharedNavBar(page, current_route="/contact_staff"),
    )
