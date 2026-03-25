# src/screens/advisor/advisor_home.py
import logging
import flet as ft
from controllers.advisor_controller import AdvisorController
from components.shared_navbar import SharedNavBar
from components.base_card import BaseCard
from components.error_banner import ErrorBanner
from core.auth_guard import require_auth

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
    student_list_column = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO)
    activities_list = ft.Column(spacing=15, scroll=ft.ScrollMode.AUTO)
    student_count_text = ft.Text(
        "นักศึกษาในความดูแล (กำลังโหลด...)",
        size=16,
        weight=ft.FontWeight.BOLD,
        color="black",
    )
    error_container = ft.Column(spacing=0)

    # --- 3. ฟังก์ชันโหลดข้อมูลแบบ Async (เหมือน student_home) ---
    async def load_data(e=None):
        error_container.controls.clear()

        # แสดง Spinner ระหว่างโหลด (ทั้งรอบแรกและ refresh)
        activities_list.controls.clear()
        activities_list.controls.append(
            ft.Container(
                content=ft.ProgressRing(), alignment=ft.alignment.center, padding=20
            )
        )
        page.update()

        # 🌟 เรียกแบบ Async
        result = await controller.get_dashboard_data(user_id)

        raw_data = result.get("data")
        error = result.get("message") if not result.get("success") else None

        if not error and raw_data:
            # 1. อัปเดตจำนวนนักศึกษา
            student_count_text.value = f"นักศึกษาในความดูแล ({raw_data.student_count} คน)"

            # 2. วาดรายชื่อนักศึกษา
            student_list_column.controls.clear()
            for student in raw_data.students:
                student_list_column.controls.append(
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Icon(ft.Icons.ACCOUNT_CIRCLE, color="#EF3961", size=35),
                                ft.Column(
                                    [
                                        ft.Text(
                                            student.name,
                                            size=16,
                                            weight=ft.FontWeight.BOLD,
                                            color="black",
                                        ),
                                        ft.Text(
                                            student.doc_status,
                                            size=12,
                                            color="black54",
                                        ),
                                    ],
                                    spacing=0,
                                    expand=True,
                                ),
                            ]
                        ),
                        padding=ft.padding.only(bottom=10),
                        border=ft.border.only(bottom=ft.border.BorderSide(1, "#F0F0F0")),
                    )
                )

            # 3. วาดกิจกรรมล่าสุด
            activities_list.controls.clear()
            for act in raw_data.activities:
                form_type = act.form_type
                sub_id = act.submission_id
                target_route = f"/{form_type}/{sub_id}"

                activities_list.controls.append(
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Container(
                                    content=ft.Icon(
                                        ft.Icons.FOLDER_OUTLINED, color="black54", size=24
                                    ),
                                    bgcolor="#F5F5F5",
                                    padding=12,
                                    border_radius=10,
                                ),
                                ft.Column(
                                    [
                                        ft.Text(
                                            act.title,
                                            size=16,
                                            color="black",
                                            weight=ft.FontWeight.BOLD,
                                        ),
                                        ft.Text(
                                            f"Name: {act.name}",
                                            size=14,
                                            color="black",
                                        ),
                                        ft.Text(
                                            f"Status: {act.status}",
                                            size=14,
                                            color="#EF3961",
                                        ),
                                    ],
                                    spacing=2,
                                    expand=True,
                                ),
                            ]
                        ),
                        bgcolor="white",
                        padding=15,
                        border_radius=10,
                        border=ft.border.all(1, "#E5E5E5"),
                        on_click=lambda e, route=target_route: page.go(route),
                    )
                )

            page.update()
        else:
            # กรณี Error
            activities_list.controls.clear()
            error_container.controls.append(
                ErrorBanner(f"เกิดข้อผิดพลาดในการโหลดข้อมูล: {error}")
            )
            page.update()

    # --- 4. ประกอบร่าง Layout ---
    students_card = BaseCard(
        content=ft.Column(
            [
                student_count_text,
                ft.Container(height=5),
                ft.Container(content=student_list_column, height=220),
            ]
        )
    )

    activities_card = BaseCard(
        content=activities_list,
        expand=True,
    )

    # รันฟังก์ชันโหลดข้อมูลแบบไม่บล็อก UI
    page.run_task(load_data)

    return ft.View(
        route="/advisor_home",
        bgcolor="#FFF6FE",
        padding=0,
        controls=[
            ft.Container(
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                name_text,
                                ft.IconButton(
                                    icon=ft.Icons.REFRESH_ROUNDED,
                                    icon_color="#EF3961",
                                    icon_size=24,
                                    tooltip="รีเฟรชข้อมูล",
                                    on_click=lambda _: page.run_task(load_data),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        error_container,
                        students_card,
                        ft.Text(
                            "Tasks & Activities",
                            size=22,
                            weight=ft.FontWeight.BOLD,
                            color="black",
                        ),
                        activities_card,
                    ],
                    expand=True,
                ),
                padding=ft.padding.only(left=20, right=20, top=60),
                expand=True,
            )
        ],
        bottom_appbar=SharedNavBar(page, current_route="/advisor_home"),
    )
