# src/screens/advisor/advisor_activities.py
import logging
import flet as ft
from controllers.advisor_controller import AdvisorController
from components.shared_navbar import SharedNavBar
from components.error_banner import ErrorBanner
from core.auth_guard import require_auth
from core.config import APP_COLORS

logger = logging.getLogger(__name__)


def AdvisorActivities(page: ft.Page):
    controller = AdvisorController()

    # 1. ดึงข้อมูลจาก Session
    user_id = require_auth(page)
    if not user_id:
        return ft.View(
            route="/advisor_activities",
            controls=[ft.Text("Redirecting to login...")],
        )

    # --- 2. เตรียม UI Components ---
    activities_list = ft.Column(spacing=15, scroll=ft.ScrollMode.AUTO)
    error_container = ft.Column(spacing=0)

    # --- 3. ฟังก์ชันโหลดข้อมูลแบบ Async ---
    async def load_data(e=None):
        error_container.controls.clear()

        # แสดง Spinner ระหว่างโหลด
        activities_list.controls.clear()
        activities_list.controls.append(
            ft.Container(
                content=ft.ProgressRing(), alignment=ft.alignment.center, padding=20
            )
        )
        page.update()

        result = await controller.get_dashboard_data(user_id)

        raw_data = result.get("data")
        error = result.get("message") if not result.get("success") else None

        if not error and raw_data:
            activities_list.controls.clear()
            for act in raw_data.activities:
                form_type = act.form_type
                sub_id = act.submission_id
                target_route = f"/{form_type}/{sub_id}"

                activities_list.controls.append(
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Icon(
                                    ft.Icons.FOLDER_OUTLINED,
                                    color="black54",
                                    size=28,
                                ),
                                ft.Column(
                                    [
                                        ft.Text(
                                            act.title,
                                            size=14,
                                            color="black",
                                            weight=ft.FontWeight.BOLD,
                                        ),
                                        ft.Text(
                                            f"Name : {act.name}",
                                            size=13,
                                            color="black87",
                                        ),
                                        ft.Text(
                                            f"Status : {act.status}",
                                            size=13,
                                            color="black87",
                                        ),
                                    ],
                                    spacing=2,
                                    expand=True,
                                ),
                            ],
                            spacing=14,
                        ),
                        bgcolor="white",
                        padding=ft.padding.symmetric(horizontal=18, vertical=14),
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
            activities_list.controls.clear()
            error_container.controls.append(
                ErrorBanner(f"เกิดข้อผิดพลาดในการโหลดข้อมูล: {error}")
            )
            page.update()

    # รันฟังก์ชันโหลดข้อมูลแบบไม่บล็อก UI
    page.run_task(load_data)

    # --- 4. ประกอบร่าง Layout ---
    return ft.View(
        route="/advisor_activities",
        bgcolor=APP_COLORS["background"],
        padding=0,
        controls=[
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            "Lastest Activities",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            color="black",
                        ),
                        error_container,
                        ft.Container(height=5),
                        activities_list,
                    ],
                    expand=True,
                ),
                padding=ft.padding.only(left=20, right=20, top=60),
                expand=True,
            )
        ],
        bottom_appbar=SharedNavBar(page, current_route="/advisor_activities"),
    )
