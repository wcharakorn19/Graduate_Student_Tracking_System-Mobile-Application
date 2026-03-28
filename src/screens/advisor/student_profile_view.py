# src/screens/advisor/student_profile_view.py
"""หน้าดูรายละเอียด Profile ของนักศึกษา (สำหรับ Advisor เข้าดู)"""
import logging
import flet as ft
from controllers.student_controller import StudentController
from components.base_card import BaseCard
from components.error_banner import ErrorBanner
from core.auth_guard import require_auth
from core.config import APP_COLORS
from models.profile_model import ProfileModel

logger = logging.getLogger(__name__)


def StudentProfileViewScreen(page: ft.Page, student_id: str):
    # Auth guard — ต้อง login ก่อนถึงจะดูได้
    user_id = require_auth(page)
    if not user_id:
        return ft.View(
            route=f"/student_profile/{student_id}",
            controls=[ft.Text("Redirecting to login...")],
        )

    controller = StudentController()
    profile = ProfileModel(full_name="กำลังโหลด...")
    error_container = ft.Column()
    main_scroll = ft.Column(scroll=ft.ScrollMode.AUTO, spacing=0, expand=True)

    # --- ฟังก์ชันช่วยสร้าง UI ---
    def create_info_row(icon_name, label, value, show_divider=True):
        row = ft.Container(
            content=ft.Row(
                [
                    ft.Container(
                        content=ft.Icon(icon_name, color=APP_COLORS["primary"], size=20),
                        bgcolor=APP_COLORS["background"],
                        padding=12,
                        border_radius=12,
                    ),
                    ft.Column(
                        [
                            ft.Text(
                                label, size=13, color="black54",
                                weight=ft.FontWeight.W_500,
                            ),
                            ft.Text(
                                value, size=14, color="black87",
                                weight=ft.FontWeight.W_600,
                            ),
                        ],
                        spacing=2,
                        expand=True,
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.padding.symmetric(vertical=15, horizontal=20),
        )
        if show_divider:
            return ft.Column(
                [row, ft.Divider(height=1, color=APP_COLORS["border_light"], thickness=1)],
                spacing=0,
            )
        return row

    def section_title(title):
        return ft.Container(
            content=ft.Text(title, size=16, weight=ft.FontWeight.BOLD, color=APP_COLORS["primary"]),
            padding=ft.padding.only(left=25, top=20, bottom=10),
        )

    # --- โหลดข้อมูล ---
    async def load_data(e=None):
        nonlocal profile
        error_container.controls.clear()

        main_scroll.controls.clear()
        main_scroll.controls.append(
            ft.Container(
                content=ft.ProgressRing(), alignment=ft.alignment.center, padding=50
            )
        )
        page.update()

        # ใช้ StudentController เพื่อดึง profile ของ student_id
        result = await controller.get_profile_data(student_id, None, "student")

        if result["success"]:
            profile = result["data"]
            build_layout()
            page.update()
        else:
            main_scroll.controls.clear()
            error_container.controls.append(
                ErrorBanner(f"เกิดข้อผิดพลาด: {result.get('message', 'Unknown Error')}")
            )
            build_layout()
            page.update()

    def build_layout():
        # --- Header ---
        header = ft.Container(
            content=ft.Column(
                [
                    ft.Container(height=10),
                    # ปุ่มกลับ
                    ft.Row(
                        [
                            ft.IconButton(
                                icon=ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED,
                                icon_color="white",
                                icon_size=20,
                                on_click=lambda _: page.go("/advisor_home"),
                            ),
                        ],
                    ),
                    ft.Container(
                        content=ft.Icon(
                            ft.Icons.PERSON_OUTLINE, size=45, color="white"
                        ),
                        bgcolor="white24",
                        width=100,
                        height=100,
                        border_radius=50,
                        alignment=ft.alignment.center,
                    ),
                    ft.Container(height=10),
                    ft.Text(
                        profile.full_name,
                        size=22,
                        weight=ft.FontWeight.BOLD,
                        color="white",
                    ),
                    ft.Text(profile.role, size=16, color="white70"),
                    ft.Container(height=20),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[APP_COLORS["gradient_start"], APP_COLORS["gradient_end"]],
            ),
            padding=20,
            border_radius=ft.border_radius.only(bottom_left=30, bottom_right=30),
            width=float("inf"),
        )

        # --- ข้อมูลส่วนตัว ---
        personal_list = BaseCard(
            content=ft.Column(
                [
                    create_info_row(ft.Icons.PERSON_OUTLINE, "ชื่อ-นามสกุล", profile.full_name),
                    create_info_row(ft.Icons.ACCOUNT_BOX_OUTLINED, "รหัสนักศึกษา", profile.user_id),
                    create_info_row(ft.Icons.SCHOOL_OUTLINED, "ระดับการศึกษา", profile.education_level),
                    create_info_row(
                        ft.Icons.ACCOUNT_BALANCE_OUTLINED,
                        "คณะ/สาขาวิชา",
                        f"{profile.faculty}\n{profile.major}",
                    ),
                    create_info_row(ft.Icons.INFO_OUTLINE, "สถานะ", profile.status),
                    create_info_row(ft.Icons.MAIL_OUTLINE, "อีเมล", profile.email),
                    create_info_row(
                        ft.Icons.PHONE_OUTLINED, "เบอร์โทรศัพท์", profile.phone,
                        show_divider=False,
                    ),
                ],
                spacing=0,
            ),
            margin=ft.margin.symmetric(horizontal=20),
            padding=0,
        )

        # --- ข้อมูลวิทยานิพนธ์ ---
        thesis_list = BaseCard(
            content=ft.Column(
                [
                    create_info_row(ft.Icons.MENU_BOOK_OUTLINED, "วิทยานิพนธ์ (ภาษาไทย)", profile.thesis.title_th),
                    create_info_row(ft.Icons.BOOK_OUTLINED, "วิทยานิพนธ์ (ภาษาอังกฤษ)", profile.thesis.title_en),
                    create_info_row(ft.Icons.SUPERVISOR_ACCOUNT_OUTLINED, "อาจารย์ที่ปรึกษาหลัก", profile.thesis.main_advisor),
                    create_info_row(ft.Icons.PERSON_OUTLINE, "อาจารย์ที่ปรึกษาร่วม 1", profile.thesis.co_advisor_1),
                    create_info_row(
                        ft.Icons.PERSON_OUTLINE, "อาจารย์ที่ปรึกษาร่วม 2", profile.thesis.co_advisor_2,
                        show_divider=False,
                    ),
                ],
                spacing=0,
            ),
            margin=ft.margin.symmetric(horizontal=20),
            padding=0,
        )

        # --- สรุปผลการดำเนินการ ---
        progress_list = BaseCard(
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Text("การสอบหัวข้อและเค้าโครง", size=14, weight=ft.FontWeight.BOLD, color="black87"),
                        padding=ft.padding.only(left=20, top=15, bottom=5),
                    ),
                    ft.Divider(height=1, color=APP_COLORS["border_light"]),
                    create_info_row(ft.Icons.EVENT_OUTLINED, "วันที่สอบหัวข้อ", profile.progress.topic_exam_date),
                    create_info_row(ft.Icons.ASSIGNMENT_OUTLINED, "สถานะสอบหัวข้อ", profile.progress.topic_status),
                    create_info_row(ft.Icons.EVENT_AVAILABLE_OUTLINED, "วันที่อนุมัติหัวข้อ", profile.progress.topic_approve_date),
                    ft.Container(
                        content=ft.Text("การสอบวิทยานิพนธ์ขั้นสุดท้าย", size=14, weight=ft.FontWeight.BOLD, color="black87"),
                        padding=ft.padding.only(left=20, top=15, bottom=5),
                    ),
                    ft.Divider(height=1, color=APP_COLORS["border_light"]),
                    create_info_row(ft.Icons.EVENT_OUTLINED, "วันที่สอบขั้นสุดท้าย", profile.progress.final_exam_date),
                    create_info_row(ft.Icons.ASSIGNMENT_TURNED_IN_OUTLINED, "สถานะสอบขั้นสุดท้าย", profile.progress.final_status),
                    create_info_row(ft.Icons.EVENT_AVAILABLE_OUTLINED, "วันที่สำเร็จการศึกษา", profile.progress.final_approve_date),
                    ft.Container(
                        content=ft.Text("ผลการสอบภาษาอังกฤษ ป.โท", size=14, weight=ft.FontWeight.BOLD, color="black87"),
                        padding=ft.padding.only(left=20, top=15, bottom=5),
                    ),
                    ft.Divider(height=1, color=APP_COLORS["border_light"]),
                    create_info_row(ft.Icons.DOCUMENT_SCANNER_OUTLINED, "ประเภทการสอบ", profile.progress.english_test_type),
                    create_info_row(ft.Icons.EVENT_AVAILABLE_OUTLINED, "วันที่อนุมัติผลสอบ", profile.progress.english_test_date),
                    create_info_row(
                        ft.Icons.LANGUAGE_OUTLINED, "สถานะ", profile.progress.english_test_status,
                        show_divider=False,
                    ),
                ],
                spacing=0,
            ),
            margin=ft.margin.symmetric(horizontal=20),
            padding=0,
        )

        main_scroll.controls.clear()
        main_scroll.controls.extend([
            header,
            error_container,
            section_title("ข้อมูลส่วนตัว"),
            personal_list,
            section_title("ข้อมูลวิทยานิพนธ์"),
            thesis_list,
            section_title("สรุปผลการดำเนินการ"),
            progress_list,
            ft.Container(height=30),
        ])

    # รัน Async
    page.run_task(load_data)

    return ft.View(
        route=f"/student_profile/{student_id}",
        bgcolor=APP_COLORS["background"],
        padding=0,
        controls=[main_scroll],
    )
