# src/screens/profile_screen.py
import flet as ft
from components.shared_navbar import SharedNavBar
from components.base_card import BaseCard
from components.error_banner import ErrorBanner

from controllers.student_controller import StudentController
from controllers.advisor_controller import AdvisorController
from models.profile_model import ProfileModel
from models.advisor_profile_model import AdvisorProfileModel
from core.auth_guard import require_auth


def ProfileScreen(page: ft.Page):
    # --- ดึง Session ---
    user_id = require_auth(page)
    if not user_id:
        return ft.View(
            route="/profile", controls=[ft.Text("Redirecting to login...")]
        )
    session_name = page.session.get("user_full_name")
    session_role = page.session.get("user_role")

    # 🌟 เลือก Controller ที่ถูกต้องตาม Role
    is_advisor = session_role == "advisor"

    if is_advisor:
        controller = AdvisorController()
        profile = AdvisorProfileModel(full_name=session_name or "-", role="อาจารย์ที่ปรึกษา")
    else:
        controller = StudentController()
        profile = ProfileModel(full_name=session_name or "-", role=session_role or "นักศึกษา")

    error_container = ft.Column()

    # ฟังก์ชันสำหรับโหลดข้อมูลแบบ Async
    async def load_data(e=None):
        nonlocal profile
        error_container.controls.clear()

        # แสดง Spinner แทน layout หลัก
        main_scroll.controls.clear()
        main_scroll.controls.append(
            ft.Container(
                content=ft.ProgressRing(), alignment=ft.alignment.center, padding=50
            )
        )
        page.update()

        # 🌟 เรียก Controller ตาม Role
        result = await controller.get_profile_data(user_id, session_name, session_role)

        if result["success"]:
            profile = result["data"]
            build_main_layout()
            page.update()
        else:
            main_scroll.controls.clear()
            error_container.controls.append(
                ErrorBanner(f"เกิดข้อผิดพลาด: {result.get('message', 'Unknown Error')}")
            )
            # แสดงหน้าแต่ไม่มีข้อมูล พร้อม Error
            if is_advisor:
                profile = AdvisorProfileModel(
                    full_name=session_name or "-", role="อาจารย์ที่ปรึกษา"
                )
            else:
                profile = ProfileModel(
                    full_name=session_name or "-", role=session_role or "นักศึกษา"
                )
            build_main_layout()
            page.update()

    # ฟังก์ชันช่วยสร้างรายการข้อมูลแต่ละแถว
    def create_info_row(icon_name, label, value, show_divider=True):
        row = ft.Container(
            content=ft.Row(
                [
                    ft.Container(
                        content=ft.Icon(icon_name, color="#EF3961", size=20),
                        bgcolor="#FFF6FE",
                        padding=12,
                        border_radius=12,
                    ),
                    ft.Column(
                        [
                            ft.Text(
                                label,
                                size=13,
                                color="black54",
                                weight=ft.FontWeight.W_500,
                            ),
                            ft.Text(
                                value,
                                size=14,
                                color="black87",
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
                [row, ft.Divider(height=1, color="#F0F0F0", thickness=1)], spacing=0
            )
        return row

    def section_title(title):
        return ft.Container(
            content=ft.Text(title, size=16, weight=ft.FontWeight.BOLD, color="#EF3961"),
            padding=ft.padding.only(left=25, top=20, bottom=10),
        )

    main_scroll = ft.Column(scroll=ft.ScrollMode.AUTO, spacing=0, expand=True)

    def build_main_layout():
        # --- 1. ส่วนหัว (Header) ---
        header = ft.Container(
            content=ft.Column(
                [
                    ft.Container(height=30),
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
                colors=["#FF9EBB", "#FFB6C8"],
            ),
            padding=20,
            border_radius=ft.border_radius.only(bottom_left=30, bottom_right=30),
            width=float("inf"),
        )

        # --- 2. ข้อมูลโปรไฟล์ (แยกตาม Role) ---
        if is_advisor:
            content_sections = _build_advisor_sections()
        else:
            content_sections = _build_student_sections()

        # --- 3. ปุ่มออกจากระบบ ---
        def handle_logout(e):
            page.session.clear()
            page.go("/login")

        logout_btn = ft.Container(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.LOGOUT, color="#EF3961", size=20),
                    ft.Text(
                        "ออกจากระบบ",
                        color="#EF3961",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            border=ft.border.all(1, "#F48FB1"),
            border_radius=15,
            padding=15,
            margin=ft.margin.only(left=20, right=20, top=15, bottom=30),
            bgcolor="white",
            on_click=handle_logout,
        )

        # โหลดเข้า main_scroll
        main_scroll.controls.clear()
        main_scroll.controls.extend(
            [header, error_container]
            + content_sections
            + [ft.Container(height=10), logout_btn]
        )

    # =============================================
    # 🧑‍🏫 Advisor Profile Sections
    # =============================================
    def _build_advisor_sections():
        personal_list = BaseCard(
            content=ft.Column(
                [
                    create_info_row(
                        ft.Icons.PERSON_OUTLINE, "ชื่อ-นามสกุล", profile.full_name
                    ),
                    create_info_row(
                        ft.Icons.BADGE_OUTLINED, "รหัสอาจารย์", profile.user_id
                    ),
                    create_info_row(
                        ft.Icons.MAIL_OUTLINE,
                        "อีเมล",
                        profile.email,
                        show_divider=False,
                    ),
                ],
                spacing=0,
            ),
            margin=ft.margin.symmetric(horizontal=20),
            padding=0,
        )

        position_list = BaseCard(
            content=ft.Column(
                [
                    create_info_row(
                        ft.Icons.SCHOOL_OUTLINED, "ตำแหน่งวิชาการ", profile.academic_position
                    ),
                    create_info_row(
                        ft.Icons.WORK_OUTLINE, "ประเภทอาจารย์", profile.advisor_type
                    ),
                    create_info_row(
                        ft.Icons.LOCATION_ON_OUTLINED, "สถานที่ทำงาน", profile.workplace
                    ),
                    create_info_row(
                        ft.Icons.PHONE_OUTLINED,
                        "เบอร์โทรศัพท์",
                        profile.phone,
                        show_divider=False,
                    ),
                ],
                spacing=0,
            ),
            margin=ft.margin.symmetric(horizontal=20),
            padding=0,
        )

        other_list = BaseCard(
            content=ft.Column(
                [
                    create_info_row(
                        ft.Icons.VERIFIED_USER_OUTLINED, "บทบาทการอนุมัติ", profile.approval_role
                    ),
                    create_info_row(
                        ft.Icons.MENU_BOOK_OUTLINED,
                        "หลักสูตรที่รับผิดชอบ",
                        profile.program,
                        show_divider=False,
                    ),
                ],
                spacing=0,
            ),
            margin=ft.margin.symmetric(horizontal=20),
            padding=0,
        )

        return [
            section_title("ข้อมูลส่วนตัวและการติดต่อ"),
            personal_list,
            section_title("ตำแหน่งและสถานที่"),
            position_list,
            section_title("ข้อมูลด้านอื่น ๆ"),
            other_list,
        ]

    # =============================================
    # 🧑‍🎓 Student Profile Sections (เดิม)
    # =============================================
    def _build_student_sections():
        personal_list = BaseCard(
            content=ft.Column(
                [
                    create_info_row(
                        ft.Icons.PERSON_OUTLINE, "ชื่อ-นามสกุล", profile.full_name
                    ),
                    create_info_row(
                        ft.Icons.ACCOUNT_BOX_OUTLINED, "รหัสนักศึกษา", profile.user_id
                    ),
                    create_info_row(
                        ft.Icons.SCHOOL_OUTLINED, "ระดับการศึกษา", profile.education_level
                    ),
                    create_info_row(
                        ft.Icons.ACCOUNT_BALANCE_OUTLINED,
                        "คณะ/สาขาวิชา",
                        f"{profile.faculty}\n{profile.major}",
                    ),
                    create_info_row(ft.Icons.INFO_OUTLINE, "สถานะ", profile.status),
                    create_info_row(ft.Icons.MAIL_OUTLINE, "อีเมล", profile.email),
                    create_info_row(
                        ft.Icons.PHONE_OUTLINED,
                        "เบอร์โทรศัพท์",
                        profile.phone,
                        show_divider=False,
                    ),
                ],
                spacing=0,
            ),
            margin=ft.margin.symmetric(horizontal=20),
            padding=0,
        )

        thesis_list = BaseCard(
            content=ft.Column(
                [
                    create_info_row(
                        ft.Icons.MENU_BOOK_OUTLINED,
                        "วิทยานิพนธ์ (ภาษาไทย)",
                        profile.thesis.title_th,
                    ),
                    create_info_row(
                        ft.Icons.BOOK_OUTLINED,
                        "วิทยานิพนธ์ (ภาษาอังกฤษ)",
                        profile.thesis.title_en,
                    ),
                    create_info_row(
                        ft.Icons.SUPERVISOR_ACCOUNT_OUTLINED,
                        "อาจารย์ที่ปรึกษาหลัก",
                        profile.thesis.main_advisor,
                    ),
                    create_info_row(
                        ft.Icons.PERSON_OUTLINE,
                        "อาจารย์ที่ปรึกษาร่วม 1",
                        profile.thesis.co_advisor_1,
                    ),
                    create_info_row(
                        ft.Icons.PERSON_OUTLINE,
                        "อาจารย์ที่ปรึกษาร่วม 2",
                        profile.thesis.co_advisor_2,
                        show_divider=False,
                    ),
                ],
                spacing=0,
            ),
            margin=ft.margin.symmetric(horizontal=20),
            padding=0,
        )

        progress_list = BaseCard(
            content=ft.Column(
                [
                    # สอบหัวข้อเรื่อง
                    ft.Container(
                        content=ft.Text(
                            "การสอบหัวข้อและเค้าโครง",
                            size=14,
                            weight=ft.FontWeight.BOLD,
                            color="black87",
                        ),
                        padding=ft.padding.only(left=20, top=15, bottom=5),
                    ),
                    ft.Divider(height=1, color="#F0F0F0"),
                    create_info_row(
                        ft.Icons.EVENT_OUTLINED,
                        "วันที่สอบหัวข้อ",
                        profile.progress.topic_exam_date,
                    ),
                    create_info_row(
                        ft.Icons.ASSIGNMENT_OUTLINED,
                        "สถานะสอบหัวข้อ",
                        profile.progress.topic_status,
                    ),
                    create_info_row(
                        ft.Icons.EVENT_AVAILABLE_OUTLINED,
                        "วันที่อนุมัติหัวข้อ",
                        profile.progress.topic_approve_date,
                    ),
                    # สอบวิทยานิพนธ์ขั้นสุดท้าย
                    ft.Container(
                        content=ft.Text(
                            "การสอบวิทยานิพนธ์ขั้นสุดท้าย",
                            size=14,
                            weight=ft.FontWeight.BOLD,
                            color="black87",
                        ),
                        padding=ft.padding.only(left=20, top=15, bottom=5),
                    ),
                    ft.Divider(height=1, color="#F0F0F0"),
                    create_info_row(
                        ft.Icons.EVENT_OUTLINED,
                        "วันที่สอบขั้นสุดท้าย",
                        profile.progress.final_exam_date,
                    ),
                    create_info_row(
                        ft.Icons.ASSIGNMENT_TURNED_IN_OUTLINED,
                        "สถานะสอบขั้นสุดท้าย",
                        profile.progress.final_status,
                    ),
                    create_info_row(
                        ft.Icons.EVENT_AVAILABLE_OUTLINED,
                        "วันที่สำเร็จการศึกษา",
                        profile.progress.final_approve_date,
                    ),
                    # สอบภาษาอังกฤษ
                    ft.Container(
                        content=ft.Text(
                            "ผลการสอบภาษาอังกฤษ ป.โท",
                            size=14,
                            weight=ft.FontWeight.BOLD,
                            color="black87",
                        ),
                        padding=ft.padding.only(left=20, top=15, bottom=5),
                    ),
                    ft.Divider(height=1, color="#F0F0F0"),
                    create_info_row(
                        ft.Icons.DOCUMENT_SCANNER_OUTLINED,
                        "ประเภทการสอบ",
                        profile.progress.english_test_type,
                    ),
                    create_info_row(
                        ft.Icons.EVENT_AVAILABLE_OUTLINED,
                        "วันที่อนุมัติผลสอบ",
                        profile.progress.english_test_date,
                    ),
                    create_info_row(
                        ft.Icons.LANGUAGE_OUTLINED,
                        "สถานะ",
                        profile.progress.english_test_status,
                        show_divider=False,
                    ),
                ],
                spacing=0,
            ),
            margin=ft.margin.symmetric(horizontal=20),
            padding=0,
        )

        return [
            section_title("ข้อมูลส่วนตัว"),
            personal_list,
            section_title("ข้อมูลวิทยานิพนธ์"),
            thesis_list,
            section_title("สรุปผลการดำเนินการ"),
            progress_list,
        ]

    # รัน Async แบบไม่บล็อก UI
    page.run_task(load_data)

    return ft.View(
        route="/profile",
        bgcolor="#FFF6FE",
        padding=0,
        controls=[main_scroll],
        bottom_appbar=SharedNavBar(page, current_route="/profile"),
    )
