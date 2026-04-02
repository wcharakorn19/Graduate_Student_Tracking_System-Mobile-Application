# ==============================================================================
# src/screens/advisor/advisor_home.py — หน้าหลักของอาจารย์ที่ปรึกษา (Advisor Dashboard)
# ==============================================================================
# หน้าจอนี้แสดง Dashboard ของอาจารย์ที่ปรึกษาหลัง Login สำเร็จ
# ประกอบด้วย:
#   1. Header: "Process Document"
#   2. Latest documents: แสดงเอกสารล่าสุด 1 รายการ
#   3. Student Documents: แสดงรายการเอกสารทั้งหมดของนักศึกษา
#   4. Bottom Navigation Bar
#
# ข้อมูลโหลดแบบ Async ผ่าน AdvisorController
# Route: "/advisor_home"
# ==============================================================================
import logging
import flet as ft
from controllers.advisor_controller import AdvisorController  # Controller อาจารย์
from components.shared_navbar import SharedNavBar
from components.error_banner import ErrorBanner
from components.base_card import BaseCard
from core.auth_guard import require_auth
from core.config import APP_COLORS
from models.document_model import ActivityModel

logger = logging.getLogger(__name__)


def create_document_card(activity: ActivityModel, page: ft.Page):
    """สร้างการ์ดแสดงรายละเอียดของเอกสาร"""
    # ตัวแปรสำหรับนำทาง (หากมี)
    target_route = f"/{activity.form_type}/{activity.submission_id}"
    
    return ft.Container(
        content=ft.Row(
            [
                # แบบ Folder Icon พื้นหลังสี่เหลี่ยม/วงกลมมนๆ
                ft.Container(
                    content=ft.Icon(
                        ft.Icons.FOLDER_OUTLINED,
                        color="black87",
                        size=24,
                    ),
                    bgcolor="#F5EFFB", # สีพื้นหลังของไอคอน (แบบในแบบร่าง)
                    padding=10,
                    border_radius=12,
                ),
                # ส่วนข้อความ
                ft.Column(
                    [
                        ft.Text(
                            activity.title,
                            size=14,
                            weight=ft.FontWeight.W_500,
                            color="black",
                        ),
                        ft.Text(
                            f"Name : {activity.name}",
                            size=12,
                            color="black87",
                        ),
                        ft.Text(
                            f"Status : {activity.status}",
                            size=12,
                            color="black87",
                        ),
                    ],
                    spacing=4,
                    expand=True,
                ),
            ],
            spacing=16,
            vertical_alignment=ft.CrossAxisAlignment.START,
        ),
        bgcolor="#F6F6F6",  # สีเทาอ่อนเหมือนแบบร่าง
        padding=ft.padding.all(16),
        border_radius=12,
        margin=ft.margin.only(bottom=12),
        # กดเปิดรายละเอียดได้ถ้าต้องการ
        on_click=lambda e: page.go(target_route) if activity.submission_id else None
    )


def AdvisorHome(page: ft.Page):
    """สร้างหน้าจอ Dashboard ของอาจารย์ที่ปรึกษา"""
    controller = AdvisorController()

    # ── Auth Guard: ตรวจสอบว่า Login แล้วหรือยัง ──
    user_id = require_auth(page)
    if not user_id:
        return ft.View(
            route="/advisor_home", controls=[ft.Text("Redirecting to login...")]
        )

    # ── ขั้นตอนที่ 1: เตรียม UI Components (State) ──
    header_text = ft.Text(
        "Process Document", size=24, weight=ft.FontWeight.BOLD, color="black"
    )
    
    # ส่วน Latest Documents
    latest_docs_header = ft.Text(
        "Latest documents:", size=16, weight=ft.FontWeight.BOLD, color="black"
    )
    latest_docs_container = ft.Column(spacing=0)
    
    # ส่วน Student Documents
    student_docs_header = ft.Text(
        "Student Documents:", size=16, weight=ft.FontWeight.BOLD, color="black"
    )
    student_docs_container = ft.Column(spacing=0, scroll=ft.ScrollMode.AUTO, expand=True)
    
    main_content_column = ft.Column(
        spacing=24,
        expand=True,
    )
    main_scroll_container = ft.Container(
        content=main_content_column,
        expand=True,
    )

    error_container = ft.Column(spacing=0)

    # ── ขั้นตอนที่ 2: ฟังก์ชันโหลดข้อมูลแบบ Async ──
    async def load_data(e=None):
        """โหลดข้อมูล Dashboard อาจารย์จาก API"""
        error_container.controls.clear()

        # แสดง Spinner ระหว่างโหลด
        latest_docs_container.controls.clear()
        student_docs_container.controls.clear()
        
        main_content_column.controls = [
            ft.Container(
                content=ft.ProgressRing(), alignment=ft.alignment.center, padding=20
            )
        ]
        page.update()

        # เรียก Controller แบบ Async
        result = await controller.get_dashboard_data(user_id)

        raw_data = result.get("data")
        error = result.get("message") if not result.get("success") else None

        if not error and raw_data:
            activities = raw_data.activities
            
            latest_docs_container.controls.clear()
            student_docs_container.controls.clear()
            
            if len(activities) > 0:
                # Latest Document: หยิบอันแรกสุด
                first_activity = activities[0]
                latest_docs_container.controls.append(create_document_card(first_activity, page))
                
                # Student Documents: หยิบที่เหลือ หรือถ้ามีน้อยก็แสดงหมด
                # ถ้าอ้างอิงจากดีไซน์ น่าจะเป็นเอกสารที่เหลือถัดๆ ไป
                for activity in activities[1:]:
                    student_docs_container.controls.append(create_document_card(activity, page))
            else:
                # กรณีไม่มีเอกสาร
                student_docs_container.controls.append(
                    ft.Text("ไม่มีเอกสารที่ต้องดำเนินการ", color="black54")
                )
            
            # ประกอบ Layout ใหม่
            main_content_column.controls.clear()
            
            # ส่วน Latest 
            latest_section = BaseCard(
                content=ft.Column(
                    [
                        latest_docs_header,
                        ft.Container(height=16),
                        latest_docs_container
                    ],
                    spacing=0
                )
            )
            main_content_column.controls.append(latest_section)
            
            # ส่วน Student Documents  
            student_section = BaseCard(
                content=ft.Column(
                    [
                        student_docs_header,
                        ft.Container(height=16),
                        student_docs_container
                    ],
                    spacing=0,
                    expand=True
                ),
                expand=True
            )
            main_content_column.controls.append(student_section)

            page.update()
        else:
            # กรณี Error: แสดง ErrorBanner
            main_content_column.controls.clear()
            error_container.controls.append(
                ErrorBanner(f"เกิดข้อผิดพลาดในการโหลดข้อมูล: {error}")
            )
            page.update()

    # รันฟังก์ชันโหลดข้อมูลแบบไม่บล็อก UI
    page.run_task(load_data)

    # คืนค่า View
    return ft.View(
        route="/advisor_home",
        bgcolor=APP_COLORS["background"],
        padding=0,
        controls=[
            ft.Container(
                content=ft.Column(
                    [
                        # Header: Process Document
                        ft.Row(
                            [
                                header_text,
                            ],
                            alignment=ft.MainAxisAlignment.START,
                        ),
                        error_container,
                        # เลื่อนได้
                        main_scroll_container,
                    ],
                    expand=True,
                ),
                padding=ft.padding.only(left=20, right=20, top=60),
                expand=True,
            )
        ],
        bottom_appbar=SharedNavBar(page, current_route="/advisor_home"),
    )
