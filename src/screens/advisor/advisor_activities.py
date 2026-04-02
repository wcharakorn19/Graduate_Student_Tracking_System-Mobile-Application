# ==============================================================================
# src/screens/advisor/advisor_activities.py — หน้ารายการนักศึกษาในความดูแล
# ==============================================================================
# หน้าจอนี้แสดงรายชื่อนักศึกษาที่อาจารย์ที่ปรึกษาดูแล
# ตามแท็บแรก (แท็บนักศึกษา)
# แต่ละรายการแสดง: ชื่อนักศึกษา, สถานะ/ตำแหน่ง
# กดเข้าแต่ละรายการ → ไปหน้าโปรไฟล์นักศึกษา
#
# ข้อมูลโหลดแบบ Async ผ่าน AdvisorController
# Route: "/advisor_activities"
# ==============================================================================
import logging
import flet as ft
from controllers.advisor_controller import AdvisorController
from components.shared_navbar import SharedNavBar
from components.base_card import BaseCard
from components.error_banner import ErrorBanner
from core.auth_guard import require_auth
from core.config import APP_COLORS
from models.document_model import StudentSummaryModel

logger = logging.getLogger(__name__)


def create_student_card(student: StudentSummaryModel, page: ft.Page):
    """สร้างการ์ดรายชื่อนักศึกษาย่อย ๆ"""
    target_route = f"/student_profile/{student.student_id}"

    return ft.Container(
        content=ft.Row(
            [
                # ไอคอนโปรไฟล์สีชมพู (primary)
                ft.Icon(
                    ft.Icons.ACCOUNT_CIRCLE_OUTLINED,
                    color=APP_COLORS["primary"],
                    size=36,
                ),
                # ข้อมูลนักศึกษา
                ft.Column(
                    [
                        ft.Text(
                            student.name,
                            size=14,
                            color="black",
                            weight=ft.FontWeight.W_500,
                        ),
                        ft.Text(
                            f"ตำแหน่ง : {student.doc_status}",
                            size=12,
                            color="black",
                            weight=ft.FontWeight.W_500,
                        ),
                    ],
                    spacing=2,
                    expand=True,
                ),
            ],
            spacing=16,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor="#F8F8F8", # พื้นหลังสีเทาอ่อนเล็กน้อยตามแบบร่าง หรือใช้ "white" หากต้องการสีขาวล้วน
        padding=ft.padding.symmetric(horizontal=16, vertical=16),
        border_radius=16,
        shadow=ft.BoxShadow(
            blur_radius=6,
            color="black08",
            offset=ft.Offset(0, 2),
        ),
        margin=ft.margin.only(bottom=16),
        # กดที่รายการ → ไปหน้าโปรไฟล์นักศึกษา
        on_click=lambda e: page.go(target_route) if student.student_id else None,
    )


def AdvisorActivities(page: ft.Page):
    """สร้างหน้าจอนักศึกษาในความดูแล"""
    controller = AdvisorController()

    # ── Auth Guard ──
    user_id = require_auth(page)
    if not user_id:
        return ft.View(
            route="/advisor_activities",
            controls=[ft.Text("Redirecting to login...")],
        )

    # ── ดึงชื่ออาจารย์ ──
    user_full_name = page.session.get("user_full_name") or "อาจารย์ที่ปรึกษา"

    # ── เตรียม UI Components ──
    student_count_text = ft.Text(
        "นักศึกษาในความดูแล (กำลังโหลด...)",
        size=16,
        weight=ft.FontWeight.BOLD,
        color="black",
    )
    students_list_column = ft.Column(spacing=0)
    error_container = ft.Column(spacing=0)

    # ── ฟังก์ชันโหลดข้อมูลแบบ Async ──
    async def load_data(e=None):
        """โหลดรายชื่อนักศึกษาจาก API"""
        error_container.controls.clear()

        # แสดง Spinner ระหว่างโหลด
        students_list_column.controls.clear()
        students_list_column.controls.append(
            ft.Container(
                content=ft.ProgressRing(), alignment=ft.alignment.center, padding=20
            )
        )
        page.update()

        # เรียก Controller แบบ Async
        result = await controller.get_dashboard_data(user_id)

        raw_data = result.get("data")
        error = result.get("message") if not result.get("success") else None

        if not error and raw_data:
            # อัปเดตจำนวนนักศึกษา
            student_count_text.value = f"นักศึกษาในความดูแล {raw_data.student_count} คน"

            # สร้างรายการการ์ดนักศึกษา
            students_list_column.controls.clear()
            for student in raw_data.students:
                students_list_column.controls.append(create_student_card(student, page))

            page.update()
        else:
            # กรณี Error
            students_list_column.controls.clear()
            student_count_text.value = "ไม่สามารถโหลดข้อมูลได้"
            error_container.controls.append(
                ErrorBanner(f"เกิดข้อผิดพลาดในการโหลดข้อมูล: {error}")
            )
            page.update()

    # รันฟังก์ชันโหลดข้อมูลแบบไม่บล็อก UI
    page.run_task(load_data)

    # โครงสร้างเนื้อหาหลัก (การ์ดใหญ่)
    main_card = BaseCard(
        content=ft.Column(
            [
                student_count_text,
                ft.Container(height=12),
                students_list_column,
            ]
        ),
        padding=24, # เพิ่ม padding ให้เหมือนการ์ดใหญ่ตามแบบ
    )
    
    # ── ประกอบร่าง Layout ──
    return ft.View(
        route="/advisor_activities",
        bgcolor=APP_COLORS["background"],
        padding=0,
        controls=[
            ft.Container(
                content=ft.Column(
                    [
                        # Header
                        ft.Row(
                            [
                                ft.Text(
                                    user_full_name,
                                    size=20,
                                    weight=ft.FontWeight.BOLD,
                                    color="black",
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.ACCOUNT_CIRCLE_OUTLINED,
                                    icon_color=APP_COLORS["primary"],
                                    icon_size=28,
                                    tooltip="โปรไฟล์",
                                    on_click=lambda _: page.go("/profile"),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        error_container,
                        # เลื่อนเนื้อหาการ์ดหลัก
                        ft.Container(
                            content=ft.Column(
                                [main_card],
                                scroll=ft.ScrollMode.AUTO,
                            ),
                            expand=True,
                        ),
                    ],
                    expand=True,
                ),
                padding=ft.padding.only(left=20, right=20, top=60),
                expand=True,
            )
        ],
        bottom_appbar=SharedNavBar(page, current_route="/advisor_activities"),
    )

