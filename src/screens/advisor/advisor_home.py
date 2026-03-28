# src/screens/advisor/advisor_home.py
import logging
import flet as ft
from controllers.advisor_controller import AdvisorController
from components.shared_navbar import SharedNavBar
from components.base_card import BaseCard
from components.error_banner import ErrorBanner
from core.auth_guard import require_auth
from core.config import APP_COLORS

logger = logging.getLogger(__name__)


def AdvisorHome(page: ft.Page):
    controller = AdvisorController()

    # 1. ดึงข้อมูลจาก Session
    user_id = require_auth(page)
    if not user_id:
        return ft.View(
            route="/advisor_home", controls=[ft.Text("Redirecting to login...")]
        )

    user_full_name = page.session.get("user_full_name") or "อาจารย์ที่ปรึกษา"
    logger.debug(f"โหลดหน้า Home -> user_id = {user_id}, name = {user_full_name}")

    # --- 2. เตรียม UI Components (State) ---
    name_text = ft.Text(
        user_full_name, size=24, weight=ft.FontWeight.BOLD, color="black"
    )
    student_list_column = ft.Column(spacing=12, scroll=ft.ScrollMode.AUTO)
    student_count_text = ft.Text(
        "นักศึกษาในความดูแล (กำลังโหลด...)",
        size=16,
        weight=ft.FontWeight.BOLD,
        color="black",
    )
    error_container = ft.Column(spacing=0)

    # --- 3. ฟังก์ชันโหลดข้อมูลแบบ Async ---
    async def load_data(e=None):
        error_container.controls.clear()

        # แสดง Spinner ระหว่างโหลด
        student_list_column.controls.clear()
        student_list_column.controls.append(
            ft.Container(
                content=ft.ProgressRing(), alignment=ft.alignment.center, padding=20
            )
        )
        page.update()

        # เรียกแบบ Async
        result = await controller.get_dashboard_data(user_id)

        raw_data = result.get("data")
        error = result.get("message") if not result.get("success") else None

        if not error and raw_data:
            # 1. อัปเดตจำนวนนักศึกษา
            student_count_text.value = (
                f"นักศึกษาในความดูแล {raw_data.student_count} คน"
            )

            # 2. วาดรายชื่อนักศึกษา — แต่ละคนเป็นการ์ดแยก
            student_list_column.controls.clear()
            for student in raw_data.students:
                target_route = f"/student_profile/{student.student_id}"
                student_list_column.controls.append(
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Icon(
                                    ft.Icons.ACCOUNT_CIRCLE_OUTLINED,
                                    color=APP_COLORS["primary"],
                                    size=40,
                                ),
                                ft.Column(
                                    [
                                        ft.Text(
                                            student.name,
                                            size=14,
                                            weight=ft.FontWeight.BOLD,
                                            color="black",
                                        ),
                                        ft.Text(
                                            f"ตำแหน่ง : {student.doc_status}",
                                            size=12,
                                            color="black54",
                                        ),
                                    ],
                                    spacing=2,
                                    expand=True,
                                ),
                            ],
                            spacing=12,
                        ),
                        bgcolor="white",
                        padding=ft.padding.symmetric(horizontal=16, vertical=12),
                        border_radius=12,
                        shadow=ft.BoxShadow(
                            blur_radius=8,
                            color="black08",
                            offset=ft.Offset(0, 2),
                        ),
                        on_click=lambda e, route=target_route: page.go(route),
                    )
                )

            page.update()
        else:
            # กรณี Error
            student_list_column.controls.clear()
            error_container.controls.append(
                ErrorBanner(f"เกิดข้อผิดพลาดในการโหลดข้อมูล: {error}")
            )
            page.update()

    # --- 4. ประกอบร่าง Layout ---
    students_card = BaseCard(
        content=ft.Column(
            [
                student_count_text,
                ft.Container(height=8),
                student_list_column,
            ]
        )
    )

    # รันฟังก์ชันโหลดข้อมูลแบบไม่บล็อก UI
    page.run_task(load_data)

    return ft.View(
        route="/advisor_home",
        bgcolor=APP_COLORS["background"],
        padding=0,
        controls=[
            ft.Container(
                content=ft.Column(
                    [
                        # Header: ชื่อ + ไอคอนโปรไฟล์
                        ft.Row(
                            [
                                name_text,
                                ft.IconButton(
                                    icon=ft.Icons.ACCOUNT_CIRCLE_OUTLINED,
                                    icon_color=APP_COLORS["primary"],
                                    icon_size=30,
                                    tooltip="โปรไฟล์",
                                    on_click=lambda _: page.go("/profile"),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        error_container,
                        students_card,
                    ],
                    expand=True,
                ),
                padding=ft.padding.only(left=20, right=20, top=60),
                expand=True,
            )
        ],
        bottom_appbar=SharedNavBar(page, current_route="/advisor_home"),
    )
