# ==============================================================================
# src/screens/student/student_home.py — หน้าหลักของนักศึกษา (Student Dashboard)
# ==============================================================================
# หน้าจอนี้แสดง Dashboard ของนักศึกษาหลัง Login สำเร็จ
# ประกอบด้วย:
#   1. ชื่อนักศึกษา (Header)
#   2. Status Card — แสดงเอกสารที่กำลัง "รอดำเนินการ"
#   3. Latest Activities — รายการเอกสาร/กิจกรรมทั้งหมด (กดเข้าดูรายละเอียดได้)
#   4. Bottom Navigation Bar
#
# ข้อมูลโหลดแบบ Async ผ่าน StudentController
# Route: "/student_home"
# ==============================================================================
import flet as ft
from controllers.student_controller import StudentController  # Controller ดึงข้อมูลนักศึกษา
from components.shared_navbar import SharedNavBar            # แถบนำทางด้านล่าง
from components.base_card import BaseCard                    # การ์ดพื้นฐาน
from components.error_banner import ErrorBanner              # แบนเนอร์แสดง Error
from core.auth_guard import require_auth                     # ตรวจสอบ Login


def StudentHome(page: ft.Page):
    """สร้างหน้าจอ Dashboard ของนักศึกษา"""
    controller = StudentController()

    # ── Auth Guard: ตรวจสอบว่า Login แล้วหรือยัง ──
    user_id = require_auth(page)
    if not user_id:
        # ถ้ายังไม่ Login → แสดงข้อความ Redirect
        return ft.View(
            route="/student_home", controls=[ft.Text("Redirecting to login...")]
        )

    # ดึงชื่อนักศึกษาจาก Session
    user_name = page.session.get("user_full_name") or "นักศึกษา"

    # ── ขั้นตอนที่ 1: เตรียมตัวแปร UI (สร้างก่อน, ใส่ข้อมูลทีหลัง) ──
    name_text = ft.Text(user_name, size=20, weight=ft.FontWeight.BOLD, color="black")
    doc_name_text = ft.Text(
        "Doc Name: Loading...", weight=ft.FontWeight.BOLD, color="black"
    )
    status_label_text = ft.Text("สถานะ :", color="black54")
    status_value_text = ft.Text(
        "Loading...", size=16, weight=ft.FontWeight.BOLD, color="black"
    )

    activities_list = ft.Column(spacing=15, scroll=ft.ScrollMode.AUTO)  # รายการกิจกรรม (scroll ได้)
    error_container = ft.Column(spacing=0)  # กล่องสำหรับใส่ ErrorBanner

    # ── ขั้นตอนที่ 2: ฟังก์ชันโหลดข้อมูลแบบ Async ──
    async def load_data(e=None):
        """
        โหลดข้อมูล Dashboard จาก API แบบ Async
        แสดง Spinner ระหว่างโหลด แล้วอัปเดต UI เมื่อได้ข้อมูล
        """
        error_container.controls.clear()

        # แสดง Spinner ระหว่างโหลด
        activities_list.controls.clear()
        activities_list.controls.append(
            ft.Container(
                content=ft.ProgressRing(), alignment=ft.alignment.center, padding=20
            )
        )
        page.update()

        # เรียก Controller แบบ Async
        result = await controller.get_dashboard_data(user_id, user_name)

        if result["success"]:
            data = result["data"]

            # อัปเดตชื่อบนหน้าจอ
            name_text.value = data.user_name

            # อัปเดต Status Card ด้วยข้อมูลเอกสารปัจจุบัน
            doc_name_text.value = f"Doc Name: {data.current_doc.doc_name}"
            status_label_text.value = data.current_doc.status_label
            status_value_text.value = data.current_doc.status_text

            # กำหนดสีสถานะบน Status Card ตามข้อความ
            status_txt = data.current_doc.status_text
            if "อนุมัติ" in status_txt:
                status_value_text.color = "#4CAF50"     # เขียว (อนุมัติ)
            elif "ปฏิเสธ" in status_txt or "แก้ไข" in status_txt:
                status_value_text.color = "#F44336"     # แดง (ปฏิเสธ)
            else:
                status_value_text.color = "#FF9800"     # ส้ม (รอดำเนินการ)

            # สร้างรายการ Activities จากข้อมูลที่ได้
            activities_list.controls.clear()
            for act in data.activities:
                # สร้าง route สำหรับนำทางไปหน้ารายละเอียดฟอร์ม
                form_type = getattr(act, "form_type", "form1")
                sub_id = getattr(act, "submission_id", "")
                target_route = f"/{form_type}/{sub_id}"

                # กำหนดสีสถานะแต่ละรายการ
                if "อนุมัติ" in act.status:
                    status_color = "#4CAF50"    # เขียว
                elif "ปฏิเสธ" in act.status or "แก้ไข" in act.status:
                    status_color = "#F44336"    # แดง
                else:
                    status_color = "#FF9800"    # ส้ม

                # สร้างการ์ดกิจกรรมแต่ละรายการ
                act_item = ft.Container(
                    content=ft.Row(
                        [
                            # ไอคอนโฟลเดอร์
                            ft.Container(
                                content=ft.Icon(
                                    ft.Icons.FOLDER_OUTLINED, color="black54", size=20
                                ),
                                bgcolor="#F0F0F0",
                                padding=10,
                                border_radius=10,
                            ),
                            # ชื่อเอกสาร + สถานะ
                            ft.Column(
                                [
                                    ft.Text(
                                        act.title,
                                        size=14,
                                        color="black",
                                        weight=ft.FontWeight.W_500,
                                    ),
                                    ft.Text(
                                        f"Status : {act.status}",
                                        size=12,
                                        color=status_color,
                                        weight=ft.FontWeight.W_600,
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
                    # เมื่อกดที่รายการนี้ → นำทางไปหน้ารายละเอียดฟอร์ม
                    on_click=lambda e, route=target_route: page.go(route),
                )
                activities_list.controls.append(act_item)

            page.update()
        else:
            # กรณี Error: แสดง ErrorBanner
            activities_list.controls.clear()
            error_msg = result.get("message", "Unknown Error")
            error_container.controls.append(
                ErrorBanner(f"เกิดข้อผิดพลาดในการโหลดข้อมูล: {error_msg}")
            )
            page.update()

    # ── ขั้นตอนที่ 3: สร้าง UI Components ──
    # Status Card: แสดงเอกสารที่กำลังดำเนินการ
    status_card = BaseCard(
        content=ft.Column(
            [
                doc_name_text,
                ft.Container(height=10),
                status_label_text,
                status_value_text,
            ]
        )
    )

    # Activities Card: แสดงรายการกิจกรรมทั้งหมด (ขยายเต็มพื้นที่)
    activities_card = BaseCard(content=activities_list, expand=True)

    # รันฟังก์ชันโหลดข้อมูลแบบ Async (ไม่บล็อก UI)
    page.run_task(load_data)

    # ── ขั้นตอนที่ 4: ประกอบร่าง Layout ──
    main_content = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        name_text,      # ชื่อนักศึกษา
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                error_container,        # แจ้งเตือน Error (ถ้ามี)
                ft.Container(height=10),
                status_card,            # Status Card
                ft.Container(height=20),
                ft.Text(
                    "Latest Activities",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color="black",
                ),
                activities_card,        # รายการกิจกรรมทั้งหมด
            ],
            expand=True,
        ),
        padding=ft.padding.only(left=20, right=20, top=50),
        expand=True,
    )

    # คืนค่า View พร้อม Bottom Navigation Bar
    return ft.View(
        route="/student_home",
        bgcolor="#FFF6FE",
        padding=0,
        controls=[main_content],
        # เรียกใช้ SharedNavBar พร้อมบอกว่าอยู่หน้า "/student_home"
        bottom_appbar=SharedNavBar(page, current_route="/student_home"),
    )
